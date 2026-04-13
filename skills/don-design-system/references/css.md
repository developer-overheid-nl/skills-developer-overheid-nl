# CSS conventies

## Huisstijl onafhankelijk
- 🔴 Geen hardcoded waarden voor designbeslissingen (kleur, grootte, spacing). Gebruik altijd CSS custom properties (component design tokens).
- 🔴 Geen huisstijl-tokens van de eigen organisatie in gedeelde componenten.
- ✅ Gebruik component design tokens: `var(--example-button-background-color)`
- ✅ Gebruik basis tokens als fallback voor componenten buiten het design system.

## Geïsoleerde theming
- Thema-code staat in een **apart thema-bestand**, nooit in de component-CSS zelf.
- Thema's worden geactiveerd via een **expliciete CSS class** (bijv. `.example-theme`), nooit via `:root`.
- Gedeelde CSS heeft **geen side-effects**: stijlen hebben pas effect na toepassen van een class.

## Herleidbare prefix
- Alle class names, CSS custom properties en keyframes beginnen met een **organisatie-prefix**.
- De prefix bestaat alleen uit letters en cijfers (geen koppelstreepjes erin).
- Gebruik the prefix van de organisatie die het component beheert, ook in andere applicaties.

## BEM-format
- Class names volgen **BEM** (Block, Element, Modifier):
  - Block: `.example-button`
  - Element: `.example-button__icon`
  - Modifier: `.example-button--primary`

## Lage CSS-specificity
- Gebruik **geen ID-selectors** (`#id`) in component-CSS.
- Gebruik **geen `!important`** tenzij absoluut noodzakelijk.
- Geef de voorkeur aan class selectors boven element selectors.

## Herbruikbare mixins
- Bied CSS-onderdelen aan als **SCSS mixin** in een apart `_mixin.scss` bestand.
- Zo kunnen andere projecten dezelfde stijlen toepassen op afwijkende selectors.
