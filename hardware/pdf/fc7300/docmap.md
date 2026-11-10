# Карта документации FC7300

Индекс документации по контроллеру **Flagchip FC7300** для типовых запросов.
Уровень — средний: что где лежит и куда смотреть, без углубления в содержимое.

**Основной источник:** сетевая директория `Y:\Flagchip\FC7300` (полный комплект
вендорской документации). **Локальные копии** — в `hardware\pdf\fc7300\` (схемы
демо-платы) и `hardware\pinout\` (пинаут).

## Ключевые документы (актуальные версии)

| Документ | Путь | Для чего |
| :--- | :--- | :--- |
| **FC7300 Data Sheet A4** | `Y:\Flagchip\FC7300\FC7300 Data Sheet_A4.pdf` | Электрорежимы чипа: abs. max / operating ranges, LDO V25/V15/V11 (Tables 10–12), LVD/HVD, ESD, I/O DC, pin table |
| **FC7300 Reference Manual V2.3** | `Y:\Flagchip\FC7300\FC7300F8MDQ\FC7300 Reference Manual_V2.3.pdf` (V2.2 — в корне) | Архитектура модулей и регистры: питание/PMC (гл. 18), FLEXCAN, Ethernet, SPI, I2C, UART, ADC, clocking, boot |
| **FC7300F8MDT Pinout V1.3** | `Y:\Flagchip\FC7300\FC7300F8MDT Pinout_V1.3.xlsx` + локально `hardware\pinout\` | Назначение шаров BGA320, MUX-функции (DEFAULT/ALT0–7), домены питания, BGA_mapping |
| **AN0001 Hardware Design Guideline V0.7** | `Y:\Flagchip\FC7300\Application Note\` | Рекомендации по схемотехнике: питание (вкл. NPN mode V15), обвязка, strapping-выводы, layout |
| **AN0002 SBC适配分析 V0.3** | `Y:\Flagchip\FC7300\Application Note\` (копия в `SCH_PCB_Lib\`) | Анализ подключения FC7300 к SBC |
| **AN0003 LBIST MISR V0.1** | `Y:\Flagchip\FC7300\Application Note\` | Настройка LBIST/MISR |
| **FC7300 Errata Sheet V4.5-1** | `Y:\Flagchip\FC7300\` (архивы V2.0–V3.4 — в `Errata\`) | Известные ошибки кремния |
| **FC7300 Clocking Diagram V1.3** | `Y:\Flagchip\FC7300\` | Схема генерации тактов (PLL/oscillators) |
| **FC7300 Security User Guide V1.0** | `Y:\Flagchip\FC7300\` | Безопасность (secure boot и т.п.) |
| **SDK V2.6.0 + Bootloader v3.0.3** | `Y:\Flagchip\FC7300\FC7300 SDK + Bootloader\` | Firmware: драйверы, примеры, проект IAR; загрузчик (flashing) |
| **SDK Quick Start / SDK User Guide V0.2 / IDE Guide V2.0** | `…\SDK_V2_6_0\`, `FC7300 SDK User Guide and IDE Guide\` | Вход в SDK, сборка, IDE (FCIAR) |
| **EVB / демо-платы** | `Y:\Flagchip\FC7300\EVB\` + локально `hardware\pdf\fc7300\` | Схемы (JL V2.0, YT V1.0), layout, 3D, User Manual, Hardware Design Guideline V0.3 |
| **FC7300 rev. C (F4MDD/F4MDS T1C)** | `Y:\Flagchip\FC7300\FC7300 rev. C\` | Данные по вариантам F4MDD/F4MDS (T1C): datasheets, RM V0.3, сравнения с Infineon TC2x/TC3x |
| **FC7300F8MDQ** | `Y:\Flagchip\FC7300\FC7300F8MDQ\` | Вариант F8MDQ: datasheet V0.3, RM V0.4, errata V0.2.2 |
| **SafetyDemo** | `Y:\Flagchip\FC7300\SafetyDemo\` | Safety Manual V0.4.4 + safety-библиотеки |
| **SCH_PCB_Lib** | `Y:\Flagchip\FC7300\SCH_PCB_Lib\` | CAD-библиотеки: footprint BGA320, символы (Altium/Cadence), минимальная система |
| **eFTU -_ GMT** | `Y:\Flagchip\FC7300\eFTU -_ GMT\` | Презентация EFTU (англ./кит.) |

## Типовые запросы → куда смотреть

| Запрос | Документ / место |
| :--- | :--- |
| Функция пина X / шар BGA / MUX-режимы | `Pinout_V1.3.xlsx` (листы `Pinout_FC7300F8MDT`, `BGA_mapping`) |
| Питание V15/V25/V11, **V15_CFG**, **V15_BASE_DRIVER**, NPN mode, **V15_MCU** | AN0001 V0.7 p3/p14 · RM V2.3 p189, p329–330 · DS A4 §3.8 · локально: [`v15_mcu-config.md`](../schematics/v15_mcu-config.md) |
| Abs. max / operating ranges, LVD/HVD, токи IDD | DS A4, Tables 2–9 |
| Тактирование, PLL, кристаллы 24/32 MHz | `FC7300 Clocking Diagram_V1.3.pdf` + RM (Clocking chapter) |
| FLEXCAN / CAN FD / base driver / wake-up | RM (FLEXCAN chapter) + демо-схемы (трансиверы) |
| 1000Base-T1 / Ethernet MAC / RGMII | RM (ETH chapter) + демо-схемы (листы T1 PHY) |
| Boot / bootloader / flashing / ISP | `FC7300_BootLoader` + RM (Boot chapter); ISP — пин PTD21 (AN0001 p14) |
| SDK / драйверы / примеры / сборка IAR | `FC7300 SDK V2.6.0` + Quick Start + SDK User Guide |
| Errata / известные проблемы | `FC7300 Errata Sheet_V4.5-1.pdf` |
| Схема демо-платы / питание EVB / V15_MCU | `EVB\` (локальные копии — `hardware\pdf\fc7300\`), лист `02A_FC7300_PWR` |
| Подключение к SBC (ArmSoM и др.) | `AN0002 SBC适配分析` + локально: `hardware\schematics\` (40-pin-*, spi-wiring-*) |
| Footprint BGA320 / символы / мин. система | `SCH_PCB_Lib\` |
| Безопасность / safety | `Security User Guide`, `SafetyDemo\` |
| Сравнение вариантов (F4MDD/F4MDS/F8MDQ vs TC2x/TC3x) | `FC7300 rev. C\` (xlsx-сравнения), `FC7300F8MDQ\` |

## Локальные копии в репозитории

| Файл | Источник |
| :--- | :--- |
| `FC7300_Demo_Schematic_JL_V2.0.pdf`, `FC7300_Demo_V1.0_Schematic_YT.pdf`, `FC7300_Demo_Board_3D_Top.jpg` | `EVB\` (схемы демо-плат) |
| `..\pinout\FC7300F8MDT Pinout_V1.3.xlsx` | корень `Y:\Flagchip\FC7300` |
| `..\pinout\fc7300-320-pin-a1.xlsx` | локальная выжимка пинаута под шилд (см. `pinout-rules-xls.md`) |
| `..\schematics\fc7300-hat-pinout.md`, `v15_mcu-config.md` | разборы на основе пинаута/документации |

> ⚠️ Версии: при работе по конкретному вопросу брать **самую новую** версию
> документа из списка выше (напр. RM V2.3 > V2.2; AN0001 V0.7 > EVB V0.3;
> Errata V4.5-1 > V3.4).
