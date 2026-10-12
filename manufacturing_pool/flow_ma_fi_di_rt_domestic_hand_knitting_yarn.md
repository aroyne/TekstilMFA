---
layout: default
title: Domestic hand knitting yarn
parent: Fibre and yarn production (MA.FI)
grand_parent: 3. Manufacturing (MA)
nav_order: 2
---

# Domestic hand knitting yarn

| | |
|---|---|
| Flytkode | `MA.FI-DI.RT-Domestic hand knitting yarn-TOT` |
| Fra | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Til | [Wholesale and retail (DI.RT)](../distribution_pool/subpool_di_rt.html) |
| Tekstilform | FIB – fibre og garn |
| Dimensjoner | år × produkt |
| Metode | data |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | SSB Industristatistikk Varetall 1988-1989 (5109.10) and SSB 10455 (Prodcom 13.10.50.50, 2008-2023 with gaps), large units only; SNL (about 1000 t per year); Sandnes Garn (about 600 t) |
| Merknad | Product YA only. Interpolated over 1990-2007, when SSB published no commodity figures. Uncertainty skewed upwards because small units are missing |

## Tidsserie

<iframe src="../output_files/plots/pages/ma_fi_di_rt_domestic_hand_knitting_yarn.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 0.92 | 0.86 – 1.21 |
| 2000 | 0.94 | 0.88 – 1.23 |
| 2010 | 0.78 | 0.73 – 1.02 |
| 2018 | 0.63 | 0.59 – 0.83 |
| 2022 | 0.61 | 0.57 – 0.80 |
| 2025 | 0.71 | 0.67 – 0.94 |

## Materialsammensetning (fiberlag, D19)

Råull er ull (uvasket ull regnes som ull, inkludert fettet, så vaskesvinnet er også ull). Fiber og garn i handelen har hovedfiberen fra HS-koden. Norsk spunnet håndstrikkegarn er ull. Garn til MA.TX er balansen per materiale, klippet til 0 (eksportens sammensetning tar opp differansen).

<iframe src="../output_files/plots/pages/ma_fi_di_rt_domestic_hand_knitting_yarn_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_domestic_hand_knitting_yarn_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L89). Dokumentasjonen i koden:

> Yarn spun in Norway and put up for retail sale (product YA), sold to
> households through retail; hand knitting yarn is by far the largest
> product of the Norwegian spinning mills. Wool yarn put up for retail
> sale produced in large establishments: 0.99 and 0.89 kt in 1988 and 1989
> (SSB Industristatistikk, Varetall, commodity 5109.10), and 0.59-1.03 kt
> in 2008-2023 (SSB 10455, Prodcom 13.10.50.50, sold production). SSB
> published no commodity figures for 1990-2007, and suppresses some
> Prodcom years; those years are interpolated, and the series is held at
> its last value after 2023. Both sources cover large units only (Sandnes
> Garn alone makes about 600 t a year, and SNL gives about 1000 t for all
> Norwegian spinning mills), so the noise factor is skewed upwards. Cotton
> and synthetic yarn put up for retail sale are suppressed in every year
> and are left out.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
