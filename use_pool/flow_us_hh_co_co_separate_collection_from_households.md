---
layout: default
title: Separate collection from households
parent: Households (US.HH)
grand_parent: 5. Use (US)
nav_order: 1
---

# Separate collection from households

| | |
|---|---|
| Flytkode | `US.HH-CO.CO-Separate collection from households-TOT` |
| Fra | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Til | [Separate collection (CO.CO)](../collection_and_sorting_pool/subpool_co_co.html) |
| Tekstilform | MIX – brukte, usortert |
| Dimensjoner | år × produktgruppe |
| Metode | data |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | SSB 08801 export of HS 6309+6310 + share kept in Norway (Watson 2020, NORSUS 2023, NORSUS 2026), minus unsold goods donated by retailers |
| Merknad | Anchor years only - interpolation between anchors. Clipped at 0 if donations exceed export plus retained |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_co_co_separate_collection_from_households.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.HH-CO.CO-Separate collection from households-TOT** er brukte tekstiler (klær, hjemmetekstiler og sko) som husholdningene leverer til separat innsamling: containere, butikker og gjenbruksstasjoner.

#### Datakilder (og hvordan kildetallene er produsert)

- Innsamlet = eksport av brukte tekstiler og filler (HS 6309+6310, SSB 08801) + den delen som blir i Norge (D17) − usolgte klær som forhandlerne gir til innsamlerne (D27).
- Andelen som blir i Norge, er regnet som andel av eksporten fra de nasjonale kartleggingene: Watson m.fl. (2020) for 2018 (3,3 %), Rubach m.fl. (2023) for 2022 (2,9 %) og de Sadeleer & Rubach (2026) for 2025 (5,8 %). Kartleggingene bygger på tall fra innsamlerne.

#### Antakelser

- Nesten alt som samles inn, eksporteres usortert samme år.
- Usolgte klær fra forhandlere eksporteres sammen med de innsamlede tekstilene og trekkes derfor fra. Blir resultatet negativt, klippes det til 0.
- Andelen som blir i Norge, holdes fast før 2018 og interpoleres mellom ankerpunktene (usikkerhet ±50 %).
- Statistikken dekker klær, hjemmetekstiler og sko samlet, så flyten er bare i produktgruppen CORE.

#### Sammensetning (varetype og materiale)

- Bare CORE.
- Materialet er utstrømmen fra årgangsmodellen for husholdningene, altså det som ble kjøpt tidligere. Bomull falt fra 46 % i 1990 til 37 % i 2022, og syntetisk økte fra 27 % til 36 %. Ikke-tekstil (17 %) er mest såler fra sko.

#### Tidsutvikling og sammenligninger

- Innsamlingen økte fra 0,6 kt i 1988 til 39 kt i 2019 og var 33–36 kt i 2022–2025.
- Modellen gir mer enn kartleggingene: 36,9 kt mot 31,7 kt i 2018 (Watson), 32,3 kt mot 29,6 kt i 2022 (NORSUS) og 36,1 kt mot 33,7 kt i 2025. Forskjellen kommer fra eksporten i 08801, som trolig også omfatter filler og brukte tekstiler fra andre enn husholdningene.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Klær, hjemmetekstiler og sko | 100 % | 100 % | 100 % | 100 % | 100 % | 100 % |

### Materiale (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For andre produkter: tilførselssammensetningen samme år.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 46 % | 47 % | 44 % | 40 % | 37 % | 36 % |
| Regenerert cellulose | 3 % | 2 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 18 % | 17 % | 18 % | 17 % | 17 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 2 % |
| Syntetisk | 27 % | 26 % | 29 % | 33 % | 36 % | 37 % |
| Ull | 6 % | 6 % | 5 % | 5 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/us_hh_co_co_separate_collection_from_households_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

## Beregning i koden

Beregnes i `_separate_collection_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L26). Dokumentasjonen i koden:

> Separately collected from households = exported used textiles + the part
> kept in Norway (D17) - unsold clothing donated by retailers, which is
> exported with the used textiles (D27). A negative value is not physical
> and is clipped at 0; the clipped mass is recorded and reported on the
> flow page.
