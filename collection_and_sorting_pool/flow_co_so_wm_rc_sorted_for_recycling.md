---
layout: default
title: Sorted for recycling
parent: Sorting (CO.SO)
grand_parent: 6. Collection and sorting (CO)
nav_order: 3
---

# Sorted for recycling

| | |
|---|---|
| Flytkode | `CO.SO-WM.RC-Sorted for recycling-TOT` |
| Fra | [Sorting (CO.SO)](../collection_and_sorting_pool/subpool_co_so.html) |
| Til | [Material recycling (WM.RC)](../waste_management_pool/subpool_wm_rc.html) |
| Tekstilform | WRN – brukte, utslitte |
| Dimensjoner | år × produktgruppe |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | Watson et al. 2020 (93 t of 467 t rejects from domestic sorting in 2018); de Sadeleer & Rubach 2026 (142 t from households recycled at NTG in 2025) |
| Merknad | Share of the rejects from domestic sorting: 20 % (2018), 39 % (2025), held before 2018 (D34) |

## Tidsserie

<iframe src="../output_files/plots/pages/co_so_wm_rc_sorted_for_recycling.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **CO.SO-WM.RC-Sorted for recycling-TOT** er tekstiler fra husholdninger, sortert i Norge, som går til materialgjenvinning: i utlandet fram til 2023, og fra 2024 også hos NTG.

#### Datakilder (og hvordan kildetallene er produsert)

- 2018: 93 t av 467 t utsortert fra norsk sortering gikk til materialgjenvinning (Watson m.fl. 2020, tall fra innsamlerne).
- 2025: 142 t fra husholdninger ble gjenvunnet hos NTG (de Sadeleer & Rubach 2026). Det er husholdningenes andel av det NTG tok inn (254 av 651 t), ganget med det som ble gjenvunnet (364 t).
- Norsk Tekstilgjenvinning AS (NTG) i Sandefjord er det første anlegget i Norge for mekanisk materialgjenvinning av tekstiler til fiber som kan spinnes til nytt garn. Det startet kommersiell drift i 2024 og gjenvant 93 t i 2024 og 364 t i 2025 (de Sadeleer & Rubach 2026, kapittel 3.2.9.7, figur 3-8 og 3-9).

#### Antakelser

- Mengden uttrykkes som andel av det som blir utsortert ved norsk sortering (det som beholdes i Norge minus det som selges brukt): 20 % i 2018 og 39 % i 2025. Andelen holdes på 2018-nivået før 2018, med økende usikkerhet bakover (D30, D34).
- Bare det som faktisk gjenvinnes, regnes med. Det NTG sorterer ut til avfall og ombruk, ligger i restavfallet og bruktsalget.

#### Sammensetning (varetype og materiale)

- Bare CORE, med blandingen av innsamlede tekstiler.

#### Tidsutvikling og sammenligninger

- Flyten er liten: under 0,05 kt per år fram til 2010, 0,1 kt i 2018 og 0,17 kt i 2025. Den var lav i 2022 (0,03 kt), fordi nesten alt som ble beholdt det året, ble solgt brukt.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Klær, hjemmetekstiler og sko | 100 % | 100 % | 100 % | 100 % | 100 % | 100 % |

### Materiale (fiberlag, D19)

Blandingen av det som samles inn fra husholdningene (utstrømmen av årgangsmodellen) og usolgte klær som forhandlerne gir til innsamlerne (tilførselssammensetningen).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 50 % | 48 % | 45 % | 40 % | 37 % | 36 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 12 % | 16 % | 18 % | 17 % | 17 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 2 % |
| Syntetisk | 28 % | 27 % | 29 % | 33 % | 36 % | 37 % |
| Ull | 5 % | 6 % | 5 % | 5 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/co_so_wm_rc_sorted_for_recycling_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_sorted_for_recycling_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L69). Dokumentasjonen i koden:

> Part of the rejects from domestic sorting (retained minus sold second
> hand, imported clothing not counted) sent to material recycling: 93 of
> 467 t in 2018 (Watson et al. 2020, recycled abroad) and 142 of 364 t in
> 2025 (de Sadeleer & Rubach 2026, recycled at Norsk Tekstilgjenvinning).
> The share is held at the 2018 level before 2018 (D34).
