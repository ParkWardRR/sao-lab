# AND!XOR SAO EEPROM format (DC27)

- **Source:** <https://github.com/ANDnXOR/sao-reference-designs> top-level README (Apache-2.0; GitHub shows the canonical owner as `zapp1337/sao-reference-designs`). Also `DC27/DC619-EEPROM_sao1.69bis/README.md`. Fetched 2026-11-09.
- **Role:** the identification structure Badge.team calls unusable. The v1.69bis article says a reference I2C EEPROM SAO existed "identical to the Tide Pod SAO of last year"; we found no "Tide Pod" mention in the repo folders we read.

An AT24C32 EEPROM at `0x50`, all address pins low. "Badges that detect the AT24C32 on the I2C bus should query for bytes at known addresses then perform actions."

| Offset | Field | Notes |
|---|---|---|
| 0 | DC Year | `0x1B` for DC27 |
| 1 | Maker ID | Unique per maker; AND!XOR uses `0x49` (middle 8 bits of their registered Bluetooth ID) |
| 2 | SAO Type ID | Assigned by the maker |
| 3..n | Data | Arbitrary, parseable by anything that recognises the three IDs above |

No magic bytes, checksum, length field or example dump.

## Why Badge.team calls it unusable

Judgement from the layout, not from a source: there is no magic marker, so any EEPROM content at `0x50` looks like a valid (year, maker, type) triple; there is no length or data schema; IDs rely on a maker-ID registry that does not exist in the repo; and the first byte, which is a live field here, is exactly the byte a stray 16-bit read can corrupt. `LIFE`/`JSON` fix this with a magic that can be checked after ignoring byte 0.

## Source inconsistencies

- Top-level README says the part is an AT24C32 (addresses `0x50`); the DC27 folder README says AT24C02N, same address, and that AND!XOR's badge "will only be able to address the first 256 bytes". An AT24C32 has a 2-byte address; the AT24C02 a 1-byte one. This is the exact 8-bit/16-bit mismatch behind the [Badge.team write hazard](badge-team-sao.md#identification).
- The README table also lists MCP23017 (GPIO expander) at `0x20` and a redacted entry.
- Not opened: `BobRoss_sao1.69bis`, `GPIO-16-MCP23017_sao1.69bis`, `Shitty-Brooch`.
