---
layout: default
title: Export of finished textile products
parent: Wholesale and retail (DI.RT)
grand_parent: 4. Distribution (DI)
nav_order: 3
---

# Export of finished textile products

| | |
|---|---|
| Flytkode | `DI.RT-RW.RW-Export of finished textile products-TOT` |
| Fra | [Wholesale and retail (DI.RT)](../distribution_pool/subpool_di_rt.html) |
| Til | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | data |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | SSB 08801 (HS 61, 62, 6301-6304, 64 export) |
| Merknad | Includes re-export and returns from online sales |

## Tidsserie

<iframe src="../output_files/plots/pages/di_rt_rw_rw_export_of_finished_textile_products.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 3.44 | 3.33 – 3.57 |
| 2000 | 4.17 | 4.03 – 4.32 |
| 2010 | 4.30 | 4.15 – 4.45 |
| 2018 | 4.68 | 4.52 – 4.85 |
| 2022 | 6.63 | 6.41 – 6.87 |
| 2025 | 7.37 | 7.12 – 7.63 |

## Materialsammensetning (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden).

<iframe src="../output_files/plots/pages/di_rt_rw_rw_export_of_finished_textile_products_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_finished_products_export_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L17). Dokumentasjonen i koden:

> Registered exports of finished goods, SSB 08801. Export from DI.RT covers
> both re-export and export of domestically manufactured products (D6).

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
