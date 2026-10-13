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
| 1990 | 0.03 | 0.01 – 0.04 |
| 2000 | 0.15 | 0.08 – 0.27 |
| 2010 | 0.33 | 0.18 – 0.59 |
| 2018 | 0.65 | 0.35 – 1.16 |
| 2022 | 0.77 | 0.46 – 1.13 |
| 2025 | 1.51 | 0.82 – 2.28 |

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- *Ikke skrevet ennå.*

#### Datakilder (og hvordan kildetallene er produsert)

- *Ikke skrevet ennå.*

#### Antakelser

- *Ikke skrevet ennå.*

#### Sammensetning (varetype og materiale)

- *Ikke skrevet ennå.*

#### Tidsutvikling og sammenligninger

- *Ikke skrevet ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Klær, hjemmetekstiler og sko | 100 % | 100 % | 100 % | 100 % | 100 % | 100 % |

### Materiale (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For andre produkter: tilførselssammensetningen samme år.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 46 % | 48 % | 44 % | 40 % | 37 % | 36 % |
| Regenerert cellulose | 3 % | 2 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 17 % | 16 % | 18 % | 17 % | 17 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 2 % |
| Syntetisk | 27 % | 26 % | 30 % | 33 % | 36 % | 37 % |
| Ull | 6 % | 6 % | 5 % | 5 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/co_re_us_hh_secondhand_sales_to_households_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_secondhand_sales_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L59). Dokumentasjonen i koden:

> Balance of CO.RE: everything sorted for second-hand sale is sold.
