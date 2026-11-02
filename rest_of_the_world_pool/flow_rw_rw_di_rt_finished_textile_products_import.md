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

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **RW.RW-DI.RT-Finished textile products import-TOT** er registrert import av ferdige tekstilvarer til handelen: klær (HS 61, 62), hjemmetekstiler (6301–6304, dyner, puter og møbelputer i 9404.40/9404.90), sko (64), tepper (57), sekker (6305), presenninger, telt og soveposer (6306, 9404.30), andre konfeksjonerte varer (6307, 6308) og garn i detaljopplegg (YA).
- Privatimport på dagsturer og direkte netthandel i lavverdisendinger er egne flyter (RW.RW-US.HH-Private imports-TOT og RW.RW-US.HH-Direct online imports-TOT).

#### Datakilder (og hvordan kildetallene er produsert)

- SSB tabell 08801, utenrikshandel med varer etter varenummer (HS8) og land, nettovekt i kg. 1988–2022 fra den fulle 08801-fila i NitrogenBudsjett og 2023–2025 fra SSBs API.
- Handelsstatistikken bygger på tolldeklarasjoner. Nettovekten er varens vekt uten emballasje, men med knapper, glidelåser, såler og annet ikke-tekstil.
- Lavverdisendinger under VOEC og næringslivets varelinjer under 1 000 kr er ikke med under HS-kodene (D7, D14).

#### Antakelser

- HS-kodene kobles til varetyper i `parameters/hs_mapping.csv`, der den lengste prefiksen gjelder.
- Datasettusikkerhet ±5 % (plassholder), fullt korrelert mellom år og flyter fra 08801.

#### Sammensetning (varetype og materiale)

- Klær er omtrent 40 % av massen hele perioden. Tepper falt fra 22 % i 1990 til 10 % i 2022, mens sekker, presenninger og andre konfeksjonerte varer økte.
- Materialet er hovedfiberen i HS-koden. Koder uten fiber fordeles etter `parameters/fibre_composition.csv`, og ikke-tekstil (NT) legges til med andelen per varetype (sko 80 %). Møbelputer er NT som helhet. Bomull falt fra 37 % i 1990 til 28 % i 2022, og syntetisk økte fra 34 % til 46 %.

#### Tidsutvikling og sammenligninger

- Importen økte fra 76–79 kt rundt 1990 til 136 kt i 2005 og var høyest i 2022 med 158 kt. I 2025 var den 138 kt.
- Klesimporten falt i 2023, mest fra Kina. Omtrent en tredjedel av fallet forklares av økt direkte netthandel via VOEC.
- For klær, hjemmetekstiler og sko gir modellen 105,9 kt tilført markedet i 2022 (salg, privatimport og netthandel), det samme som NORSUS (Rubach m.fl. 2023).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Med og uten sekker

Sekker (SA) er emballasje (D13) og kan dominere flyten. Kt per år, median med 95 %-intervall i parentes. Summen uten sekker er regnet per iterasjon.

| År | I alt | Sekker | Uten sekker | Sekkenes andel |
|---|---|---|---|---|
| 1990 | 77.68 (71.99–83.56) | 2.87 (2.66–3.09) | 74.81 (69.33–80.47) | 4 % |
| 2000 | 105.16 (97.61–112.76) | 6.55 (6.08–7.03) | 98.60 (91.53–105.73) | 6 % |
| 2010 | 151.40 (140.28–162.99) | 8.50 (7.87–9.15) | 142.91 (132.41–153.84) | 6 % |
| 2018 | 147.16 (137.36–159.31) | 12.82 (11.97–13.88) | 134.34 (125.39–145.43) | 9 % |
| 2022 | 158.41 (147.36–170.46) | 14.49 (13.48–15.60) | 143.92 (133.88–154.87) | 9 % |
| 2025 | 138.21 (128.45–148.96) | 13.31 (12.37–14.34) | 124.90 (116.08–134.61) | 10 % |

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 22 % | 11 % | 9 % | 10 % | 10 % | 11 % |
| Klær | 43 % | 49 % | 47 % | 41 % | 40 % | 40 % |
| Sko | 16 % | 14 % | 13 % | 12 % | 12 % | 12 % |
| Hjemmetekstiler | 12 % | 15 % | 17 % | 17 % | 15 % | 14 % |
| Andre konfeksjonerte varer | 1 % | 3 % | 3 % | 5 % | 6 % | 8 % |
| Sekker | 4 % | 6 % | 6 % | 9 % | 9 % | 10 % |
| Presenninger og telt | 1 % | 2 % | 4 % | 5 % | 6 % | 4 % |
| Garn i detaljsalg | 1 % | 0 % | 1 % | 2 % | 1 % | 2 % |

### Materiale (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 35 % | 35 % | 35 % | 28 % | 28 % | 29 % |
| Regenerert cellulose | 1 % | 2 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 22 % | 18 % | 18 % | 18 % | 18 % | 17 % |
| Andre fibre | 2 % | 2 % | 2 % | 2 % | 2 % | 2 % |
| Syntetisk | 35 % | 38 % | 39 % | 45 % | 45 % | 45 % |
| Ull | 3 % | 5 % | 4 % | 5 % | 5 % | 5 % |

<iframe src="../output_files/plots/pages/rw_rw_di_rt_finished_textile_products_import_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `08801:import:finished` | 53 % | 53 % | 53 % |
| `08801_classification:import:finished` | 47 % | 47 % | 47 % |
| Halvt 95 %-intervall, førsteordens (kt) | 7.25 | 10.45 | 9.54 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 7.57 | 11.36 | 10.25 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_finished_products_import_mc` i [calculations/rw_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/rw_mc.py#L19). Dokumentasjonen i koden:

> Registered imports of finished goods, SSB 08801.
