---
layout: default
title: Fibre release in industrial laundry
parent: Institutions and businesses (US.IC)
grand_parent: 5. Use (US)
nav_order: 2
---

# Fibre release in industrial laundry

| | |
|---|---|
| Flytkode | `US.IC-EN.WA-Fibre release in industrial laundry-TOT` |
| Fra | [Institutions and businesses (US.IC)](../use_pool/subpool_us_ic.html) |
| Til | [Wastewater and water (not followed) (EN.WA)](../environment_pool/subpool_en_wa.html) |
| Tekstilform | MFR – mikrofibre |
| Dimensjoner | år × produkt |
| Metode | parameter |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | Same release per kt textile in use as household laundry (D37), applied to the textile stock of the US.IC cohort model |
| Merknad | No Norwegian data; more frequent washing and filters in industrial laundries pull in opposite directions (D29). Released to wastewater; treatment is not modelled (D35) |

## Tidsserie

<iframe src="../output_files/plots/pages/us_ic_en_wa_fibre_release_in_industrial_laundry.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.IC-EN.WA-Fibre release in industrial laundry-TOT** er fibre som løsner når tekstiler brukt av bedrifter og offentlig sektor vaskes (mest i industrivaskerier), og som går med avløpsvannet.
- Både syntetiske fibre og naturfibre er med, og de skilles i fiberlaget.
- Flyten går ut av systemet til avløp (D35).

#### Datakilder (og hvordan kildetallene er produsert)

- Det finnes ingen norske data for industrivask, og tøymengden i sektoren er ukjent.
- Utslippet per kt tekstil i bruk er det samme som for husholdningene: utslippet fra husholdningsvask (Lant m.fl. 2020, se `US.HH-EN.WA-Fibre release in laundry`) delt på tekstillageret i husholdningenes årgangsmodell.

#### Antakelser

- Samme utslipp per kt tekstil som i husholdningene, brukt på tekstillageret i årgangsmodellen for US.IC (D29, D37). Institusjonstekstiler vaskes oftere, men industrivaskerier filtrerer og renser ofte vannet. De to effektene trekker hver sin vei.
- Sekker har ikke lager og slipper ikke fibre.

#### Sammensetning (varetype og materiale)

- Materialet er fibergruppene i tekstillageret i US.IC, vektet med utslipp per kg: ca. 50 % bomull og 10 % syntetisk i 2025.

#### Tidsutvikling og sammenligninger

- Ca. 0,01 kt per år (0,004–0,026), mot 0,1–0,15 kt før D37.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 48 % | 30 % | 23 % | 25 % | 25 % | 28 % |
| Klær | 34 % | 47 % | 51 % | 46 % | 44 % | 43 % |
| Sko | 1 % | 2 % | 2 % | 2 % | 2 % | 1 % |
| Hjemmetekstiler | 9 % | 12 % | 14 % | 13 % | 13 % | 12 % |
| Andre konfeksjonerte varer | 1 % | 2 % | 2 % | 3 % | 4 % | 5 % |
| Presenninger og telt | 6 % | 8 % | 8 % | 11 % | 12 % | 11 % |

### Materiale (fiberlag, D19)

Fibergruppene i tekstillageret i årgangsmodellen for institusjoner og bedrifter, per varetype (uten ikke-tekstil).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 53 % | 59 % | 62 % | 56 % | 55 % | 55 % |
| Regenerert cellulose | 8 % | 6 % | 6 % | 7 % | 7 % | 7 % |
| Andre fibre | 13 % | 12 % | 12 % | 14 % | 14 % | 14 % |
| Syntetisk | 8 % | 5 % | 5 % | 8 % | 9 % | 9 % |
| Ull | 17 % | 19 % | 15 % | 16 % | 15 % | 16 % |

<iframe src="../output_files/plots/pages/us_ic_en_wa_fibre_release_in_industrial_laundry_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `institutional_share` | 45 % | 47 % | 45 % |
| `laundry_kg_per_capita` | 15 % | 15 % | 15 % |
| `lifetime_mean_US.HH_CL` | 12 % | 12 % | 14 % |
| `laundry_release_ppm` | 11 % | 11 % | 11 % |
| `lifetime_mean_US.HH_HT` | 3 % | 3 % | 4 % |
| `lifetime_mean_US.IC_CL` | 4 % | 5 % | 4 % |
| `lifetime_mean_US.IC_CA` | 8 % | 3 % | 4 % |
| Halvt 95 %-intervall, førsteordens (kt) | 0.01 | 0.01 | 0.01 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 0.01 | 0.01 | 0.01 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_industrial_laundry_release_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L295). Dokumentasjonen i koden:

> Fibres released when textiles used by institutions and businesses are
> washed (mostly in industrial laundries) to wastewater, where the model
> stops following them (D35). There are no Norwegian data, and the laundry
> washed in the sector is not known, so the release per kt textile fibre
> in use is that of household laundry (the household release divided by
> the textile stock of the household cohort model), applied to the textile
> stock of the US.IC cohort model per product. Institutional textiles are
> washed more often, but industrial laundries often filter and treat their
> water; the two pull in opposite directions. Sacks have no stock and
> release nothing.
>
> `_household_textile_stock`: Stock of textile fibre in the CORE group of US.HH by fibre group, array
> (year, fibre group), from the cohort model of new goods entering the
> households, with the composition of registered imports.
