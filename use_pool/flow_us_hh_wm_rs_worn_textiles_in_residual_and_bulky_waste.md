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

- CORE: tekstiler i restavfall og grovavfall fra plukkanalysene minus den brukbare delen (se US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT).
- Tepper, presenninger og andre konfeksjonerte varer: utstrømmen av en årgangsmodell av salget til husholdningene, med levetider fra `parameters/lifetimes.csv` (tepper 10 år, presenninger og telt 4 år, andre konfeksjonerte varer 2 år; Napolano m.fl. 2025 og van Oorschot m.fl. 2020).

#### Antakelser

- Tepper, presenninger og andre konfeksjonerte varer har ikke kasseringsstatistikk, så kasseringene beregnes med årgangsmodellen. Det er et unntak fra D8 (D28). Innstrømmen før 1988 holdes på 1988-nivå (D2).
- Restavfallet for CORE holdes fast per innbygger før 2009 (se US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT).
- Sekker brukes ikke av husholdninger (D13).

#### Sammensetning (varetype og materiale)

- CORE falt fra 66 % i 1990 til 45 % i 2022. Tepper er 23–24 %, og presenninger og andre konfeksjonerte varer økte.
- CORE har utstrømmen fra årgangsmodellen for nye varer, og de andre varetypene utstrømmen fra årgangsmodellen for salget. Syntetisk økte fra 35 % i 1990 til 49 % i 2022.

#### Tidsutvikling og sammenligninger

- Flyten var 44–47 kt per år fram til 2018 og økte til 56–57 kt i 2022–2025, i takt med tekstilene i restavfallet.
- Kasserte tepper falt fra 20 kt rundt 1990 til 11–13 kt etter 2005, fordi teppeimporten falt på 1990-tallet og levetiden er lang.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 43 % | 34 % | 24 % | 27 % | 22 % | 22 % |
| Klær, hjemmetekstiler og sko | 45 % | 50 % | 53 % | 43 % | 47 % | 47 % |
| Andre konfeksjonerte varer | 4 % | 5 % | 9 % | 12 % | 15 % | 15 % |
| Presenninger og telt | 8 % | 11 % | 14 % | 18 % | 16 % | 16 % |

### Materiale (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For tepper, presenninger og andre konfeksjonerte varer: utstrømmen av en årgangsmodell av salget.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 26 % | 30 % | 29 % | 23 % | 24 % | 23 % |
| Regenerert cellulose | 3 % | 2 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 21 % | 19 % | 19 % | 18 % | 17 % | 17 % |
| Andre fibre | 3 % | 4 % | 4 % | 4 % | 4 % | 4 % |
| Syntetisk | 42 % | 37 % | 40 % | 47 % | 47 % | 48 % |
| Ull | 6 % | 8 % | 6 % | 6 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/us_hh_wm_rs_worn_textiles_in_residual_and_bulky_waste_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_worn_residual_waste_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L87). Dokumentasjonen i koden:

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
> and NORSUS 2023 and 2026), interpolated between them. Before 2009 the
> waste per inhabitant is held at the 2009 level. SSB's textile accounts
> for 1998 (58.5 kt) are not used as a level: the clothing in the waste in
> 1991 and 1998 (34.8 and 47.2 kt) is nearly equal to net clothing imports
> those years (34.5 and 46.6 kt), so it was probably calculated from the
> supply, and it would make the stock shrink in the early 1990s.
