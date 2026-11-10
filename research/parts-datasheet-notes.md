# Parts datasheet notes (power and BOM research)

Pulled 2026-11-09 from manufacturer/LCSC datasheets and live LCSC/JLCPCB part data. Feeds [POWER.md](../POWER.md) and the BOM CSVs in each project folder. Prices are USD and move; JLCPCB class is "ext" (extended) for every part below except the crystal. Items marked *(unverified)* were not confirmed against a datasheet. Estimates marked **est** are ours.

## MCUs

| Part (LCSC) | Run current at 3.3 V (3.0 V for STM32) | I2C client | Price 1 / about 100 |
|---|---|---|---|
| RP2350A (C42411118) | 14.7 mA VREG_VIN + 0.5 mA IOVDD + 0.14 mA ADC at 150 MHz, from the Raspberry Pi `hello_adc` test with USB connected; about 2.5 / 4.5 mA at 25 / 50 MHz **est** from the DVDD chart (80 % buck efficiency assumed); sleep P1.7 about 57 uA, all-retained P1.0 about 166 uA | yes (DW_apb_i2c) | 1.30 / 1.13 |
| ATtiny1616-MNR (C507118) | 1.8 mA at 5 MHz, 3.1 mA at 10 MHz (3 V); 20 MHz at 3 V not specified; sleep current not extracted | yes, TWI, dual address match | 1.34 / 0.84 |
| STM32C011F6U6TR (C5456206) | 0.66 mA at 8 MHz, 1.25 mA at 16 MHz, 2.25 mA at 24 MHz, 3.40 mA at 48 MHz | yes, wake from Stop on address match | 1.86 / 1.77, stock 0 |
| CH32V003F4U6 (C5299908) | 2.0 mA at 8 MHz, 3.3 mA at 16 MHz, 4.0 mA at 48 MHz (peripherals off, clocks add 0.4 to 2.4 mA); standby 9.1 uA | yes, 7/10-bit, dual slave address (v1.8 datasheet 1.4.15) | 0.305 / 0.245 (50+ tier) |

RP2350 facts: RP2350A (QFN-60) has 4 ADC inputs plus a temperature sensor (GPIO26-29); RP2350B (QFN-80) has 8 (GPIO40-47). The ADC needs a fixed 48 MHz clock, so a PLL stays on. The core buck needs a 3.3 uH +-20 % shielded inductor (DCR 250 mOhm or less, Isat 1.5 A or more; AOTA-B201610S3R3-101-T recommended) and 4.7 uF in and out; the inductor can be omitted if DVDD is fed externally. A 12 MHz crystal is not mandatory (XOSC takes 1 to 50 MHz, ROSC works without) but USB boot assumes 12 MHz. Erratum RP2350-E9 (input-pad leakage) affects only the A2 stepping; which stepping the JLC part is was not confirmed. [Datasheet](https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf).

Flash: W25Q16JVSNIQ (C2456211) standby 10 uA, power-down 1 uA, read about 4 mA at 50 MHz, 8 mA at 104 MHz; 1.18 / 0.78. W25Q32JVSSIQ (C179173) 1.56 / 1.08, read current *(unverified)*. 12 MHz crystal YXC C9002 is a JLCPCB basic part, 0.095 / 0.07.

