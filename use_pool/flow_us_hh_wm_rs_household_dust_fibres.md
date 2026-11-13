---
layout: default
title: Household dust fibres
parent: Households (US.HH)
grand_parent: 5. Use (US)
nav_order: 7
---

# Household dust fibres

| | |
|---|---|
| Flytkode | `US.HH-WM.RS-Household dust fibres-TOT` |
| Fra | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Til | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Tekstilform | MFR – mikrofibre |
| Dimensjoner | år × produktgruppe |
| Metode | parameter |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | Release during wear (see Fibre release to air and dust) x share vacuumed (assumption 0.8, 0.5-0.95) |
| Merknad | No measurements of textile fibre mass in vacuum cleaner bags found. Goes with residual waste (D37) |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_wm_rs_household_dust_fibres.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.HH-WM.RS-Household dust fibres-TOT** er fibre som løsner fra tekstiler mens de brukes, blir del av husstøvet og støvsuges. Støvsugerposen går i restavfallet.

#### Datakilder (og hvordan kildetallene er produsert)

- Det finnes ingen målinger av tekstilfibre i masse i støvsugerposer.
- De Falco m.fl. (2020) fant at utslippet ved bruk er av samme størrelse som ved vask, målt per plagg.
- Mepex (Sundt m.fl. 2014) peker på at de største partiklene støvsuges og går med restavfallet til forbrenning.

#### Antakelser

- Utslippet ved slitasje er utslippet ved vask ganget med en faktor 1 (0,3–3, lognormal).
- 80 % (50–95 %, flat fordeling) av det støvsuges. Resten blir i luft og støv (EN.AI).
- Plukkanalysene teller støv som finstoff, ikke tekstil, så flyten kommer i tillegg til restavfallsankrene.

#### Sammensetning (varetype og materiale)

- Som for vask: ca. 74 % bomull og under 4 % syntetisk i 2025.

#### Tidsutvikling og sammenligninger

- 0,09 kt i 1988 og 0,12 kt i 2025 (0,03–0,42). Usikkerheten er stor, fordi både nivået og andelen som støvsuges er antakelser.
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
| Bomull | 80 % | 79 % | 80 % | 75 % | 74 % | 74 % |
| Regenerert cellulose | 6 % | 5 % | 4 % | 5 % | 5 % | 5 % |
| Andre fibre | 1 % | 2 % | 2 % | 3 % | 4 % | 3 % |
| Syntetisk | 3 % | 3 % | 3 % | 4 % | 4 % | 4 % |
| Ull | 11 % | 12 % | 10 % | 13 % | 14 % | 14 % |

<iframe src="../output_files/plots/pages/us_hh_wm_rs_household_dust_fibres_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `air_release_relative_to_laundry` | 91 % | 91 % | 91 % |
| `laundry_kg_per_capita` | 3 % | 3 % | 3 % |
| `vacuumed_dust_share` | 3 % | 3 % | 3 % |
| `laundry_release_ppm` | 2 % | 2 % | 2 % |
| Halvt 95 %-intervall, førsteordens (kt) | 0.17 | 0.19 | 0.21 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 0.16 | 0.17 | 0.19 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_household_dust_fibres_mc` i `calculations/us_mc.py`. Dokumentasjonen i koden:

> Fibres shed during wear that end up in house dust and are vacuumed:
> 80 % (50-95 %, assumption) of the release during wear (D37). Mepex
> (2014) notes that the larger particles are vacuumed and go with residual
> waste to incineration. No measurements of textile fibre mass in vacuum
> cleaner bags have been found.
>
> `_wear_release`: Fibres shed while household textiles are worn and used, array (year,
> group): the release in laundry times a factor of 1 (0.3-3). De Falco et
> al. (2020) found a release during wear of the same order as in washing.
> There are no Norwegian data.
