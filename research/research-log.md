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

## 2026-11-09 — Parts research for the three SAO projects
Datasheet/vendor-page research feeding the briefs in [planning-design/](../planning-design/README.md): RTC and GPS parts ([rtc-gps](../planning-design/rtc-gps/README.md)), entropy sources and SP 800-90B pipeline ([rng](../planning-design/rng/README.md)), I2C fan-out and power-path parts ([splitter](../planning-design/splitter/README.md)). Sourcing and prices came from cached snapshots and must be rechecked live.

## 2026-11-09 — Badge port power and BOM/part research
Read the hardware files of the 2026 Billboard, 2025 Communicator and 2024 Supercon 8 badges for what an SAO port can really supply ([badges/](badges/)); pulled datasheet currents and live LCSC/JLCPCB prices for the three designs ([parts-datasheet-notes.md](parts-datasheet-notes.md)); results in [POWER.md](../POWER.md) and the BOM CSVs. Finding: no surveyed badge limits or switches SAO ports; plan for 100 mA continuous and about 150 mA brief per port. RNG brief revised for a differential, AC-coupled, multi-channel front end ([rng](../planning-design/rng/README.md)).

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
- [x] Billboard badge: per-port current budget (no port limiting, AP2112K 600 mA shared), bus pull-ups (5.1 kOhm), pin pairs: read from the hardware files; see [note](badges/2026-supercon-billboard.md)
- [ ] Billboard badge: pad-level pin 5 vs pin 6 mapping, whether `0x50` is probed, e-paper boost and WS2812B draw
- [ ] NXP UM10204 timing figures (1000 ns / 300 ns rise times) not re-read
- [ ] Wokwi paid-plan pricing, atopile pricing (not verified in the research pass)
- [ ] KiCad CLI flags against the installed version
- [ ] Parts research: DS3231 datasheet (Analog PDFs would not download), AB1805 I2C address, ATtiny1616 sleep current, JST-SH Qwiic pin order, whether STEMMA QT boards pull up to 5 V, TPS2051C at 3.3 V, TPS62840 3.3 V VSET option
- [ ] RNG: conductive fabric options (EeonTex, silver/steel fabric, conductive thread) were not researched; 3M Velostat datasheet not opened; measure real min-entropy of the fabric before committing to the design
- [ ] Indoor GPS time-to-first-fix at a conference venue (datasheet figures are open-sky)
- [ ] Pin-1 convention conflict (v1.69bis square pad = GND vs Simple Add-On = VCC) matters for splitter and adapters
- [x] I2C client mode confirmed from datasheets for RP2350, ATtiny1616, STM32C011, CH32V003 ([notes](parts-datasheet-notes.md))
- [ ] Measure on hardware: all POWER.md figures marked est (RP2350 at 25/50 MHz, flash XIP duty, splitter LED), and the GPS start-up inrush on the badge rail
- [ ] DEF CON 31/33 port current claims ([third-party](badges/third-party-power-claims.md)) against their schematics
- [ ] GNSS patch antenna gain and ground-plane needs; MAX-M10S matching network
- [ ] TPS2553 + LM66100 on-resistance at 3.3 V; AP2112K SOT-23-5 thermal limit at the 5 V USB input
