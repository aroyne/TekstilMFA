---
layout: default
title: Secondhand sales to households
parent: Second-hand retail (CO.RE)
grand_parent: 6. Collection and sorting (CO)
nav_order: 1
---

# Secondhand sales to households

| | |
|---|---|
| Flytkode | `CO.RE-US.HH-Secondhand sales to households-TOT` |
| Fra | [Second-hand retail (CO.RE)](../collection_and_sorting_pool/subpool_co_re.html) |
| Til | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Tekstilform | USE – brukte, ombrukbare |
| Dimensjoner | år × produktgruppe |
| Metode | balance |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Balance of CO.RE |
| Merknad | Re-enters the in-use stock |

## Tidsserie

<iframe src="../output_files/plots/pages/co_re_us_hh_secondhand_sales_to_households.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 0.03 | 0.01 – 0.05 |
| 2000 | 0.16 | 0.08 – 0.28 |
| 2010 | 0.35 | 0.19 – 0.60 |
| 2018 | 0.69 | 0.37 – 1.19 |
| 2022 | 0.78 | 0.46 – 1.13 |
| 2025 | 1.50 | 0.85 – 2.31 |

## Materialsammensetning (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For andre produkter: tilførselssammensetningen samme år.

<iframe src="../output_files/plots/pages/co_re_us_hh_secondhand_sales_to_households_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_secondhand_sales_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L59). Dokumentasjonen i koden:

> Balance of CO.RE: everything sorted for second-hand sale is sold.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
