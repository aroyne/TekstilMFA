---
layout: default
title: Export of unsorted collected textiles
parent: Separate collection (CO.CO)
grand_parent: 6. Collection and sorting (CO)
nav_order: 1
---

# Export of unsorted collected textiles

| | |
|---|---|
| Flytkode | `CO.CO-RW.RW-Export of unsorted collected textiles-TOT` |
| Fra | [Separate collection (CO.CO)](../collection_and_sorting_pool/subpool_co_co.html) |
| Til | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Tekstilform | MIX – brukte, usortert |
| Dimensjoner | år × produktgruppe |
| Metode | data |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | SSB 08801 (HS 6309/6310 export); collector reports; NORSUS 2023 (about 85 % exported) |
| Merknad | HS 6309 export may also contain sorted grades - split needed |

## Tidsserie

<iframe src="../output_files/plots/pages/co_co_rw_rw_export_of_unsorted_collected_textiles.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

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

<iframe src="../output_files/plots/pages/co_co_rw_rw_export_of_unsorted_collected_textiles_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_export_unsorted_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L24). Dokumentasjonen i koden:

> Export of used textiles and rags (HS 6309+6310), SSB 08801.
