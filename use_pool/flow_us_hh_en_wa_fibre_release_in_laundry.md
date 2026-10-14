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
| Kandidatdata | Mepex 2014 (Sundt et al. 2014; cited in Sundt et al. 2016, M545): about 600 t synthetic microfibres a year from household laundry; scaled with the textile stock of the household cohort model |
| Merknad | Synthetic and natural fibres, split in the fibre layer; natural fibres at the same release per kg as synthetic. Released to wastewater; treatment is not modelled (D35) |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_en_wa_fibre_release_in_laundry.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.HH-EN.WA-Fibre release in laundry-TOT** er fibre som løsner fra tekstiler når de vaskes i husholdningenes vaskemaskiner, og som går med avløpsvannet.
- Flyten omfatter både syntetiske fibre (mikroplast) og naturfibre og regenerert cellulose. De to typene skilles i fiberlaget (se sammensetningen).
- Flyten går ut av systemet til avløp. Rensing i renseanlegg, slam og videre spredning til vann og jord følges ikke (D35). Usikkerheten i tilbakeholdelse og slambruk er stor og mengdene små, så det hører hjemme i en egen mikroplastmodell. Se Sundt m.fl. (2016) for Miljødirektoratet.

#### Datakilder (og hvordan kildetallene er produsert)

- Mepex (Sundt m.fl. 2014) anslo for Miljødirektoratet at husholdningsvask slipper ut omtrent 600 t syntetiske mikrofibre per år i Norge. Tallet gjengis i Sundt m.fl. (2016, M545). Anslaget bygger på utslipp per vask fra laboratorieforsøk, ganget opp med antall vasker og andelen syntetiske tekstiler.
- Lant m.fl. (2020) målte 114 mg fibre per kg tøy i ekte husholdningsvask, og de fleste fibrene var naturfibre.

#### Antakelser

- Utslippet per kt syntetisk fiber i husholdningenes lager settes slik at det syntetiske utslippet i 2014 blir 0,6 kt (±50 %).
- Naturfibre og regenerert cellulose slipper like mye per kt som syntetisk.
- Lageret er tekstillageret i årgangsmodellen for husholdningene (klær, hjemmetekstiler, sko og garn), ikke restleddet i balansen, fordi restleddet trolig er for høyt.

#### Sammensetning (varetype og materiale)

- Flyten er i produktgruppen CORE.
- Materialet er fibergruppene i tekstillageret i årgangsmodellen. Syntetisk utgjør omtrent 32 % i 1990 og 38–43 % etter 2014, og resten er mest bomull.

#### Tidsutvikling og sammenligninger

- Utslippet øker fra 0,9 kt i 1988 til 1,6 kt i 2014 og ligger på 1,5–1,6 kt siden, i takt med lageret i årgangsmodellen.
- Det syntetiske utslippet øker fra omtrent 0,3 kt i 1990 til 0,6–0,7 kt etter 2014.
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
| Bomull | 57 % | 55 % | 54 % | 46 % | 43 % | 44 % |
| Regenerert cellulose | 4 % | 3 % | 2 % | 3 % | 3 % | 3 % |
| Andre fibre | 1 % | 1 % | 2 % | 2 % | 2 % | 2 % |
| Syntetisk | 32 % | 32 % | 36 % | 42 % | 43 % | 43 % |
| Ull | 7 % | 8 % | 6 % | 8 % | 8 % | 8 % |

<iframe src="../output_files/plots/pages/us_hh_en_wa_fibre_release_in_laundry_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_laundry_fibre_release_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L133). Dokumentasjonen i koden:

> Fibres released from household textiles in washing machines to
> wastewater, where the model stops following them: treatment, sludge and
> spread in the environment are not modelled (D35). Mepex (Sundt et al. 2014, cited in Sundt et al.
> 2016 for the Norwegian Environment Agency) estimated about 600 t
> synthetic microfibres a year from household laundry. The release per kt
> synthetic fibre in the household stock is set so that the synthetic
> release in 2014 matches that estimate, and the other fibre groups
> (cotton, wool, regenerated cellulose, other) release the same per kt
> (Lant et al. 2020 found that most fibres released in real laundry are
> natural). The stock is that of the household cohort model, because the
> residual stock of the balance is probably too high. The fibre layer
> splits the flow into synthetic and other fibres.
>
> `_household_textile_stock`: Stock of textile fibre in the CORE group of US.HH by fibre group, array
> (year, fibre group), from the cohort model of new goods entering the
> households, with the composition of registered imports.
>
> `_laundry_release_per_kt`: Fibres released in laundry per kt textile fibre in use, from the synthetic release in 2014.
