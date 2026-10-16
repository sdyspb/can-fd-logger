# Rule for Cline: Pinout Table (Short)

## Columns
`Pin | Ball | Type | Side | №`

- `Pin` — имя пина (см. Naming).
- `Ball` — координата в BGA-корпусе (например, `B4`). Заполнять, если у чипа есть BGA-карта.
- `Type`: `PWR`, `GND`, `BIDIR`, `INPUT`, `OUTPUT`.
- `Side`: `LEFT`, `RIGHT` (см. Grouping).
- `№` — номер пина из Datasheet-таблицы (LQFP и т.д.). Пусто, если у чипа несколько корпусов и пин существует только в BGA (нет LQFP-эквивалента).

## Grouping
1. Split into separate tables by function: `GPIO`, `PWR`, `GND` (optionally `Control` for RESET, XTAL, ISP etc.).
2. GPIO: if the device has port banks, put each bank on its own sheet (`GPIO1`, `GPIO2`, …). If banks are not defined in the datasheet, use a single `GPIO` sheet.
3. If a block is a GPIO bank — set `Side = RIGHT` only.
4. For `Ground` / `Power` blocks with many identical pins — distribute `LEFT` / `RIGHT` roughly evenly.

## Naming
- Multi-function GPIO pins: `<Pin Name>/<FUNC1>/<FUNC2>/...` — no spaces.
  - First item is the **pin name from the Datasheet** (e.g., `PTA4`, `GPIO0`).
  - Then **all alternative functions** from the MUX table in the order given by the Datasheet (`DEFAULT`, `ALT0`, `ALT1`, …).
  - Do **not** wrap in `GPIO[n]`-style brackets (that was specific to the FX3 reference only).
  - Skip duplicates (if a function appears in both DEFAULT and some ALT, list it once).
  - Keep `DISABLED` if it is listed in the Datasheet as a real function value.
- Duplicate pin names: `ORIGINAL_NAME_1`, `ORIGINAL_NAME_2`, … (underscore + number, starting from 1).

## Sorting
Within each block keep the Datasheet row order. For GPIO: by port bank ascending, then by pin number (or LQFP order when both apply).

## Document Format
- Single `.md` file.
- Title: `# <Device> — Pinout`.
- One `## <Block>` section per functional block.
- Section order: `GND`, `PWR`, then GPIO banks ascending (or `GPIO` if no banks).
- Each section contains exactly one table, no extra text between tables.

## Example
```markdown
# FC7300F8MDT — Pinout

## GND
| Pin | Ball | Type | Side | № |
|:----|:-----|:-----|:-----|---:|
| VSSA_0 | K8 | GND | LEFT |  |
| VSS_1  | VSS | GND | LEFT | 177 |
| VSS_2  | VSS | GND | RIGHT| 177 |

## PWR
| Pin | Ball | Type | Side | № |
|:----|:-----|:-----|:-----|---:|
| VDDA_0 | H9 | PWR | LEFT | 1 |

## GPIO
| Pin | Ball | Type | Side | № |
|:----|:-----|:-----|:-----|---:|
| JTAG_TMS/SWD_DIO/PTA4/CMP0_OUT | B4 | BIDIR | RIGHT | 172 |
| ADC1_SE14/PTA8/FCUART2_RX | A3 | BIDIR | RIGHT | 175 |
```

## XLS Output
- Same columns in A–E: `Pin | Ball | Type | Side | №`.
- **Each functional block (`GND`, `PWR`, `GPIO1`, …) must be placed on a separate worksheet (tab).**
- Worksheet name = block name (e.g., `GND`, `PWR`, `GPIO`).
- Sheet order follows the document section order.
- No extra rows, columns, or sheets (no header row inside the sheet).

> ⚠️ **Предупреждение:** Never reorder rows, change pin names/case, or mix blocks in one table. Always split blocks into separate tabs in XLS.