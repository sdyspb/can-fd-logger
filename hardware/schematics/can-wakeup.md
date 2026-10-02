# Реализация пробуждения по CAN-шине

Пробуждение процессора RK3588 (ArmSoM Sige7) по событию на CAN-шине реализуется через вывод `/IRQ` контроллера MCP2518FD. Для пробуждения используются только пины домена **GPIO0** (PMUIO), способные разбудить процессор из глубокого сна.

## Аппаратная реализация

### Выбор пинов

- **Пин 8** — `UART2_TX_M0` (GPIO0_B5)
- **Пин 10** — `UART2_RX_M0` (GPIO0_B6)

Оба пина относятся к GPIO0 и подходят для пробуждения.

<img width="811" height="351" alt="image" src="https://github.com/user-attachments/assets/7838e563-fd78-4bc8-8d23-e993070c310e" />

### Перемычка

На этапе отладки пины 8/10 используются как UART2. Чтобы сигнал `/IRQ` не мешал, ставится **переключающая перемычка**:

- **Отладка:** `/IRQ` отключен, пины работают как UART2.
- **Рабочий режим:** `/IRQ` подключен к пину 10 (GPIO0_B6).

> ⚠️ **Предупреждение:** Перемычка должна разрывать цепь `/IRQ` в режиме отладки, иначе будут помехи на UART2.

### Защита

- TVS-диод на линию `/IRQ`.
- Подтягивающий резистор к 3.3V (выход MCP2518FD — открытый сток).

## Программная реализация

### Overlay 1: Режим отладки

**`rk3588-armsom-uart2-m0.dts`:**

```dts
/dts-v1/;
/plugin/;

&uart2 {
    status = "okay";
    pinctrl-names = "default";
    pinctrl-0 = <&uart2m0_xfer>;
};
```

### Overlay 2: Рабочий режим (GPIO Wakeup)

**`rk3588-armsom-mcp2518fd-wakeup.dts`:**

```dts
/dts-v1/;
/plugin/;

/ {
    fragment@0 {
        target = <&uart2>;
        __overlay__ { status = "disabled"; };
    };

    fragment@1 {
        target = <&pinctrl>;
        __overlay__ {
            mcp2518fd_int: mcp2518fd-int {
                rockchip,pins = <0 RK_PB6 RK_FUNC_GPIO &pcfg_pull_up>;
            };
        };
    };

    fragment@2 {
        target = <&spi0>;
        __overlay__ {
            status = "okay";
            can0: can@0 {
                compatible = "microchip,mcp2518fd";
                reg = <0>;
                spi-max-frequency = <20000000>;
                interrupt-parent = <&gpio0>;
                interrupts = <RK_PB6 IRQ_TYPE_LEVEL_LOW>;
                pinctrl-names = "default";
                pinctrl-0 = <&mcp2518fd_int>;
                wakeup-source;
            };
        };
    };

    fragment@3 {
        target = <&rockchip_suspend>;
        __overlay__ {
            rockchip,wakeup-config = <(0 | RKPM_GPIO_WKUP_EN)>;
        };
    };
};
```

### Ключевые моменты

1. `status = "disabled"` для `&uart2` — освобождает пины.
2. `rockchip,pins = <0 RK_PB6 RK_FUNC_GPIO ...>` — настройка GPIO0_B6.
3. `interrupts = <RK_PB6 IRQ_TYPE_LEVEL_LOW>` — прерывание по низкому уровню.
4. `wakeup-source;` — разрешает пробуждение.
5. `RKPM_GPIO_WKUP_EN` — активирует пробуждение от GPIO.

### Переключение режимов

В `/boot/uEnv/uEnv.txt`:

```ini
# Для отладки:
overlays=rk3588-armsom-uart2-m0

# Для рабочего режима:
overlays=rk3588-armsom-mcp2518fd-wakeup
```

После смены оверлея переставить перемычку и выполнить `sync && reboot`.
