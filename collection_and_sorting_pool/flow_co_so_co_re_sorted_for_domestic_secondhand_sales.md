---
layout: default
title: Sorted for domestic secondhand sales
parent: Sorting (CO.SO)
grand_parent: 6. Collection and sorting (CO)
nav_order: 1
---

# Sorted for domestic secondhand sales

| | |
|---|---|
| Flytkode | `CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT` |
| Fra | [Sorting (CO.SO)](../collection_and_sorting_pool/subpool_co_so.html) |
| Til | [Second-hand retail (CO.RE)](../collection_and_sorting_pool/subpool_co_re.html) |
| Tekstilform | USE – brukte, ombrukbare |
| Dimensjoner | år × produktgruppe |
| Metode | data |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Collector annual reports |
| Merknad | – |

## Tidsserie

<iframe src="../output_files/plots/pages/co_so_co_re_sorted_for_domestic_secondhand_sales.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

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

<iframe src="../output_files/plots/pages/co_so_co_re_sorted_for_domestic_secondhand_sales_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_sorted_for_secondhand_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L41). Dokumentasjonen i koden:

> Share of the retained textiles sold second-hand in Norway (same anchors).
