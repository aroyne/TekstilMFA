---
layout: default
title: Tumble dryer lint
parent: Households (US.HH)
grand_parent: 5. Use (US)
nav_order: 6
---

# Tumble dryer lint

| | |
|---|---|
| Flytkode | `US.HH-WM.RS-Tumble dryer lint-TOT` |
| Fra | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Til | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Tekstilform | MFR – mikrofibre |
| Dimensjoner | år × produktgruppe |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | Laundry mass x households with a tumble dryer (SSB via SNL: 44 % 1996, 47 % 2012) x share of loads dried x release in drying (Cummins et al. 2023, 256-342 ppm) x share caught on the filter (86-91 %) |
| Merknad | Mostly cotton (Lant et al. 2022). Emptied into residual waste; counted as fines, not textile, in pick analyses, so not double counted (D37) |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_wm_rs_tumble_dryer_lint.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.HH-WM.RS-Tumble dryer lint-TOT** er lo som fanges i filteret i tørketrommelen, og som tømmes i restavfallet.
- Lo er korte fibre som er slitt løs fra tekstilene, mest bomull.

#### Datakilder (og hvordan kildetallene er produsert)

- Tøymengden er som for vask: 280 kg per innbygger per år × folketallet.
- Andelen husholdninger med tørketrommel er 44 % i 1996 og 47 % i 2012 (SSBs forbruksundersøkelse, gjengitt i Store norske leksikon). Nyere tall er ikke funnet.
- Cummins m.fl. (2023) målte utslipp ved tørking av ekte skittentøy: 256 mg/kg i trommel med avtrekk og 342 mg/kg i kondenstrommel. Filteret fanget 86 % og 91 %.
- Lant m.fl. (2022) fant at 83–96 % av loet fra et stoff med 48 % bomull var bomull.

#### Antakelser

- 60 % (40–80 %, flat fordeling) av vaskene i husholdninger med trommel tørkes i den.
- Andelen med trommel holdes på 1996-nivå før og på 2012-nivå etter, med økende usikkerhet (D30).
- Plukkanalysene teller lo som finstoff, ikke som tekstil, så flyten kommer i tillegg til restavfallsankrene.

#### Sammensetning (varetype og materiale)

- Flyten er i produktgruppen CORE.
- Materialet er tekstillageret i årgangsmodellen, vektet med utslipp per kg: ca. 74 % bomull og under 4 % syntetisk i 2025. Det stemmer med Lant m.fl. (2022).

#### Tidsutvikling og sammenligninger

- 0,08 kt i 1988 og 0,11 kt i 2025 (0,03–0,31). Intervallet er bredt etter 2012, fordi andelen med trommel ikke er kjent.
- Loet er av samme størrelse som utslippet til avløp ved vask (forholdet er 0,7, mot 1,4–3 i forsøkene, som bare gjelder vasker som tørkes).
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
| Bomull | 80 % | 80 % | 81 % | 75 % | 73 % | 73 % |
| Regenerert cellulose | 5 % | 4 % | 4 % | 5 % | 5 % | 5 % |
| Andre fibre | 1 % | 2 % | 2 % | 3 % | 4 % | 3 % |
| Syntetisk | 2 % | 2 % | 3 % | 3 % | 4 % | 4 % |
| Ull | 11 % | 12 % | 10 % | 13 % | 15 % | 15 % |

<iframe src="../output_files/plots/pages/us_hh_wm_rs_tumble_dryer_lint_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `gap: dryer_ownership_share` | 7 % | 4 % | 63 % |
| `tumble_dried_share` | 46 % | 48 % | 18 % |
| `laundry_kg_per_capita` | 33 % | 34 % | 13 % |
| `drying_release_ppm` | 10 % | 10 % | 4 % |
| `dryer_ownership_share` | 4 % | 4 % | 2 % |
| Halvt 95 %-intervall, førsteordens (kt) | 0.04 | 0.05 | 0.09 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 0.04 | 0.05 | 0.09 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_tumble_dryer_lint_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L198). Dokumentasjonen i koden:

> Lint caught on the filter of tumble dryers, 88 % (86-91 %, Cummins et
> al. 2023) of the fibres released in drying (D37). The filter is emptied
> into residual waste, so the lint goes to WM.RS. Pick analyses count it
> as fines, not textile, so it is not in the residual waste anchors. It
> is mostly cotton (83-96 % on the filter from a 48 % cotton fabric, Lant
> et al. 2022), which the fibre layer gives through the higher release per
> kg of natural fibres. The rest goes to air (vented dryers) and is added
> to the release to air.
>
> `_tumble_drying_release`: Fibres released in tumble drying (kt), array (year,): laundry times the
> share of households with a tumble dryer (44 % in 1996 and 47 % in 2012,
> SSB via Store norske leksikon; held before and after) times the share of
> their loads that are dried (0.6, 0.4-0.8, assumption) times the release
> in drying, 300 mg per kg (256 for vented and 342 for condenser dryers,
> Cummins et al. 2023, real soiled laundry).
