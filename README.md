# CAN / CAN FD Automotive Logger

Automotive CAN / CAN FD logger built on a single-board computer running Armbian.

## Overview

A standalone in-vehicle device that records raw CAN and CAN FD frames
with hardware timestamps to internal storage for diagnostics,
debugging, and reverse engineering.

## Hardware

- SBC: ARM64 or RISC-V compatible
- CAN interface: 7-CH CAN FD HAT modules with galvanic isolation
- Storage: eMMC and single M.2 NVME / M.2 SATA or RAID-10 array for data reliability
- RTC: on-HAT or external
- GNSS
- 4G / 5G / LTE modem
- Power: 12 V automotive input with load-dump protection and UPS (internal or external)

## Repository layout

```structure
can-logger/
├── README.md
├── LICENSE
│
├── hardware/
│   ├── README.md              # selected boards, modules, links
│   ├── bom.md                 # bill of materials
│   ├── wiring.md              # wiring diagram
│   ├── power.md               # 12V → 5V power, protection
│   ├── schematics/            # module, shield and custom board schematics
│   └── custom/                # custom boards (kicad + gerbers)
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
