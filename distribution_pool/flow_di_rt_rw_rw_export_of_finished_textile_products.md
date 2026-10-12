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
| Kandidatdata | SSB 08801 (HS 61, 62, 63, 64, 57 and retail yarn export) |
| Merknad | Includes re-export and returns from online sales, and retail yarn spun in Norway |

## Tidsserie

<iframe src="../output_files/plots/pages/di_rt_rw_rw_export_of_finished_textile_products.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 3.93 | 3.83 – 4.01 |
| 2000 | 4.46 | 4.35 – 4.55 |
| 2010 | 4.81 | 4.69 – 4.91 |
| 2018 | 5.48 | 5.34 – 5.59 |
| 2022 | 8.05 | 7.85 – 8.22 |
| 2025 | 9.52 | 9.28 – 9.72 |

## Materialsammensetning (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). For garn i detaljsalg blandes norsk spunnet håndstrikkegarn (ull) inn i flytene ut av DI.RT.

<iframe src="../output_files/plots/pages/di_rt_rw_rw_export_of_finished_textile_products_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_finished_products_export_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L17). Dokumentasjonen i koden:

> Registered exports of finished goods, SSB 08801. Export from DI.RT covers
> both re-export and export of domestically manufactured products (D6).
> In a year where exports of a product exceed what DI.RT has, they are
> reduced by the deficit (see _sales_to_users_mc).

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
