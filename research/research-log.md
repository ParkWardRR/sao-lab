# Research log

## 2026-11-09 — Badge.team SAO page and tooling research
Captured [Badge.team's SAO standard](specs/badge-team-sao.md), consolidated electrical/interop notes ([specs/electrical-and-interop.md](specs/electrical-and-interop.md)), a note on the [2026 Billboard badge](badges/2026-supercon-billboard.md) and the [dev-environment research](dev-environment.md). The electrical figures and tool claims came from a pasted secondary research pass; only the Badge.team page was pasted as source text.

## 2026-11-09 (later) — primary sources fetched
Read Badge.team's binary descriptor page, the v1.69bis article, the Simple Add-On v2 project, `urish/badge-addon-id` and `ANDnXOR/sao-reference-designs`. New notes in `specs/`. Findings:
- v1.69bis limits (3.6 V, 330 ohm, 1.1 mhp, UART at 115200) confirmed. The 0.82 W / 250 mA figure is **not** in the article; it is a conversion.
- Simple Add-On v2 is electrically identical to v1.69bis. It adds a rename, a footprint, and "only VCC and GND guaranteed".
- Badge.team's `LIFE` descriptor is badge-addon-id's layout with the reserved byte 7 repurposed as additional-driver count.
- `JSON` header is defined only in badge-addon-id; Badge.team links no doc.
- The "32-bit address length" text really is on the Badge.team page.
- AND!XOR format found: year / maker / type / data, no magic.

## Open questions
- Exact current limits per badge
- I2C address conventions and conflicts (known so far: `0x50` ID EEPROM, MCP23017 `0x20` in AND!XOR designs)
- Whether the extra-driver entries in Badge.team's `LIFE` header are implemented in any firmware (spec page says docs for drivers are unwritten; see MCH2022 `sao_eeprom.h`)
- Simple Add-On v2 footprint silkscreen: which of the two conflicting descriptions is right (check a physical part)

## To verify against primary sources
- [x] v1.69bis: 3.6 V signal ceiling, 330 ohm GPIO series resistor, 1.1 mhp, UART convention
- [x] Badge.team "32-bit address length": confirmed as published, likely an upstream error
- [x] Badge.team child page "Binary SAO descriptor" (`LIFE`)
- [x] `JSON` header spec: only in badge-addon-id
- [x] Uri Shaked's badge addon id and the AND!XOR structure
- [ ] Read MCH2022 `sao_eeprom.h` to see how drivers and extra drivers are actually parsed
- [ ] Billboard badge: SAO pin 5/6 to GPIO mapping, per-port current budget, bus pull-ups, whether `0x50` is probed (needs the hardware files)
- [ ] NXP UM10204 timing figures (1000 ns / 300 ns rise times) not re-read
- [ ] Wokwi paid-plan pricing, atopile pricing (not verified in the research pass)
- [ ] KiCad CLI flags against the installed version
