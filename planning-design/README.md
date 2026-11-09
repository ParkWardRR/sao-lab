# Planning & design

Plans and design docs for what we build in [`../workbench/`](../workbench/).

- `decisions/` — short decision records (one file each, e.g. `0001-target-spec-version.md`): context, decision, consequences
- One folder per SAO project, each with a `README.md` design brief

## Projects

| # | Project | Brief | Workbench | Status |
|---|---------|-------|-----------|--------|
| 1 | SAO RTC with GPS add-on | [`rtc-gps/`](rtc-gps/README.md) | [`hardware`](../workbench/hardware/rtc-gps/) · [`firmware`](../workbench/firmware/rtc-gps/) | prepped, nothing built |
| 2 | SAO random number generator (fabric between two binder clips) | [`rng/`](rng/README.md) | [`hardware`](../workbench/hardware/rng/) · [`firmware`](../workbench/firmware/rng/) | prepped, nothing built |
| 3 | SAO splitter / power hub | [`splitter/`](splitter/README.md) | [`hardware`](../workbench/hardware/splitter/) · [`firmware`](../workbench/firmware/splitter/) | prepped, nothing built |

How the three share a bus, a power budget and an address map: [`system-overview.md`](system-overview.md).

BOMs and power consumption: [`power-analysis.md`](power-analysis.md) (BOM CSVs sit in each project folder).

## Rules every brief follows

- Facts carry a source URL or are tagged *(unverified)*. Recommendations are tagged as such.
- Each brief ends with open questions for the owner and a first-prototype plan, so it can be picked up cold.
- Electrical rules come from [`research/specs/electrical-and-interop.md`](../research/specs/electrical-and-interop.md): 3.3 V only, no signal above 3.6 V, 330 ohm series on SAO-driven GPIO, no backfeed into the badge, DNP pull-ups.