Datasheets: Microchip DS40002204A, [ST stm32c011d6 (SparkFun mirror)](https://cdn.sparkfun.com/assets/d/4/7/1/b/stm32c011d6-3082107.pdf), WCH v1.8 datasheet.

## Op-amps for a x100 to x1000 AC-coupled gain stage

| Part (LCSC) | Iq per channel | Voltage noise | Input bias | GBW | Price 1 / 100 |
|---|---|---|---|---|---|
| TLV9062IDR (C398355) | 538 uA | 16 nV/rtHz at 1 kHz, 10 at 10 kHz | +-0.5 pA | 10 MHz *(unverified)* | 0.119 / 0.09, stock 183k |
| OPA2316IDGKR (C2058895) | 400 uA | 11 nV/rtHz at 1 kHz | +-5 pA | 10 MHz | 0.94 / 0.56 |
| TLV9002IDGKR (C398361) | 60 uA | 30 nV/rtHz at 1 kHz | +-5 pA | 1 MHz | 0.25 / 0.17 |
| OPA2333AIDR (C38732) | 17 uA | 1.1 uVpp 0.1-10 Hz; density *(unverified)* | +-70 pA | 350 kHz | 0.65 / 0.40 |
| MCP6001T-E/OT (C29429) | 100 uA | 28 nV/rtHz | +-1 pA | 1 MHz | 0.32 / 0.22 |
| MCP6021-I/SN (C148054) | 1 mA | 8.7 nV/rtHz at 10 kHz | +-1 pA | 10 MHz | 1.78 / 1.14 |
| LMV358IDR (C63813) | *(unverified)* | *(unverified)* | *(unverified)* | *(unverified)* | 0.22 / 0.15 |

Picks: TLV9062 for the bench rig (low noise, wide bandwidth, cheap); TLV9002 if power matters, as two x32 stages since 1 MHz is too slow for one x1000 stage. Avoid OPA2333 here (350 kHz).

## Power path, protection and connectors

| Part (LCSC) | Figure | Price 1 / 100 |
|---|---|---|
| AP2112K-3.3TRG1 (C51118) | Iq 55 uA typ, 80 uA max | 0.183 / 0.13 |
| LM66100DCKR (C2869734) | Iq 0.15 uA, shutdown 0.12 uA, reverse leakage 0.2 uA typ at 25 C (2.7 uA max to 85 C) | 0.21 / 0.14 |
| TPS2553DBVR (C55266) | on 100 to 120 uA typ, off 0.1 uA | 0.55 / 0.34 |
| TCA4307DGKR (C880333) | ICC 2.5 mA typ, 4.5 mA max (at 5.5 V; 3.3 V *unverified*); shutdown 10 uA; heavy for a battery board | 2.69 / 2.0, stock 50 |
| ESD5Z3.3T1G (C61148) | rejected for clip leads: unidirectional, 50 uA max leakage, 105 pF | 0.048 / 0.036 |
| PTVSLC3D3V3B (C246774) | chosen for clip leads: 3.3 V standoff, 1 uA leakage, 3.5 pF, 7 V clamp at 1 A, +-30 kV IEC; bidirectional use mentioned | 0.056 / 0.045 |
| USB-C 16-pin TYPE-C-31-M-12 (C165948) | leave D+/D- unrouted for power only | 0.187 / 0.13 |
| 2x3 male header (C65114) / 2x3 female (C32713304) | through-hole | 0.045 / 0.155 |
| 1x7 male (C53055676), 2x4 male (C55829516) | | 0.042, 0.16 |
| CR1220 holder KH-BS1220-2 (C4943311) | cell itself is not on JLC | 0.176 / 0.139 |
| JST-SH 4-pin SMD: JST (C160404), clone (C2763614) | | 0.215, 0.058 |
| Green 0603 LED NCD0603G1 (C84267) | Vf 3.0 V typ at 10 mA; Vf at 1 mA not confirmed (expect 2.6 to 2.8 V) | 0.016 / 0.011 |

**TPS2553 current limit** (RILIM in kOhm, 15 to 232): nominal mA = 23950 / RILIM^0.977; minimum = 25230 / RILIM^1.016; maximum = 22980 / RILIM^0.94. Checked values: 232 k gives about 100 to 137 mA, 180 k gives about 129 to 174 mA (nominal 150), 133 k gives about 175 to 232 mA.

Supercaps 0.1 F / 0.33 F: none found on JLC or LCSC. 0.33 F 5.5 V radial from Future Electronics about $1.09 at 1 *(snapshot, unverified)*.

## RTC

RV-3028-C7 (C3304278): 45 nA at 3 V, 1.2 to 5.5 V, 2.79 / 1.86 (JLC 2.76 / 1.84). **LCSC/JLC stock 0 to 143**, so it may be unavailable; an earlier snapshot listed C3019759. Full RTC comparison with addresses and accuracy: [rtc-gps brief](../planning-design/rtc-gps/README.md#rtc-choice).

## GPS (u-blox M10, 3.0 V table; 3.3 V near-identical *unverified*)

| Mode | MAX-M10S and SAM-M10Q |
|---|---|
| Acquisition (GPS / GPS+GAL) | 8 / 10 mA on VCC |
| Continuous tracking | 7.5 / 8 mA VCC plus about 2.1 mA V_IO |
| Power-save (cyclic) tracking | 4.5 / 5 mA VCC plus 2 mA V_IO |
| Hardware backup (V_BCKP 3.3 V, VCC = V_IO = 0) | 28 uA |
| Software standby | 46 uA V_IO plus 0.12 uA VCC |
| V_BCKP in normal operation | about 3 uA |

MAX-M10S start-up inrush up to about 100 mA; SAM-M10Q assumed the same (unchecked). SAM-M10Q VCC range 2.7 to 3.6 V; MAX-M10S range not extracted.

| Item | Source | Price 1 / about 100 |
|---|---|---|
| SAM-M10Q-00B (C5443880) | LCSC/JLC, stock 102, no tier above 10 | 20.65 / 20.15 (10+) |
| SAM-M10Q-00B | DigiKey DE, EUR search snippet, may be stale | 27.21 / 14.26 |
| MAX-M10S-00B (C4153167) | LCSC, stock 828 | 11.02 / 10.76 (10+) |
| MAX-M10S-00B | DigiKey FI, EUR snippet | n/a / 11.02 |
| Patch BWGNSCNX18-18W4 (C784395), 18x18 through-hole | | 0.71 / 0.43 |
| Patch KH-GPS181804-WY (C962215) | | 1.04 / 0.63 |
| Patch Abracon APAE1575R1840AADB7-T (C6746077), 18x18 SMD, stock 14 | | 1.81 / 1.71 |
| u.FL C47986640 / C2987682 | | 0.041 / 0.076 |

Antenna gain and ground-plane requirements were **not** checked. DigiKey and Mouser block automated fetches.

## Not verified here

DS3231 datasheet (Analog PDFs would not download), AB1805 I2C address, TPS2051C at 3.3 V, TPS62840 3.3 V VSET option, ATtiny1616 sleep current, W25Q32JV read current, PIO current (the research used the PWM figure of about 9.9 uA/MHz as a stand-in).
