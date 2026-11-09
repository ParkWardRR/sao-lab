# Simple Add-On v2 (SAOv2)

- **Source:** <https://hackaday.io/project/175182-simple-add-ons-sao> (author TwinkleTwinkie; project created 2020-10-03)
- **Fetched:** 2026-11-09

## What changed from v1.69bis

Nothing electrical. The author's "Why SAO v2" log (2020-10-03): "Simple Add-on v2's specs are identical to SAOv169bis", compatible with it and with the original 2x2 v1 spec; "no differences".

| Change | Detail |
|---|---|
| Name | "Simple Add-on", a "fork / rebranding" to reach a wider audience |
| Version label | Skipped "v1" and the legacy numbering to avoid confusion with SAOv169Bis |
| Footprint | KiCad files with better dimensional accuracy; the square pad moved from GND to **Pin 1 (VCC)** |
| Data pins | Stated explicitly as optional: "the only two pins that are always expected to work are VCC and GND". Designers should coordinate pins 3-6 with badge makers or document them |

Pin table is identical to [v1.69bis](v1.69bis.md): 1 VCC (expected 3.3 V), 2 GND, 3 SDA, 4 SCL, 5 GPIO, 6 GPIO.

**Not on the page:** electrical limits, power limits, GPIO resistor rule, any identification scheme. For those, the v1.69bis article still applies (the page itself says so).

## Connector and footprint

- SAO side: male 2x3 2.54 mm shield (shrouded) header; the key hole "should align with the top row".
- Badge side: female 2x3 with polarizing key, key aligned with the top row. A non-keyed one works but "will have a poor grip on Add-ons and they will fall off unless the host is stationary".
- Download: `KiCad_SAOv2.zip` (2.55 kB), footprints and library. The badge footprint has the keyed outline on front silkscreen and pinout on the back; the SAO footprint has pinout and male-header outline on the back.
- **Unresolved:** a 2021 comment says those silkscreen descriptions are swapped; the author replied "it's not". Verify against a physical part before ordering boards (the same warning as in [electrical-and-interop.md](electrical-and-interop.md#connector)).
- Parts links on the page: Tindie keyed female pack, AliExpress, and a Sullins Digi-Key part (MOQ 1,000; a 2026 comment says the link is dead and suggests Digi-Key `SFH11-NBPC-D03-ST-BK`, unvetted).
