---
layout: default
title: Unsold goods discarded
parent: Wholesale and retail (DI.RT)
grand_parent: 4. Distribution (DI)
nav_order: 4
---

# Unsold goods discarded

| | |
|---|---|
| Flytkode | `DI.RT-WM.RS-Unsold goods discarded-TOT` |
| Fra | [Wholesale and retail (DI.RT)](../distribution_pool/subpool_di_rt.html) |
| Til | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | Share of clothing, household textiles and footwear placed on the market: lognormal, 95 % interval 0.2-9 % (survey minimums of Watson et al. 2020 and Rubach et al. 2023 to EEA 2024), median 1.3 % (geometric mean); SOA 2022 found at least 0.8 % overstock |
| Merknad | Clothing, household textiles and footwear (D38). Destroyed goods are commercial waste and not in the pick analyses of household waste, so there is no double counting |

## Tidsserie

<iframe src="../output_files/plots/pages/di_rt_wm_rs_unsold_goods_discarded.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **DI.RT-WM.RS-Unsold goods discarded-TOT** er usolgte klær, hjemmetekstiler og sko som produsenter og forhandlere sender til forbrenning, i stedet for å selge eller gi dem bort.

#### Datakilder (og hvordan kildetallene er produsert)

- 2018: forhandlerne som oppga mengder (16 av 44 som svarte), sendte 95 t til forbrenning (Watson m.fl. 2020).
- 2022: produsenter og forhandlere rapporterte 221 t usolgte tekstiler som ikke ble donert (Rubach m.fl. 2023).
- Tallene fra undersøkelsene er minimum, fordi de største kjedene ikke oppga mengder.
- Samfunnsøkonomisk analyse (2022) fant et overskuddslager på minst 825 t klær, ca. 0,8 % av klestilførselen. Én kjede sto for nesten 430 t.
- EEA (2024) anslår at 4–9 % av tekstilene som settes på markedet i Europa, destrueres uten å ha vært brukt.

#### Antakelser

- Flyten er en andel av det som settes på markedet (import + norsk produksjon − eksport) av klær, hjemmetekstiler og sko (D38).
- Andelen er lognormal med 95 %-intervall 0,2–9 % og median 1,3 % (geometrisk snitt av grensene). Nedre grense tilsvarer minimum fra undersøkelsene, øvre grense EEA-anslaget.
- Destruerte varer er næringsavfall og er ikke med i plukkanalysene for husholdningsavfall, så de telles ikke to ganger.
- Materialgjenvinning er ikke skilt ut, så alt går til WM.RS.

#### Sammensetning (varetype og materiale)

- Klær ca. 62 %, hjemmetekstiler 21 % og sko 17 % i 2025.
- Materialet er sammensetningen til tilførselen samme år.

#### Tidsutvikling og sammenligninger

- 0,8 kt i 1988, ca. 1,3 kt rundt 2012–2022 og 1,1 kt i 2025 (0,2–8,1). Flyten følger det som settes på markedet.
- Før D38 var flyten 0,1–0,3 kt (minimum fra undersøkelsene). Med EEA-nivået (6,5 %) blir den 4–6 kt per år, og lageret i husholdningene blir 176 kt lavere i 2025 (`structural_sensitivity.py`).
- EUs økodesignforordning (ESPR) forbyr store virksomheter å destruere usolgte klær og sko fra 19. juli 2026. Det er bare relevant for scenarier.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Klær | 58 % | 61 % | 60 % | 58 % | 60 % | 62 % |
| Sko | 18 % | 16 % | 17 % | 17 % | 17 % | 17 % |
| Hjemmetekstiler | 24 % | 22 % | 23 % | 25 % | 22 % | 21 % |

### Materiale (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 47 % | 42 % | 41 % | 33 % | 34 % | 36 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 3 % | 2 % | 2 % |
| Ikke-tekstil | 17 % | 16 % | 18 % | 18 % | 18 % | 18 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 1 % |
| Syntetisk | 29 % | 34 % | 33 % | 39 % | 39 % | 38 % |
| Ull | 3 % | 4 % | 4 % | 5 % | 4 % | 4 % |

<iframe src="../output_files/plots/pages/di_rt_wm_rs_unsold_goods_discarded_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `unsold_destroyed_share` | 100 % | 100 % | 100 % |
| Halvt 95 %-intervall, førsteordens (kt) | 3.81 | 5.13 | 3.82 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 3.92 | 5.22 | 3.96 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_unsold_goods_discarded_mc` i `calculations/di_mc.py`. Dokumentasjonen i koden:

> Unsold clothing, household textiles and footwear that producers and
> retailers send to incineration (D38): a share of what is placed on the
> market (registered imports plus finished goods made in Norway minus
> exports). The share is lognormal with 95 % interval 0.2-9 % and median
> 1.3 %, the geometric mean of the bounds (an assumption). The lower end
> is the survey minimums where the largest retailers did not report (95 t
> incinerated in 2018, Watson et al. 2020; 221 t in 2022, Rubach et al.
> 2023), and the upper end the EEA (2024) estimate that 4-9 % of textiles
> put on the market in Europe are destroyed unused. Samfunnsøkonomisk
> analyse (2022) found an overstock of at least 825 t of clothing, about
> 0.8 % of the clothing supply. Destroyed goods are commercial waste and are not in
> the pick analyses of household waste, so they are not counted twice.
> Material recycling is not split out, so all of it goes to WM.RS. Large
> enterprises may not destroy unsold clothing and footwear from 19 July
> 2026 (ESPR), which matters only for scenarios.
