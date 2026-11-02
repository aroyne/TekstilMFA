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
| 1990 | 11.07 (6.52–15.83) | 2.76 (2.55–2.97) | 8.31 (3.77–12.97) | 25 % |
| 2000 | 16.61 (11.02–22.23) | 6.47 (6.00–6.95) | 10.10 (4.60–15.61) | 39 % |
| 2010 | 21.89 (14.54–29.88) | 8.45 (7.82–9.09) | 13.50 (6.17–21.08) | 39 % |
| 2018 | 25.32 (18.14–32.97) | 12.50 (11.64–13.55) | 12.71 (5.82–19.97) | 49 % |
| 2022 | 27.34 (19.88–35.36) | 13.90 (12.88–14.98) | 13.49 (6.05–20.95) | 51 % |
| 2025 | 24.58 (17.99–31.47) | 13.16 (12.23–14.19) | 11.37 (5.16–17.93) | 54 % |

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 15 % | 7 % | 6 % | 6 % | 5 % | 6 % |
| Klær | 31 % | 30 % | 30 % | 22 % | 22 % | 21 % |
| Sko | 10 % | 8 % | 8 % | 7 % | 6 % | 6 % |
| Hjemmetekstiler | 13 % | 11 % | 12 % | 10 % | 8 % | 7 % |
| Andre konfeksjonerte varer | 2 % | 2 % | 2 % | 3 % | 3 % | 4 % |
| Sekker | 25 % | 39 % | 39 % | 49 % | 51 % | 54 % |
| Presenninger og telt | 4 % | 3 % | 3 % | 4 % | 4 % | 3 % |

### Materiale (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 30 % | 24 % | 23 % | 15 % | 15 % | 14 % |
| Regenerert cellulose | 2 % | 2 % | 1 % | 1 % | 1 % | 1 % |
| Ikke-tekstil | 15 % | 11 % | 12 % | 11 % | 10 % | 10 % |
| Andre fibre | 3 % | 2 % | 3 % | 2 % | 3 % | 2 % |
| Syntetisk | 48 % | 57 % | 58 % | 68 % | 69 % | 71 % |
| Ull | 3 % | 3 % | 3 % | 2 % | 2 % | 2 % |

<iframe src="../output_files/plots/pages/di_rt_us_ic_sales_to_institutions_and_businesses_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `institutional_share` | 95 % | 95 % | 91 % |
| `08801:import:finished` | 3 % | 3 % | 5 % |
| `08801_classification:import:finished` | 2 % | 2 % | 4 % |
| Halvt 95 %-intervall, førsteordens (kt) | 5.71 | 7.66 | 6.54 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 5.61 | 7.67 | 6.74 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

## Beregning i koden

Beregnes i `_sales_to_users_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L73). Dokumentasjonen i koden:

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
