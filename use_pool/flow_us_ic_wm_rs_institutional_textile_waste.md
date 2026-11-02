---
layout: default
title: Institutional textile waste
parent: Institutions and businesses (US.IC)
grand_parent: 5. Use (US)
nav_order: 2
---

# Institutional textile waste

| | |
|---|---|
| Flytkode | `US.IC-WM.RS-Institutional textile waste-TOT` |
| Fra | [Institutions and businesses (US.IC)](../use_pool/subpool_us_ic.html) |
| Til | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Tekstilform | MIX – brukte, usortert |
| Dimensjoner | år × produkt |
| Metode | stock_model |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | Cohort model of sales to institutions and businesses with lifetimes per product (parameters/lifetimes.csv); SSB 10513 cannot separate textiles from mixed business waste |
| Merknad | No discard statistics for the sector, so an exception to D8 (D29). Sacks discarded in the year supplied (D13) |

## Tidsserie

<iframe src="../output_files/plots/pages/us_ic_wm_rs_institutional_textile_waste.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.IC-WM.RS-Institutional textile waste-TOT** er kasserte tekstiler fra bedrifter og offentlig sektor: arbeidsklær, uniformer og vernesko, institusjonstekstiler (sengetøy, håndklær), tepper i næringsbygg, presenninger og markiser, andre konfeksjonerte varer og sekker.

#### Datakilder (og hvordan kildetallene er produsert)

- Det finnes ingen kasseringsstatistikk for sektoren. I SSBs avfallsregnskap (10513) ligger tekstiler fra næringslivet mest i blandet avfall og kan ikke skilles ut. NORSUS (Rubach m.fl. 2023) fikk heller ikke data fra private avfallsaktører eller vaskerier.
- Flyten beregnes derfor med en årgangsmodell av salget til institusjoner og bedrifter (DI.RT-US.IC-Sales to institutions and businesses-TOT), et unntak fra D8 (D29).

#### Antakelser

- Weibull-levetider (form 2) per varetype i `parameters/lifetimes.csv`: arbeidsklær 3 år (2–4; ECAP 2017/WRAP 2015, van Oorschot m.fl. 2020), vernesko 2 år (1–3), institusjonstekstiler 2 år (1–4), tepper 10 år (5–15), presenninger og markiser 5 år (3–8) og andre konfeksjonerte varer 2 år (1–3). Alle unntatt arbeidsklær er antakelser.
- Innstrømmen før 1988 holdes på 1988-nivå (D2).
- Sekker er emballasje og kastes samme år (D13).
- Det som gjenvinnes hos NTG fra 2024 (0,05–0,2 kt hjemmetekstiler), trekkes fra (D34). Resten går til restavfall (WM.RS). Innsamling fra institusjoner er ikke implementert.

#### Sammensetning (varetype og materiale)

- Sekker økte fra 21 % i 1990 til 47 % i 2022. Klær er 23–31 %.
- Materialet er utstrømmen av årgangsmodellen, altså sammensetningen til det som ble kjøpt tidligere. Sekker har sammensetningen til salget samme år.

#### Tidsutvikling og sammenligninger

- Flyten følger salget med et lite etterslep: 13 kt i 1990, 23 kt i 2008 (salg 25 kt) og 28–30 kt i 2018–2025.
- Lageret i US.IC endrer seg lite (−1 til +1,4 kt per år), fordi levetidene er korte.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Med og uten sekker

Sekker (SA) er emballasje (D13) og kan dominere flyten. Kt per år, median med 95 %-intervall i parentes. Summen uten sekker er regnet per iterasjon.

| År | I alt | Sekker | Uten sekker | Sekkenes andel |
|---|---|---|---|---|
| 1990 | 11.20 (6.64–16.06) | 2.76 (2.55–2.97) | 8.47 (3.86–13.17) | 25 % |
| 2000 | 16.46 (11.01–21.97) | 6.47 (6.00–6.95) | 9.95 (4.56–15.47) | 39 % |
| 2010 | 21.23 (14.24–28.58) | 8.45 (7.82–9.09) | 12.81 (5.81–19.92) | 40 % |
| 2018 | 25.35 (18.18–32.68) | 12.50 (11.64–13.55) | 12.79 (5.78–19.84) | 49 % |
| 2022 | 26.67 (19.51–33.92) | 13.90 (12.88–14.98) | 12.73 (5.77–19.65) | 52 % |
| 2025 | 25.18 (18.31–32.35) | 13.16 (12.23–14.19) | 12.05 (5.33–18.76) | 52 % |

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 19 % | 10 % | 6 % | 5 % | 5 % | 5 % |
| Klær | 30 % | 28 % | 29 % | 23 % | 21 % | 21 % |
| Sko | 10 % | 8 % | 9 % | 7 % | 6 % | 6 % |
| Hjemmetekstiler | 12 % | 10 % | 12 % | 10 % | 9 % | 8 % |
| Andre konfeksjonerte varer | 2 % | 2 % | 2 % | 2 % | 3 % | 4 % |
| Sekker | 25 % | 39 % | 40 % | 49 % | 52 % | 52 % |
| Presenninger og telt | 4 % | 3 % | 3 % | 3 % | 4 % | 4 % |

### Materiale (fiberlag, D19)

Utstrømmen av en årgangsmodell av salget til institusjoner og bedrifter. Sekker har tilførselssammensetningen samme år.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 26 % | 24 % | 23 % | 16 % | 14 % | 14 % |
| Regenerert cellulose | 3 % | 2 % | 1 % | 1 % | 1 % | 1 % |
| Ikke-tekstil | 15 % | 12 % | 12 % | 11 % | 10 % | 10 % |
| Andre fibre | 3 % | 2 % | 3 % | 2 % | 3 % | 2 % |
| Syntetisk | 50 % | 57 % | 58 % | 67 % | 70 % | 71 % |
| Ull | 3 % | 4 % | 3 % | 2 % | 2 % | 2 % |

<iframe src="../output_files/plots/pages/us_ic_wm_rs_institutional_textile_waste_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

## Beregning i koden

Beregnes i `_institutional_waste_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L184). Dokumentasjonen i koden:

> Goods discarded by institutions and businesses: the outflow of a cohort
> model of the goods sold to them, with Weibull lifetimes per product
> (workwear 3, footwear 2, institutional linen 2, carpets 10, tarpaulins
> and awnings 5 and other made-up articles 2 years; all but workwear are
> assumptions). There are no discard statistics for this sector: textiles
> from businesses are mostly in mixed waste in SSB's waste accounts.
> Sacks (SA) are packaging and are discarded in the year they are
> supplied (D13), and retail yarn is not sold to this sector.
