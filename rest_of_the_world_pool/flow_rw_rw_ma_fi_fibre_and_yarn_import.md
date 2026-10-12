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
| Merknad | HS 56 (nonwovens, ropes, nets) and high-tenacity filament yarn (5402.10/11/19/20, for ropes and nets) are outside the scope. Retail yarn goes to DI.RT as product YA |

## Tidsserie

<iframe src="../output_files/plots/pages/rw_rw_ma_fi_fibre_and_yarn_import.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 15.43 | 15.04 – 15.75 |
| 2000 | 12.33 | 12.02 – 12.58 |
| 2010 | 7.05 | 6.87 – 7.19 |
| 2018 | 8.03 | 7.83 – 8.20 |
| 2022 | 7.58 | 7.39 – 7.73 |
| 2025 | 7.14 | 6.96 – 7.29 |

## Materialsammensetning (fiberlag, D19)

Råull er ull (uvasket ull regnes som ull, inkludert fettet, så vaskesvinnet er også ull). Fiber og garn i handelen har hovedfiberen fra HS-koden. Norsk spunnet håndstrikkegarn er ull. Garn til MA.TX er balansen per materiale, klippet til 0 (eksportens sammensetning tar opp differansen).

<iframe src="../output_files/plots/pages/rw_rw_ma_fi_fibre_and_yarn_import_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_fibre_and_yarn_import_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L46). Dokumentasjonen i koden:

> Registered imports of fibre and yarn, SSB 08801 (HS 50-55 except woven
> fabric and retail yarn). Includes raw, scoured and carbonised wool and
> tops returning after scouring abroad.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
