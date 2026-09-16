# Bill of Materials

Component and module breakdown for the CAN Logger.
Each section describes one part: purpose, selection notes, and source.
Full summary table at the end.

---

## SBC

Selected: Armsom Sige7

<img width="798" height="1103" alt="image" src="https://github.com/user-attachments/assets/cede7d53-b3fc-45ca-bbf4-afe67acceb93" />

**SoC:** Rockchip RK3588 (8nm)

**CPU:** 4x Cortex-A76 @ 2.4 GHz + 4x Cortex-A55 @ 1.8 GHz

**GPU:** ARM Mali-G610 MP4

**NPU:** 6 TOPS (INT8)

**Memory:** 8 / 16 / 32 GB LPDDR4/LPDDR4x

**Storage:** 64 / 128 GB eMMC, MicroSD card slot

**Power input:** 5–23 V DC (wide range), USB-C PD

**Operating temperature:** 0…80 °C

**Dimensions:** 92 × 62 × 14.6 mm

**OS support:** Debian 12, Ubuntu 22.04/24.04, Android 12, Armbian, Arch Linux, openSUSE

**Interfaces:**

- Ethernet: 2x 2.5 Gbps RJ45
- WiFi/BT: Onboard AP6275P (WiFi 6, BT 5)
- USB: 1x USB 2.0 Type-A, 1x USB 3.0 Type-A, 1x USB 3.0 Type-C (DP Alt Mode)
- Video Output: 1x HDMI 2.1 (8K@60), 1x Type-C DP
- Camera: 2x MIPI-CSI connectors
- Display: 1x MIPI-DSI connector
- PCIe: 1x M.2 Key M 2280 (PCIe 3.0 x4, NVMe only, no M.2 SATA)
- RTC: On-board, with battery connector
- GPIO: 40-pin header for expansion

**SPI:**

- SPI0: SPI0_MOSI_M2, SPI0_MISO_M2, SPI0_CLK_M2, SPI0_CS0_M2, SPI0_CS1_M2
- SPI1: SPI1_CLK_M1, SPI1_MOSI_M1, SPI1_MISO_M1, SPI1_CS0_M1, SPI1_CS1_M1
- SPI3: SPI3_MOSI, SPI3_MISO, SPI3_CLK_M0, SPI4_CS1

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
