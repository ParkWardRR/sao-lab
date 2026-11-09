# SAO RTC with GPS add-on

Status: prepped 2026-11-09, nothing built. Datasheets read for RV-3028, RV-8803, MCP79410, PCF8523 (NXP page), MAX-M10S, SAM-M10Q, L76K, AT6558. Everything else is tagged *(unverified)*. LCSC/JLCPCB prices and stock came from cached snapshots that disagree with each other: **recheck live before ordering**. *(recommendation)* marks our proposals.

## Goal

An SAO that keeps accurate time when the badge is off or has no clock of its own, and an optional GPS add-on that sets the time and (later) disciplines the RTC and reports position.

## Architecture *(recommendation)*

Two boards:

| Board | Contents | Works alone? |
|---|---|---|
| **RTC base SAO** | RV-3028-C7, CR1220 on VBACKUP, small MCU (client on the SAO bus), GPS connector, GPS power switch | Yes, as a clock |
| **GPS add-on** | GPS module + antenna, on a dedicated header (not an SAO connector) | No, needs the base |

Why a dedicated header and not a second SAO port: a six-pin SAO header cannot carry UART + PPS + enable + backup, and the weak points of chaining are the shared 3V3 and I2C ([research report](#sources)). Other layouts considered: everything on one board (simplest, bulky, blows the power budget on weak badges) and a GPS board behind a pass-through SAO port (reuses the standard connector, but PPS only fits on GPIO1). The [splitter](../splitter/README.md) is how you power the GPS from USB if the badge port is weak.

### Key decision: where does the RTC sit on the bus?

| Mode | Wiring | Pro | Con |
|---|---|---|---|
| **Smart** *(recommended)* | RTC on a **private** I2C bus owned by the MCU; only the MCU faces the SAO header | one address, one protocol, no multi-master on the shared bus, RTC discipline possible | generic RTC drivers do not work; needs host driver |
| Plain | RTC directly on the header bus at 0x52, MCU DNP | works with any RTC driver, no firmware | no GPS discipline; adds a fixed address to the shared bus |

Make both buildable: two solder jumpers and an MCU DNP footprint. First prototype: smart.

## RTC choice

| Chip | Addr | Accuracy | Timekeeping | Backup | Notes |
|---|---|---|---|---|---|
| **RV-3028-C7** *(recommended)* | 0x52 | +-1 ppm at 25 C, factory-calibrated | 45 nA at 3 V | VBACKUP pin, switchover, trickle charger (disabled by default), 32-bit UNIX counter | LGA 3.2x1.5x0.8; JLC extended [C3019759](https://jlcpcb.com/partdetail/C3019759), about $1.4 to 2.2 |
| RV-8803-C7 | 0x32 | +-3 ppm over -40..85 C | 240 nA | no VBACKUP pin | fallback; address checked |
| MCP79410 | 0x6F (RTCC), 0x57 (EEPROM) | depends on external crystal | 925 nA | VBAT, no charger | its 0x57 EEPROM lives next to the 0x50 ID range |
| AB1805-T3 | 0x69 *(unverified)* | +-2 ppm with calibration | 14 nA RC / 55 nA crystal, distributor lists 170 to 220 nA *(unresolved)* | power switch, supercap charger, watchdog | alternative if watchdog is wanted |
| DS3231M/SN | 0x68 *(unverified)* | +-2 to 5 ppm *(unverified)* | ~1 uA *(unverified)* | VBAT | datasheet not downloadable; more expensive |
| PCF8523 | 0x68 | offset register only | 150 nA | VBAT | NXP page says "No Longer Manufactured": avoid |

Sources: [RV-3028 manual](https://www.microcrystal.com/fileadmin/Media/Products/RTC/App.Manual/RV-3028-C7_App-Manual.pdf), [RV-8803 manual](https://www.microcrystal.com/fileadmin/Media/Products/RTC/App.Manual/RV-8803-C7_App-Manual.pdf), [MCP79410](https://www.farnell.com/datasheets/4020463.pdf), [PCF8523](https://www.nxp.com/products/PCF8523).

### Backup power and no backfeed

- **CR1220 (recommended):** not rechargeable, so leave the RV-3028 trickle charger **off** (TCE=0, the default); enabling it would try to charge a primary cell. About 100 nA should last years *(our estimate)*.
- **Supercap 0.1 to 0.33 F:** charge via the RV-3028 trickle charger; the internal Schottky tops out near 3.0 V. Runtime days to weeks at best, dominated by leakage *(our arithmetic: 0.1 F x 2.2 V / 100 nA about 25 days, if leakage is negligible)*.
- **LIR / Li-ion:** avoid; needs a real charger with a 4.2 V cutoff.
- Battery only on VBACKUP; if VBACKUP is unused tie it to VSS through 10 kOhm. In backup state the RV-3028 releases SCL and SDA, so it does not load the bus.
- **Never power the MCU or GPS from the backup source.** Check MCU I2C pin clamp diodes to VDD: an unpowered MCU can be parasitically powered through SDA/SCL, so add series resistors or choose a part without the clamp. Put pull-ups on the badge side (or DNP), per [electrical-and-interop](../../research/specs/electrical-and-interop.md).
- 10 to 47 uF bulk cap plus ferrite on the GPS 3V3 branch to limit inrush from a weak rail. Gate the GPS with a load switch controlled by the MCU, **default off**.

## GPS module options

| Module | Interface | Supply | Acq / track current | Power save | PPS | Size / antenna | Price |
|---|---|---|---|---|---|---|---|
| **u-blox SAM-M10Q** | UART, I2C 0x42 | 2.7 to 3.6 V | same M10 core, 8 to 13 mA acquisition | same | TIMEPULSE | about 15 mm built-in patch | about $11 at 250 |
| **u-blox MAX-M10S** | UART, I2C 0x42 | 1.76 to 3.6 V | 8 to 13 mA / 7.5 to 10 mA, +2 mA V_IO | cyclic tracking about 5 mA; backup 28 uA | 30 ns RMS | 10.1x9.7x2.5 mm, external antenna, LNA_EN | LCSC [C4153167](https://jlcpcb.com/partdetail/C4153167) extended, $10 to 15 |
| Quectel L76K | UART only | 2.7 to 3.4 V | 26 / 26 mA; 100 mA supply recommended | standby 20 uA, backup 8 uA | <30 ns | 10.1x9.7x2.0 mm | *(unverified)* |
| ATGM336H (AT6558) | UART (I2C on chip, module *(unverified)*) | 2.7 to 3.6 V | <23 mA at 3.3 V | standby <10 uA | yes | 9.7x10.1 mm *(unverified)* | LCSC [C90770](https://lcsc.com/product-detail/image/ATGM336H-5N31_C90770.html) $3.27 at 1 |
| Adafruit PA1010D | UART, I2C 0x10 *(third-party)* | 3.3 to 5 V (breakout) | about 30 mA | WAKE pin | +-20 ns | 25.5x25.4 mm breakout | $29.95 |

Cold start, datasheet: MAX-M10S 23 to 28 s (1 s hot), L76K under 30 s (under 5.5 s with AGNSS), AT6558 up to 32 s. Sources: [MAX-M10S](https://content.u-blox.com/sites/default/files/MAX-M10S_DataSheet_UBX-20035208.pdf), [SAM-M10Q](https://cdn.sparkfun.com/assets/1/1/d/f/4/SAM-M10Q_DataSheet_UBX-22013293.pdf), [L76K](https://atta.szlcsc.com/upload/public/pdf/source/20220718/161EA7C8E41D7B6341312B03CEF3291C.pdf), [AT6558](https://wiki.millerjs.org/_media/at6558_datasheet.pdf), [PA1010D](https://learn.adafruit.com/adafruit-mini-gps-pa1010d-module).

**Indoor performance at a conference is unverified.** Expectation: no fix inside a hall without a window, and cold starts there taking minutes rather than the datasheet seconds. So keep the GPS backup supply (V_BCKP) alive from the RTC board's backup for hot/warm starts, and plan for "sync outside once, RTC holds the time".

*(Recommendation)* Rev 1 add-on: **SAM-M10Q** (patch built in, nothing to tune) for the first board; MAX-M10S with a u.FL and active antenna for a second variant. All of these fit a 50 to 100 mA budget; only the L76K's 100 mA recommendation is tight.

## Disciplining the RTC

1. GPS PPS edge latches an MCU timer capture.
2. Compare against the RTC 1 Hz output (CLKOUT/INT).
3. `drift_ppm = (delta_ticks / 32768) x 1e6`, filtered over many seconds.
4. Write the correction to the RV-3028 offset register (0.9537 ppm per LSB, +-244 ppm range).
5. NMEA/UBX time sets the UNIX counter; only the PPS edge sets the subsecond phase.

## MCU candidates (I2C client + UART)

| MCU | Flash / RAM | Price (LCSC) | Notes |
|---|---|---|---|
| ATtiny1616 | 16 KB / 2 KB | about $1.1 to 1.7 [C609652](https://lcsc.com/product-detail/Microcontrollers-MCU-MPU-SOC_Microchip-Tech-ATTINY1616-SNR_C609652.html) | TWI client + USART, from memory, *(unverified)* |
| CH32V003F4U6 | 16 KB / 2 KB | about $0.14 to 0.28 [C5299908](https://www.lcsc.com/product-detail/C5299908.html) | I2C slave not confirmed in the pages read; used by Supercon 2024 add-on badge |
| STM32C011F6U6 | 32 KB / 6 KB (one listing says 12 KB) | $0.59 to 1.63 | more RAM for a UBX/NMEA parser; I2C not named in snippets |
| RP2040 / RP2350 | 264 / 520 KB | about $0.7 to 1.7 | big BOM for this job |
| PY32F002B | 24 KB / 3 KB | not found | I2C slave not stated |

No MCU pick is made; **the first prototype runs on a dev board and settles it.** Check I2C client mode in the reference manual before committing.

## I2C register map (draft, ours)

Fits the intelligent-SAO draft in [electrical-and-interop](../../research/specs/electrical-and-interop.md#draft-elements-of-a-reusable-intelligent-sao-protocol). Address: see [system address plan](../system-overview.md#i2c-address-plan).

| Reg | Size | Contents |
|---|---|---|
| 0x00 | 1 | ID / protocol version |
| 0x01 | 1 | Status: bit0 time_valid, bit1 fix, bit2 pps_seen |
| 0x02 | 1 | Fix quality |
| 0x03 | 1 | Satellites |
| 0x04 | 4 | UNIX time |
| 0x08 | 2 | Subsecond (1/65536) |
| 0x0A | 4 | Latitude (1e-7 deg, signed) |
| 0x0E | 4 | Longitude (1e-7 deg, signed) |
| 0x12 | 4 | PPS counter |
| 0x16 | 2 | Drift (0.01 ppm, signed) |
| 0x18 | 1 | Command (GPS on/off, resync) |

Still to specify: coherent snapshot (latch on reading reg 0x04 so time and subsecond match), byte order, behaviour with no RTC, what "time_valid" means after a battery loss. GPIO2 as alarm/PPS interrupt out.

## GPS add-on header (draft nets)

3V3_SW (switched), GND, GPS_TX, GPS_RX, PPS, V_BCKP from RTC backup. Exact connector and pinout to decide, keyed so it cannot be flipped.

## Test plan

- Native tests: register map, snapshot latch, UBX/NMEA parser against recorded sentences, discipline filter against synthetic drift.
- Bench: drift of RV-3028 vs GPS PPS over 24 h, at room temperature and warm.
- Power: measure idle, GPS acquisition, GPS tracking at the SAO pin; confirm zero current into the badge with the badge off and the CR1220 fitted.
- Fixture: cold/hot/warm start timing near a window, backup retention after badge power cycle.
- Backfeed: scope pin 1 and SDA/SCL with the badge unpowered.

## First-prototype plan

1. Dev board + RV-3028 breakout + SAM-M10Q breakout: prove I2C access, PPS capture and the discipline loop. Pick the MCU.
2. Firmware core + protocol with desktop tests.
3. KiCad: RTC base (smart mode, DNP footprint for plain mode) and GPS add-on.
4. First boards: two-layer, DNP pull-ups, test pads on 3V3, GND, SDA, SCL, PPS.

## Open questions

- Does "GPS add-on" mean a stacked daughter board (assumed) or a separate SAO plugged in elsewhere?
- Smart (private bus) or plain RTC as the default?
- GPS: integrated patch (SAM-M10Q) or external antenna (MAX-M10S + u.FL)?
- Do you want position reported over I2C, or time only?
- CR1220 or supercap?

## Sources

All inline above. Not reachable: Analog's DS3231 datasheet (so DS3231 rows are unverified).
