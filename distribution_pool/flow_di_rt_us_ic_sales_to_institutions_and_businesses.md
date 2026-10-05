---
layout: default
title: Sales to institutions and businesses
parent: Wholesale and retail (DI.RT)
grand_parent: 4. Distribution (DI)
nav_order: 2
---

# Sales to institutions and businesses

| | |
|---|---|
| Flytkode | `DI.RT-US.IC-Sales to institutions and businesses-TOT` |
| Fra | [Wholesale and retail (DI.RT)](../distribution_pool/subpool_di_rt.html) |
| Til | [Institutions and businesses (US.IC)](../use_pool/subpool_us_ic.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | parameter |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | Share of workwear/linen in supply; public procurement data (Doffin/DFØ); industry reports |
| Merknad | – |

## Tidsserie

<iframe src="../output_files/plots/pages/di_rt_us_ic_sales_to_institutions_and_businesses.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 10.99 | 9.12 – 12.60 |
| 2000 | 17.25 | 14.80 – 19.42 |
| 2010 | 23.98 | 20.46 – 27.09 |
| 2018 | 26.89 | 23.63 – 29.93 |
| 2022 | 29.17 | 25.70 – 32.41 |
| 2025 | 26.29 | 23.32 – 29.11 |

## Materialsammensetning (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden).

<iframe src="../output_files/plots/pages/di_rt_us_ic_sales_to_institutions_and_businesses_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

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
