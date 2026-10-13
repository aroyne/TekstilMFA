---
layout: default
title: Fibre and yarn import
parent: Rest of the world (RW.RW)
grand_parent: 1. Rest of the world (RW)
nav_order: 1
---

# Fibre and yarn import

| | |
|---|---|
| Flytkode | `RW.RW-MA.FI-Fibre and yarn import-TOT` |
| Fra | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Til | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Tekstilform | FIB – fibre og garn |
| Dimensjoner | år |
| Metode | data |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | SSB 08801 (HS 50-55 fibre and yarn; woven fabric and retail yarn excluded) |
| Merknad | HS 56, high-tenacity filament yarn (5402.10/11/19/20), nylon net twine (5402.61), other single synthetic filament yarn (5402.49) and polypropylene staple fibre (5503.40) are outside the scope: they go to ropes, nets, nonwovens and technical products. Retail yarn goes to DI.RT as product YA |

## Tidsserie

<iframe src="../output_files/plots/pages/rw_rw_ma_fi_fibre_and_yarn_import.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 14.29 | 13.81 – 14.80 |
| 2000 | 11.82 | 11.42 – 12.24 |
| 2010 | 6.29 | 6.08 – 6.52 |
| 2018 | 5.83 | 5.63 – 6.04 |
| 2022 | 5.93 | 5.73 – 6.14 |
| 2025 | 6.17 | 5.96 – 6.39 |

## Materialsammensetning (fiberlag, D19)

Råull er ull (uvasket ull regnes som ull, inkludert fettet, så vaskesvinnet er også ull). Fiber og garn i handelen har hovedfiberen fra HS-koden. Norsk spunnet håndstrikkegarn er ull. Metervare har hovedfiberen fra HS-koden. Garn til MA.TX er balansen per materiale, klippet til 0. Produksjonsavfall har blandingen av garn og metervare inn i MA.TX, og ferdigvarer til DI.RT resten av MA.TX per materiale.

<iframe src="../output_files/plots/pages/rw_rw_ma_fi_fibre_and_yarn_import_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_fibre_and_yarn_import_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L64). Dokumentasjonen i koden:

> Registered imports of fibre and yarn, SSB 08801 (HS 50-55 except woven
> fabric and retail yarn). Includes raw, scoured and carbonised wool and
> tops returning after scouring abroad.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
