# Design Token conventies

## Naamgeving
- Namen bestaan **alleen uit kleine letters en koppelstreepjes** (geen hoofdletters, underscores of spaties).
- Namen beginnen **altijd met een letter**, nooit met een cijfer. Gebruik bijv. `level-1` in plaats van `1`.
- Tokens hebben altijd een **organisatie-prefix** (bijv. `nl-`, `ams-`, `utrecht-`).
- De token-naam **eindigt op een bestaande CSS property-naam** (bijv. `color`, `font-size`, `border-radius`).

## Structuur
De aanbevolen structuur is: `prefix.component.element-of-variant.state.css-property`

Voorbeelden:
- `example.button.background-color` ✅
- `example.text-input.placeholder.color` ✅ (met element)
- `example.paragraph.lead.font-size` ✅ (met variant)
- `example.button.disabled.cursor` ✅ (met state)

## CSS logical properties
Gebruik **altijd** CSS logical properties. Gebruik **niet** de fysieke equivalenten:

| ✅ Gebruik dit | 🔴 Niet dit |
|---|---|
| `block-size`, `min-block-size`, `max-block-size` | `height`, `min-height`, `max-height` |
| `inline-size`, `min-inline-size`, `max-inline-size` | `width`, `min-width`, `max-width` |
| `padding-block`, `padding-inline` | `padding-top`, `padding-bottom`, `padding-left`, `padding-right` |
| `margin-block`, `margin-inline` | `margin-top`, `margin-bottom`, `margin-left`, `margin-right` |

## Platformonafhankelijke waarden
- ✅ Gebruik: `24px`, `#FF0000`, `1.5`
- 🔴 Vermijd: `1ch`, `2em`, `cornflowerblue` (CSS-only, werkt niet in Figma/Android)
- 🔴 Vermijd CSS keywords als token-waarde: `auto`, `currentColor`, `flex-end`, `inherit`, `monospace`

## Geen tokens voor layout-properties
Gebruik **geen** design tokens for:
- `display` (bijv. `none`, `flex`)
- `flex-direction` (bijv. `column`, `row`)
- `overflow` (bijv. `auto`, `hidden`)
- `position` (bijv. `sticky`, `absolute`)

Deze properties kun je wel als interne CSS variabelen gebruiken, maar niet als gepubliceerde design tokens.

## Essentiële tokenparen voor white-label componenten
- Voeg `color` en `background-color` altijd **als paar** toe (voor voldoende contrastmogelijkheden).
- Voeg `font-size` en `line-height` altijd **als paar** toe.
- Gebruik liever `min-inline-size`/`max-inline-size` dan `inline-size` (flexibeler voor responsive en toegankelijkheid).

## tokens.json metadata
Publiceer een `tokens.json` zonder `$value`, alleen met `$type` en `$extensions`:
```json
{
  "example": {
    "button": {
      "background-color": {
        "$type": "color",
        "$extensions": {
          "nl.nldesignsystem.css-property-syntax": "<color>",
          "nl.nldesignsystem.figma-implementation": true
        }
      }
    }
  }
}
```
