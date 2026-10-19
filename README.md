# CAN / CAN FD Automotive Logger

Automotive CAN / CAN FD logger built on a single-board computer running Armbian.

## Overview

A standalone in-vehicle device that records raw CAN and CAN FD frames
with hardware timestamps to internal storage for diagnostics,
debugging, and reverse engineering.

## Hardware

- Compute (SBC): [ArmSom Sige7](https://docs.armsom.org/armsom-sige7) — Rockchip RK3588 (ARM64), 8 GB RAM, 2× 2.5 GbE, 40-pin expansion header
- CAN interface: custom **FC7300 CAN FD HAT** around the Flagchip **FC7300F8MDT** (BGA320) — 8 CAN FD channels (1 wake-up + 7 standard), 1000Base-T1 Ethernet, galvanic isolation
- System controller: always-on **RP2040** MCU for power sequencing, ignition monitoring and battery management
- Storage: eMMC and single M.2 NVME / M.2 SATA or RAID-10 array for data reliability
- RTC
- GNSS
- 4G / 5G / LTE modem
- Display
- Power: 12 V automotive input with load-dump protection and a LiFePO4 backup battery (UPS, internal or external)

> Hardware details, pinouts, schematics and the bill of materials live in [`hardware/`](hardware/README.md).

## Repository layout

```structure
can-logger/
├── README.md
├── LICENSE
│
├── hardware/
│   ├── README.md              # selected boards, modules, links
│   ├── bom.md                 # bill of materials
│   ├── schematics/            # FC7300 HAT, SBC, power and wake-up
│   ├── pinout/                # FC7300 BGA320 pinout (vendor mux + per-bank sheets)
│   └── pdf/                   # reference PDFs (SBC boards, demo boards, transceivers)
│
├── firmware/
│   ├── overlays/              # device tree overlays (can, nvme, rtc, gnss)
│   └── armbianEnv.txt         # Armbian config
│
├── software/
│   ├── src/                   # logger source code
│   ├── services/              # systemd units
│   ├── config/                # configuration files
│   └── scripts/               # install.sh, setup.sh
│
├── mechanical/
│   ├── enclosure/             # enclosure (scad + stl/step)
│   └── mounts/                # mounting brackets
│
└── docs/
    ├── assembly.md            # how to assemble
    ├── installation.md        # how to install in a vehicle
    └── troubleshooting.md
```

## Status

Work in progress.
