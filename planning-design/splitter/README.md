# SAO splitter / power hub

Status: prepped 2026-11-09, nothing built. Research pass by datasheet and vendor page; items tagged *(unverified)* were not confirmed, *(recommendation)* is our proposal.

## Problem

An SAO plugged into a badge uses the only port. Three situations break that:

1. **The badge has fewer ports than add-ons** (the Billboard badge has 3 on one shared bus; many badges have 1).
2. **The next board has no SAO port** (a bare dev board, a breadboard, a Qwiic/STEMMA QT device, a power-only socket).
3. **The port cannot supply enough power** (v1.69bis says "1.1 millihorsepower", about 250 mA at 3.3 V, but that is a ceiling, not a guarantee, and Badge.team says never feed power back into the badge).

Our RTC+GPS ([rtc-gps](../rtc-gps/README.md)) and RNG ([rng](../rng/README.md)) boards both want a port, and the GPS draws real current, so this is the glue for the other two projects.

## Three variants, one family *(recommendation)*

| Variant | What | Power | I2C | Firmware |
|---|---|---|---|---|
| **A. Passive splitter** | 1 male in, 3 or 4 female out, shared 3V3/GND/SDA/SCL, GPIO jumpers | from badge | shared bus, DNP pull-ups | none |
| **B. Powered hub** (rev 1 target) | A plus USB-C power input, current-limited upstream leg, ideal-diode power path, LEDs | USB when present, else badge (limited) | shared bus, optional hot-plug buffer footprint | none |
| **C. Adapters** | SAO to Qwiic/STEMMA QT (JST-SH 4-pin), SAO to 0.1" breadboard header, SAO to solder pads | passes through | passes through | none |
| *(rev 2)* **D. Smart hub** | B plus MCU + I2C mux: per-port enable, current sense, address isolation | as B, per-port switches | muxed per port | yes |

Build A+B as one board (B populates the power parts, A leaves them DNP) so the first order tests both. C is a trivial second board.

## Rev 1 power path (variant B) *(recommendation)*

Goal: automatic choice between badge and USB, with **zero current into the badge's 3V3 pin ever**, and a short on any downstream port unable to brown out the badge.

```mermaid
flowchart LR
    BADGE[Badge pin 1 3V3] --> LIM[TPS2553 current limit ~130-175 mA (RILIM 180k), FAULT LED]
    LIM --> D1[LM66100 ideal diode]
    USB[USB-C 5V VBUS] --> LDO[AP2112K-3.3]
    LDO --> D2[LM66100 ideal diode, CE tied to VOUT]
    D1 --> RAIL[Downstream 3V3 rail]
    D2 --> RAIL
    RAIL --> P1[Port 1] & P2[Port 2] & P3[Port 3]
    USB -. VBUS present disables badge leg .-> LIM
```

Rules:
- When VBUS is present the badge leg is off and the ideal diode blocks in both directions, so USB has strict priority and the badge never shares load.
- Share one GND (pin 2) across everything; I2C needs the reference. Keep the USB-C shield off signal GND where possible. A second ground path through USB can form a loop (how bad is *unverified*).
- Add soft-start or bulk capacitance sized to the current limit to cover hot-plug inrush.
- USB-C is power-only: 5.1 kOhm CC pulldowns, no data lines.

Parts, all from datasheets the research pass read:

