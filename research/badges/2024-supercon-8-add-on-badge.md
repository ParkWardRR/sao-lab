# 2024 Hackaday Supercon 8 Add-On Badge

- **Source:** <https://github.com/Hack-a-Day/2024-Supercon-8-Add-On-Badge> (read 2026-11-09; schematic read from `hardware/Badge_2024_schematic.jpg`)
- **Host:** Raspberry Pi Pico W
- **SAO ports:** 6

| Item | Finding |
|---|---|
| SAO supply | "+V" wired to the Pico's 3V3(OUT) pin 36 (from the schematic image) |
| Regulator | the Pico's on-board buck-boost; the [Pico W datasheet](https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf) says to keep the load on that pin under 300 mA |
| Port switching | none; six ports share the rail |
| Battery | 2 x AA through a P-FET (T1) to VSYS, plus an external power input; alkaline sag under load *unverified* |
| I2C pull-ups | R1 to R4, 3.3 kOhm (BOM text); which SDA/SCL pair each serves is *unverified* |
| Spare for SAOs | up to about 300 mA nominal across all six ports |

**Conflicting claim:** a Hackaday.io builder wrote that "the SAO ports on the Supercon badges usually are connected to the AA battery directly" and measured 3 V ([source](https://hackaday.io/project/197669-video-button-sao/details)). That disagrees with the schematic reading above; unverified either way.

Precedent for us: a CH32V003 protoboard add-on that the badge can program (CH32fun and I2C examples).
