---
layout: default
title: Sales to households
parent: Wholesale and retail (DI.RT)
grand_parent: 4. Distribution (DI)
nav_order: 1
---

# Sales to households

| | |
|---|---|
| Flytkode | `DI.RT-US.HH-Sales to households-TOT` |
| Fra | [Wholesale and retail (DI.RT)](../distribution_pool/subpool_di_rt.html) |
| Til | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | balance |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Balance of DI.RT |
| Merknad | Key inflow to the in-use stock |

## Tidsserie

<iframe src="../output_files/plots/pages/di_rt_us_hh_sales_to_households.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **DI.RT-US.HH-Sales to households-TOT** er nye tekstilvarer solgt til private husholdninger gjennom handelen (butikk og norsk netthandel).

#### Datakilder (og hvordan kildetallene er produsert)

- Flyten er balansen i DI.RT og har ingen egen datakilde: import (08801) + norske ferdigvarer (MA.TX) + norsk håndstrikkegarn − eksport (08801), minus salget til institusjoner og bedrifter.

#### Antakelser

- Alt som tilføres handelen, selges samme år. Lager i handelen og usolgte varer er ikke med ennå.
- 12 % av klær, hjemmetekstiler, sko, tepper, presenninger og andre konfeksjonerte varer går til institusjoner og bedrifter. Sekker går bare dit, og garn i detaljopplegg bare til husholdningene.
- En negativ balanse er ikke-fysisk og klippes til 0. Det har ikke skjedd.

#### Sammensetning (varetype og materiale)

- Klær er 41–44 %, hjemmetekstiler 17 % og sko 13 %. Tepper falt fra 20 % i 1990 til 11 % i 2022.
- Materialet er blandingen av det som går inn i DI.RT per varetype. Syntetisk økte fra 32 % i 1990 til 42 % i 2022.

#### Tidsutvikling og sammenligninger

- Salget økte fra 76–81 kt rundt 1990 til 116 kt i 2005 og har ligget på 106–131 kt siden (høyest i 2011).
- Fallet til 107 kt i 2025 følger fallet i klesimporten etter 2023, men en del av det er erstattet av direkte netthandel.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 20 % | 11 % | 10 % | 11 % | 11 % | 12 % |
| Klær | 41 % | 49 % | 48 % | 43 % | 44 % | 44 % |
| Sko | 13 % | 13 % | 13 % | 13 % | 13 % | 12 % |
| Hjemmetekstiler | 17 % | 18 % | 19 % | 19 % | 17 % | 16 % |
| Andre konfeksjonerte varer | 2 % | 3 % | 3 % | 5 % | 7 % | 9 % |
| Presenninger og telt | 6 % | 5 % | 5 % | 8 % | 8 % | 6 % |
| Garn i detaljsalg | 2 % | 1 % | 1 % | 2 % | 1 % | 1 % |

### Materiale (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 40 % | 39 % | 37 % | 29 % | 29 % | 31 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 18 % | 17 % | 18 % | 18 % | 18 % | 17 % |
| Andre fibre | 2 % | 3 % | 2 % | 3 % | 3 % | 2 % |
| Syntetisk | 32 % | 33 % | 35 % | 42 % | 42 % | 41 % |
| Ull | 5 % | 6 % | 5 % | 6 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/di_rt_us_hh_sales_to_households_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

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
