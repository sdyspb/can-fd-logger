# V15 (1.5 V) — конфигурация источника питания FC7300F8MDT

Назначение выводов **V15_CFG** и **V15_BASE_DRIVER** и варианты конфигурации
источника питания ядра **V15** (шина **V15_MCU** на демо-платах FC7300).

> **Целевой чип:** Flagchip **FC7300F8MDT** (BGA320). V15 — внутреннее доменное
> напряжение ядра: **1.425…1.89 V** (абс. максимум −0.3…2.5 V). Из домена V15
> внутренним LDO формируется V11 (0.99…1.21 V) для core.

## Вывод (TL;DR)

Источник V15 выбирается **strapping-выводом V15_CFG в момент power-up** +
программно (регистр PMC):

| Режим | V15_CFG | Источник V15 | Когда использовать |
| :--- | :---: | :--- | :--- |
| **1. Внешний** (PMIC / DC-DC / LDO на плате) | **1** (pull-up на VDD_HV_A) | Внешний преобразователь питает V15 напрямую | Основной вариант для нашего шилда (rail 1.6 V из `power.md`) |
| **2. NPN mode** | **0** (pull-down на GND) | Внешний NPN-транзистор, управляемый чипом через **V15_BASE_DRIVER** (внешний LDO) | Когда нужен только один внешний rail 3.3 V / 5 V (single-supply) |
| **3. Внутренний LDO** | **0** + `V15_CTRL_EN` | Встроенный LDO PMC из VDD_HV_A (3…5.5 V) | Только на время startup; V15 работает в FPM, внутренний LDO отключается, когда выбран внешний режим |

Проверить активный источник: бит **V15_STATUS** (PMC LVSCR, bit 30):
`00b` — внутренний LDO; `01b` — внутренний контроллер + NPN; `10b` — внешний
драйвер (V15_CFG = 1); `11b` — зарезервировано.

## Выводы

| Вывод | BGA | LQFP | Назначение |
| :--- | :---: | :---: | :--- |
| **V15_CFG** | J5 | 15 | Strapping-конфигурация источника V15. Чится при power-up. `1` (pull-up через **1 kΩ** на VDD_HV_A) — внешний источник; `0` (на GND) — внутренний (NPN mode / LDO) |
| **V15_BASE_DRIVER** | K5 | 16 | Только NPN mode: источник тока базы внешнего NPN-транзистора (вместе с NPN образует LDO). DEFAULT = DISABLED, ALT0 = V15_BASE_DRIVER. **Нельзя использовать как обычный GPIO** (AN0001 V0.7, п.14) |
| **V15_0…V15_3** | K6, R11, K13, H11 | 18, 73, 111, 152 | Силовые пины домена V15 (питание ядра). На каждом — обязательный внешний конденсатор |

## Режим 1 — внешний источник (V15_CFG = 1)

- Внешний DC-DC / LDO / PMIC питает шины V15_0…3 (1.425…1.89 V).
- **Sequencing:** V15 включать **после** того, как VDD_HV_A достигнет **2.3 V**
  (RM V2.3, p189). Дополнительное ограничение из RM (гл. PMC): при V15_CFG = 1
  V15 может формироваться только после того, как V5 > 1.5 V.
- Внутренний V15 LDO **отключается** (datasheet §3.8).
- На шилде FC7300 (наш проект): rail **1.6 V / 3 A** (3.3 V → 1.6 V, см.
  [`power.md`](power.md)) = внешний V15. Схема: `V15_CFG` — pull-up 1 kΩ на
  VDD_HV_A; V15_BASE_DRIVER не используется (не подключать как GPIO).
- Ток: по layout hints демо-платы rail V15 расчитывается **≥ 2 A**.

## Режим 2 — NPN mode (V15_CFG = 0)

Топология (AN0001 V0.7, p3): чип через **V15_BASE_DRIVER** управляет внешним
NPN-транзистором; NPN образует линейный регулятор (LDO):

```
VDD_HV_A (3.3/5 V) ──► Коллектор NPN ──► Эмиттер NPN ──► [100 mΩ] ──► V15 (1.5 V)
                                                                    │
V15_BASE_DRIVER ──[Rbase]──► База NPN                     [4.7 µF] ┴──► GND
```

