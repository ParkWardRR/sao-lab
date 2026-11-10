# 🧇 sao-lab

[![Visibility](https://img.shields.io/badge/repo-public-brightgreen?style=for-the-badge&logo=github)](https://github.com/ParkWardRR/sao-lab)
[![Status](https://img.shields.io/badge/status-research%20%26%20design-orange?style=for-the-badge)](docs/research-log.md)
[![Last commit](https://img.shields.io/github/last-commit/ParkWardRR/sao-lab?style=for-the-badge&logo=git&logoColor=white)](https://github.com/ParkWardRR/sao-lab/commits/main)
[![Stars](https://img.shields.io/github/stars/ParkWardRR/sao-lab?style=for-the-badge&logo=github)](https://github.com/ParkWardRR/sao-lab/stargazers)
[![Issues](https://img.shields.io/github/issues/ParkWardRR/sao-lab?style=for-the-badge&logo=github)](https://github.com/ParkWardRR/sao-lab/issues)

[![Hackaday Supercon](https://img.shields.io/badge/Hackaday-Supercon%202026-black?style=flat-square&logo=hackaday&logoColor=white)](https://hackaday.com/tag/supercon/)
[![SAO v1.69bis](https://img.shields.io/badge/SAO-v1.69bis-yellow?style=flat-square)](https://hackaday.com/2019/03/20/introducing-the-shitty-add-on-v1-69bis-standard/)
[![Badgelife](https://img.shields.io/badge/%23badgelife-yes-ff69b4?style=flat-square)](https://hackaday.io/project/52950-shitty-add-ons)
[![I²C](https://img.shields.io/badge/bus-I%C2%B2C-blue?style=flat-square)](POWER.md)
[![3.3 V](https://img.shields.io/badge/supply-3.3%20V-red?style=flat-square)](POWER.md)
[![Power budget](https://img.shields.io/badge/power-assessed-success?style=flat-square)](POWER.md)
[![KiCad](https://img.shields.io/badge/EDA-KiCad-314cb0?style=flat-square&logo=kicad&logoColor=white)](https://www.kicad.org/)
[![Waffles](https://img.shields.io/badge/aesthetic-waffles-f5c542?style=flat-square)](#the-waffles)

> I went to Hackaday Supercon 2026 and came home inspired by the beautiful, functional (and sometimes gloriously useless) **Shitty Add-Ons** people hang on their badges. So I'm making my own.

The goal is **three devices that puzzle together, all designed as aesthetic waffles.**

## The waffles

| Device | What it is | Role |
|--------|------------|------|
| 🧇 **Waffle 1** | Random number generator | Hardware entropy on an SAO |
| 🧇 **Waffle 2** | Real-time clock (RTC) | Keeps time with a backup cell |
| 🧈 **Pad of butter** | GPS add-on for the RTC | Stacks onto Waffle 2; its 1PPS output disciplines the clock |
| 👻 **SAO splitter** | *Unseen*, hidden behind the waffles | Turns one SAO port into several |

The waffles, the butter and the splitter fit together like a breakfast puzzle. Waffle 1 and Waffle 2 both plug into the splitter, and the butter sits on top of Waffle 2.

```
 badge ──[ SAO splitter ]──┬── 🧇 Waffle 1 (RNG)
                           └── 🧇 Waffle 2 (RTC) ── 🧈 butter (GPS)
```

## Stretch goal: the 2027 splitter / hacker

I don't know what badge Supercon will hand out in 2027. So the splitter should be more than a splitter: a **hacker's SAO interposer** that gives me extra capability during the con, whatever the badge turns out to be. For example:

- Feeding the SAOs **more power from the side** (USB-C or a battery) when the badge's port can't supply enough
- Isolating the badge's supply so injected power never back-feeds it
- I²C sniffing, address remapping and level shifting
- Breaking out the GPIOs for poking around

The first thing to settle is whether the power works. See **[POWER.md](POWER.md)**.

## Repo layout

| Path | Contents |
|------|----------|
| [`POWER.md`](POWER.md) | Power assessment: budgets per device, SAO port limits, injection design |
| [`docs/`](docs) | Spec notes, badge compatibility, [research log](docs/research-log.md) |
| [`hardware/`](hardware) | Schematics, PCBs, waffle outlines |
| [`firmware/`](firmware) | Firmware for each waffle and the splitter |

## The SAO port

A 2×3, 0.1" header carrying 3.3 V, ground, I²C and two GPIOs. Check the [v1.69bis standard](https://hackaday.com/2019/03/20/introducing-the-shitty-add-on-v1-69bis-standard/) for the authoritative pinout.

| Pin | Signal |
|-----|--------|
| 1 | VCC (3.3 V) |
| 2 | GND |
| 3 | SDA |
| 4 | SCL |
| 5 | GPIO1 |
| 6 | GPIO2 |
