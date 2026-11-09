# SAO electrical constraints and interoperability

Consolidated from the Badge.team page ([capture](badge-team-sao.md)) and a secondary research pass (pasted 2026-11-09) that cites the original v1.69bis write-up, the Simple Add-On hackaday.io project and the NXP I2C spec.

**Provenance:** rows tagged **[BT]** come from Badge.team, **[v1.69bis]** from the 2019 Hackaday article ([verified 2026-11-09](v1.69bis.md)), **[NXP]** from UM10204 (not re-read by us). Check the primary source before relying on a number in a design.

## Sources

| Resource | Establishes | Limitation |
|---|---|---|
| [SAO v1.69bis (Hackaday, 2019)](https://hackaday.com/2019/03/20/introducing-the-shitty-add-on-v1-69bis-standard/) | Six-pin connector, electrical conventions, GPIO protection, LED/UART conventions | Informal community spec; some features explicitly unfinished |
| [Simple Add-On / SAOv2 (hackaday.io)](https://hackaday.io/project/175182-simple-add-ons-sao) | Renamed compatible spec, KiCad symbols and footprints (badge-side and SAO-side) | Describes data pins as optional; power-only hosts exist |
| [Badge.team SAO docs](https://badge.team/docs/standards/sao/) | Pin numbering, EEPROM discovery, newer identification | Identification depends on host firmware |
| [NXP I2C spec UM10204](https://www.nxp.com/docs/en/user-guide/UM10204.pdf) | Bus electrical behaviour, timing, addressing, arbitration | SAO compatibility does not waive I2C requirements |
| The target badge's schematic and firmware | Current available, bus topology, pin map, boot behaviour | Final authority for that host |

## Connector

2x3, 2.54 mm. Badge has the female socket, add-on has the male header, preferably shrouded/keyed and through-hole for strength. Pin table: see [badge-team-sao.md](badge-team-sao.md#connector).

The hackaday.io footprint resource distinguishes badge-side and SAO-side footprints, including backside labels and connector outlines. **Verify pad numbers, mating face, PCB side and key orientation together.** Do not copy an unlabelled connector drawing and assume which side you are viewing.

## Electrical constraints

| Constraint | Requirement / consequence | Source |
|---|---|---|
| Supply | Nominal 3.3 V. Do not assume a 5 V rail. | [BT] |
| Signal voltage | No signals above 3.6 V. Our parts may be stricter. | [v1.69bis] |
| GPIO driven by the SAO | MUST go through at least 330 ohm. Not a substitute for correct levels or bus ownership. | [v1.69bis] |
| Power ceiling | "1.1 millihorsepower". The article gives no W or mA; 0.82 W / ~250 mA at 3.3 V is our own conversion (reader comments made the same). Not proof every badge can supply that at every port at once. | [v1.69bis] |
| Power-only add-on | Use only VCC and GND; "other pins should be NC". | [v1.69bis] |
| Backfeed | Never feed the host through the SAO power pin. Battery/USB-powered SAOs need a deliberate power-path isolation. | [BT] |
| I2C | Open-drain SDA/SCL, pull-ups, timing and loading per NXP. | [NXP] |
| UART | Historical convention: GPIO1 = badge TX / SAO RX, GPIO2 = badge RX / SAO TX, suggested 115200 baud. Needs host cooperation; can fail on shared GPIO wiring. | [v1.69bis] |
| GPIO1/GPIO2 alternates | WS2812 / APA102 data and clock, interrupt input. | [BT] |

**Check:** 1.1 mhp: 1 hp is 745.7 W, so 1.1 mhp = 0.82 W; 0.82 W / 3.3 V = 249 mA. The conversion is ours, not the spec's.

### Three separate compatibility claims

| Claim | What must be proven |
|---|---|
| Power-compatible | Safe voltage/current, connector orientation, no backfeed |
| Bus-compatible | Correct I2C/GPIO electrical behaviour, addresses, loading |
| Application-compatible | The host knows the protocol and exposes the feature |

A working connector does not give you a driver, an application or discovery.

## I2C traps

### Pull-ups and bus loading

Pull-ups from several add-ons combine in parallel. The **resulting** resistance sets sink current and rise time, not any single board's resistor.

```
R_eq = ( sum_i 1 / R_i )^-1
t_r  ~ 0.8473 * R_eq * C_bus
```

Max rise time: Standard-mode 1000 ns, Fast-mode 300 ns [NXP]. Choose values from the weakest device's sink-current limit, then measure the assembled system.

**Layout rule for us:** provide DNP pull-ups or a jumper, never assume our SAO is the only peripheral.

### Address collisions

A conflict is a system problem; firmware cannot readdress a fixed-address part. Keep an address map covering every onboard peripheral **and the identification EEPROM at `0x50`**. For repeated identical SAOs choose early between address straps, an MCU-configurable address, or a host-side I2C mux. A passive socket splitter does not make independent buses.

### Identification support is not universal

Badge.team's `0x50` EEPROM is optional, and the wrong address width can write to small parts (see [safe procedure](badge-team-sao.md#safe-identification-procedure)). An EEPROM footprint helps but does not give universal auto-detection. Match the target host ecosystem's descriptor format and write-protect production ID data.

## Architectures for an SAO (proposals, not spec)

| Architecture | Runs on the SAO | Burden | Best for |
|---|---|---|---|
| Power-only | LEDs or autonomous circuit | Lowest | Decorative / standalone |
| Direct I2C peripheral | RTC, sensor, expander, display controller | Host driver + bus compatibility | Small functional add-ons |
| Local MCU as I2C target | State machine, input handling, display/LED timing | Device firmware + host protocol | Clocks, controllers, instruments |
| Host-specific GPIO/UART | MCU or peripheral on agreed extra pins | Tight host integration | High throughput, special purpose |
| Self-powered intelligent | Local battery/USB, isolated power path | Highest | Radio bridges, standalone devices |

Preferred direction (a recommendation, not an SAO requirement): a local MCU owns precise timing and rendering; the badge exchanges commands and state over I2C. Keep a generic SAO device protocol separate from any host-specific adapter.

### Draft elements of a reusable intelligent-SAO protocol

Device ID and protocol version; capability bits (RTC, display, buttons, encoder, LEDs); status (ready/busy/error/event); coherent state snapshot; explicit commands (not raw memory writes); event queue; sequence counter; error counters; address configuration; defined reset defaults.

Decisions to write down: byte order, register-pointer behaviour, repeated START handling, partial writes, max transfer length, queue overflow, unknown commands, whether reads have side effects.

## Physical constraints (our proposed requirements, not SAO rules)

The standard specifies a connector, not a board outline or guaranteed clearance. The original text discusses mechanical weakness and recommends through-hole connectors. Record per design: envelope and max installed height; clearance to connector body, display, buttons, battery, enclosure; neighbour-port keepout; mechanical support for heavy batteries and encoders; exact connector part and insertion depth; assembly process; fab limits (trace/space, drills, annular ring, edge clearance); measured normal/startup/peak/sleep/fault current; programming access and test points (GND, 3V3, SDA, SCL); reset/recovery; revision labels; radio antenna keepout; art layers checked separately.

First revision preference: two-layer board, conservative dimensions. A starting strategy only.
