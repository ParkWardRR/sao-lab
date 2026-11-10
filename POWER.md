# Power analysis and BOM summary

Covers [RTC + GPS](planning-design/rtc-gps/README.md), [RNG](planning-design/rng/README.md) and [splitter](planning-design/splitter/README.md). Prepared 2026-11-09. All current figures are at 3.3 V (some datasheet tables are at 3.0 V; the difference was not checked). Rows marked **est** are our estimates, not datasheet values, and need a bench measurement before anyone relies on them. Nothing here has been measured on hardware.

## Can an SAO port feed this? Short answer

**Steady state: yes, with about 4x margin. Start-up peak: only just, and it needs care.**

| | Current at 3.3 V |
|---|---|
| All three boards, typical running | about 23 mA |
| All three, worst steady state | about 38 mA |
| Worst start-up peak (GPS inrush + RNG at full speed) | about 126 mA, for a few ms |
| What a port can safely give (practical rule below) | 100 mA continuous, about 150 mA brief |
| v1.69bis "1.1 millihorsepower" ceiling | about 250 mA, a commenter's conversion, not a guarantee |

**What real badges actually do** (read from their own files, see the sources):

| Badge | 3.3 V source | Port protection | Spare for SAOs |
|---|---|---|---|
| 2026 Billboard (3 ports) | AP2112K-3.3, 600 mA min | none; ports tied to the rail; a short collapses the whole badge | about 245 mA worst case (Wi-Fi TX peak), 300 to 450 mA idle, near zero with all 8 WS2812 LEDs white |
| 2025 Communicator (1 port) | AP2112K-3.3, 600 mA min | none | about 100 to 200 mA at radio peaks (ESP32-S3 355 mA + LoRa 125 mA) |
| 2024 Supercon 8 (6 ports) | Pico W 3V3(OUT) | none | Pico datasheet: keep load on that pin under 300 mA, shared across 6 ports |
| DEF CON 33 | not verified | onboard fuses | a third party says about 300 mA total, and only about 30 mA on USB/barrel power with all SAOs running (unverified) |

The researcher's bottom line, which I adopt as the design rule: **plan for 100 mA continuous and about 150 mA brief peaks per port, tolerate 3.0 to 3.6 V, keep bulk capacitance at or below about 100 uF, and soft-start anything heavy.** Most badges have no per-port current limit, so a fault in our board can take the badge down. That is why the splitter's badge leg is current-limited.

## Per-board current

### 1. RTC + GPS (SAM-M10Q or MAX-M10S, ATtiny1616, RV-3028)

| Item | Current | Basis |
|---|---|---|
| RV-3028 timekeeping | 0.000045 mA (45 nA) | datasheet |
| ATtiny1616 at 5 MHz, 3 V | 1.8 mA (3.1 mA at 10 MHz) | datasheet (DS40002204A) |
| TPS2553 GPS switch, on | about 0.12 mA | datasheet |
| GPS acquisition (GPS+Galileo) | 10 mA VCC + about 2 mA V_IO | u-blox M10 tables, 3.0 V |
| GPS continuous tracking | 8 mA + 2.1 mA = about 10 mA | same |
| GPS power-save tracking | 5 mA + 2 mA = about 7 mA | same |
| GPS V_BCKP backup | 28 uA (normal operation about 3 uA) | same |
| GPS start-up inrush | up to about 100 mA | MAX-M10S datasheet; SAM-M10Q assumed the same core, unchecked |

| State | Total | Energy per day |
|---|---|---|
| GPS off (RTC + MCU) | 1.8 mA (worst 3.1) | 43 mAh/day |
| GPS tracking | 12.0 mA | 288 mAh/day |
| GPS acquiring | 13.9 mA | 334 mAh/day |
| GPS start-up peak | about 103 mA | milliseconds |

**Findings**
- The MCU, not the RTC, dominates the idle drain. 1.8 mA continuous is about 43 mAh a day taken from the badge battery, versus nanoamps for the RTC. If the MCU can sleep between I2C accesses this drops by orders of magnitude, but **no sleep-current figure was extracted for the ATtiny1616**. STM32C011 can wake from Stop on an I2C address match (confirmed), so it is the better pick if idle current matters, but its stock showed 0 on the last check.
- Duty-cycle the GPS. A 5-minute daily fix at 12 mA costs about 1 mAh/day; always-on costs 288.
- The start-up inrush is the only item near the peak limit. Mitigate with the 22 uF-class bulk cap on the GPS branch, the TPS2553 current limit (RILIM 232 kOhm gives about 100 to 137 mA) and a ferrite. A Quectel L76K would be worse (26 mA, 100 mA supply recommended).
- RTC backup needs no badge power: CR1220 on VBACKUP at about 100 nA (our estimate) lasts years; do not enable the trickle charger on a primary cell.

### 2. RNG (RP2350A, TLV9062 front end)

