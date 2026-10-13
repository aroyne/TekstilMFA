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
| Kandidatdata | SSB 08801 (HS 61, 62, 63, 64, 57, 9404.30/40/90 and retail yarn export) |
| Merknad | Includes re-export and returns from online sales, and retail yarn spun in Norway |

## Tidsserie

<iframe src="../output_files/plots/pages/di_rt_rw_rw_export_of_finished_textile_products.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 4.57 | 4.41 – 4.73 |
| 2000 | 6.51 | 6.29 – 6.74 |
| 2010 | 6.99 | 6.75 – 7.24 |
| 2018 | 9.68 | 9.36 – 10.03 |
| 2022 | 12.31 | 11.90 – 12.75 |
| 2025 | 13.02 | 12.59 – 13.49 |

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
| Tepper | 3 % | 5 % | 1 % | 2 % | 1 % | 2 % |
| Klær | 32 % | 29 % | 37 % | 28 % | 28 % | 30 % |
| Sko | 18 % | 11 % | 9 % | 5 % | 10 % | 10 % |
| Hjemmetekstiler | 23 % | 39 % | 37 % | 47 % | 38 % | 33 % |
| Andre konfeksjonerte varer | 7 % | 3 % | 2 % | 3 % | 4 % | 3 % |
| Sekker | 3 % | 1 % | 1 % | 3 % | 5 % | 1 % |
| Presenninger og telt | 4 % | 9 % | 7 % | 5 % | 4 % | 5 % |
| Garn i detaljsalg | 10 % | 4 % | 7 % | 8 % | 11 % | 16 % |

### Materiale (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 41 % | 42 % | 39 % | 31 % | 29 % | 31 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 1 % | 1 % |
| Ikke-tekstil | 18 % | 15 % | 14 % | 11 % | 14 % | 14 % |
| Andre fibre | 1 % | 3 % | 2 % | 3 % | 3 % | 2 % |
| Syntetisk | 28 % | 31 % | 35 % | 42 % | 40 % | 35 % |
| Ull | 9 % | 7 % | 9 % | 11 % | 13 % | 16 % |

<iframe src="../output_files/plots/pages/di_rt_rw_rw_export_of_finished_textile_products_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_finished_products_export_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L18). Dokumentasjonen i koden:

> Registered exports of finished goods, SSB 08801. Export from DI.RT covers
> both re-export and export of domestically manufactured products (D6).
