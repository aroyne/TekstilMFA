---
layout: default
title: Reusable textiles in residual and bulky waste
parent: Households (US.HH)
grand_parent: 5. Use (US)
nav_order: 2
---

# Reusable textiles in residual and bulky waste

| | |
|---|---|
| Flytkode | `US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT` |
| Fra | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Til | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Tekstilform | USE – brukte, ombrukbare |
| Dimensjoner | år × produktgruppe |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Pick analyses (Mepex/Avfall Norge) x SSB household waste amounts; Reusable share of pick analyses: Laitala et al. 2012 (via Huygens et al. 2023), Rubach et al. 2023, de Sadeleer & Rubach 2026 |
| Merknad | D18. CORE group only: residual textiles x reusable share; CA/TA/OM are counted as worn |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_wm_rs_reusable_textiles_in_residual_and_bulky_waste.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT** er klær, hjemmetekstiler og sko i husholdningenes restavfall og grovavfall som kunne vært brukt om igjen (form USE, D18).

#### Datakilder (og hvordan kildetallene er produsert)

- Tekstiler i restavfall og grovavfall (CORE): plukkanalyser fra Mepex og kommunene, via Watson m.fl. (2020) for 2018 (31,6 kt), Rubach m.fl. (2023) for 2022 (48,8 kt) og de Sadeleer & Rubach (2026) for 2025 (44,5 kt). For 2009 brukes Laitala m.fl. (2012), 5,6 kg per innbygger i restavfallet (33,5 kt med gjenbruksstasjoner).
- I en plukkanalyse sorteres et utvalg restavfall fra husholdninger, og andelen tekstiler skaleres opp med kommunenes avfallsmengder.
- Andel brukbart: Laitala m.fl. (2012) for Oslo 2010–2011 (27,5 %), Rubach m.fl. (2023) for 2022 (45 %, bare hentet restavfall) og de Sadeleer & Rubach (2026) for 2025 (40 %).

#### Antakelser

- Mengden og andelen interpoleres mellom ankerpunktene. Andelen holdes fast før 2011.
- **Før 2009 holdes restavfallet per innbygger fast på 2009-nivået** (befolkning fra SSB 05803). SSBs avfallsregnskap for tekstiler for 1998 (58,5 kt) brukes ikke som nivå: klærne i avfallet i 1991 og 1998 (34,8 og 47,2 kt) er nesten like store som nettoimporten av klær de samme årene (34,5 og 46,6 kt), så tallene er trolig beregnet ut fra tilførselen og ikke målt. De ville også gitt et krympende lager tidlig på 1990-tallet. Fast mengde per innbygger er den enkleste antakelsen uten målinger, men gir et høyt lager (se tidsutviklingen).
- Usikkerhet: 30–40 % på mengden og 0,2–0,6 (absolutt) på andelen.
- Andre varetyper (tepper, presenninger, andre konfeksjonerte varer) regnes som utslitte.

#### Sammensetning (varetype og materiale)

- Bare CORE.
- Materialet er utstrømmen fra årgangsmodellen. Brukbart og utslitt har samme sammensetning.

#### Tidsutvikling og sammenligninger

- Flyten var 7,9–9,2 kt per år fram til 2011 og økte til 21,9 kt i 2022 og 17,8 kt i 2025.
- Økningen etter 2011 kommer både fra mer tekstiler i restavfallet og fra høyere andel brukbart i de nye plukkanalysene.
- Med fast restavfall per innbygger før 2009 blir lagerendringen i husholdningene 24–36 kt per år på 1990-tallet, og lageret (restleddet) blir omtrent 275 kg per innbygger i 2018–2025. Det er mer enn garderobestudiene tilsier, og et diskusjonspunkt.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Klær, hjemmetekstiler og sko | 100 % | 100 % | 100 % | 100 % | 100 % | 100 % |

### Materiale (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For tepper, presenninger og andre konfeksjonerte varer: utstrømmen av en årgangsmodell av salget.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 45 % | 47 % | 44 % | 40 % | 37 % | 36 % |
| Regenerert cellulose | 3 % | 2 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 17 % | 16 % | 19 % | 18 % | 17 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 2 % |
| Syntetisk | 27 % | 26 % | 30 % | 33 % | 36 % | 37 % |
| Ull | 6 % | 6 % | 5 % | 5 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/us_hh_wm_rs_reusable_textiles_in_residual_and_bulky_waste_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_reusable_residual_waste_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L76). Dokumentasjonen i koden:

> Part of the CORE residual textiles that could have been reused (D18),
> share from the pick analyses. The analyses cover CL+HT+FW only, so the
> other products are 0 here and counted as worn.
>
> `_residual_core`: CL+HT+FW in household residual and bulky waste from pick analyses: 2009
> (Laitala et al. 2012), 2018, 2022 and 2025 (Mepex, via Watson et al. 2020
> and NORSUS 2023 and 2026), interpolated between them. Before 2009 the
> waste per inhabitant is held at the 2009 level. SSB's textile accounts
> for 1998 (58.5 kt) are not used as a level: the clothing in the waste in
> 1991 and 1998 (34.8 and 47.2 kt) is nearly equal to net clothing imports
> those years (34.5 and 46.6 kt), so it was probably calculated from the
> supply, and it would make the stock shrink in the early 1990s.
