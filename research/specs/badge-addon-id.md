# Badge Add-On Identification System (Uri Shaked)

- **Source:** <https://github.com/urish/badge-addon-id> (README, one commit; fetched 2026-11-09)
- **Role:** the origin of the `LIFE` / `JSON` EEPROM headers that [Badge.team](badge-team-sao.md) builds on.

## Hardware

2 kbit (256 byte) EEPROM at I2C `0x50` (address pins grounded). Suggested: 10 kohm pull-up on write-protect (WC), 0.1 uF decoupling near VCC.

## Binary descriptor (8-byte header)

| Offset | Size | Field |
|---|---|---|
| 0 | 4 | Magic `LIFE` (`4C 49 46 45`) |
| 4 | 1 | Device name length |
| 5 | 1 | Driver name length |
| 6 | 1 | Driver data length |
| 7 | 1 | Reserved, must be 0 |

Followed by device name (UTF-8), driver name (ASCII), optional driver data.

Example: `4c 49 46 45 10 0a 04 00 "My amazing addon" "amazing.py" 01 ff ff ff`.

## JSON descriptor (5-byte header)

| Offset | Size | Field |
|---|---|---|
| 0 | 4 | Magic `JSON` |
| 4 | 1 | Length of JSON data |
| 5 | n | UTF-8 JSON payload |

Must contain `name` and `driver`; may carry extra driver fields. Example: `{"name": "My amazing addon", "driver": "amazing.py"}`.

No checksum or CRC, no multi-byte integers.

## Differences from Badge.team's binary descriptor

| | badge-addon-id | Badge.team |
|---|---|---|
| Byte 7 | Reserved, must be 0 | **Additional driver count** (0 = none) |
| Device name encoding | UTF-8 | ASCII (7-bit recommended) |
| Corrupted first byte | not addressed | check only `IFE`, repair by writing `L` |
| Extra drivers | none | appended after the main header |

Badge.team's format is a compatible superset for the single-driver case: a reserved `0` is the same byte as "no additional drivers".

## AND!XOR structure

The structure Badge.team calls unusable is captured in [andnxor-eeprom.md](andnxor-eeprom.md): `[DC year][maker ID][SAO type ID][data...]`, no magic.
