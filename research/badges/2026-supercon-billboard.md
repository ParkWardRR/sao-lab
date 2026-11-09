# 2026 Hackaday Supercon "Billboard" badge

- **Source:** <https://github.com/Hack-a-Day/2026-Billboard_Badge> (as read by the 2026-11-09 research pass; we have **not** re-read the repo ourselves)
- **Host MCU:** ESP32-S3
- **SAO ports:** 3, sharing one I2C bus, each with its own extra GPIO pair

| Interface | GPIO |
|---|---|
| Shared SDA | GPIO17 |
| Shared SCL | GPIO18 |
| SAO1 extra pair | GPIO2, GPIO42 |
| SAO2 extra pair | GPIO4, GPIO5 |
| SAO3 extra pair | GPIO7, GPIO6 |

## Not established

The README lists each pair but does not by itself give the **connector-pad mapping** (which GPIO is SAO pin 5 vs pin 6) or the **current budget per port**. Read the hardware files before turning this into a production pin map. Also unknown: pull-up values on the shared bus, whether the `0x50` EEPROM is probed, port power switching.

## Notes

- The repo asks contributed apps to live in `user_apps/`, separate from core firmware. Keep our generic SAO protocol separate from a Billboard host adapter so the add-on stays portable.
- Because three ports share SDA/SCL, any identical-SAO design needs an address plan (see [electrical-and-interop](../specs/electrical-and-interop.md#address-collisions)).
- Related precedent: [2024 Supercon 8 Add-On Badge](https://github.com/Hack-a-Day/2024-Supercon-8-Add-On-Badge), which has a CH32V003 protoboard add-on the badge can program (CH32fun + I2C examples).
