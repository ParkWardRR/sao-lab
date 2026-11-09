# sao-lab

Research and development of **Shitty Add-Ons (SAO)**, the small add-on boards for electronic conference badges ("badgelife").

## What an SAO is (to verify against the spec)

A small PCB that plugs into a badge through a 2x3 0.1" header (v1.69bis). The pins are:

| Pin | Signal |
|-----|--------|
| 1 | VCC (3.3 V) |
| 2 | GND |
| 3 | SDA (I2C) |
| 4 | SCL (I2C) |
| 5 | GPIO1 |
| 6 | GPIO2 |

## Layout

- `docs/` — spec notes, badge compatibility, research log
- `hardware/` — schematics, PCB, 3D parts
- `firmware/` — add-on firmware and badge-side test code

## Goals

1. Collect the SAO spec versions (v1.69bis, newer Simple Add-On revisions) and their differences.
2. Survey badges and their SAO ports: voltage, current budget, I2C behaviour.
3. Design and build our own SAOs.
4. Build a test harness that checks an SAO against the spec.