| Item | Current | Basis |
|---|---|---|
| RP2350A, 150 MHz with ADC | 14.7 mA VREG_VIN + 0.5 mA IOVDD + 0.14 mA ADC = about 15.3 mA | Raspberry Pi `hello_adc` measurement, with USB connected |
| RP2350A at 25 / 50 MHz | about 2.5 / 4.5 mA (est: read from the DVDD chart, 80 % buck efficiency assumed) | **est**, chart-derived; add about 1 mA margin for the 48 MHz ADC PLL |
| RP2350A sleep (P1.7) | about 57 uA | datasheet |
| W25Q16JV flash | standby 10 uA, read at 50 MHz about 4 mA | datasheet; XIP duty cycle is unknown |
| 2 x TLV9062 (4 amplifier channels) | 2 x 2 x 538 uA = 2.15 mA | datasheet |
| Alternative 2 x TLV9002 | 2 x 2 x 60 uA = 0.24 mA | datasheet; 1 MHz is too slow for one x1000 stage, use two x32 stages |
| Fabric bias | about 0.05 mA | our design (10 to 50 uA) |

| Build | Total | Energy per day |
|---|---|---|
| Low power (25 MHz, TLV9002) | about 4.3 mA (est) | 103 mAh/day |
| Typical (50 MHz, TLV9062) | about 10 mA (est) | 245 mAh/day |
| Worst (150 MHz, TLV9062, flash reads) | about 21.6 mA | 517 mAh/day |

**Findings**
- Run the CPU slow. SHA-256 and HMAC-DRBG need little; 25 to 50 MHz saves about 10 mA over 150 MHz.
- The op-amps are the largest fixed load at 2.15 mA with TLV9062. Choose by noise: TLV9062 (16 nV/rtHz at 1 kHz, 10 MHz GBW) for the first bench rig, then move to TLV9002 only if its noise (30 nV/rtHz) is still adequate.
- **Duty-cycle the whole device.** The FIFO only needs filling when it is empty. With the analog stage on a load switch and the MCU asleep (about 57 uA) between bursts, average draw can fall below 1 mA. That is the real power design, and needs firmware, not parts.
- RP2350 needs a core-supply inductor and caps (3.3 uH, 4.7 uF in and out). It is a larger BOM than the other two boards.

### 3. Splitter (variant A+B)

| Item | Current | Basis |
|---|---|---|
| TPS2553, on | about 0.11 mA | datasheet |
| LM66100 x2 | 0.15 uA typ each; reverse leakage 0.2 uA typ at 25 C | datasheet |
| AP2112K, quiescent (only when USB present) | 55 uA typ, 80 uA max | datasheet |
| Power LED | about 1 mA (est) | make it a jumper/DNP |
| Fault LED | 0 unless a fault | |

- Overhead taken from the badge: about **1.1 mA** with the LED, about 0.11 mA without it. With USB present, the badge leg is off and the badge sees about 0.2 uA reverse leakage.
- **USB path thermal limit.** The AP2112K is a linear regulator from 5 V: it dissipates (5 - 3.3) x I, so 0.17 W at 100 mA, 0.43 W at 250 mA and 1.0 W at its 600 mA rating. Treat the USB path as limited to about 250 mA until a buck converter replaces it (the SOT-23-5 thermal limit was not checked, so even 250 mA is unverified).
- **Badge-leg limit:** RILIM 180 kOhm gives about 129 to 174 mA (min to max over tolerance; nominal about 150 mA). This is deliberately near the practical per-port rule, so a downstream short cannot pull more than that from the badge. The earlier 200 mA figure in the splitter brief has been corrected.
- Voltage drop through TPS2553 + LM66100 on the badge leg is expected in the tens of mV at 100 mA; their on-resistance at 3.3 V was **not verified**.
- AP2112K foldback limits a downstream short to about 50 mA, which also means a large capacitive load may not start; keep downstream bulk capacitance small.

## All three together on one port

| Scenario | Total |
|---|---|
| Idle: GPS off, RNG low-power, splitter LED off | about 6 mA |
| Typical running: GPS tracking, RNG typical | about 23 mA |
| Worst steady: GPS acquiring, RNG worst, MCU at 10 MHz | about 38 mA |
| Worst peak: GPS inrush + RNG worst + splitter | about 126 mA, milliseconds |

Against the 100 mA continuous rule: steady state uses 23 to 38 %. The peak is 126 mA against a 150 mA brief limit, and the GPS switch plus bulk cap should keep a weak badge from ever seeing all of it at once.

**Where it can still fail**
- A badge that really only has about 30 mA free on USB power (the unverified DEF CON 33 claim) would not carry the typical load, and the splitter's USB input is the fix.
- Badge rails sagging to 3.0 V under battery power: the AP2112K-based badges drop out below 3.3 V + 0.25 V headroom as the LiPo drains; our parts all accept 3.0 V or below (RP2350, ATtiny1616, M10 at 2.7 V or 1.76 V minimum depending on module), but the u-blox SAM-M10Q minimum is 2.7 V.
- Badges with all eight LEDs on or Wi-Fi bursts: our boards do not see a regulated rail at that moment. That is the badge's problem, but we should not be the load that tips it: keep our peaks soft.
- Battery life: 23 mA continuous is 560 mAh per day. On a badge LiPo of a few hundred mAh that is under a day, so **duty-cycling is a requirement, not an optimisation** (GPS on demand, RNG on demand, MCUs sleeping).

