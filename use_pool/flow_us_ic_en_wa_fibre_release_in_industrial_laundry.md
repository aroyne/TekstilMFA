---
layout: default
title: Fibre release in industrial laundry
parent: Institutions and businesses (US.IC)
grand_parent: 5. Use (US)
nav_order: 3
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
| Kandidatdata | Same release per kt textile in use as in household laundry (Mepex 2014), applied to the textile stock of the US.IC cohort model |
| Merknad | No Norwegian data; more frequent washing and filters in industrial laundries pull in opposite directions (D29). Released to wastewater; treatment is not modelled (D35) |

## Tidsserie

<iframe src="../output_files/plots/pages/us_ic_en_wa_fibre_release_in_industrial_laundry.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.IC-EN.WA-Fibre release in industrial laundry-TOT** er fibre som løsner når tekstiler brukt av bedrifter og offentlig sektor vaskes (mest i industrivaskerier), og som går med avløpsvannet.
- Både syntetiske fibre og naturfibre er med, og de skilles i fiberlaget.
- Flyten går ut av systemet til avløp. Rensing i renseanlegg, slam og videre spredning til vann og jord følges ikke (D35). Usikkerheten i tilbakeholdelse og slambruk er stor og mengdene små, så det hører hjemme i en egen mikroplastmodell. Se Sundt m.fl. (2016) for Miljødirektoratet.

#### Datakilder (og hvordan kildetallene er produsert)

- Det finnes ingen norske data for industrivask.
- Utslippet per kt tekstil i bruk er det samme som for husholdningene, ankret i Mepex sitt anslag på 600 t syntetiske mikrofibre fra husholdningsvask i 2014 (se US.HH-WM.WW-Fibre release in laundry-TOT).

#### Antakelser

- Samme utslipp per kt tekstil som i husholdningene, brukt på tekstillageret i årgangsmodellen for US.IC (D29). Institusjonstekstiler vaskes oftere, men industrivaskerier filtrerer og renser ofte vannet. De to effektene trekker hver sin vei.
- Sekker har ikke lager og slipper ikke fibre.

#### Sammensetning (varetype og materiale)

- Klær (arbeidsklær) er omtrent 43 % og tepper 25 % i 2022.
- Materialet er fibergruppene i tekstillageret i US.IC: omtrent 57 % syntetisk og 28 % bomull.

#### Tidsutvikling og sammenligninger

- Utslippet er lite: 0,12 kt i 1990 og 0,14–0,15 kt etter 2008, omtrent en tidel av utslippet fra husholdningsvask.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 49 % | 31 % | 23 % | 25 % | 25 % | 28 % |
| Klær | 34 % | 47 % | 52 % | 47 % | 44 % | 44 % |
| Sko | 1 % | 2 % | 2 % | 2 % | 2 % | 2 % |
| Hjemmetekstiler | 8 % | 11 % | 12 % | 12 % | 12 % | 11 % |
| Andre konfeksjonerte varer | 1 % | 2 % | 2 % | 3 % | 5 % | 5 % |
| Presenninger og telt | 6 % | 8 % | 8 % | 11 % | 12 % | 11 % |

### Materiale (fiberlag, D19)

Fibergruppene i tekstillageret i årgangsmodellen for institusjoner og bedrifter, per varetype (uten ikke-tekstil).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 29 % | 36 % | 38 % | 29 % | 28 % | 28 % |
| Regenerert cellulose | 3 % | 3 % | 3 % | 3 % | 3 % | 3 % |
| Andre fibre | 4 % | 6 % | 5 % | 5 % | 5 % | 5 % |
| Syntetisk | 57 % | 46 % | 47 % | 56 % | 58 % | 58 % |
| Ull | 7 % | 9 % | 7 % | 7 % | 6 % | 7 % |

<iframe src="../output_files/plots/pages/us_ic_en_wa_fibre_release_in_industrial_laundry_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_industrial_laundry_release_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L206). Dokumentasjonen i koden:

> Fibres released when textiles used by institutions and businesses are
> washed (mostly in industrial laundries) to wastewater, where the model
> stops following them (D35). There are no Norwegian data, so the release per kt textile
> fibre in use is the same as in household laundry, applied to the textile
> stock of the US.IC cohort model per product. Institutional textiles are
> washed more often, but industrial laundries often filter and treat their
> water; the two pull in opposite directions. Sacks have no stock and
> release nothing.
>
> `_laundry_release_per_kt`: Fibres released in laundry per kt textile fibre in use, from the synthetic release in 2014.
>
> `_household_textile_stock`: Stock of textile fibre in the CORE group of US.HH by fibre group, array
> (year, fibre group), from the cohort model of new goods entering the
> households, with the composition of registered imports.
