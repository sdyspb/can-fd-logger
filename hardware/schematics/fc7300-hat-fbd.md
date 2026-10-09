# Диаграмма подключения интерфейсов к контроллеру FC7300F8MDT

Распределение всех разработанных интерфейсов шилда и портов отладки по конкретным физическим выводам микроконтроллера FC7300F8MDT в корпусе BGA320.

```mermaid
graph LR
    %% Стилизация компонентов
    classDef mcu fill:#1a365d,stroke:#0f172a,stroke-width:2px,color:#ffffff;
    classDef can fill:#d97706,stroke:#7c2d12,stroke-width:1px,color:#ffffff;
    classDef eth fill:#059669,stroke:#064e3b,stroke-width:1px,color:#ffffff;
    classDef debug fill:#dc2626,stroke:#7f1d1d,stroke-width:1px,color:#ffffff;
    classDef peri fill:#4f46e5,stroke:#1e1b4b,stroke-width:1px,color:#ffffff;

    %% Центральный процессор
    MCU[«MCU Flagchip»<br>FC7300F8MDT<br>BGA320]:::mcu

    %% Группа интерфейсов CANFD
    subgraph CANFD_Group [Сеть CANFD]
        CAN_W[CAN0 Wakeup<br>PTE21 / PTE22]:::can
        CAN1[CAN1FD<br>PTA11 / PTA12]:::can
        CAN2[CAN2FD<br>PTD16 / PTD15]:::can
        CAN3[CAN3FD<br>PTA31 / PTB18]:::can
        CAN4[CAN4FD<br>PTC8 / PTB17]:::can
        CAN5[CAN5FD<br>PTC13 / PTC12]:::can
        CAN6[CAN6FD<br>PTC19 / PTC24]:::can
        CAN7[CAN7FD<br>PTD25 / PTB10]:::can
    end

    %% Группа Ethernet RGMII
    subgraph ETH_Group [Сеть Ethernet Gigabit]
        RGMII_TX[RGMII TX Линии<br>PTC2, PTD7, PTD6, PTD5<br>TX_EN CTL: PTD12<br>TX_CLK: PTD11]:::eth
        RGMII_RX[RGMII RX Линии<br>PTC1, PTC0, PTD9, PTB23<br>RX_DV CTL: PTD8<br>RX_CLK: PTD10]:::eth
        SMI_MGMT[SMI Управление PHY<br>MDC: PTE8<br>MDIO: PTB4]:::eth
    end

    %% Системная периферия
    subgraph PERI_Group [Периферия шилда]
        UART_CONS[Отладочная консоль UART1<br>D2: PTA18 TX<br>D3: PTA19 RX]:::peri
        I2C_EEPROM[Шина EEPROM I2C1<br>V4: PTB5 SDA<br>V5: PTB30 SCL]:::peri
        SPI_FLASH[NOR Flash Memory SPI2<br>L3: PTE11 CS<br>L2: PTE10 MISO<br>M1: PTE13 CLK<br>M2: PTA25 MOSI]:::peri
    end

    %% Отладка и Программирование
    subgraph DEBUG_Group [Интерфейс отладки и ISP]
        SWD_LINES[SWD Порт отладки<br>E7: PTC4 SWD_CLK<br>B4: PTA4 SWD_DIO]:::debug
        JTAG_LINES[Доп. линии JTAG<br>C6: PTC5 TDI<br>F8: PTA10 TDO]:::debug
        SYS_CTRL[Линии управления<br>B5: RESET_b<br>H16: PTD21 ISP_EN_B]:::debug
    end

    %% Связи интерфейсов с контроллером
    MCU <==>|ALT4 / ALT3| CAN_W
    MCU <==>|ALT3| CAN1
    MCU <==>|ALT3| CAN2
    MCU <==>|ALT5| CAN3
    MCU <==>|ALT4 / ALT5| CAN4
    MCU <==>|ALT5| CAN5
    MCU <==>|ALT3| CAN6
    MCU <==>|ALT5 / ALT4| CAN7

    MCU ===>|ALT5 UHS| RGMII_TX
    MCU <===|ALT4 / ALT5 UHS/HS| RGMII_RX
    MCU <==>|ALT5| SMI_MGMT

    MCU ===>|ALT4| UART_CONS
    MCU <==>|ALT3| I2C_EEPROM
    MCU <==>|ALT5| SPI_FLASH

    MCU <===|ALT0| SWD_LINES
    MCU <==>|ALT0| JTAG_LINES
    MCU <===>|Dedicated / ALT0| SYS_CTRL
```

# Mermaid-диаграмма с радиальным расположением интерфейсов вокруг контроллера

Для того чтобы обойти стандартную особенность вертикального рендеринга Mermaid (сверху вниз) и расположить устройства строго **вокруг** контроллера, используется радиальная структура связей. Ниже представлена переработанная диаграмма, где за счет жесткого распределения невидимых связей блоки разнесены по сторонам света относительно центрального процессора.

