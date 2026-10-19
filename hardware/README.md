# Hardware

Hardware design files, component selection, and assembly references for the CAN Logger.

## Contents

| File / Dir       | Description                                      |
|------------------|--------------------------------------------------|
| `bom.md`         | Bill of materials with part numbers and sources  |
| `schematics/`    | Schematics and wiring for the FC7300 HAT, SBC, power and wake-up |
| `pdf/`           | Reference PDFs (SBC boards, FC7300 demo boards, transceivers) |
| `custom/`        | Custom board designs (cad sources + gerbers)   |

The FC7300 pinout tables (vendor mux sheet + per-bank BGA320 sheets) live in the
top-level [`../pinout/`](../pinout) directory.

## Modules

| Module            | Role                                              |
|-------------------|---------------------------------------------------|
| SBC               | [ArmSom Sige7](https://docs.armsom.org/armsom-sige7) — RK3588, ARM64 (Armbian) |
| CAN HAT           | Custom 8-CH CAN FD HAT around FC7300F8MDT (BGA320), galvanic isolation |
| System controller | RP2040 — always-on power sequencing and battery management |
| Storage           | eMMC + M.2 NVMe / SATA, optional RAID-10          |
| RTC               | On-board / LK8563S, I2C                          |
| GNSS              | Position and time source                          |
| Cellular          | 4G / 5G / LTE modem                               |
| Power             | 12V automotive input, load-dump protection, LiFePO4 UPS |

## Notes

- Reference schematics and board PDFs are stored under `pdf/`.
- The FC7300 CAN FD HAT provides 8 channels: 1 wake-up (`FLEXCAN0`) + 7 standard, plus 1000Base-T1 Ethernet (RGMII).
- Custom board designs live under `custom/` with gerbers ready for fabrication.
