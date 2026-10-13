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

- 12 % (8–15 %, PERT) av tilførselen av klær, hjemmetekstiler, sko, tepper, presenninger og andre konfeksjonerte varer. Sekker (SA) er emballasje og går helt hit (D13), og garn i detaljopplegg går ikke hit.
- Samme andel i alle år.

#### Sammensetning (varetype og materiale)

- Sekker økte fra 21 % i 1990 til 45 % i 2022. Klær er 24–33 %.
- Materialet er blandingen av det som går inn i DI.RT. Syntetisk er 46–67 %, på grunn av sekker og storsekker av polypropylen.

#### Tidsutvikling og sammenligninger

- Flyten økte fra 13 kt i 1990 til 28–31 kt i 2018–2025, mest på grunn av importen av sekker.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 16 % | 7 % | 7 % | 6 % | 6 % | 6 % |
| Klær | 33 % | 33 % | 33 % | 25 % | 24 % | 23 % |
| Sko | 10 % | 9 % | 9 % | 7 % | 7 % | 6 % |
| Hjemmetekstiler | 14 % | 12 % | 13 % | 11 % | 9 % | 8 % |
| Andre konfeksjonerte varer | 2 % | 2 % | 2 % | 3 % | 4 % | 4 % |
| Sekker | 21 % | 34 % | 33 % | 44 % | 45 % | 48 % |
| Presenninger og telt | 5 % | 3 % | 4 % | 4 % | 4 % | 3 % |

### Materiale (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 32 % | 26 % | 25 % | 16 % | 16 % | 16 % |
| Regenerert cellulose | 2 % | 2 % | 1 % | 2 % | 1 % | 1 % |
| Ikke-tekstil | 15 % | 11 % | 12 % | 11 % | 10 % | 9 % |
| Andre fibre | 3 % | 2 % | 3 % | 2 % | 3 % | 2 % |
| Syntetisk | 46 % | 55 % | 55 % | 66 % | 67 % | 69 % |
| Ull | 3 % | 3 % | 3 % | 3 % | 3 % | 3 % |

<iframe src="../output_files/plots/pages/di_rt_us_ic_sales_to_institutions_and_businesses_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

## Beregning i koden

Beregnes i `_sales_to_users_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L27). Dokumentasjonen i koden:

> Balance of DI.RT per product: registered imports plus finished goods
> and hand knitting yarn made in Norway minus exports, split between
> households and institutions/businesses. Sacks (SA) are packaging
> used by businesses (D13) and go entirely to US.IC; retail yarn (YA) goes
> entirely to households. Unsold goods are not yet included. A negative
> balance is not physical and is clipped at 0; the clipped mass is recorded and reported on the flow
> pages.
