# API conventies

## Taal en naamgeving
- Gebruik **Engels** als taal voor de API van UI-componenten.
- Baseer namen op bestaande termen uit het **Web Platform**: HTML, CSS, SVG en ARIA.
- Vermijd namen uit populaire frameworks (React, Vue, Angular) of zelfbedachte namen als een Web Platform term beschikbaar is.
- Bied APIs aan om **alle hardcoded teksten** in een component aan te passen (i18n-vriendelijk).

## npm packages
- Gebruik **semantic versioning** voor alle wijzigingen.
- Gebruik `"type": "module"` in `package.json`.
- Bestanden die via `"exports"` of `"files"` worden gedeeld, zijn onderdeel van de publieke API.

## Breaking changes vermijden
- Gebruik **enumeration attributes** (string values) in plaats van boolean attributes voor varianten.
- 🔴 Vermijd: `<Button danger>` (boolean — lastig uit te breiden zonder breaking change)
- ✅ Gebruik: `<Button variant="danger">` (enumeration — makkelijk uitbreidbaar)
- Globale HTML-attributen (`data-*`, `dir`, `hidden`, `id`, `lang`, `tabIndex`, `aria-*`) moeten **hun normale gedrag behouden**.

## JavaScript
- Gebruik **ES Modules** in bestanden met extensie `.mjs`.
- Geen CommonJS (`require`) in nieuwe code.

## TypeScript
- Lever altijd `.d.ts` en `.d.mts` typebestanden mee in npm packages.

## React
- Gebruik **geen `React.FC`** (verouderd patroon).
- Sta extra HTML-properties toe via **spread operators**: `{...props}` voor HTML-elementen.
- Gebruik `forwardRef` om refs door te sturen naar het onderliggende HTML-element.
