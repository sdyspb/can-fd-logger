# Bill of Materials

Component and module breakdown for the CAN Logger.
Each section describes one part: purpose, selection notes, and source.
Full summary table at the end.

---

## SBC

**Purpose:** Main compute unit running Armbian.

**Selected:** TBD

**Notes:**
- Architecture: ARM64 / RISC-V
- RAM: TBD
- eMMC: TBD
- Interfaces required: PCIe, USB, SPI, I2C, UART, GPIO

**Source:** TBD

---

## CAN HAT

**Purpose:** CAN / CAN FD interface with galvanic isolation.

**Selected:** TBD

**Notes:**
- Channels: 7
- Protocol: CAN FD
- Interface: SPI
- Isolation: yes
- Termination: on-board

**Source:** TBD

---

## Storage

**Purpose:** Persistent log storage.

**Selected:** TBD

**Notes:**
- Primary: eMMC (size TBD)
- Secondary: M.2 NVMe / M.2 SATA
- Optional: RAID-10 array
- Endurance: high TBW recommended

**Source:** TBD

---

## RTC

**Purpose:** Reliable timekeeping without network.

**Selected:** TBD

**Notes:**
- Interface: I2C
- Battery: coin cell / supercapacitor
- Backup retention: TBD

**Source:** TBD

---

## GNSS

**Purpose:** Position and time source.

**Selected:** TBD

**Notes:**
- Constellation: GPS / GLONASS / Galileo / BeiDou
- Interface: UART / USB
- Antenna: active, external mount

**Source:** TBD

---

## Cellular Modem

**Purpose:** Remote upload and management.

**Selected:** TBD

**Notes:**
- Generation: 4G / 5G / LTE
- Interface: M.2 / Mini PCIe / USB
- SIM: nano, optional eSIM
- Antenna: external

**Source:** TBD

---

## Power

**Purpose:** 12V automotive input conversion and protection.

**Selected:** TBD

**Notes:**
- Input: 12V nominal (9–36V range)
- Output: 5V for SBC and modules
- Protection: load dump, reverse polarity, overcurrent
- UPS: internal or external

**Source:** TBD

---

## Mechanical

**Purpose:** Enclosure and mounting.

**Selected:** TBD

**Notes:**
- Enclosure: 3D printed / CNC
- Mounting: vehicle bracket
- Cooling: passive / active

**Source:** TBD

---

## Summary

| # | Module       | Part / Model | Qty | Interface   | Source |
|---|--------------|--------------|-----|-------------|--------|
| 1 | SBC          | TBD          | 1   | —           | TBD    |
| 2 | CAN HAT      | TBD          | 1   | SPI         | TBD    |
| 3 | Storage      | TBD          | 1   | PCIe / SATA | TBD    |
| 4 | RTC          | TBD          | 1   | I2C         | TBD    |
| 5 | GNSS         | TBD          | 1   | UART / USB  | TBD    |
| 6 | Cellular     | TBD          | 1   | M.2 / USB   | TBD    |
| 7 | Power        | TBD          | 1   | —           | TBD    |
| 8 | Enclosure    | TBD          | 1   | —           | TBD    |
