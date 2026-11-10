# Power assessment

[![Supply](https://img.shields.io/badge/supply-3.3%20V-red?style=flat-square)](#the-constraint)
[![Status](https://img.shields.io/badge/figures-estimates-orange?style=flat-square)](#caveat)

Can a badge's SAO port power all three devices at once? Short answer: **probably not the GPS on a weak port**, which is why the splitter needs side power.

## The constraint

The SAO standard gives a 3.3 V pin and **no guaranteed current**. The budget depends entirely on the badge's regulator, so each badge has to be measured or looked up. Until I know the 2027 badge, I design for the worst case: assume a port that can give little, and supply the rest from the side.

## Budget per device

| Device | Main load | Typical | Peak | Notes |
|--------|-----------|---------|------|-------|
| 🧇 Waffle 1: RNG | MCU + noise source | 3–10 mA | 15 mA | An avalanche source needs a boost converter, which costs more than a ring-oscillator or ADC-noise approach |
| 🧇 Waffle 2: RTC | RTC IC | 0.2 mA | 0.3 mA | The backup cell carries the time when the badge is off, so the load is negligible |
| 🧈 Butter: GPS | GNSS module | 10–25 mA | 40 mA+ | The dominant load; cold-start acquisition draws the most |
| 👻 Splitter | Regulation, mux, pull-ups | 1–3 mA | 5 mA | Plus whatever the side-power path costs |
| **Total** | | **~15–40 mA** | **~60 mA** | |

## Caveat

Every figure above is a **planning estimate from my own recall, not a datasheet value.** Replace each row with the datasheet number for the part I pick, then with a measured number from a built board.

## Findings so far

1. **The GPS decides everything.** Without it, the two waffles fit in a small budget. With it, a weak port can brown out.
2. **The RTC is nearly free.** Put it on a backup cell so the time survives.
3. **I²C address conflicts need a plan.** Many common RTCs answer at `0x68`. Pick parts and addresses that don't collide with each other or with the badge's other devices.
4. **Pull-ups multiply on a splitter.** Each SAO and the badge may carry its own I²C pull-ups, and in parallel they can pull the lines too hard.

## Side-power design (splitter, stretch goal)

Goal: feed the SAOs from a USB-C port or battery when the badge can't.

- **Never back-feed the badge.** Use an ideal-diode or power-path controller so the side supply and the badge's 3.3 V can't fight.
- **Regulate to 3.3 V** at the splitter, so the SAOs always see the right rail.
- **Share ground** with the badge.
- **Make it switchable**, so the badge's own supply can power the SAOs whenever it's enough.
- **Add inrush and overcurrent protection**, so a short on one waffle doesn't take down the others.

## To do

- [ ] Choose parts for each waffle, then fill in the datasheet currents
- [ ] Build a bench rig to measure real draw, including GPS cold start
- [ ] Collect SAO-port current limits for common badges
- [ ] Prototype the side-power path and test for back-feed
