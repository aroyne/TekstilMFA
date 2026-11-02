---
layout: default
title: Sales to institutions and businesses
parent: Wholesale and retail (DI.RT)
grand_parent: 4. Distribution (DI)
nav_order: 2
---

# Sales to institutions and businesses

| | |
|---|---|
| Flytkode | `DI.RT-US.IC-Sales to institutions and businesses-TOT` |
| Fra | [Wholesale and retail (DI.RT)](../distribution_pool/subpool_di_rt.html) |
| Til | [Institutions and businesses (US.IC)](../use_pool/subpool_us_ic.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | parameter |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | Share of workwear/linen in supply; public procurement data (Doffin/DFØ); industry reports |
| Merknad | – |

## Tidsserie

<iframe src="../output_files/plots/pages/di_rt_us_ic_sales_to_institutions_and_businesses.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **DI.RT-US.IC-Sales to institutions and businesses-TOT** er tekstilvarer brukt av bedrifter og offentlig sektor: arbeidsklær, uniformer, sengetøy og håndklær i hoteller og sykehus, tepper i bygg, presenninger og sekker til emballasje.

#### Datakilder (og hvordan kildetallene er produsert)

- Det finnes ingen norsk statistikk over denne fordelingen. Andelen er hentet fra Watson m.fl. (2020) og Rubach m.fl. (2023), som bruker den danske fordelingen 88/12, og kontrollert mot Nederland (omtrent 8 % arbeidsklær, Xu m.fl. 2024).

#### Antakelser

- 12 % (4–15 %, flat fordeling fordi andelen er et ekspertanslag; MC-medianen blir derfor ca. 9,5 %) av tilførselen av klær, hjemmetekstiler, sko, tepper, presenninger og andre konfeksjonerte varer. Sekker (SA) er emballasje og går helt hit (D13), og garn i detaljopplegg går ikke hit.
- Samme andel i alle år.

#### Sammensetning (varetype og materiale)

- Sekker økte fra 21 % i 1990 til 45 % i 2022. Klær er 24–33 %.
- Materialet er blandingen av det som går inn i DI.RT. Syntetisk er 46–67 %, på grunn av sekker og storsekker av polypropylen.

#### Tidsutvikling og sammenligninger

- Flyten økte fra 13 kt i 1990 til 28–31 kt i 2018–2025, mest på grunn av importen av sekker.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Med og uten sekker

Sekker (SA) er emballasje (D13) og kan dominere flyten. Kt per år, median med 95 %-intervall i parentes. Summen uten sekker er regnet per iterasjon.

| År | I alt | Sekker | Uten sekker | Sekkenes andel |
|---|---|---|---|---|
| 1990 | 10.98 (6.49–15.70) | 2.76 (2.55–2.97) | 8.23 (3.71–12.86) | 25 % |
| 2000 | 16.45 (10.98–22.03) | 6.47 (6.00–6.95) | 9.95 (4.52–15.43) | 39 % |
| 2010 | 21.70 (14.49–29.54) | 8.45 (7.82–9.09) | 13.30 (6.01–20.90) | 39 % |
| 2018 | 25.06 (18.09–32.70) | 12.50 (11.64–13.55) | 12.55 (5.70–19.77) | 50 % |
| 2022 | 27.19 (19.75–35.32) | 13.90 (12.88–14.98) | 13.32 (5.98–20.76) | 51 % |
| 2025 | 24.34 (17.97–31.33) | 13.16 (12.23–14.19) | 11.21 (5.07–17.70) | 54 % |

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 15 % | 7 % | 6 % | 6 % | 6 % | 6 % |
| Klær | 31 % | 30 % | 30 % | 22 % | 22 % | 20 % |
| Sko | 10 % | 8 % | 8 % | 7 % | 6 % | 6 % |
| Hjemmetekstiler | 13 % | 11 % | 12 % | 10 % | 8 % | 7 % |
| Andre konfeksjonerte varer | 2 % | 2 % | 2 % | 3 % | 3 % | 4 % |
| Sekker | 25 % | 39 % | 39 % | 50 % | 51 % | 54 % |
| Presenninger og telt | 4 % | 3 % | 3 % | 4 % | 4 % | 3 % |

### Materiale (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 30 % | 24 % | 23 % | 15 % | 15 % | 14 % |
| Regenerert cellulose | 2 % | 2 % | 1 % | 1 % | 1 % | 1 % |
| Ikke-tekstil | 14 % | 11 % | 12 % | 11 % | 10 % | 9 % |
| Andre fibre | 3 % | 2 % | 3 % | 2 % | 3 % | 2 % |
| Syntetisk | 48 % | 57 % | 58 % | 68 % | 69 % | 71 % |
| Ull | 3 % | 3 % | 3 % | 2 % | 2 % | 2 % |

<iframe src="../output_files/plots/pages/di_rt_us_ic_sales_to_institutions_and_businesses_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `institutional_share` | 94 % | 94 % | 91 % |
| `08801:import:finished` | 3 % | 3 % | 5 % |
| `08801_classification:import:finished` | 2 % | 2 % | 4 % |
| `unsold_destroyed_share` | 1 % | 1 % | – |
| Halvt 95 %-intervall, førsteordens (kt) | 5.67 | 7.61 | 6.50 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 5.52 | 7.53 | 6.68 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

## Beregning i koden

Beregnes i `_sales_to_users_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L90). Dokumentasjonen i koden:

> Balance of DI.RT per product: registered imports plus finished goods
> and hand knitting yarn made in Norway minus exports and unsold goods,
> split between households and institutions/businesses. Sacks (SA) are packaging
> used by businesses (D13) and go entirely to US.IC; retail yarn (YA) goes
> entirely to households. The institutional share of the other products is
> 12 % (4-15 %), the Danish split used by Watson et al. 2020 and Rubach et
> al. 2023; no Norwegian statistic gives it. The lower bound is the share
> of clothing imported directly by businesses and the public sector outside
> wholesale and retail, 3-4 % of the import value in 2016-2024 (Eurostat
> ext_tec05, D36); the rest of their purchases goes through wholesale and
> cannot be separated. A negative balance is not physical and is
> clipped at 0; the clipped mass is recorded and reported on the flow
> pages.
