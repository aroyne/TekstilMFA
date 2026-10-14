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
| Kandidatdata | Same level as the release in laundry (factor 1, 0.3-3; De Falco et al. 2020) |
| Merknad | No Norwegian data |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_en_ai_fibre_release_to_air_and_dust.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.HH-EN.AI-Fibre release to air and dust-TOT** er fibre som løsner fra tekstiler mens de brukes, og som havner i luft og innendørs støv.
- Som ved vask skilles syntetiske fibre og naturfibre i fiberlaget.

#### Datakilder (og hvordan kildetallene er produsert)

- Det finnes ingen norske data. De Falco m.fl. (2020) fant at polyesterplagg slipper ut omtrent like mye fibre til luft ved bruk som ved vask.

#### Antakelser

- Utslippet settes til samme nivå som utslippet ved vask, med en faktor 1 (0,3–3, PERT). Usikkerheten er stor.
- EN.AI er et sluk. Fibrene følges ikke videre (for eksempel til støvsugerposer og restavfall).

#### Sammensetning (varetype og materiale)

- Samme som ved vask: fibergruppene i tekstillageret i årgangsmodellen.

#### Tidsutvikling og sammenligninger

- Flyten følger utslippet ved vask: omtrent 1,1 kt i 1990 og 1,8–1,9 kt etter 2014 (medianen ligger over vaskeutslippet fordi faktoren er skjevfordelt).
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
| Bomull | 56 % | 55 % | 54 % | 46 % | 43 % | 43 % |
| Regenerert cellulose | 4 % | 3 % | 2 % | 3 % | 3 % | 3 % |
| Andre fibre | 1 % | 1 % | 2 % | 2 % | 2 % | 2 % |
| Syntetisk | 32 % | 32 % | 36 % | 42 % | 43 % | 43 % |
| Ull | 7 % | 8 % | 6 % | 8 % | 8 % | 8 % |

<iframe src="../output_files/plots/pages/us_hh_en_ai_fibre_release_to_air_and_dust_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_air_and_dust_release_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L158). Dokumentasjonen i koden:

> Fibres released to air and indoor dust while household textiles are worn
> and used, set to the same level as the release in laundry, with a factor
> of 1 (0.3-3): De Falco et al. (2020) found a release during wear of the
> same order as in washing. There are no Norwegian data.
