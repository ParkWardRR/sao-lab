# 2025 Hackaday Supercon "Communicator" badge

- **Source:** <https://github.com/Hack-a-Day/2025-Communicator_Badge> (read 2026-11-09: `hardware/communicator_pcb/communicator_pcb.kicad_pcb`, `Power.kicad_sch`)
- **Host:** ESP32-S3 plus Wio-SX1262 LoRa module
- **SAO ports:** 1

| Item | Finding |
|---|---|
| 3.3 V regulator | AP2112K-3.3 (600 mA minimum), same power design as the [2026 Billboard](2026-supercon-billboard.md): MCP73831 charger (R8 = 2 k) and a DMG2305 P-FET |
| Port switching | None: J8 pin 1 is directly on +3V3 |
| I2C pull-ups for the SAO | R14 and R15, 5.1 kOhm |
| Other loads | ESP32-S3 (355 mA peak TX), LoRa module (125 mA at 22 dBm per the Wio datasheet) |
| Spare for SAOs | about 100 to 200 mA at worst-case radio peaks *(estimate)* |
