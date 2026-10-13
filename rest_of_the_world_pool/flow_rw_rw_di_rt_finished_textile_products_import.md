---
layout: default
title: Finished textile products import
parent: Rest of the world (RW.RW)
grand_parent: 1. Rest of the world (RW)
nav_order: 3
---

# Finished textile products import

| | |
|---|---|
| Flytkode | `RW.RW-DI.RT-Finished textile products import-TOT` |
| Fra | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Til | [Wholesale and retail (DI.RT)](../distribution_pool/subpool_di_rt.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | data |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | SSB 08801 (HS 61, 62, 63, 64, 57; retail yarn 5109, 5207, 520420, 5406, 5511; bedding 9404.30, 9404.40, 9404.90) |
| Merknad | Net weight as declared; includes non-textile parts (buttons/zips/soles). Retail yarn is product YA |

## Tidsserie

<iframe src="../output_files/plots/pages/rw_rw_di_rt_finished_textile_products_import.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 77.55 | 74.94 – 80.34 |
| 2000 | 104.95 | 101.42 – 108.72 |
| 2010 | 151.39 | 146.30 – 156.83 |
| 2018 | 147.43 | 142.47 – 152.72 |
| 2022 | 158.40 | 153.07 – 164.09 |
| 2025 | 138.24 | 133.58 – 143.20 |

## Materialsammensetning (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

<iframe src="../output_files/plots/pages/rw_rw_di_rt_finished_textile_products_import_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_finished_products_import_mc` i [calculations/rw_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/rw_mc.py#L19). Dokumentasjonen i koden:

> Registered imports of finished goods, SSB 08801.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
