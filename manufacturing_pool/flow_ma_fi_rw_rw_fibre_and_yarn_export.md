---
layout: default
title: Fibre and yarn export
parent: Fibre and yarn production (MA.FI)
grand_parent: 3. Manufacturing (MA)
nav_order: 3
---

# Fibre and yarn export

| | |
|---|---|
| Flytkode | `MA.FI-RW.RW-Fibre and yarn export-TOT` |
| Fra | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Til | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Tekstilform | FIB – fibre og garn |
| Dimensjoner | år |
| Metode | data |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | SSB 08801 (HS 50-55 fibre and yarn export, incl. greasy wool 5101; high-tenacity filament yarn excluded) |
| Merknad | Greasy wool is 90-100 % of Norwegian wool since 2007. Yarn export may include re-export of yarn spun abroad |

## Tidsserie

<iframe src="../output_files/plots/pages/ma_fi_rw_rw_fibre_and_yarn_export.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 5.32 | 5.19 – 5.43 |
| 2000 | 5.17 | 5.04 – 5.28 |
| 2010 | 4.63 | 4.52 – 4.73 |
| 2018 | 4.06 | 3.96 – 4.15 |
| 2022 | 3.25 | 3.16 – 3.31 |
| 2025 | 3.02 | 2.95 – 3.08 |

## Materialsammensetning (fiberlag, D19)

Råull er ull (uvasket ull regnes som ull, inkludert fettet, så vaskesvinnet er også ull). Fiber og garn i handelen har hovedfiberen fra HS-koden. Norsk spunnet håndstrikkegarn er ull. Garn til MA.TX er balansen per materiale, klippet til 0 (eksportens sammensetning tar opp differansen).

<iframe src="../output_files/plots/pages/ma_fi_rw_rw_fibre_and_yarn_export_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_fibre_and_yarn_export_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L56). Dokumentasjonen i koden:

> Registered exports of fibre and yarn, SSB 08801 (HS 50-55 except woven
> fabric and retail yarn). Dominated by greasy Norwegian wool (HS 5101.11
> and 5101.19), which since 2007 is 90-100 % of Norwegian wool. Yarn
> exports may include re-export of yarn spun abroad for Norwegian brands,
> which the trade statistics do not separate from domestic production.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
