# Hardware

The **Tiiny z01** (released 01/2026) is a compact local-inference box built around a CIX
"sky1"-class SoC with a discrete NPU.

## Official spec

| | |
|---|---|
| Model | Tiiny z01 |
| CPU | ARMv9.2, 12 cores |
| GPU / NPU | published as **160 BF16 TOPS / 190 INT8 TOPS** |
| RAM | **80 GB total** = 32 GB SoC (≈102 GB/s) + 48 GB on the discrete NPU (≈154 GB/s); ≈33 GB usable for a model |
| Storage | 1 TB |
| Networking | Wi-Fi + Bluetooth; USB-C acts as an RNDIS / USB-Ethernet gadget |
| OS | TiinyOS (firmware 0.1.30+) |

## Teardown / internals (community)

Confirmed by community teardowns and `uname`/`lscpu`-style inspection from inside a container:

- **Board:** CIX "sky1" (P1-class) SoC.
- **CPU:** 8× Cortex-A720 + 4× Cortex-A520 (big.LITTLE, 12 cores total).
- **NPU:** **Houmo LQ50-48GB**, a discrete accelerator on **PCIe 4.0 ×4** with its own 48 GB of
  high-bandwidth memory — this is where large models actually run.
- **Wi-Fi:** MediaTek MT7922.
- **OS stack:** Debian 12, Linux 6.6, Docker 27.
- **Storage:** the `/data` partition is **LUKS-encrypted**; it is unlocked at boot.

## Why the memory split matters

The 80 GB headline is two pools: 32 GB attached to the SoC and 48 GB attached to the NPU. A model
that must live entirely on the NPU (e.g. a 120B-class MoE) needs the 48 GB NPU pool to itself, so you
cannot keep other large models loaded alongside it. Small models and the SoC pool coexist fine.

## Inference engine

The on-device engine is **PowerInfer** (SJTU-IPADS / Tiiny-AI fork), which is what exposes the model
ports internally and schedules work onto the NPU.