| Part | Role | Key facts | Source |
|---|---|---|---|
| LM66100 | ideal diode, both legs | 1.5 to 5.5 V, 1.5 A, 79 mOhm at 5 V; CE blocks when CE exceeds VIN by 80 mV; tolerates VIN down to -6 V | [TI](https://www.ti.com/lit/ds/symlink/lm66100.pdf) |
| TPS2553 | badge-leg current limit | 2.5 to 6.5 V, adjustable 75 mA to 1.7 A, FAULT pin, reverse-voltage comparator. Limit (mA) = 23950 / RILIM(kOhm)^0.977 nominal; 180 kOhm gives about 129 to 174 mA, chosen to match the practical per-port rule in the [power analysis](../power-analysis.md) | [TI](https://www.ti.com/lit/ds/symlink/tps2553.pdf) |
| AP2112K-3.3 | USB 5 V to 3.3 V | 600 mA min, 250 mV dropout at 600 mA, foldback short-circuit about 50 mA. As a linear regulator from 5 V it burns (5 - 3.3) x I: 0.17 W at 100 mA, 0.43 W at 250 mA, so treat USB-path load as limited to about 250 mA until a buck (e.g. TPS62A02) replaces it | [Diodes](https://www.diodes.com/assets/Datasheets/AP2112.pdf) |

JLCPCB: AP2112K-3.3TRG1 [C51118](https://jlcpcb.com/partdetail/C51118) (extended), LM66100DCKR [C2869734](https://lcsc.com/product-detail/power-distribution-switches_texas-instruments-lm66100dckr_C2869734.html), TPS2553DBVR-1 [C111738](https://jlcpcb.com/partdetail/C111738) (extended).

Rejected: TPS2121 (adjustable limit only from 1 A, too high to protect a badge), TPS22918 (no current limit, no fault flag), AP22802 (NRND), TPS2051C (3.3 V operation not checked *(unverified)*). A cheaper "Option A" (2x LM66100 + AP2112K + polyfuse, no TPS2553) limits fault current only via fuse and LDO foldback; fine for a throwaway, not for lending to others.

## I2C topology

- **Rev 1 is passive.** Limit is 400 pF bus capacitance; rise time is 0.8473 x R_pullup x C_bus, max 1000 ns standard and 300 ns fast mode ([TI SLVA689](https://www.ti.com/lit/an/slva689/slva689.pdf)). N boards with 4.7 kOhm pull-ups give 4.7 k/N; keep the combined value at or above about 1 kOhm (3.3 V, 3 mA sink). Budget about 4 pull-up-equipped boards.
- Splitter's own pull-ups: **DNP solder jumper, default off**.
- Optional footprint for a **TCA4307** hot-swap buffer in the upstream path: it precharges on insertion and disconnects a stuck-low bus after about 40 ms ([TI](https://www.ti.com/lit/ds/symlink/tca4307.pdf)). It protects the badge from a stuck bus but does not isolate individual ports.
- All ports stay **always powered** from the shared rail: an unpowered board with wired SDA/SCL can clamp the bus through its ESD diodes.
- Not in rev 1: muxes. PCA9546A/TCA9548A power up with channels off (a mux-unaware badge would see no SAOs) and need a controller; their 0x70 to 0x77 range can collide with SAOs ([PCA9546A](https://www.ti.com/lit/ds/symlink/pca9546a.pdf), [TCA9548A](https://www.ti.com/lit/ds/symlink/tca9548a.pdf)).
- **Known unfixable by a passive splitter:** two downstream SAOs both with an ID EEPROM at `0x50` (Badge.team) or any other same-address pair. Document it; the smart hub (D) solves it with a mux per channel.

## GPIO1 / GPIO2

Shared by default, with per-port solder jumpers (any driver needs at least 330 ohm series). WS2812 chains need data pass-through, not a shared net, so offer a daisy option on GPIO1. SAOship, an existing 4-slot hub, does not wire GPIOs at all ([Tindie](https://www.tindie.com/products/thelogicofpi/planet-express-saoship)), so GPIO fan-out is a differentiator but also a collision risk.

## Adapters (variant C)

- SAO to Qwiic/STEMMA QT: 3V3 to pin 1, GND to pin 2, SDA to pin 3, SCL to pin 4, pins 5 and 6 not connected. JST-SH pin order not verified against SparkFun/Adafruit pages *(unverified)*.
- **Pin 1 gotcha:** v1.69bis put the square pad on GND; SAOv2 moved it to VCC ([captured](../../research/specs/simple-add-on-v2.md)). Label every adapter by net name and test against a real badge.
- **Mirror gotcha:** if the adapter mates on the opposite board face, left-right order flips; check in 3D.
- **5 V gotcha:** STEMMA QT boards may use 5 V pull-ups *(unverified)*, but SAO signals must not exceed 3.6 V. Add a level shifter or refuse such boards.
- Power-only hosts: pass 3V3 and GND, leave the rest NC. 5 V-only hosts: use variant B's USB power; never put 5 V on pin 1.
- Keying: key and shroud the male side, add a polarity silkscreen. Keyed female through-hole parts are scarce.

## Failure modes to test

| Failure | Mitigation |
|---|---|
| Downstream short browns out badge | TPS2553 limit on the badge leg; fault LED |
| Duplicate `0x50` / address clash | Documented limit; smart hub later |
| Pull-up stack-up | DNP jumpers, 1 kOhm combined floor |
| Ground loop via USB | single GND, test with USB plugged and unplugged |
| Hot-plug inrush | soft-start, bulk cap |
| Reversed insertion | shroud, keying, LM66100 reverse tolerance |
| Backfeed | scope pin 1 with USB present and badge unpowered; zero current |

## Prior art

SAOship (4 slots, GPIOs unwired), Bus Pirate SAO Plank (3 SAOs, gerbers on [Hackaday.io](https://forum.buspirate.com/t/my-first-add-on-sao-plank/504)), [SAO Explorer](https://hackaday.io/project/198465-sao-explorer) (mikroBUS + Qwiic), a [2019 SAO-to-Qwiic log](https://hackaday.io/project/166838/logs). No dedicated splitter was found *(absence is unverified)*. No source documents what these got wrong; the gaps visible from their pages are no stated pull-up policy, no current limiting or backfeed protection, unwired GPIO and no address handling.

## First-prototype plan

1. KiCad: variant A+B board, 3 female ports, USB-C, DNP options as above, test pads for every rail and a port-current shunt footprint.
2. Fixture test: backfeed, limit, hot-plug, bus rise time with 1 to 4 loaded pull-up boards (scope).
3. Variant C boards (Qwiic, breadboard) from the same footprints.
4. Plug RTC+GPS and RNG into it on a real badge and check the shared [address plan](../system-overview.md#i2c-address-plan).

## Open questions

- 3 ports or 4? Does the splitter itself stay SAO-sized, and which way do the ports face?
- USB-C only, or also a JST battery input?
- Is a mux/MCU "smart hub" wanted in rev 1, or later?
- Female connector: keyed shrouded or plain through-hole?
