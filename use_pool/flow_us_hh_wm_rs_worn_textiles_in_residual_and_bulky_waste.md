---
layout: default
title: Worn textiles in residual and bulky waste
parent: Households (US.HH)
grand_parent: 5. Use (US)
nav_order: 3
---

# Worn textiles in residual and bulky waste

| | |
|---|---|
| Flytkode | `US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT` |
| Fra | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Til | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Tekstilform | WRN – brukte, utslitte |
| Dimensjoner | år × produktgruppe |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Pick analyses (Mepex/Avfall Norge) x SSB household waste amounts; Reusable share of pick analyses: Laitala et al. 2012 (via Huygens et al. 2023), Rubach et al. 2023, de Sadeleer & Rubach 2026 |
| Merknad | D18. CORE residual textiles not reusable, plus CA/TA/OM discarded by the household cohort model (lifetimes) |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_wm_rs_worn_textiles_in_residual_and_bulky_waste.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT** er tekstiler i husholdningenes restavfall og grovavfall som ikke kan brukes om igjen (form WRN, D18): utslitte klær, hjemmetekstiler og sko, og alle tepper, presenninger, telt og andre konfeksjonerte varer som kasseres.

#### Datakilder (og hvordan kildetallene er produsert)

- CORE: tekstiler i restavfall og grovavfall fra plukkanalysene, minus varene utenfor CORE (12 %, D44) og minus den brukbare delen (se US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT).
- Tepper, presenninger og andre konfeksjonerte varer: utstrømmen av en årgangsmodell av salget til husholdningene, med levetider fra `parameters/lifetimes.csv` (tepper 10 år, presenninger og telt 4 år, andre konfeksjonerte varer 2 år; Napolano m.fl. 2025 og van Oorschot m.fl. 2020).

#### Antakelser

- Varene utenfor CORE i plukkanalysene (D44) legges ikke til her, fordi tepper, presenninger og andre konfeksjonerte varer kommer fra årgangsmodellen. Ellers ville de blitt telt to ganger.
- Tepper, presenninger og andre konfeksjonerte varer har ikke kasseringsstatistikk, så kasseringene beregnes med årgangsmodellen. Det er et unntak fra D8 (D28). Innstrømmen før 1988 holdes på 1988-nivå (D2).
- Før 2009 er restavfallet for CORE 2009-nivået per innbygger pluss det som ennå ikke ble samlet inn separat (D40, se US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT). Det gir 58 kt utslitte tekstiler i 1990 (alle produkter), mot 47 kt med fast nivå per innbygger og de gamle ankrene.
- Sekker brukes ikke av husholdninger (D13).

#### Sammensetning (varetype og materiale)

- CORE falt fra 54 % i 1990 til 43 % i 2022. Tepper er 23–24 %, og presenninger og andre konfeksjonerte varer økte.
- CORE har utstrømmen fra årgangsmodellen for nye varer, og de andre varetypene utstrømmen fra årgangsmodellen for salget. Syntetisk økte fra 35 % i 1990 til 49 % i 2022.

#### Tidsutvikling og sammenligninger

- Flyten var 47–58 kt per år fram til 2018 og 53–54 kt i 2022–2025, i takt med tekstilene i restavfallet.
- Kasserte tepper falt fra 20 kt rundt 1990 til 11–13 kt etter 2005, fordi teppeimporten falt på 1990-tallet og levetiden er lang.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 36 % | 31 % | 24 % | 24 % | 24 % | 24 % |
| Klær, hjemmetekstiler og sko | 54 % | 55 % | 54 % | 49 % | 43 % | 43 % |
| Andre konfeksjonerte varer | 3 % | 5 % | 9 % | 11 % | 16 % | 16 % |
| Presenninger og telt | 7 % | 9 % | 13 % | 16 % | 17 % | 17 % |

### Materiale (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For tepper, presenninger og andre konfeksjonerte varer: utstrømmen av en årgangsmodell av salget.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 29 % | 31 % | 29 % | 24 % | 23 % | 23 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 20 % | 19 % | 19 % | 19 % | 18 % | 18 % |
| Andre fibre | 2 % | 3 % | 4 % | 4 % | 4 % | 4 % |
| Syntetisk | 40 % | 37 % | 41 % | 46 % | 48 % | 48 % |
| Ull | 5 % | 7 % | 6 % | 5 % | 5 % | 5 % |

