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
| 1990 | 61.87 | 59.04 – 64.57 |
| 2000 | 80.56 | 76.89 – 84.11 |
| 2010 | 116.13 | 110.87 – 121.24 |
| 2018 | 108.05 | 103.17 – 112.80 |
| 2022 | 114.03 | 108.86 – 119.05 |
| 2025 | 98.17 | 93.72 – 102.49 |

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

## Materialsammensetning (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). For garn i detaljsalg blandes norsk spunnet håndstrikkegarn (ull) inn i flytene ut av DI.RT.

<iframe src="../output_files/plots/pages/di_rt_us_hh_sales_to_households_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_sales_to_users_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L27). Dokumentasjonen i koden:

> Balance of DI.RT per product: registered imports plus hand knitting yarn
> spun in Norway minus exports, split between households and
> institutions/businesses. Sacks (SA) are packaging
> used by businesses (D13) and go entirely to US.IC; retail yarn (YA) goes
> entirely to households. Other domestic manufacturing (MA.TX) and unsold
> goods are not yet included. A negative balance is not physical and is
> clipped at 0; the clipped mass is recorded and reported on the flow
> pages.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
