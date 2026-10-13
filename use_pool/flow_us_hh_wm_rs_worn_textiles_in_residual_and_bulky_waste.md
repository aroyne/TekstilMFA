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
| Kandidatdata | Pick analyses (Mepex/Avfall Norge) x SSB household waste amounts; SSB 10513; Reusable share of pick analyses: Laitala et al. 2012 (via Huygens et al. 2023), Rubach et al. 2023, de Sadeleer & Rubach 2026 |
| Merknad | D18. CORE residual textiles not reusable, plus CA/TA/OM discarded in the year supplied |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_wm_rs_worn_textiles_in_residual_and_bulky_waste.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT** er tekstiler i husholdningenes restavfall og grovavfall som ikke kan brukes om igjen (form WRN, D18): utslitte klær, hjemmetekstiler og sko, og alle tepper, presenninger, telt og andre konfeksjonerte varer som kasseres.

#### Datakilder (og hvordan kildetallene er produsert)

- CORE: tekstiler i restavfall og grovavfall fra plukkanalysene minus den brukbare delen (se US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT).
- Tepper, presenninger og andre konfeksjonerte varer: salget til husholdningene samme år (DI.RT-US.HH-Sales to households-TOT).

#### Antakelser

- Tepper, presenninger og andre konfeksjonerte varer har ikke kasseringsstatistikk og kasseres samme år som de kjøpes (ingen lagerendring). Sekker brukes ikke av husholdninger (D13).

#### Sammensetning (varetype og materiale)

- CORE falt fra 66 % i 1990 til 45 % i 2022. Tepper er 23–24 %, og presenninger og andre konfeksjonerte varer økte.
- CORE har utstrømmen fra årgangsmodellen, og de andre varetypene har sammensetningen til salget samme år. Syntetisk økte fra 35 % i 1990 til 49 % i 2022.

#### Tidsutvikling og sammenligninger

- Flyten falt fra 68 kt i 1988 til 46 kt i 2009 og økte til 56–59 kt i 2022–2025, i takt med tekstilene i restavfallet.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 24 % | 18 % | 26 % | 27 % | 23 % | 23 % |
| Klær, hjemmetekstiler og sko | 66 % | 68 % | 51 % | 41 % | 45 % | 48 % |
| Andre konfeksjonerte varer | 3 % | 5 % | 9 % | 13 % | 15 % | 16 % |
| Presenninger og telt | 7 % | 8 % | 14 % | 19 % | 16 % | 12 % |

### Materiale (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For andre produkter: tilførselssammensetningen samme år.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 34 % | 38 % | 27 % | 22 % | 23 % | 25 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 19 % | 17 % | 19 % | 18 % | 17 % | 17 % |
| Andre fibre | 2 % | 3 % | 4 % | 4 % | 3 % | 3 % |
| Syntetisk | 35 % | 32 % | 43 % | 49 % | 49 % | 47 % |
| Ull | 6 % | 7 % | 5 % | 5 % | 5 % | 6 % |

<iframe src="../output_files/plots/pages/us_hh_wm_rs_worn_textiles_in_residual_and_bulky_waste_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_worn_residual_waste_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L48). Dokumentasjonen i koden:

> CORE: residual textiles that are not reusable. CA, TA and OM: discarded
> in the year supplied. Sacks (SA) are not used by households (D13).
>
> `_residual_core`: CL+HT+FW in household residual and bulky waste, SSB and Mepex pick analyses (D15).
