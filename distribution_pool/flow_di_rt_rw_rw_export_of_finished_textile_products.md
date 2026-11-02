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

## Med og uten sekker

Sekker (SA) er emballasje (D13) og kan dominere flyten. Kt per år, median med 95 %-intervall i parentes. Summen uten sekker er regnet per iterasjon.

| År | I alt | Sekker | Uten sekker | Sekkenes andel |
|---|---|---|---|---|
| 1990 | 4.59 (4.26–4.90) | 0.12 (0.11–0.12) | 4.47 (4.15–4.77) | 3 % |
| 2000 | 6.54 (6.03–7.02) | 0.08 (0.08–0.09) | 6.46 (5.95–6.93) | 1 % |
| 2010 | 7.01 (6.49–7.55) | 0.05 (0.05–0.06) | 6.96 (6.44–7.49) | 1 % |
| 2018 | 9.69 (9.00–10.47) | 0.33 (0.30–0.35) | 9.36 (8.69–10.11) | 3 % |
| 2022 | 12.32 (11.42–13.22) | 0.60 (0.56–0.65) | 11.72 (10.86–12.57) | 5 % |
| 2025 | 13.11 (12.14–14.03) | 0.15 (0.14–0.16) | 12.96 (12.00–13.87) | 1 % |

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
| Ikke-tekstil | 19 % | 15 % | 14 % | 12 % | 15 % | 14 % |
| Andre fibre | 1 % | 3 % | 2 % | 3 % | 3 % | 2 % |
| Syntetisk | 27 % | 30 % | 34 % | 41 % | 39 % | 34 % |
| Ull | 9 % | 7 % | 9 % | 10 % | 13 % | 16 % |

<iframe src="../output_files/plots/pages/di_rt_rw_rw_export_of_finished_textile_products_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `08801:export:finished` | 53 % | 53 % | 53 % |
| `08801_classification:export:finished` | 47 % | 47 % | 47 % |
| Halvt 95 %-intervall, førsteordens (kt) | 0.45 | 0.48 | 0.90 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 0.49 | 0.53 | 0.94 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_finished_products_export_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L64). Dokumentasjonen i koden:

> Registered exports of finished goods, SSB 08801. Export from DI.RT covers
> both re-export and export of domestically manufactured products (D6).
