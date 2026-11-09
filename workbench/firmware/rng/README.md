# RNG SAO: firmware

Layers (desktop-testable first): `core/` (health tests, conditioner, DRBG), `protocol/` (I2C register map), `platform/` (MCU drivers). Brief: [`planning-design/rng/`](../../../planning-design/rng/README.md).

Also holds the raw-sample capture tool for the go/no-go entropy measurement.
