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
| 1990 | 60.53 | 57.87 – 63.40 |
| 2000 | 79.35 | 75.85 – 83.10 |
| 2010 | 114.32 | 109.29 – 119.73 |
| 2018 | 105.78 | 101.12 – 110.79 |
| 2022 | 112.49 | 107.54 – 117.81 |
| 2025 | 96.71 | 92.45 – 101.29 |

## Materialsammensetning (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden).

<iframe src="../output_files/plots/pages/di_rt_us_hh_sales_to_households_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_sales_to_users_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L26). Dokumentasjonen i koden:

> Balance of DI.RT per product: registered imports minus exports, split
> between households and institutions/businesses. Sacks (SA) are packaging
> used by businesses (D13) and go entirely to US.IC. Domestic manufacturing
> (MA.TX) and unsold goods are not yet included.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
