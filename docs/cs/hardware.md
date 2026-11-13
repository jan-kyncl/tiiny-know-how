# Hardware

**Tiiny z01** (vydán 01/2026) je kompaktní box pro lokální inferenci postavený na SoC třídy CIX
„sky1“ s diskrétním NPU.

## Oficiální specifikace

| | |
|---|---|
| Model | Tiiny z01 |
| CPU | ARMv9.2, 12 jader |
| GPU / NPU | uváděno jako **160 BF16 TOPS / 190 INT8 TOPS** |
| RAM | **80 GB celkem** = 32 GB SoC (≈102 GB/s) + 48 GB na diskrétním NPU (≈154 GB/s); ≈33 GB využitelných pro model |
| Úložiště | 1 TB |
| Síť | Wi-Fi + Bluetooth; USB-C jako RNDIS / USB-Ethernet gadget |
| OS | TiinyOS (firmware 0.1.30+) |

## Rozbor / vnitřek (komunita)

Potvrzeno komunitními rozbory a inspekcí (`uname`/`lscpu`) zevnitř kontejneru:

- **Deska:** SoC CIX „sky1“ (třída P1).
- **CPU:** 8× Cortex-A720 + 4× Cortex-A520 (big.LITTLE, celkem 12 jader).
- **NPU:** **Houmo LQ50-48GB**, diskrétní akcelerátor na **PCIe 4.0 ×4** s vlastními 48 GB rychlé
  paměti — tady reálně běží velké modely.
- **Wi-Fi:** MediaTek MT7922.
- **OS stack:** Debian 12, Linux 6.6, Docker 27.
- **Úložiště:** oddíl `/data` je **šifrovaný LUKS**; odemyká se při startu.

## Proč je rozdělení paměti důležité

Oněch 80 GB jsou dva zdroje: 32 GB u SoC a 48 GB u NPU. Model, který se musí celý vejít na NPU (např.
MoE třídy 120B), potřebuje celý 48GB NPU zdroj sám pro sebe, takže vedle něj neudržíš další velké
modely. Malé modely a SoC zdroj koexistují v pohodě.

## Inferenční engine

Engine v zařízení je **PowerInfer** (fork SJTU-IPADS / Tiiny-AI), ten interně vystavuje porty modelů a
plánuje výpočet na NPU.
