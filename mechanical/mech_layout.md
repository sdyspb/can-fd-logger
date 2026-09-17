# Mechanical Layout

## 1. Enclosure Dimensions

| Parameter | Value |
| :--- | :--- |
| Length (front panel) | **230 mm** |
| Depth | **100 mm** |
| Height | **30 mm** |
| Material | Aluminum (recommended) |
| Shielding | Metallized coating or full metal enclosure |

The front panel runs along the **long side of the Sige7**, so all main connectors (USB, HDMI, Ethernet, CAN) face the same direction. The power input is on the rear panel.

## 2. Top View (230 × 100 mm)

```
┌────────────────────────────────────────────────────────────────────┐
│  FRONT PANEL (230 mm)                                              │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────┐ │
│  │  STACK A     │  │  STACK B     │  │        Sige7              │ │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌─────────────────────┐  │ │
│  │  │Shield 1│  │  │  │Shield 3│  │  │  │ USB  HDMI  ETH  ... │  │ │
│  │  ├────────┤  │  │  ├────────┤  │  │  │                     │  │ │
│  │  │Shield 2│  │  │  │Shield 4│  │  │  │                     │  │ │
│  │  └────────┘  │  │  └────────┘  │  │  └─────────────────────┘  │ │
│  │  CAN0-3      │  │  CAN4-7      │  │   (connectors to front)   │ │
│  └──────────────┘  └──────────────┘  └───────────────────────────┘ │
│                                                                    │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │           Adapter Board (40-pin mapper)                       │ │
│  │           connects Sige7 ↔ both shield stacks                 │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────┐  ┌────────────┐  ┌────────────────────────────┐  │
│  │   RP2040     │  │  BMS +     │  │   LiFePO4 Battery          │  │
│  │   + glue     │  │  Charger   │  │   12 × 66 × 131 mm         │  │
│  │   logic      │  │  + DC-DC   │  │   (along rear wall)        │  │
│  └──────────────┘  └────────────┘  └────────────────────────────┘  │
│                                                                    │
│  REAR PANEL (200 mm)                                               │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │   USB-C PD (12V)   │   GND   │   IGN   │   MAIN_PWR           │ │
│  └───────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

## 3. Component Placement

### 3.1. Front Panel (230 mm)

| Connector | Source | Purpose |
| :--- | :--- | :--- |
| **USB 3.0 / USB 2.0** | Sige7 | Peripherals, debug |
| **HDMI / DisplayPort** | Sige7 | Video output (optional) |
| **Ethernet RJ45** | Sige7 | Network (if available) |
| **4 × CAN FD (terminals)** | Shield stacks A + B | 8 CAN channels (CAN0–CAN7) |
| **UART / SWD** | RP2040 | Debug / flashing |
| **Status LEDs** | RP2040 | IGN, MAIN_PWR, BATT, FAULT |
| **Power button** | RP2040 | Manual start/stop |

### 3.2. Rear Panel (200 mm)

| Connector | Source | Purpose |
| :--- | :--- | :--- |
| **USB Type-C PD (12 V)** | Sige7 | Primary power input |
| **GND terminal** | Power board | Ground |
| **IGN terminal** | RP2040 | Ignition key input |
| **MAIN_PWR terminal** | RP2040 | Main power presence |
| **Ventilation slots** | — | Heat dissipation |

### 3.3. Internal Components

| Component | Size (mm) | Placement |
| :--- | :--- | :--- |
| **Stack A** (Shield 1 + 2) | ~55 × 55 × 25 | Front-left, connectors to front |
| **Stack B** (Shield 3 + 4) | ~55 × 55 × 25 | Front-center, connectors to front |
| **Sige7** | ~85 × 56 × 20 | Front-right, connectors to front |
| **Adapter Board** | ~150 × 60 × 2 | Below stacks, full width |
| **RP2040 + glue logic** | ~60 × 40 × 10 | Rear-left |
| **BMS + Charger + DC-DC** | ~60 × 40 × 10 | Rear-center |
| **LiFePO4 Battery** | 12 × 66 × 131 | Along rear wall |

## 4. Dimensional Check

### 4.1. Length (230 mm)

| Element | Width (mm) |
| :--- | :--- |
| Stack A | 65 |
| Stack B | 65 |
| Sige7 | 92 |
| **Total** | **222** |
| Remaining clearance | **8** |

### 4.2. Depth (100 mm)

| Element | Depth (mm) |
| :--- | :--- |
| Stack A / B | 57 |
| Sige7 | 62 |
| Battery | 66 |
| **Total (worst case)** | **66** |
| Remaining clearance | **34** |

### 4.3. Height (30 mm)

| Element | Height (mm) |
| :--- | :--- |
| Stack (2 shields + connector) | ~25–30 |
| Sige7 with heatsink | ~20–25 |
| Battery | 12 |
| Adapter board | 2 |
| **Total (worst case)** | **~30** |

> **Note:** The shield stack height is the critical dimension. Use a **low-profile mezzanine connector** (5–8 mm) and ensure the top shield has no tall components.

## 5. Thermal Considerations

| Source | Power (W) | Notes |
| :--- | :--- | :--- |
| Sige7 (RK3588) | 3–8 | Requires heatsink |
| 4 × CAN FD shields | 1–2 | Low heat |
| DC-DC + Charger | 1–2 | Moderate heat |
| **Total** | **5–12** | Needs ventilation |

**Recommendations:**
- Aluminum enclosure acts as a heatsink.
- Ventilation slots on the rear panel.
- Optional 40 mm low-RPM fan if thermal margin is tight.
- Thermal pad between RK3588 heatsink and enclosure wall.

## 6. Shielding and EMC

- Use a **metal enclosure** (aluminum) or apply a **metallized coating** inside a plastic enclosure.
- Connect enclosure ground to system GND at a single point.
- Use **shielded CAN cables** with proper termination (120 Ω).
- Add **TVS diodes** on IGN and MAIN_PWR inputs for automotive transient protection (ISO 7637-2).

## 7. Summary

| Parameter | Value |
| :--- | :--- |
| Enclosure size | **230 × 100 × 30 mm** |
| Front panel | All main connectors (USB, HDMI, ETH, CAN) |
| Rear panel | Power input (USB-C PD), GND, IGN, MAIN_PWR |
| Shield stacks | 2 × (2 shields) in front |
| Sige7 | Front-right, connectors to front |
| Adapter board | Below stacks |
| Battery | Along rear wall |
| RP2040 + BMS + DC-DC | Rear area |
| Thermal | Passive + optional fan |
| Shielding | Metal enclosure recommended |
