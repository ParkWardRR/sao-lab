# Research log

## 2026-11-09 — Badge.team SAO page and tooling research
Captured [Badge.team's SAO standard](specs/badge-team-sao.md), consolidated electrical/interop notes ([specs/electrical-and-interop.md](specs/electrical-and-interop.md)), a note on the [2026 Billboard badge](badges/2026-supercon-billboard.md) and the [dev-environment research](dev-environment.md). The electrical figures and tool claims came from a pasted secondary research pass; only the Badge.team page was pasted as source text.

## Open questions
- Exact current limits per badge
- I2C address conventions and conflicts
- Differences between v1.69bis and later Simple Add-On revisions

## To verify against primary sources
- [ ] v1.69bis: 3.6 V signal ceiling, 330 ohm GPIO series resistor, 1.1 mhp (~250 mA) power limit, UART convention (GPIO1 badge TX, 115200 baud)
- [ ] Badge.team page says "32-bit address length" for large EEPROMs; likely means 16-bit. Confirm on the binary descriptor page
- [ ] Fetch and capture the Badge.team child page "Binary SAO descriptor" (`LIFE` header)
- [ ] Find a spec for the `JSON` header (page links none)
- [ ] Uri Shaked's badge addon id standard and the AND!XOR structure: capture and compare with Badge.team's
- [ ] Billboard badge: SAO pin 5/6 to GPIO mapping, per-port current budget, bus pull-ups, whether `0x50` is probed (needs the hardware files)
- [ ] Wokwi paid-plan pricing, atopile pricing (not verified in the research pass)
- [ ] KiCad CLI flags against the installed version
