# Roadmap

Status: `[ ]` not started · `[~]` in progress · `[x]` done. Phases map to the goals in the [README](README.md).

## Phase 1 — Spec research
- [ ] Collect SAO spec versions (v1.69bis and later Simple Add-On revisions) into `research/specs/`
- [ ] Write up differences between versions
- [ ] Resolve open questions in [`research/research-log.md`](research/research-log.md)

## Phase 2 — Badge survey
- [ ] Pick the badges to survey
- [ ] Record per badge in `research/badges/`: SAO port voltage, current budget, I2C behaviour
- [ ] Document I2C address conventions and conflicts

## Phase 3 — Design
- [ ] Decide the target spec version and scope (decision record in `planning-design/decisions/`)
- [ ] Draft the first SAO design in `planning-design/`
- [ ] Schematic and PCB in `workbench/hardware/`

## Phase 4 — Build
- [ ] Order and assemble the first boards
- [ ] Firmware in `workbench/firmware/`
- [ ] Bring-up on at least one real badge

## Phase 5 — Test harness
- [ ] Define the spec checks (voltage, current, I2C, pinout)
- [ ] Badge-side test code in `workbench/firmware/`
- [ ] Run the harness against our own SAOs

## Later / ideas
- Publish findings and designs
