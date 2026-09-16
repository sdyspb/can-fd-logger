# Bill of Materials

Component and module breakdown for the CAN Logger.
Each section describes one part: purpose, selection notes, and source.
Full summary table at the end.

---

## SBC

**Selected:** ArmSoM-Sige5

<img width="774" height="1087" alt="image" src="https://github.com/user-attachments/assets/01f75eb4-8c8e-45f0-8fbc-cbdb3870160d" />

**SoC:** Rockchip RK3576 (8nm)
- 4x Cortex-A72 @ 2.2 GHz
- 4x Cortex-A53 @ 1.8 GHz

**Memory:** 8 / 16 GB LPDDR4x

**Storage:** 32 / 64 / 128 GB eMMC

**Power input:** 5–23 V DC (wide range), USB-C PD

**Operating temperature:** 0…80 °C

**Dimensions:** 92 × 62 × 14.6 mm

**OS support:** Armbian (community), Debian 12, Ubuntu

**Interfaces:**
- CAN: 2x native CAN controllers (RK3576), routed to 40-pin GPIO, external transceiver required
- PCIe: 1x M.2 Key M 2280 (PCIe 2.1 x1, NVMe only, no M.2 SATA)
- RTC: on-board LK8563S (I2C, with battery)
- USB: available for cellular modem and GNSS
- GPIO: 40-pin header for expansion

**Notes:**
- Only one M.2 slot, Key M — cannot host both NVMe and a cellular module simultaneously.
- Cellular modem must use USB.
- GNSS must use USB or UART.
- For more than 2 CAN channels, use SPI-CAN controllers (e.g. MCP2518FD) on the 40-pin header.

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
