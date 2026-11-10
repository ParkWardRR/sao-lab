# 2026 Hackaday Supercon "Billboard" badge

- **Source:** <https://github.com/Hack-a-Day/2026-Billboard_Badge> (first read by the 2026-11-09 research pass; power and wiring details below were read from the hardware files by a second pass the same day: `hardware/billboard_pcb/`, `production/netlist.ipc`, `billboard_pcb_BOM.csv`, `power.kicad_sch`)
- **Host MCU:** ESP32-S3
- **SAO ports:** 3, sharing one I2C bus, each with its own extra GPIO pair

| Interface | GPIO |
|---|---|
| Shared SDA | GPIO17 |
| Shared SCL | GPIO18 |
| SAO1 extra pair | GPIO2, GPIO42 |
| SAO2 extra pair | GPIO4, GPIO5 |
| SAO3 extra pair | GPIO7, GPIO6 |

## Power and bus wiring (read from the hardware files, 2026-11-09)

| Item | Finding | Evidence |
|---|---|---|
| 3.3 V regulator | AP2112K-3.3 (U3): 600 mA minimum, 250 mV typical dropout at 600 mA, short-circuit foldback to 50 mA, thermal shutdown 160 C | BOM, `power.kicad_sch`, [AP2112 datasheet](https://www.diodes.com/assets/Datasheets/AP2112.pdf) |
| Port switching / limiting | **None.** J8, J9, J10 pin 1 sit directly on the +3V3 net; a short on one SAO collapses the whole rail | `netlist.ipc` |
| Input path | Battery or USB through a P-FET (Q3) and 1N5819W diode (D5) into the regulator; on USB the LDO drops about 1.3 V (thermal impact *unverified*) | `netlist.ipc`, `power.kicad_sch` |
| Other loads on 3V3 | ESP32-S3 module (Espressif: 355 mA peak Wi-Fi TX, wants a 0.5 A supply); eight WS2812B LEDs; e-paper boost converter via Q2 (current *unverified*) | `netlist.ipc`, WROOM-1 datasheet |
| Battery | LiPo on a JST-PH connector; MCP73831 charger with R6 = 2 k (about 500 mA charge); 603450 pouch suggested, capacity not stated | `back_cover/README.md`, BOM |
| I2C pull-ups | R1 and R3, 5.1 kOhm to 3V3, on the shared bus (SDA GPIO17, SCL GPIO18) | `netlist.ipc`, `billboard_pcb.kicad_sch` |
| Pins 5/6 | SAO1 GPIO2 + GPIO42, SAO2 GPIO4 + GPIO5, SAO3 GPIO7 + GPIO6; matches the README pairs and the module pin numbers in the netlist. Which of each pair is pin 5 vs pin 6 was **not** separately confirmed | `README.md`, `netlist.ipc` |
| Spare for SAOs | about 245 mA worst case (Wi-Fi TX peak, LEDs off); about 300 to 450 mA idle; near zero if all eight LEDs are white *(estimate)* | derived |

## Still not established

- Whether the `0x50` ID EEPROM is probed by the badge firmware.
- Which GPIO of each pair is SAO pin 5 vs pin 6 (pad-level confirmation).
- Draw of the e-paper boost converter and of the eight WS2812B LEDs at 3.3 V.

## Notes

- The repo asks contributed apps to live in `user_apps/`, separate from core firmware. Keep our generic SAO protocol separate from a Billboard host adapter so the add-on stays portable.
- Because three ports share SDA/SCL, any identical-SAO design needs an address plan (see [electrical-and-interop](../specs/electrical-and-interop.md#address-collisions)).
- Related precedent: [2024 Supercon 8 Add-On Badge](2024-supercon-8-add-on-badge.md), which has a CH32V003 protoboard add-on the badge can program (CH32fun + I2C examples). The 2025 badge shares the Billboard's power design: [note](2025-supercon-communicator.md).