<iframe src="../output_files/plots/pages/us_hh_wm_rs_worn_textiles_in_residual_and_bulky_waste_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `residual_core` | 35 % | 84 % | 72 % |
| `reusable_share_residual` | 2 % | 4 % | 15 % |
| `institutional_share` | 1 % | 2 % | 5 % |
| `residual_non_core_share` | 1 % | 3 % | 3 % |
| `08801_classification:import:finished` | – | 1 % | 3 % |
| `gap: residual_core` | 44 % | 3 % | – |
| `gap: reusable_share_residual` | 13 % | 2 % | – |
| `lifetime_mean_US.HH_CA` | 4 % | 1 % | – |
| Halvt 95 %-intervall, førsteordens (kt) | 16.38 | 10.12 | 8.36 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 16.58 | 10.56 | 8.37 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_worn_residual_waste_mc` i `calculations/us_mc.py`. Dokumentasjonen i koden:

> CORE: residual textiles that are not reusable. CA, TA and OM: the
> outflow of a cohort model of the goods sold to households, with Weibull
> lifetimes (carpets 10, tarpaulins and tents 4, other made-up articles 2
> years), because there are no discard statistics for them (an exception
> to D8). Sacks (SA) are not used by households (D13).
>
> `_other_goods_discards`: Outflow of the household cohort model for CA, TA and OM, array (year, product).
>
> `_residual_core`: CL+HT+FW in household residual and bulky waste from pick analyses: 2009
> (Laitala et al. 2012), 2018, 2022 and 2025 (Mepex, via Watson et al. 2020
> and NORSUS 2023 and 2026), interpolated between them. Waste delivered at
> recycling stations in 2018 and 2009 is set at its 2022-2025 ratio to
> kerbside waste (0.51): the 2018 figure (6.1 kt) rests on three pick
> analyses, and NORSUS (Rubach et al. 2023) considers it too low (D40).
> SSB's textile
> accounts for 1998 (58.5 kt) are not used as a level: the clothing in the
> waste in 1991 and 1998 (34.8 and 47.2 kt) is nearly equal to net
> clothing imports those years (34.5 and 46.6 kt), so it was probably
> calculated from the supply, and it would make the stock shrink in the
> early 1990s.
>
> The 2018 study left footwear and leather clothing out of its scope,
> while the 2022 and 2025 pick analyses include footwear, and the
> separate collection (exports of 6309+6310) includes it in every year.
> Footwear thrown away in residual waste in 2018 is therefore added to
> the 2018 anchor: 7.5 kt (5-10, uniform), estimated from about 13 kt of
> footwear supplied per year minus 3-4 kt collected, with the 12.3 kt
> non-recyclable category of 2025 as upper bound (D42).
>
> The pick analyses count every textile article picked out of the waste,
> not only CL+HT+FW. In the Wasted Textiles analyses of 2021-2022
> (Syversen et al. 2023, Mepex/SIFO, table 18) "non-clothing other"
> (storage and packaging, sports and outdoor equipment, bags and
> backpacks, toys, hygiene articles) is 8 % of the textiles in kerbside
> residual waste and 20 % at recycling stations, about 12 % of the
> anchors. These goods are outside the CORE group (bags, HS 4202, are
> outside the system; the rest is OM or outside chapters 50-64), and OM,
> CA and TA in residual waste come from their own cohort model, so the
> share is taken out of every anchor before the missing footwear is added
> to 2018 (D44): 0.12 (0.06-0.18, uniform), since the composition rests on
> three regions and Mepex does not describe what its database counts as
> textiles. The anchors of 2009 and 2018 get the same share. Carpets,
> tarpaulins and garden textiles at recycling stations (27 % of the
> textiles found there, weighed apart in Wasted Textiles) may also be in
> the anchors; that is tested in structural_sensitivity.py, not removed.
>
> Before 2009 there are no pick analyses. The waste per inhabitant is held
> at the 2009 level, plus what was not yet collected separately: the
> separate collection per inhabitant in 2009 minus that of the year, times
> the population (D40). Textiles that were later collected went to residual
> waste before collection grew, so households did not discard less per
> inhabitant in 1990 than in 2009.