## BOM summary

Per-project CSVs, priced from LCSC/JLCPCB data pulled 2026-11-09 (**stock and prices move; recheck before ordering**). Totals exclude PCB fabrication, assembly, shipping, batteries, USB cable, fabric and clips. "est" rows are placeholders (passives, inductor, polyfuse, N-FET, female header priced by proxy).

| Board | CSV | Qty 1 | About 100 | Unique extended SMT part types |
|---|---|---|---|---|
| RTC base | [`bom-base.csv`](planning-design/rtc-gps/bom-base.csv) | $5.18 | $3.43 | 5 |
| GPS add-on (SAM-M10Q) | [`bom-gps-addon.csv`](planning-design/rtc-gps/bom-gps-addon.csv) | $20.75 | $20.23 (10+ tier, nothing higher) | 1 |
| GPS add-on, MAX-M10S variant | [`bom-gps-addon-max-m10s-variant.csv`](planning-design/rtc-gps/bom-gps-addon-max-m10s-variant.csv) | $11.83 | $11.27 (10+ tier) | 1 |
| RNG | [`bom.csv`](planning-design/rng/bom.csv) | $3.59 | $2.79 | 5 |
| Splitter A+B | [`bom.csv`](planning-design/splitter/bom.csv) | $2.16 | $1.52 | 7 (TCA4307 DNP not counted) |

- **RTC + GPS complete: about $26 at qty 1** (SAM-M10Q is 80 % of it), or about $17 with the MAX-M10S variant whose antenna matching and ground-plane needs are **unchecked**.
- The cost on a tiny run is dominated by the GPS module and by **JLCPCB's extended-part loading fee, charged per unique extended part type** (the fee amount is not quoted here; check the current JLCPCB price). The splitter's 7 types and the others' 5 each are a large share of a 5-piece order.
- Risks in the BOM: RV-3028 stock was 0 to 143 (alternate listing C3019759); STM32C011 stock 0; SAM-M10Q stock 102; no supercap found on JLC/LCSC; CR1220 cells are not on JLC. DigiKey/Mouser pages block automated fetches, so their prices are snippets and may be stale.
- Totals come from [`workbench/hardware/tools/bom_totals.py`](workbench/hardware/tools/bom_totals.py): `python3 -I workbench/hardware/tools/bom_totals.py planning-design/rng/bom.csv`.

## What changed in the designs because of this

- Splitter: badge-leg limit set to about 130 to 175 mA (RILIM 180 kOhm) and USB path flagged as thermally limited.
- RTC: MCU idle drain flagged as the main battery cost; STM32C011 or an MCU sleep mode is the likely fix.
- RNG: duty-cycling the analog stage is a design requirement; TLV9062 is the bench-rig op-amp.

## Sources

Data pulled 2026-11-09: [RP2350 datasheet](https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf), [ATtiny1616 DS40002204A](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ProductDocuments/DataSheets/ATtiny1614-16-17-DataSheet-DS40002204A.pdf), [MAX-M10S](https://content.u-blox.com/sites/default/files/MAX-M10S_DataSheet_UBX-20035208.pdf), [SAM-M10Q](https://cdn.sparkfun.com/assets/1/1/d/f/4/SAM-M10Q_DataSheet_UBX-22013293.pdf), [AP2112](https://www.diodes.com/assets/Datasheets/AP2112.pdf), [LM66100](https://www.ti.com/lit/ds/symlink/lm66100.pdf), [TPS2553](https://www.ti.com/lit/ds/symlink/tps2553.pdf), [Pico W datasheet](https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf), LCSC/JLCPCB part pages by C-number in the CSVs. Badge evidence: [2026 Billboard](https://github.com/Hack-a-Day/2026-Billboard_Badge) (`production/netlist.ipc`, `billboard_pcb_BOM.csv`, `power.kicad_sch`), [2024 Supercon 8](https://github.com/Hack-a-Day/2024-Supercon-8-Add-On-Badge), [2025 Communicator](https://github.com/Hack-a-Day/2025-Communicator_Badge); DC33 and DC31 claims from [vortexcodes](https://raw.githubusercontent.com/vortexcodes/DC33-SaO-MANY-SAOs/main/README.md) and [Tindie](https://www.tindie.com/products/makeithackin/sao-adapter-for-def-con-31-badge) (third-party, unverified); v1.69bis conversion from the [Hackaday comments](https://hackaday.com/2019/03/20/introducing-the-shitty-add-on-v1-69bis-standard).
