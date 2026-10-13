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
| 1990 | 13.16 | 10.77 – 15.17 |
| 2000 | 19.08 | 16.15 – 21.55 |
| 2010 | 25.38 | 21.48 – 28.70 |
| 2018 | 28.45 | 24.80 – 31.60 |
| 2022 | 30.59 | 26.78 – 33.90 |
| 2025 | 27.28 | 24.03 – 30.10 |

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

## Materialsammensetning (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

<iframe src="../output_files/plots/pages/di_rt_us_ic_sales_to_institutions_and_businesses_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_sales_to_users_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L27). Dokumentasjonen i koden:

> Balance of DI.RT per product: registered imports plus finished goods
> and hand knitting yarn made in Norway minus exports, split between
> households and institutions/businesses. Sacks (SA) are packaging
> used by businesses (D13) and go entirely to US.IC; retail yarn (YA) goes
> entirely to households. Unsold goods are not yet included. A negative
> balance is not physical and is clipped at 0; the clipped mass is recorded and reported on the flow
> pages.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
