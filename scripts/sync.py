#!/usr/bin/env python3
"""
Sync script for DON Kennisbank skills.

Fetches documentation from developer-overheid-nl/don-site GitHub repo
and generates Claude Code skill files.

Usage:
    python scripts/sync.py [--topic TOPIC]

Options:
    --topic TOPIC   Only sync a specific topic (e.g., 'apis', 'leidraad')
                    If not specified, syncs all topics.
"""

import argparse
import json
import os
import re
import shutil
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

GITHUB_REPO = "developer-overheid-nl/don-site"
GITHUB_BRANCH = "main"
DOCS_PATH = "docs"

# Map of topic directory names to skill metadata
TOPICS = {
    "apis": {
        "name": "don-apis",
        "title": "DON APIs",
        "description": "Dutch government API design rules and OpenAPI standards: REST APIs, webhooks, event-driven architecture for government projects.",
        "keywords": ["API", "REST", "OpenAPI", "OAS", "webhooks", "API design rules"],
    },
    "leidraad": {
        "name": "don-leidraad",
        "title": "DON Leidraad (NeRDS)",
        "description": "NeRDS software development guidelines for Dutch government: architecture, CI/CD, security, privacy, accessibility.",
        "keywords": ["NeRDS", "leidraad", "guidelines", "agile", "cloud", "security", "privacy", "accessibility"],
    },
    "security": {
        "name": "don-security",
        "title": "DON Security",
        "description": "Dutch government auth and security standards: DigiD, eHerkenning, OAuth, OIDC, PKIoverheid, BIO, NIS2.",
        "keywords": ["DigiD", "eHerkenning", "OAuth", "OIDC", "PKIoverheid", "BIO", "NIS2", "security"],
    },
    "open-source": {
        "name": "don-open-source",
        "title": "DON Open Source",
        "description": "Open source standards for Dutch government: licensing, publiccode.yml, Standard for Public Code, CONTRIBUTING.md.",
        "keywords": ["open source", "publiccode.yml", "licensing", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md"],
    },
    "infra": {
        "name": "don-infra",
        "title": "DON Infrastructure",
        "description": "Dutch government infrastructure standards: Haven (Kubernetes), FSC (Federated Service Connectivity), deployment compliance.",
        "keywords": ["Haven", "Kubernetes", "FSC", "infrastructure", "deployment", "compliance"],
    },
    "data": {
        "name": "don-data",
        "title": "DON Data",
        "description": "Dutch government data standards: data exchange, data quality, government data formats and compliance.",
        "keywords": ["data", "standards", "exchange", "quality"],
    },
    "front-end": {
        "name": "don-front-end",
        "title": "DON Front-end",
        "description": "Dutch government web standards: NL Design System, WCAG accessibility, government UI patterns.",
        "keywords": ["front-end", "NL Design System", "WCAG", "accessibility", "web development"],
    },
    "programmeertalen": {
        "name": "don-programmeertalen",
        "title": "DON Programmeertalen",
        "description": "Programming language guidelines for Dutch government software: language choice, dev environments, best practices.",
        "keywords": ["programming languages", "best practices", "coding standards"],
    },
}


def github_api_get(path: str) -> dict:
    """Fetch JSON from GitHub API."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}?ref={GITHUB_BRANCH}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        raise


def fetch_raw_file(path: str) -> str:
    """Fetch raw file content from GitHub."""
    url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{path}"
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode()
    except urllib.error.HTTPError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        raise


def list_directory(path: str) -> list[dict]:
    """List contents of a directory in the repo."""
    return github_api_get(path)


def fetch_docs_recursive(path: str, depth: int = 0, max_depth: int = 3) -> list[tuple[str, str]]:
    """
    Recursively fetch all markdown files from a directory.
    Returns list of (relative_path, content) tuples.
    """
    if depth > max_depth:
        return []

    files = []
    try:
        contents = list_directory(path)
    except Exception:
        return []

    for item in contents:
        if item["type"] == "file" and (item["name"].endswith(".md") or item["name"].endswith(".mdx")):
            try:
                content = fetch_raw_file(item["path"])
                # Store path relative to the topic directory
                rel_path = item["path"].replace(f"{DOCS_PATH}/", "")
                files.append((rel_path, content))
                print(f"  Fetched: {item['path']}")
            except Exception as e:
                print(f"  Failed to fetch {item['path']}: {e}", file=sys.stderr)
        elif item["type"] == "dir":
            files.extend(fetch_docs_recursive(item["path"], depth + 1, max_depth))

    return files


def clean_mdx_content(content: str) -> str:
    """
    Clean MDX-specific syntax to make it valid markdown.
    Removes JSX imports, components, and converts MDX features.
    """
    # Remove import statements
    content = re.sub(r'^import\s+.*?$', '', content, flags=re.MULTILINE)

    # Remove JSX-style components (simple cases)
    content = re.sub(r'<[A-Z][a-zA-Z]*\s*[^>]*/>', '', content)
    content = re.sub(r'<[A-Z][a-zA-Z]*[^>]*>.*?</[A-Z][a-zA-Z]*>', '', content, flags=re.DOTALL)

    # Remove export statements
    content = re.sub(r'^export\s+.*?$', '', content, flags=re.MULTILINE)

    # Convert MDX admonitions (:::warning[title], :::note, etc.) to blockquotes
    # Match opening with optional title: :::warning[Some Title] or :::note
    content = re.sub(r'^:::(warning|note|tip|info|caution|danger)\[([^\]]*)\]\s*$', r'> **\2**', content, flags=re.MULTILINE | re.IGNORECASE)
    content = re.sub(r'^:::(warning|note|tip|info|caution|danger)\s*$', r'> **\1:**', content, flags=re.MULTILINE | re.IGNORECASE)
    # Remove closing :::
    content = re.sub(r'^:::\s*$', '', content, flags=re.MULTILINE)

    # Clean up excessive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip()


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    frontmatter = {}
    for line in parts[1].strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip().strip('"\'')

    return frontmatter, parts[2].strip()


def generate_skill(topic: str, meta: dict, docs: list[tuple[str, str]], output_dir: Path):
    """Generate a skill directory with SKILL.md and supporting files."""
    skill_dir = output_dir / meta["name"]

    # Clean existing skill directory
    if skill_dir.exists():
        shutil.rmtree(skill_dir)
    skill_dir.mkdir(parents=True)

    # Create references directory per Agent Skills spec
    refs_dir = skill_dir / "references"
    refs_dir.mkdir(parents=True)

    # Organize docs by subdirectory
    organized: dict[str, list[tuple[str, str, dict]]] = {}
    for rel_path, content in docs:
        # Remove topic prefix from path
        if rel_path.startswith(f"{topic}/"):
            rel_path = rel_path[len(topic) + 1:]

        frontmatter, body = extract_frontmatter(content)
        body = clean_mdx_content(body)

        # Get subdirectory (or root)
        parts = rel_path.split('/')
        if len(parts) > 1:
            subdir = parts[0]
        else:
            subdir = "_root"

        if subdir not in organized:
            organized[subdir] = []
        organized[subdir].append((rel_path, body, frontmatter))

    # Build keywords string for description
    keywords = meta.get('keywords', [])
    keywords_str = ', '.join(keywords) if keywords else ''

    # Generate SKILL.md (main entry point) with improved spec compliance
    skill_content = f"""---
name: {meta['name']}
description: {json.dumps(meta['description'], ensure_ascii=False)}
metadata:
  source: developer.overheid.nl
  synced-from: https://github.com/{GITHUB_REPO}
  topic: {topic}
---

# {meta['title']}

## When to Use This Skill

Use this skill when you need guidance on:
"""

    # Add keyword-based guidance
    for keyword in keywords[:5]:  # Limit to first 5 keywords
        skill_content += f"- {keyword}\n"

    skill_content += f"""
## How to Navigate

This skill contains documentation organized by topic. Browse the references below or ask about specific topics.

## References

"""

    # Add table of contents pointing to references/
    for subdir, files in sorted(organized.items()):
        if subdir == "_root":
            for rel_path, body, fm in files:
                title = fm.get('title', rel_path.replace('.mdx', '').replace('.md', ''))
                ref_path = f"references/{rel_path.replace('.mdx', '.md')}"
                skill_content += f"- [{title}]({ref_path})\n"
        else:
            skill_content += f"\n### {subdir.replace('-', ' ').title()}\n\n"
            for rel_path, body, fm in files:
                title = fm.get('title', rel_path.split('/')[-1].replace('.mdx', '').replace('.md', ''))
                ref_path = f"references/{rel_path.replace('.mdx', '.md')}"
                skill_content += f"- [{title}]({ref_path})\n"

    skill_content += f"""

---

Source: https://github.com/{GITHUB_REPO}/tree/{GITHUB_BRANCH}/{DOCS_PATH}/{topic}
"""

    # Write SKILL.md
    (skill_dir / "SKILL.md").write_text(skill_content)

    # Write individual doc files to references/
    for rel_path, body, frontmatter in [item for items in organized.values() for item in items]:
        # Convert .mdx to .md and put in references/
        out_path = refs_dir / rel_path.replace('.mdx', '.md')
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # Add title as h1 if present in frontmatter
        if frontmatter.get('title') and not body.startswith('# '):
            body = f"# {frontmatter['title']}\n\n{body}"

        out_path.write_text(body)

    print(f"Generated skill: {meta['name']} ({len(docs)} files)")


def sync_topic(topic: str, meta: dict, output_dir: Path):
    """Sync a single topic."""
    print(f"\nSyncing topic: {topic}")
    docs_path = f"{DOCS_PATH}/{topic}"
    docs = fetch_docs_recursive(docs_path)

    if not docs:
        print(f"  No docs found for topic: {topic}", file=sys.stderr)
        return

    generate_skill(topic, meta, docs, output_dir)


def main():
    parser = argparse.ArgumentParser(description="Sync DON Kennisbank docs to skills")
    parser.add_argument("--topic", help="Only sync a specific topic")
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    plugin_dir = script_dir.parent
    output_dir = plugin_dir / "skills"

    print(f"Output directory: {output_dir}")

    if args.topic:
        if args.topic not in TOPICS:
            print(f"Unknown topic: {args.topic}", file=sys.stderr)
            print(f"Available topics: {', '.join(TOPICS.keys())}", file=sys.stderr)
            sys.exit(1)
        sync_topic(args.topic, TOPICS[args.topic], output_dir)
    else:
        for topic, meta in TOPICS.items():
            sync_topic(topic, meta, output_dir)

    print("\nSync complete!")


if __name__ == "__main__":
    main()
