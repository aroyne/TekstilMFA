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

- Tekstiler i restavfall og grovavfall (CORE): plukkanalyser fra Mepex og kommunene, via Watson m.fl. (2020) for 2018 (31,6 kt, i modellen 38,3 kt med gjenvinningsstasjonene etter D40 og + 7,5 kt sko etter D42, fordi studien holdt sko utenfor), Rubach m.fl. (2023) for 2022 (48,8 kt) og de Sadeleer & Rubach (2026) for 2025 (44,5 kt). For 2009 brukes Laitala m.fl. (2012), 5,6 kg per innbygger i restavfallet (40,7 kt med gjenvinningsstasjonene etter D40).
- **Varer utenfor CORE trekkes fra (D44):** Plukkanalysene teller alle tekstilvarer. «Ikke-klær annet» (oppbevaring, utstyr, vesker og sekker, leker, hygieneartikler) er 8 % av tekstilene i hentet restavfall og 20 % på gjenvinningsstasjonene (Syversen m.fl. 2023, tabell 18). Derfor trekkes 12 % (6–18 %) fra alle ankrene, før skoene legges til 2018.
- I en plukkanalyse sorteres et utvalg restavfall fra husholdninger, og andelen tekstiler skaleres opp med kommunenes avfallsmengder.
- Andel brukbart: Laitala m.fl. (2012) for Oslo 2010–2011 (27,5 %), Rubach m.fl. (2023) for 2022 (45 %, bare hentet restavfall) og de Sadeleer & Rubach (2026) for 2025 (40 %).

#### Antakelser

- Mengden og andelen interpoleres mellom ankerpunktene. Andelen holdes fast før 2011.
- **Før 2009 er restavfallet per innbygger 2009-nivået pluss det som ennå ikke ble samlet inn separat** (innsamling per innbygger i 2009 minus innsamlingen det året, D40; befolkning fra SSB 05803). Det som senere ble samlet inn, gikk i restavfallet før innsamlingen vokste. SSBs avfallsregnskap for tekstiler for 1998 (58,5 kt) brukes ikke som nivå: klærne i avfallet i 1991 og 1998 (34,8 og 47,2 kt) er nesten like store som nettoimporten av klær de samme årene (34,5 og 46,6 kt), så tallene er trolig beregnet ut fra tilførselen og ikke målt. De ville også gitt et krympende lager tidlig på 1990-tallet. Fast mengde per innbygger er den enkleste antakelsen uten målinger, men gir et høyt lager (se tidsutviklingen).
- Usikkerhet: 30–40 % på mengden og 0,2–0,6 (absolutt) på andelen.
- Det er ukjent hva Mepex regner som tekstiler i databasen bak ankrene. Andelen utenfor CORE bygger på tre regioner i 2021–2022 og brukes også for 2009 og 2018. Gulvtepper, presenninger og hagetekstiler på gjenvinningsstasjonene (27 % av tekstilene der) kan også være med. Det testes i strukturkjøringen `large_items_residual` (+134 kt i lageret i 2025, +2,7 prosentpoeng i innsamlingsgraden).
- Andre varetyper (tepper, presenninger, andre konfeksjonerte varer) regnes som utslitte.

#### Sammensetning (varetype og materiale)

- Bare CORE.
- Materialet er utstrømmen fra årgangsmodellen. Brukbart og utslitt har samme sammensetning.

#### Tidsutvikling og sammenligninger

- Flyten var 9,5–12,4 kt per år fram til 2011 og økte til 19,2 kt i 2022 og 15,4 kt i 2025.
- Økningen etter 2011 kommer både fra mer tekstiler i restavfallet og fra høyere andel brukbart i de nye plukkanalysene.
- Med fyllregelen fra D40 er lagerendringen i husholdningene 10–26 kt per år på 1990-tallet, og lageret (restleddet) blir 1 220 kt i 2025 (495–1 871), ca. 218 kg per innbygger, når også 2018- og 2009-ankrene har forholdet for gjenvinningsstasjoner fra 2022–2025 (D40). Med sko i 2018-ankeret (D42) er det 1 169 kt (440–1 816), og når varene utenfor CORE trekkes fra (D44), er det 1 363 kt (680–1 959), ca. 244 kg per innbygger. Med fast restavfall per innbygger og de gamle ankrene var det 1 617 kt.
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
| Bomull | 43 % | 44 % | 41 % | 37 % | 35 % | 35 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 18 % | 17 % | 19 % | 18 % | 18 % | 18 % |
| Andre fibre | 1 % | 1 % | 1 % | 1 % | 2 % | 2 % |
| Syntetisk | 30 % | 30 % | 32 % | 36 % | 38 % | 38 % |
| Ull | 6 % | 6 % | 5 % | 5 % | 5 % | 6 % |

<iframe src="../output_files/plots/pages/us_hh_wm_rs_reusable_textiles_in_residual_and_bulky_waste_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `residual_core` | 19 % | 63 % | 65 % |
| `reusable_share_residual` | 8 % | 23 % | 32 % |
| `residual_non_core_share` | – | 2 % | 3 % |
| `gap: reusable_share_residual` | 48 % | 10 % | – |
| `gap: residual_core` | 24 % | 2 % | – |
| Halvt 95 %-intervall, førsteordens (kt) | 8.40 | 4.44 | 5.80 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 8.39 | 4.44 | 5.59 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_reusable_residual_waste_mc` i `calculations/us_mc.py`. Dokumentasjonen i koden:

> Part of the CORE residual textiles that could have been reused (D18),
> share from the pick analyses. The analyses cover CL+HT+FW only, so the
> other products are 0 here and counted as worn.
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
