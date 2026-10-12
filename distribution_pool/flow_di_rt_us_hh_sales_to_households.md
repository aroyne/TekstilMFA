---
layout: default
title: Sales to households
parent: Wholesale and retail (DI.RT)
grand_parent: 4. Distribution (DI)
nav_order: 1
---

# Sales to households

| | |
|---|---|
| Flytkode | `DI.RT-US.HH-Sales to households-TOT` |
| Fra | [Wholesale and retail (DI.RT)](../distribution_pool/subpool_di_rt.html) |
| Til | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | balance |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Balance of DI.RT |
| Merknad | Key inflow to the in-use stock |

## Tidsserie

<iframe src="../output_files/plots/pages/di_rt_us_hh_sales_to_households.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 62.13 | 61.04 – 64.01 |
| 2000 | 80.87 | 79.49 – 83.37 |
| 2010 | 116.54 | 114.65 – 120.24 |
| 2018 | 108.44 | 106.70 – 111.88 |
| 2022 | 114.42 | 112.58 – 118.08 |
| 2025 | 98.51 | 96.90 – 101.63 |

## Materialsammensetning (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). For garn i detaljsalg blandes norsk spunnet håndstrikkegarn (ull) inn i flytene ut av DI.RT.

<iframe src="../output_files/plots/pages/di_rt_us_hh_sales_to_households_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_sales_to_users_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L26). Dokumentasjonen i koden:

> Balance of DI.RT per product: registered imports plus hand knitting yarn
> spun in Norway minus exports, split between households and
> institutions/businesses. Sacks (SA) are packaging
> used by businesses (D13) and go entirely to US.IC; retail yarn (YA) goes
> entirely to households. Other domestic manufacturing (MA.TX) and unsold
> goods are not yet included.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
