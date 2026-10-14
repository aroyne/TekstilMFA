---
layout: default
title: Domestic hand knitting yarn
parent: Fibre and yarn production (MA.FI)
grand_parent: 3. Manufacturing (MA)
nav_order: 2
---

# Domestic hand knitting yarn

| | |
|---|---|
| Flytkode | `MA.FI-DI.RT-Domestic hand knitting yarn-TOT` |
| Fra | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Til | [Wholesale and retail (DI.RT)](../distribution_pool/subpool_di_rt.html) |
| Tekstilform | FIB – fibre og garn |
| Dimensjoner | år × produkt |
| Metode | data |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | SSB Industristatistikk Varetall 1988-1989 (5109.10) and SSB 10455 (Prodcom 13.10.50.50, 2008-2023 with gaps), large units only; SNL (about 1000 t per year); Sandnes Garn (about 600 t) |
| Merknad | Product YA only. Interpolated over 1990-2007, when SSB published no commodity figures. Uncertainty skewed upwards because small units are missing |

## Tidsserie

<iframe src="../output_files/plots/pages/ma_fi_di_rt_domestic_hand_knitting_yarn.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **MA.FI-DI.RT-Domestic hand knitting yarn-TOT** er garn spunnet i Norge og pakket for detaljsalg (produkt YA). Det selges til husholdningene gjennom handelen.
- Håndstrikkegarn er den klart største produktgruppen til norske spinnerier.

#### Datakilder (og hvordan kildetallene er produsert)

- 1988 og 1989: SSB, Industristatistikk, Hefte II Varetall (NOS B 941 og B 998), varenummer 5109.1001 og 5109.1002 (ullgarn i detaljopplegg) for store bedrifter: 993 og 893 t. Tallene er lest manuelt fra skannede sider.
- 2008–2023: SSB 10455 (Prodcom), kode 13.10.50.50, solgt produksjon av ullgarn i detaljsalg for store foretak: 0,59–1,03 kt. Mange år er skjult av SSB.
- SSB publiserte ingen varetall for 1990–2007. Bomulls- og syntetisk garn i detaljsalg er skjult i alle år.
- Til kontroll: SNL oppgir omtrent 1 000 t håndstrikkegarn per år fra norske spinnerier, og Sandnes Garn lager omtrent 600 t.

#### Antakelser

- År uten tall interpoleres, og verdien holdes fast etter 2023.
- Statistikken dekker bare store enheter, så usikkerheten er skjevfordelt oppover (−10 / +50 %).

#### Sammensetning (varetype og materiale)

- Varetype: garn i detaljsalg (YA). Det hører til produktgruppen CORE etter bruk, fordi hjemmelagde plagg kasseres som klær.
- Materialet er ull (WO), fordi varenummer og Prodcom-kode gjelder ullgarn.

#### Tidsutvikling og sammenligninger

- Produksjonen har vært forholdsvis stabil på 0,6–1,0 kt per år. Den var 1,0 kt i 1988, 0,6 kt i 2018–2019 og 1,1 kt i 2021, da det ble strikket mye under pandemien.
- Eksporten av detaljgarn (via DI.RT) har økt fra 0,7 kt i 2018 til 2,1 kt i 2025. Noe av dette er trolig norskprodusert garn.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Garn i detaljsalg | 100 % | 100 % | 100 % | 100 % | 100 % | 100 % |

### Materiale (fiberlag, D19)

Ull (WO): Prodcom-koden og varenummeret gjelder ullgarn.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Ull | 100 % | 100 % | 100 % | 100 % | 100 % | 100 % |

<iframe src="../output_files/plots/pages/ma_fi_di_rt_domestic_hand_knitting_yarn_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_domestic_hand_knitting_yarn_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L107). Dokumentasjonen i koden:

> Yarn spun in Norway and put up for retail sale (product YA), sold to
> households through retail; hand knitting yarn is by far the largest
> product of the Norwegian spinning mills. Wool yarn put up for retail
> sale produced in large establishments: 0.99 and 0.89 kt in 1988 and 1989
> (SSB Industristatistikk, Varetall, commodity 5109.10), and 0.59-1.03 kt
> in 2008-2023 (SSB 10455, Prodcom 13.10.50.50, sold production). SSB
> published no commodity figures for 1990-2007, and suppresses some
> Prodcom years; those years are interpolated, and the series is held at
> its last value after 2023, with uncertainty growing with the distance
> to a published year (D30). Both sources cover large units only (Sandnes
> Garn alone makes about 600 t a year, and SNL gives about 1000 t for all
> Norwegian spinning mills), so the noise factor is skewed upwards. Cotton
> and synthetic yarn put up for retail sale are suppressed in every year
> and are left out.
