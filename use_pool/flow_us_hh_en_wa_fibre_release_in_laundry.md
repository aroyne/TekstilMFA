---
layout: default
title: Fibre release in laundry
parent: Households (US.HH)
grand_parent: 5. Use (US)
nav_order: 4
---

# Fibre release in laundry

| | |
|---|---|
| Flytkode | `US.HH-EN.WA-Fibre release in laundry-TOT` |
| Fra | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Til | [Wastewater and water (not followed) (EN.WA)](../environment_pool/subpool_en_wa.html) |
| Tekstilform | MFR – mikrofibre |
| Dimensjoner | år × produktgruppe |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | Laundry mass per inhabitant (Mepex 2014 after Pakula & Stamminger 2010) x SSB population x release from real soiled laundry (Lant et al. 2020, 114 ppm); Mepex 2014 (600 t synthetic) for sensitivity only |
| Merknad | Natural fibres release about 20 times more per kg than synthetic (Lant et al. 2020, 2022), split in the fibre layer (D37). Released to wastewater; treatment is not modelled (D35) |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_en_wa_fibre_release_in_laundry.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.HH-EN.WA-Fibre release in laundry-TOT** er fibre som løsner fra tekstiler når de vaskes i husholdningenes vaskemaskiner, og som går med avløpsvannet.
- Flyten omfatter både syntetiske fibre (mikroplast) og naturfibre og regenerert cellulose. De skilles i fiberlaget.
- Flyten går ut av systemet til avløp. Rensing, slam og videre spredning følges ikke (D35).

#### Datakilder (og hvordan kildetallene er produsert)

- Tøymengden er 280 kg per innbygger per år (70 vasker à 4 kg), fra Mepex (Sundt m.fl. 2014) etter Pakula & Stamminger (2010). Folketallet er fra SSB 05803.
- Lant m.fl. (2020) målte 114 mg fibre per kg tøy i 79 vasker med ekte skittentøy fra britiske husholdninger (66 mg/kg i store og 132 mg/kg i små vasker). 96 % av fibrene var naturfibre (bomull, ull, viskose).
- Mepex (Sundt m.fl. 2014) anslo 600 t syntetiske mikrofibre per år. Anslaget bygger på laboratorieforsøk med enkeltplagg og ligger over deres egne to beregninger (276 og 315 t). Det er omtrent ti ganger det ekte skittentøy gir, og brukes bare til følsomhet (D37).

#### Antakelser

- Tøymengden følger folketallet, ikke tekstillageret: det er vaskevaner som styrer hvor mye som vaskes (D37).
- Britiske målinger gjelder for Norge.
- Naturfibre og cellulose slipper ca. 20 ganger mer per kg enn syntetiske fibre (7–60, lognormal).

#### Sammensetning (varetype og materiale)

- Flyten er i produktgruppen CORE.
- Materialet er fibergruppene i tekstillageret i årgangsmodellen, vektet med utslipp per kg. I 2025 er ca. 74 % bomull, 15 % ull, 5 % viskose og under 4 % syntetisk.

#### Tidsutvikling og sammenligninger

- Utslippet øker med folketallet, fra 0,12 kt i 1988 til 0,16 kt i 2025 (0,11–0,22).
- Med Mepex-kalibreringen var flyten 1,5–1,6 kt, hvorav 0,6–0,7 kt syntetisk. Nå er det syntetiske utslippet under 0,01 kt.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Klær, hjemmetekstiler og sko | 100 % | 100 % | 100 % | 100 % | 100 % | 100 % |

### Materiale (fiberlag, D19)

Fibergruppene i tekstillageret i årgangsmodellen for husholdningene (uten ikke-tekstil). Syntetisk er mikroplast, de andre gruppene er naturfibre og regenerert cellulose.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 80 % | 79 % | 81 % | 75 % | 73 % | 73 % |
| Regenerert cellulose | 6 % | 4 % | 4 % | 5 % | 5 % | 5 % |
| Andre fibre | 1 % | 2 % | 2 % | 3 % | 4 % | 3 % |
| Syntetisk | 3 % | 3 % | 3 % | 4 % | 4 % | 4 % |
| Ull | 11 % | 12 % | 10 % | 13 % | 14 % | 14 % |

<iframe src="../output_files/plots/pages/us_hh_en_wa_fibre_release_in_laundry_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `laundry_kg_per_capita` | 58 % | 58 % | 58 % |
| `laundry_release_ppm` | 42 % | 42 % | 42 % |
| Halvt 95 %-intervall, førsteordens (kt) | 0.05 | 0.05 | 0.06 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 0.05 | 0.05 | 0.06 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_laundry_fibre_release_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L212). Dokumentasjonen i koden:

> Fibres released from household textiles in washing machines to
> wastewater, where the model stops following them: treatment, sludge and
> spread in the environment are not modelled (D35). The laundry washed per
> year times the release from real soiled laundry, 114 mg per kg (66-132;
> Lant et al. 2020, 79 loads from British households). About 96 % of what
> is released is natural or cellulosic fibre, so the fibre layer gives
> those fibres about 20 times the release per kg of synthetic fibre (D37).
>
> Mepex (Sundt et al. 2014) estimated 600 t synthetic microfibres a year,
> from single garments in laboratory tests, above their own two
> calculations (276 and 315 t); it is about ten times what real laundry
> gives and is kept for sensitivity only.
>
> `_laundry_kt`: Laundry washed in households per year (kt), array (year,): 280 kg per
> inhabitant (200-350; 70 loads of 4 kg, Mepex 2014 after Pakula &
> Stamminger 2010) times the population. It follows the population, not
> the textile stock: washing habits, not how much textile people own,
> set how much is washed (D37).
