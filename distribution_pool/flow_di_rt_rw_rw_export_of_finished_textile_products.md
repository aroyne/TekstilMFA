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

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **DI.RT-RW.RW-Export of finished textile products-TOT** er registrert eksport av ferdige tekstilvarer og garn i detaljopplegg, med samme varetyper som importen.
- Flyten omfatter både gjeneksport (importerte varer, også returer fra netthandel) og eksport av varer laget i Norge (D6).

#### Datakilder (og hvordan kildetallene er produsert)

- SSB tabell 08801, nettovekt i kg (se RW.RW-DI.RT-Finished textile products import-TOT).

#### Antakelser

- All eksport av ferdigvarer føres fra DI.RT, fordi handelsstatistikken ikke skiller gjeneksport fra norsk produksjon. Eksport av metervare føres fra MA.TX.
- Overstiger eksporten det DI.RT har av en varetype, klippes salget til 0 (se DI.RT-US.HH-Sales to households-TOT). Det har ikke skjedd.

#### Sammensetning (varetype og materiale)

- Hjemmetekstiler økte fra 23 % i 1990 til 38 % i 2022, blant annet dyner og puter. Klær er 28–32 %, sko falt fra 18 % til 10 %, og garn i detaljopplegg er 10–11 %.
- Materialet er blandingen av det som går inn i DI.RT (import, norske ferdigvarer og norsk håndstrikkegarn) per varetype.

#### Tidsutvikling og sammenligninger

- Eksporten økte fra 4,5 kt i 1988 til 13,0 kt i 2025, og veksten har vært raskest etter 2015.
- Eksport av garn i detaljopplegg økte fra 0,7 kt i 2018 til 2,1 kt i 2025.
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
