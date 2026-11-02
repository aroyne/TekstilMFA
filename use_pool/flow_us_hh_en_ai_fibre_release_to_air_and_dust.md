---
layout: default
title: Fibre release to air and dust
parent: Households (US.HH)
grand_parent: 5. Use (US)
nav_order: 5
---

# Fibre release to air and dust

| | |
|---|---|
| Flytkode | `US.HH-EN.AI-Fibre release to air and dust-TOT` |
| Fra | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Til | [Air and indoor dust (EN.AI)](../environment_pool/subpool_en_ai.html) |
| Tekstilform | MFR – mikrofibre |
| Dimensjoner | år × produktgruppe |
| Metode | parameter |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | Release during wear at the level of the release in laundry (factor 1, 0.3-3; De Falco et al. 2020), minus the share vacuumed; plus tumble dryer exhaust (Cummins et al. 2023) |
| Merknad | No Norwegian data. The vacuumed part goes to WM.RS as household dust fibres (D37). Not followed further (D35) |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_en_ai_fibre_release_to_air_and_dust.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.HH-EN.AI-Fibre release to air and dust-TOT** er fibre som løsner fra tekstiler mens de brukes, og som blir værende i luft og innendørs støv, og fibre fra tørketrommel som går ut med avtrekket.
- Den delen av slitasjen som støvsuges, er egen flyt til restavfallet (`US.HH-WM.RS-Household dust fibres`, D37).

#### Datakilder (og hvordan kildetallene er produsert)

- Det finnes ingen norske data. De Falco m.fl. (2020) fant at polyesterplagg slipper ut omtrent like mye fibre ved bruk som ved vask.
- Utslippet fra tørking og andelen som fanges i lofilteret er fra Cummins m.fl. (2023), se `US.HH-WM.RS-Tumble dryer lint`.

#### Antakelser

- Utslippet ved slitasje er utslippet ved vask ganget med en faktor 1 (0,3–3, lognormal).
- 80 % (50–95 %, flat fordeling) av slitasjen støvsuges. Resten går hit.
- Avtrekket fra tørketrommelen er 12 % av tørkeutslippet (resten fanges i filteret). I kondenstromler går dette til kondensvannet, som ikke skilles ut.
- EN.AI er en systemgrense, og fibrene følges ikke videre (D35).

#### Sammensetning (varetype og materiale)

- Samme som ved vask: tekstillageret i årgangsmodellen, vektet med utslipp per kg (ca. 74 % bomull og under 4 % syntetisk).

#### Tidsutvikling og sammenligninger

- 0,04–0,06 kt per år (0,02–0,2), mot 1,1–1,9 kt før D37. Det meste av nedgangen kommer av det lavere vaskeutslippet, og resten av at det som støvsuges, nå går til restavfallet.
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
| Bomull | 80 % | 80 % | 81 % | 75 % | 74 % | 74 % |
| Regenerert cellulose | 5 % | 4 % | 4 % | 5 % | 5 % | 5 % |
| Andre fibre | 1 % | 2 % | 2 % | 3 % | 4 % | 3 % |
| Syntetisk | 2 % | 2 % | 3 % | 3 % | 3 % | 3 % |
| Ull | 11 % | 12 % | 10 % | 13 % | 14 % | 15 % |

<iframe src="../output_files/plots/pages/us_hh_en_ai_fibre_release_to_air_and_dust_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `air_release_relative_to_laundry` | 60 % | 60 % | 57 % |
| `vacuumed_dust_share` | 34 % | 34 % | 32 % |
| `gap: dryer_ownership_share` | – | – | 5 % |
| `laundry_kg_per_capita` | 4 % | 4 % | 4 % |
| `laundry_release_ppm` | 2 % | 2 % | 1 % |
| `tumble_dried_share` | 1 % | 1 % | 1 % |
| Halvt 95 %-intervall, førsteordens (kt) | 0.05 | 0.06 | 0.07 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 0.08 | 0.08 | 0.10 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_air_and_dust_release_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L236). Dokumentasjonen i koden:

> Fibres to air and indoor dust that are not vacuumed (the rest of the
> release during wear, D37), plus the fibres from tumble drying that pass
> the lint filter and leave with the exhaust of vented dryers. In
> condenser dryers they go to the condensate, which is not split out.
>
> `_tumble_drying_release`: Fibres released in tumble drying (kt), array (year,): laundry times the
> share of households with a tumble dryer (44 % in 1996 and 47 % in 2012,
> SSB via Store norske leksikon; held before and after) times the share of
> their loads that are dried (0.6, 0.4-0.8, assumption) times the release
> in drying, 300 mg per kg (256 for vented and 342 for condenser dryers,
> Cummins et al. 2023, real soiled laundry).
>
> `_wear_release`: Fibres shed while household textiles are worn and used, array (year,
> group): the release in laundry times a factor of 1 (0.3-3). De Falco et
> al. (2020) found a release during wear of the same order as in washing.
> There are no Norwegian data.
