---
layout: default
title: Separate collection from households
parent: Households (US.HH)
grand_parent: 5. Use (US)
nav_order: 1
---

# Separate collection from households

| | |
|---|---|
| Flytkode | `US.HH-CO.CO-Separate collection from households-TOT` |
| Fra | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Til | [Separate collection (CO.CO)](../collection_and_sorting_pool/subpool_co_co.html) |
| Tekstilform | MIX – brukte, usortert |
| Dimensjoner | år × produktgruppe |
| Metode | data |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | SSB 08801 export of HS 6309+6310 (1988-2025) divided by export share anchored in Watson 2020, NORSUS 2023 and NORSUS 2026 |
| Merknad | Anchor years only - interpolation between anchors |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_co_co_separate_collection_from_households.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 1.45 | 1.40 – 1.51 |
| 2000 | 8.75 | 8.42 – 9.09 |
| 2010 | 19.19 | 18.46 – 19.92 |
| 2018 | 37.71 | 36.27 – 39.14 |
| 2022 | 32.58 | 31.38 – 33.77 |
| 2025 | 36.39 | 34.93 – 37.84 |

## Materialsammensetning (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For andre produkter: tilførselssammensetningen samme år.

<iframe src="../output_files/plots/pages/us_hh_co_co_separate_collection_from_households_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_separate_collection_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L25). Dokumentasjonen i koden:

> Separately collected = exported used textiles + the part kept in Norway (D17).

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
