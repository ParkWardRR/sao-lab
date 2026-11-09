# Badge.team Binary SAO descriptor (`LIFE`)

- **Source:** <https://badge.team/docs/standards/sao/binary_descriptor/> (last modified 2026-11-06, upstream commit `27ad94c`)
- **Fetched:** 2026-11-09
- **Scope:** "the header format used in the identification EEPROM at address 0x50". Parent: [badge-team-sao.md](badge-team-sao.md).

The page describes the fields in prose and gives one example table; it has no offset table. The layout below is derived from that example, and it matches the older [badge-addon-id](badge-addon-id.md) layout (see differences).

## Layout

| Offset | Size | Field | Notes |
|---|---|---|---|
| 0 | 4 | Magic | ASCII `LIFE` = `4C 49 46 45` |
| 4 | 1 | SAO name length | Max 255. Recommended: visible 7-bit ASCII only |
| 5 | 1 | First driver name length | |
| 6 | 1 | First driver data length | Not mentioned in the prose, present in the example |
| 7 | 1 | Additional driver count | `0` if none. "Not all badges support additional drivers" |
| 8 | name length | SAO name | ASCII |
| 8+N | driver name length | First driver name | ASCII |
| 8+N+M | driver data length | First driver data | Raw bytes, meaning defined by the driver |
| after | | Additional drivers | Appended after the main header |

Each additional driver entry: `[name len][data len][name][data]` (example `04 03 74 65 73 74 01 02 03`).

No checksum or CRC, no version field, and multi-byte values never occur (all lengths are single bytes), so endianness is moot.

## Example from the page

`4C 49 46 45 05 04 03 00 48 45 4C 4C 4F 74 65 73 74 01 02 03`: SAO "HELLO", driver "test", data `01 02 03`, no extra drivers (20 bytes).

## Corruption handling

Badges should check only the last three bytes (`IFE`). If byte 0 is found corrupted, the badge should **repair it by writing `L` to address 0**. This is the write side of the "ignore the first byte" rule in the [safe identification procedure](badge-team-sao.md#safe-identification-procedure).

## Drivers

Supported by the MCH2022 badge firmware: Storage (unused EEPROM), Basic I/O (buttons and LEDs on SAO GPIO), Neopixel, ssd1306 (I2C OLED), ntag (I2C NFC tag), app (companion app name). "Documentation for these drivers has yet to be written"; the page points to [`sao_eeprom.h`](https://github.com/badgeteam/mch2022-firmware-esp32/blob/master/main/include/sao_eeprom.h) in the MCH2022 firmware.

## JSON header

The `JSON` header is listed on the parent page with no documentation link, and this page does not mention it. The only definition found is in [badge-addon-id](badge-addon-id.md).
