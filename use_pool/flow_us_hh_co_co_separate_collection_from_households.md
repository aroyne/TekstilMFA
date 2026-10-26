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
- Andelen som blir i Norge, holdes på 2018-nivået før 2018, med usikkerhet som øker bakover (D30), og interpoleres mellom ankerpunktene (usikkerhet ±50 %). Bruktbutikker (blant annet Fretex) har eksistert hele perioden, så andelen var neppe null tidlig.
- Statistikken dekker klær, hjemmetekstiler og sko samlet, så flyten er bare i produktgruppen CORE.

#### Sammensetning (varetype og materiale)

- Bare CORE.
- Materialet er utstrømmen fra årgangsmodellen for husholdningene, altså det som ble kjøpt tidligere. Bomull falt fra 46 % i 1990 til 37 % i 2022, og syntetisk økte fra 27 % til 36 %. Ikke-tekstil (17 %) er mest såler fra sko.

#### Tidsutvikling og sammenligninger

- Innsamlingen økte fra 0,6 kt i 1988 til 39 kt i 2019 og var 33–36 kt i 2022–2025.
- Modellen gir mer enn kartleggingene: 36,9 kt mot 31,7 kt i 2018 (Watson), 32,3 kt mot 29,6 kt i 2022 (NORSUS) og 36,1 kt mot 33,7 kt i 2025. Eksportstatistikken regnes som mer fullstendig enn kartleggingene (D31): NORSUS oppgir selv eksport fra tollstatistikken (31,6 kt i 2022) som er større enn innsamlingen innsamlerne rapporterer (29,6 kt). Man kan ikke eksportere mer enn man samler inn, og importen av brukte tekstiler er under 0,3 kt. Trolig mangler kartleggingene noen aktører, for eksempel private innsamlere utenfor nettverket.
- Kommunenes tall i KOSTRA (SSB 13035, «Tekstiler til ombruk», 10–15 kt i 2015–2018) gjelder bare kommunale ordninger og er en nedre kontroll.
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
| Bomull | 46 % | 47 % | 44 % | 40 % | 37 % | 36 % |
| Regenerert cellulose | 3 % | 2 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 18 % | 16 % | 19 % | 18 % | 17 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 2 % |
| Syntetisk | 27 % | 26 % | 30 % | 33 % | 36 % | 37 % |
| Ull | 6 % | 6 % | 5 % | 5 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/us_hh_co_co_separate_collection_from_households_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT:

| År | Iterasjoner med klipping | Snitt klippet (kt) | Maks klippet (kt) | Deterministisk (kt) |
|---|---|---|---|---|
| 1988 | 192 av 1000 | 0.082 | 1.800 | 0.000 |
| 1989 | 87 av 1000 | 0.037 | 1.470 | 0.000 |
| 1990 | 43 av 1000 | 0.015 | 1.185 | 0.000 |
| 1991 | 55 av 1000 | 0.026 | 1.480 | 0.000 |
| 1992 | 3 av 1000 | 0.001 | 0.597 | 0.000 |

## Beregning i koden

Beregnes i `_separate_collection_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L40). Dokumentasjonen i koden:

> Separately collected from households = exported used textiles + the part
> kept in Norway (D17) - unsold clothing donated by retailers, which is
> exported with the used textiles (D27). A negative value is not physical
> and is clipped at 0; the clipped mass is recorded and reported on the
> flow page.
