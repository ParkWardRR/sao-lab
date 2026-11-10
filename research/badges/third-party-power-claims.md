# Third-party badge power claims (unverified)

Statements about how much current other badges' SAO ports supply, from sellers and community projects. **None checked against the badge schematic.**

| Badge | Claim | Source |
|---|---|---|
| DEF CON 33 | "it can only supply around 300 mA @ 3.3V total before the onboard fuses say 'nope'"; on USB or barrel power only about 30 mA is available if all SAOs run at once | [vortexcodes/DC33-SaO-MANY-SAOs](https://raw.githubusercontent.com/vortexcodes/DC33-SaO-MANY-SAOs/main/README.md) |
| DEF CON 31 | "safe to power up to 350 milliamps" | [Tindie seller listing](https://www.tindie.com/products/makeithackin/sao-adapter-for-def-con-31-badge) |
| DEF CON 32, flow3r / MCH2022 | no primary SAO current figure found | n/a |

## The v1.69bis number

"1.1 millihorsepower" is the only power limit in the standard ([hackaday.io log](https://hackaday.io/project/52950-shitty-add-ons/log/159806-introducing-the-shitty-add-on-v169bis-standard)). The about-250 mA figure is a conversion from [Hackaday article comments](https://hackaday.com/2019/03/20/introducing-the-shitty-add-on-v1-69bis-standard): "1.1 millihorsepower is around 820 milliwatts?", "probably 'intended' to be 250mA @ 3.3V", "It checks out." It is not a guarantee of what any port supplies. The Simple Add-On v2 page says only that VCC is expected to be 3.3 V and that "SAO Capable devices take care of the power requirements" ([page](https://hackaday.io/project/175182-simple-add-ons-sao)). Nick Sayer recommends a load switch (AP2331) to protect a badge from hot-swap inrush ([log](https://hackaday.io/project/164567/log/163546-nearing-completion)); most badges have none.

Our design rule from these sources: see [POWER.md](../../POWER.md).