| Параметр | Значение |
| :--- | :--- |
| Rbase (V15_BASE_DRIVER → база) | **100 R** при VDD_HV_A = 5 V; **22 R** при VDD_HV_A = 3.3 V |
| Вход LDO (коллектор) | Не повышать — тепловые потери NPN; 3.3 V достаточно (IO-трасса 3.3 V → single-supply система) |
| Выход LDO (эмиттер) | 100 mΩ + 4.7 µF к GND (стабильность) |
| Рекомендуемые NPN | MJD44H11A, MJD148Q, MJD2873Q (RM); также MJD31CHQ, NJD2873T4 (AN0001) |

При выборе NPN mode на startup **внутренний V15 LDO работает только на время
startup**, далее — внешний NPN-LDO (datasheet §3.8).

## Режим 3 — внутренний V15 LDO

| Параметр | Значение (datasheet, Table 11) |
| :--- | :--- |
| Вход | VDD_HV_A, 3…5.5 V |
| Выход | 1.42…1.89 V |
| Внешний конденсатор | 3.8…5.6 µF (тип. 4.7 µF) на пины V15 |

## Программное управление / статус (PMC)

| Ресурс | Назначение |
| :--- | :--- |
| `V15_CFG` (PAD) | Strapping: внешний (1) / внутренний (0). Устанавливается **до** power-up |
| `V15_CTRL_EN` (PMC CONFIG reg.) | Переключение между внутренним регулятором (LDO) и внутренним контроллером (NPN) при V15_CFG = 0 |
| `V15_STATUS` (PMC LVSCR, bit 30) | Текущий источник: 00b — LDO; 01b — контроллер + NPN; 10b — внешний; 11b — res. |

## Электрорежимы V15 (datasheet A4)

| Параметр | Значение |
| :--- | :--- |
| Рабочий диапазон | 1.425…1.89 V |
| Абс. максимум | −0.3…2.5 V |
| LVD (low-voltage reset) | 1.34…1.42 V |
| HVD (high-voltage detect) | 1.94…2.06 V |
| Режимы | Только **FPM** (Full Performance); в RPM V15 не поддерживается |
| Зависимые домены | V11 (внутр. LDO из V15, вход 1.47…2.0 V тип. 1.55); V25 — из VDD_HV_A |

## V15_MCU на демо-платах FC7300

Схемах `FC7300_Demo_Schematic_JL_V2.0` / `FC7300_Demo_V1.0_Schematic_YT`
(лист `02A_FC7300_PWR`):

- **V15_MCU** — имя шины 1.5/1.6 V, питающей V15_0…3 ядра (K6/R11/K13/H11).
- Источник на плате: buck **1.65 V** (шины `1v6_en / 1v6_sw / 1v6_fb / 1v6_bst /
  1v6_buck_vcc`, enable `v16_en_g1/g2`) — **NPN or Buck — optional mount**
  (выбор через V15_CFG).
- Примечание на схеме: `V15_CFG=high, V15 from external Power, power up after
  Vdd_hv_A reach 2.3V!! V15_CFG=low, V15 from NPN LDO.`
- Layout hints: V15 ≥ 2 A; VDD_HV_A ≤ 1 A; VDD_HV_B ≤ 500 mA; VDD_HV_B ≤
  VDD_HV_A; для Ethernet VDD_HV_B = 3.3 V.

## Источники

| Документ | Место | Раздел |
| :--- | :--- | :--- |
| FC7300 Data Sheet A4 | `Y:\Flagchip\FC7300\` | §3.8 PMC Internal LDO (Tables 10–12), Tables 2–3 (abs. max / operating), §3.5 (LVD/HVD V15), pin table (p63) |
| FC7300 Reference Manual V2.3 | `Y:\Flagchip\FC7300\FC7300F8MDQ\` (V2.2 — в корне) | p189 — выбор NPN/PMIC для V15; p329–330 — PMC: V15_CFG / V15_CTRL_EN / V15_STATUS, регистр LVSCR |
| AN0001 Hardware Design Guideline V0.7 | `Y:\Flagchip\FC7300\Application Note\` | p3 — топология NPN mode, Rbase, NPN; p14 — примечания по V15_CFG / V15_BASE_DRIVER |
| FC7300F8MDT Pinout_V1.3.xlsx | `hardware\pinout\` (копия в `Y:\Flagchip\FC7300\`) | листы `Pinout_FC7300F8MDT`, `BGA_mapping` — координаты шаров |
| Demo-схемы JL V2.0 / YT V1.0 | `hardware\pdf\fc7300\` | лист `02A_FC7300_PWR` — шина V15_MCU, buck 1.65 V |
| [`power.md`](power.md) | `hardware\schematics\` | Rail 1.6 V / 3 A шилда = внешний V15 |
