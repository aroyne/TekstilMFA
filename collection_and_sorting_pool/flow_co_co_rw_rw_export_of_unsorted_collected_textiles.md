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

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 1.40 | 1.35 – 1.45 |
| 2000 | 8.46 | 8.17 – 8.77 |
| 2010 | 18.56 | 17.90 – 19.22 |
| 2018 | 36.46 | 35.17 – 37.76 |
| 2022 | 31.64 | 30.52 – 32.77 |
| 2025 | 34.33 | 33.11 – 35.55 |

## Materialsammensetning (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For andre produkter: tilførselssammensetningen samme år.

<iframe src="../output_files/plots/pages/co_co_rw_rw_export_of_unsorted_collected_textiles_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_export_unsorted_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L24). Dokumentasjonen i koden:

> Export of used textiles and rags (HS 6309+6310), SSB 08801.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
