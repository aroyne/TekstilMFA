---
layout: default
title: Household textiles in commercial and bulky waste
parent: Households (US.HH)
grand_parent: 5. Use (US)
nav_order: 9
---

# Household textiles in commercial and bulky waste

| | |
|---|---|
| Flytkode | `US.HH-WM.RS-Household textiles in commercial and bulky waste-TOT` |
| Fra | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Til | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Tekstilform | MIX – brukte, usortert |
| Dimensjoner | år × produktgruppe |
| Metode | parameter |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | Danish analogy: bulky waste taken directly to incineration or private sorting, about 1 kg textiles per inhabitant (Watson et al. 2018, MST); Mepex/Avfall Norge pick analyses of commercial waste (requested) |
| Merknad | D42. Household textiles collected as commercial waste (moving, estates, skips, bulky waste outside municipal recycling stations), not in the household pick analyses. 0 in the main result (D8), 1 kg per inhabitant in the structural run; in the future module the gap between the scaled cohort model and a realistic stock growth |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_wm_rs_household_textiles_in_commercial_and_bulky_waste.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.HH-WM.RS-Household textiles in commercial and bulky waste-TOT** er klær, hjemmetekstiler og sko fra husholdningene som går som næringsavfall: flytting, tømming av dødsbo, storsekker og containere, og grovavfall som private firmaer henter. Tekstilene går til forbrenning.
- Det er ikke med i plukkanalysene for husholdningsavfall, som dekker restavfall fra henteordningen og brennbart avfall fra de kommunale gjenvinningsstasjonene.
- **Flyten er 0 i hovedresultatet for 1988–2025** (D8, D42). Den brukes i en strukturkjøring og i fremtidsmodulen.

#### Datakilder (og hvordan kildetallene er produsert)

- Det finnes ingen norske tall. SSB 10513 skiller ikke ut tekstiler i blandet næringsavfall, og KOSTRA dekker bare avfall som kommunene håndterer.
- I Danmark ble tekstiler i grovavfall som går rett til forbrenning eller til private sorteringsanlegg, anslått til 5,6 kt per år for 5,8 millioner innbyggere, ca. 1 kg per innbygger (Watson, Trzepacz & Gravgård Pedersen 2018, Miljøstyrelsen). Anslaget bygger på avfallsmengder fra 16 kommunale selskaper og få plukkanalyser.
- Mepex og Avfall Norge er spurt om plukkanalyser av næringsavfall (HENVENDELSER).

#### Antakelser

- Strukturkjøringen `commercial_bulky_1kg` bruker 1 kg per innbygger × folketallet, altså den danske analogien.
- Strukturkjøringen `bulky_bedding` sender i stedet dyner, puter og møbelputer (HS 9404) som kommer inn i husholdningene, til flyten samme år. Mengden er andelen HS 9404 av importen av hjemmetekstiler × de nye hjemmetekstilene. Wasted Textiles veide fylte soveartikler for seg (Syversen m.fl. 2023), og møbelputer kastes trolig sammen med møblene. Kasseringene av hjemmetekstiler i statistikken er 0,75 av lagermodellen i 2021–2022, mot 0,91 for klær (fase C).
- I fremtidsmodulen er flyten resten av balansen i US.HH (CORE) etter en lagervekst på 0,5 kg per innbygger per år (0,3–1). Der er den det som kasseres utover statistikken, ikke et anslag fra data.

#### Sammensetning (varetype og materiale)

- Flyten er i produktgruppen CORE.
- Materialet er det samme som for de andre kasseringene fra husholdningene, altså utstrømmen fra årgangsmodellen.

#### Tidsutvikling og sammenligninger

- `commercial_bulky_1kg` gir 4,2 kt i 1990 og 5,6 kt i 2025. Restlageret i 2025 faller da med 183 kt, og innsamlingsgraden går ned med ca. 3 prosentpoeng.
- `bulky_bedding` gir 4,5 kt i 2025. Restlageret faller med 198 kt, og innsamlingsgraden går ned med 3 prosentpoeng. Avviket mot lagermodellen går fra 763 til 565 kt.
- I referansebanen er flyten 7,5 kt i 2026 og 10–11 kt i 2030–2050. Innsamlingsgraden faller fra 45 % i 2025 til 41 % i 2026. Det er et brudd i definisjonen og ingen reell endring: Nevneren tar med flyten først fra 2026.
- Det danske gapet var 10 kt (1,8 kg per innbygger) i 2016, og forfatterne mente det meste var data som ikke fanges opp, ikke lagervekst. Vårt gap i 2025 er ca. 9 kt.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For tepper, presenninger og andre konfeksjonerte varer: utstrømmen av en årgangsmodell av salget.


<iframe src="../output_files/plots/pages/us_hh_wm_rs_household_textiles_in_commercial_and_bulky_waste_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_commercial_and_bulky_waste_mc` i `calculations/us_mc.py`. Dokumentasjonen i koden:

> CL+HT+FW from households collected as commercial waste: moving, estates,
> skips and bulky waste picked up by private firms, which is not in the
> pick analyses of household waste (D42). There are no Norwegian data. In
> Denmark, textiles in bulky waste taken directly to incineration or to
> private sorting were about 1 kg per inhabitant (Watson et al. 2018,
> MST).
>
> Duvets, pillows and furniture cushions (HS 9404) are 17 % of the
> household textiles supplied (3.6 kt a year net import in 2021-2022).
> The Wasted Textiles pick analyses weighed filled bedding apart and left
> it out of the composition (Syversen et al. 2023), and furniture cushions
> are probably thrown away with the furniture. Household textiles are
> discarded at 0.75 of the cohort model in 2021-2022, against 0.91 for
> clothing (claude_tekst/2026-11-09_C2), and these goods are a likely
> part of the difference. A share of the 9404 goods entering households
> (their share of the HT import mass times the new HT goods) can
> therefore leave in the same year as bulky waste.
>
> The flow is 0 in the main result, where discards come from the
> statistics (D8). The structural runs (structural_sensitivity.py) set it
> to 1 kg per inhabitant, or to all 9404 goods; both lower the residual
> stock and the collection rate.
