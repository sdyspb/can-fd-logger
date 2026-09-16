# Hardware

Hardware design files, component selection, and assembly references for the CAN Logger.

## Contents

| File / Dir       | Description                                      |
|------------------|--------------------------------------------------|
| `bom.md`         | Bill of materials with part numbers and sources  |
| `wiring.md`      | System wiring diagram and connection notes       |
| `power.md`       | 12V → 5V power supply, protection, UPS           |
| `schematics/`    | Schematics for modules, shields, custom boards   |
| `custom/`        | Custom board designs (KiCad sources + gerbers)   |

## Modules

| Module       | Role                                              |
|--------------|---------------------------------------------------|
| SBC          | ARM64 / RISC-V single-board computer (Armbian)    |
| CAN HAT      | 7-CH CAN FD HAT with galvanic isolation           |
| Storage      | eMMC + M.2 NVMe / SATA, optional RAID-10          |
| RTC          | On-HAT or external real-time clock                |
| GNSS         | Position and time source                          |
| Cellular     | 4G / 5G / LTE modem                               |
| Power        | 12V automotive input, load-dump protection, UPS   |

## Notes

- All schematics are stored as PDF sources.
- Custom board designs live under `custom/` with gerbers ready for fabrication.
- File naming: `<module>-schematic.<ext>`, e.g. `can-fd-hat-schematic.pdf`.
