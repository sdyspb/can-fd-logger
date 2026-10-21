# Schematics

Описание существующих схем проекта. Проект делится на **два этапа**:

## Этапы проекта

### Этап 1 — Шилд на FC7300 (Stage 1)

Разработка собственного 8-канального CAN FD шилда вокруг контроллера **Flagchip FC7300F8MDT**
(BGA320). Шилд содержит:

- 8 × FLEXCAN (1 × Wakeup + 7 × standard)
- 1 × RGMII → 1000Base-T1 Ethernet
- 1 × UART (debug console)
- 1 × I2C (system EEPROM)
- 1 × SPI (NOR Flash)
- SWD / JTAG debug connector
- Три регулятора: 12 V → 5 V / 3.3 V / 1.6 V
- CAN `VBAT` напрямую от 12 V (wake-up)

Схемы этапа 1:

| Файл | Содержание |
| :--- | :--- |
| [`fc7300-hat-fbd.md`](fc7300-hat-fbd.md) | Диаграмма подключения всех интерфейсов к FC7300F8MDT (CAN, RGMII, SPI, I2C, UART, SWD/JTAG, RESET/ISP) |
| [`fc7300-hat-pinout.md`](fc7300-hat-pinout.md) | Полный пинаут BGA320 под шилд: активные интерфейсы, MUX-режимы, домены питания, отладочные сигналы |
| [`power.md`](power.md) | Схема питания шилда: 12 V → 5 V / 3.3 V / 1.6 V (три регулятора), CAN VBAT, опция UPS от LiFePO4 |

### Этап 2 — Подключение шилда к одноплатнику (Stage 2)

Подключение готового шилда FC7300 к SBC **ArmSom Sige7** (RK3588). Два варианта транспорта:

- **SPI** — шилд выступает как SPI-устройство на 40-pin GPIO заголовке SBC
- **Ethernet (1000Base-T1)** — шилд подключается по RGMII / 1000Base-T1 к SBC

Схемы этапа 2:

| Файл | Содержание |
| :--- | :--- |
| [`40-pin-sige7-spi.md`](40-pin-sige7-spi.md) | Распиновка 40-pin заголовка Sige7 под SPI-интерфейсы (SPI0, SPI1, SPI3) |
| [`spi-wiring-40pin-sige7.md`](spi-wiring-40pin-sige7.md) | Адаптерная плата для подключения 4 × CAN FD шилдов (MCP251xFD) к Sige7 по SPI: pin mapping, Device Tree, jumper config |
| [`40-pin-sige5-spi.md`](40-pin-sige5-spi.md) | Распиновка 40-pin заголовка Sige5 под SPI-интерфейсы (reference, SPI4) |
| [`can-wakeup.md`](can-wakeup.md) | Реализация пробуждения RK3588 по CAN-шине через `/IRQ` MCP2518FD на GPIO0 (PMUIO) |
| [`system_controller.md`](system_controller.md) | RP2040 как always-on системный контроллер: питание, ignition, battery, power sequencing |

> **Примечание:** файлы `40-pin-sige7-spi.md`, `spi-wiring-40pin-sige7.md`, `40-pin-sige5-spi.md`
> и `can-wakeup.md` описывают подключение **Waveshare 2-CH CAN FD HAT** (MCP2518FD) —
> это промежуточное решение до готовности собственного шилда FC7300.
> После завершения этапа 1 эти схемы будут заменены на подключение шилда FC7300
> по SPI или Ethernet.

## Все файлы

| Файл | Этап | Описание |
| :--- | :---: | :--- |
| [`fc7300-hat-fbd.md`](fc7300-hat-fbd.md) | 1 | Диаграмма интерфейсов FC7300F8MDT (CAN, RGMII, SPI, I2C, UART, SWD, RESET) |
| [`fc7300-hat-pinout.md`](fc7300-hat-pinout.md) | 1 | Пинаут BGA320 для шилда: MUX, домены, отладка |
| [`power.md`](power.md) | 1 + 2 | Питание: 12 V PD, LiFePO4 UPS, FC7300 shield rails (5 V / 3.3 V / 1.6 V), CAN VBAT |
| [`40-pin-sige7-spi.md`](40-pin-sige7-spi.md) | 2 | 40-pin Sige7 SPI pinout (SPI0 / SPI1 / SPI3) |
| [`spi-wiring-40pin-sige7.md`](spi-wiring-40pin-sige7.md) | 2 | Адаптер 4 × MCP251xFD shields → Sige7 40-pin (pin map, DT, jumpers) |
| [`40-pin-sige5-spi.md`](40-pin-sige5-spi.md) | 2 | 40-pin Sige5 SPI pinout (reference) |
| [`can-wakeup.md`](can-wakeup.md) | 2 | Wake-up RK3588 по CAN через MCP2518FD `/IRQ` на GPIO0 |
| [`system_controller.md`](system_controller.md) | 2 | RP2040 always-on controller: power sequencing, ignition, battery |