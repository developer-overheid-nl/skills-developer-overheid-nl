# State naamconventies

States worden gebruikt in Figma, code, design tokens en andere APIs. Gebruik altijd de gestandaardiseerde namen gebaseerd op webstandaarden.

## Interactie-states
| State | Gebaseerd op | Gebruik |
|---|---|---|
| `active` | `:active` in CSS | Component ingedrukt (muis, touch, toetsenbord) |
| `focus` | `:focus` in CSS | Component heeft toetsenbordfocus |
| `focus-visible` | `:focus-visible` in CSS | Visueel focusindicator tonen |
| `hover` | `:hover` in CSS | Aanwijzer boven component |

## Overige states
| State | Gebaseerd op | Gebruik |
|---|---|---|
| `checked` | `:checked` CSS / `checked` HTML attr | Checkbox, Radio Button, Switch |
| `current` | `aria-current` | Huidige pagina/stap in navigatie |
| `disabled` | `:disabled` CSS / `disabled` HTML attr | Component uitgeschakeld |
| `expanded` | `aria-expanded` | Extra content geopend |
| `indeterminate` | `:indeterminate` CSS | Checkbox in tussenstaat |
| `invalid` | `:invalid` CSS / `aria-invalid` | Formuliervalidatie mislukt |
| `pressed` | `aria-pressed` | Toggle button ingedrukt |
| `read-only` | `:read-only` CSS / `readonly` HTML attr | Waarde tonen, niet aanpassen |
| `required` | `:required` CSS / `required` HTML attr | Verplicht veld |
| `selected` | `aria-selected` | Item geselecteerd uit verzameling |
| `visited` | `:visited` in CSS | Link al bezocht |

## Tegenovergestelde states
- 🔴 Verzin **geen** eigen naam voor de tegenovergestelde state.
- ✅ Gebruik het **"not something"** patroon: `not checked`, `not disabled`, `not expanded`.
- 🔴 Gebruik **niet**: `unchecked`, `enabled`, `collapsed` (zelfbedacht, geen webstandaard).
