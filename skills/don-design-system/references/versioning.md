# Versioning conventies

## Semantic Versioning (SemVer)
Kies de juiste versie op basis van de aard van de wijziging:

| Versie | Wanneer | Voorbeelden |
|---|---|---|
| **`patch`** | Bugfixes zonder API-wijziging | Waarde van design token aangepast, spelfout in beschrijving gecorrigeerd |
| **`minor`** | Nieuwe functionaliteit, backwards-compatibel | Design token toegevoegd, nieuwe export, class name toegevoegd |
| **`major`** | Breaking change | Design token verwijderd/hernoemd, class name verwijderd/hernoemd, export verwijderd, type signature verkleind |

**Leidraad voor breaking changes:**
- 🔴 Design token **verwijderd of hernoemd** → major (ook spellingcorrectie!)
- 🔴 CSS class name of mixin **verwijderd of hernoemd** → major
- 🔴 JavaScript/TypeScript **export verwijderd** of **naam gewijzigd** → major
- 🟡 CSS property **waarde uitgebreid** (bijv. `color: blue` → `color: var(--x, blue)`) → major (breaking voor CSS cascade)

## Changesets
- Voeg een **changeset toe bij elke wijziging** in een gepubliceerd package.
- Geen changeset nodig voor: documentatie-updates, build-configuratie.
- Schrijf changelogs **vanuit het perspectief van de gebruiker**:
  - patch: "Kan ik veilig installeren?"
  - minor: "Zijn er nieuwe mogelijkheden?"
  - major: "Wat moet ik aanpassen in mijn code?"
- Bij een **major update**: beschrijf **wat** er veranderd is, **waarom**, en **hoe** de gebruiker migreert.
- Zorg dat **elke pull request** met package-wijzigingen een changeset bevat.

## Deprecation
- Markeer verouderde packages via `npm deprecate`, **verwijder ze niet** van npm.
- Bij hernoemde packages: verwijs in het deprecation-bericht naar de nieuwe naam.
- Deprecation kan ongedaan gemaakt worden met een lege reden: `npm deprecate <pkg> ""`