```mermaid
graph LR
    %% Стилизация компонентов
    classDef mcu fill:#1a365d,stroke:#0f172a,stroke-width:3px,color:#ffffff;
    classDef can fill:#d97706,stroke:#7c2d12,stroke-width:1px,color:#ffffff;
    classDef eth fill:#059669,stroke:#064e3b,stroke-width:1px,color:#ffffff;
    classDef debug fill:#dc2626,stroke:#7f1d1d,stroke-width:1px,color:#ffffff;
    classDef peri fill:#4f46e5,stroke:#1e1b4b,stroke-width:1px,color:#ffffff;

    %% -------------------------------------------------------------
    %% ЛЕВАЯ СТОРОНА: СЕТЬ CANFD (КАНАЛЫ 0 - 3)
    %% -------------------------------------------------------------
    subgraph LEFT [ЛЕВАЯ СТОРОНА: Шины CANFD 0-3]
        CAN_W[CAN0 Wakeup<br>PTE21 / PTE22]:::can
        CAN1[CAN1FD<br>PTA11 / PTA12]:::can
        CAN2[CAN2FD<br>PTD16 / PTD15]:::can
        CAN3[CAN3FD<br>PTA31 / PTB18]:::can
    end

    %% -------------------------------------------------------------
    %% ВЕРХНЯЯ СТОРОНА: СЕТЕВОЙ ИНТЕРФЕЙС GIGABIT ETHERNET
    %% -------------------------------------------------------------
    subgraph TOP [ВЕРХНЯЯ СТОРОНА: Сеть RGMII]
        RGMII_TX[RGMII TX Линии<br>PTC2, PTD7, PTD6, PTD5<br>TX_EN: PTD12, TX_CLK: PTD11]:::eth
        SMI_MGMT[SMI Управление PHY<br>MDC: PTE8, MDIO: PTB4]:::eth
        RGMII_RX[RGMII RX Линии<br>PTC1, PTC0, PTD9, PTB23<br>RX_DV: PTD8, RX_CLK: PTD10]:::eth
    end

    %% -------------------------------------------------------------
    %% ЦЕНТР: МИКРОКОНТРОЛЛЕР
    %% -------------------------------------------------------------
    MCU[« ЦЕНТР ПЛАТЫ »<br><br>Flagchip Semiconductor<br>FC7300F8MDT<br>Корпус BGA320]:::mcu

    %% -------------------------------------------------------------
    %% НИЖНЯЯ СТОРОНА: ПАМЯТЬ, КОНСОЛЬ И СИСТЕМНОЕ УПРАВЛЕНИЕ
    %% -------------------------------------------------------------
    subgraph BOTTOM [НИЖНЯЯ СТОРОНА: Системная периферия]
        SPI_FLASH[NOR Flash SPI2<br>L3: PTE11 CS / L2: PTE10 MISO<br>M1: PTE13 CLK / M2: PTA25 MOSI]:::peri
        I2C_EEPROM[EEPROM I2C1<br>V4: PTB5 SDA / V5: PTB30 SCL]:::peri
        UART_CONS[Консоль UART1<br>D2: PTA18 TX / D3: PTA19 RX]:::peri
    end

    %% -------------------------------------------------------------
    %% ПРАВАЯ СТОРОНА: СЕТЬ CANFD (КАНАЛЫ 4 - 7) И ОТЛАДКА
    %% -------------------------------------------------------------
    subgraph RIGHT [ПРАВАЯ СТОРОНА: CANFD 4-7 и Отладка]
        CAN4[CAN4FD<br>PTC8 / PTB17]:::can
        CAN5[CAN5FD<br>PTC13 / PTC12]:::can
        CAN6[CAN6FD<br>PTC19 / PTC24]:::can
        CAN7[CAN7FD<br>PTD25 / PTB10]:::can
        DEBUG_PORT[Порт JTAG / SWD<br>E7: PTC4 CLK / B4: PTA4 DIO<br>C6: PTC5 TDI / F8: PTA10 TDO]:::debug
        SYS_CTRL[Линии управления<br>B5: RESET_b / H16: PTD21 ISP_EN_B]:::debug
    end

    %% -------------------------------------------------------------
    %% БЕЗНАПРАВЛЕННЫЕ СВЯЗИ ДЛЯ КОРРЕКТНОЙ ГЕОМЕТРИИ ОКРУЖЕНИЯ
    %% -------------------------------------------------------------
    %% Принудительный рендеринг верхнего и нижнего секторов через скрытые или явные связи
    TOP --- MCU
    MCU --- BOTTOM

    %% Горизонтальное распределение левого и правого секторов
    CAN_W --- MCU
    CAN1 --- MCU
    CAN2 --- MCU
    CAN3 --- MCU

    MCU --- CAN4
    MCU --- CAN5
    MCU --- CAN6
    MCU --- CAN7
    MCU --- DEBUG_PORT
    MCU --- SYS_CTRL
```

> ⚠️ **Предупреждение:** Парсер Mermaid в некоторых старых встроенных визуализаторах всё равно может перестраивать блоки горизонтально (слева направо). Для идеальной круговой топологии печатной платы рекомендуется использовать этот граф как логическое зонирование: Ethernet — строго вверх, CAN0-3 — влево, CAN4-7 и отладка — вправо, медленная шинная периферия памяти и консоли — вниз.

<FollowUp>
Помогло ли изменение типа графа (`graph LR` вместо `graph TD` со связыванием подграфов) распределить устройства по сторонам от контроллера в вашем визуализаторе? Если структура утверждена, требуется ли подготовить **C-код инициализации для регистров маппинга остальных периферийных модулей (SPI2, I2C1, UART1)**?
</FollowUp>
