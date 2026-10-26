---
layout: default
title: Export for recycling
parent: Material recycling (WM.RC)
grand_parent: 7. Waste management (WM)
nav_order: 2
---

# Export for recycling

| | |
|---|---|
| Flytkode | `WM.RC-RW.RW-Export for recycling-TOT` |
| Fra | [Material recycling (WM.RC)](../waste_management_pool/subpool_wm_rc.html) |
| Til | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Tekstilform | WRN – brukte, utslitte |
| Dimensjoner | år |
| Metode | balance |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | Balance of WM.RC: everything recycled before NTG (2024), and the part of NTG fibre not sold in Norway |
| Merknad | Clipped at 0 (D34) |

## Tidsserie

<iframe src="../output_files/plots/pages/wm_rc_rw_rw_export_for_recycling.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **WM.RC-RW.RW-Export for recycling-TOT** er tekstiler og gjenvunnet fiber som går til materialgjenvinning i utlandet: alt som ble sortert til gjenvinning før 2024, og den delen av NTGs fiber som selges til europeiske kunder fra 2024.

#### Datakilder (og hvordan kildetallene er produsert)

- Flyten er balansen i WM.RC og har ingen egen datakilde: det som går til gjenvinning (fra sortering, institusjoner og produksjon) minus fiberen som selges i Norge.
- Eksport av filler og sortert tekstilavfall (HS 6310) i handelsstatistikken ligger i eksporten fra innsamlingen (D31), ikke her.

#### Antakelser

- Før 2024 ble alt gjenvunnet i utlandet.
- En negativ verdi er ikke-fysisk og klippes til 0. Det skjer i 3 % av trekkene i 2024–2025, når den norske andelen trekkes høyt (D34).

#### Sammensetning (varetype og materiale)

- Ingen varetype.
- Materialet er balansen i WM.RC per materiale. Fordi den gjenvunne fiberen har en antatt sammensetning, klippes enkelte materialer i omtrent en fjerdedel av trekkene i 2024–2025.

#### Tidsutvikling og sammenligninger

- Flyten er liten: under 0,05 kt per år fram til 2010, 0,1 kt i 2018 og 0,2 kt i 2025.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)



| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 51 % | 48 % | 44 % | 40 % | 37 % | 22 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 1 % |
| Ikke-tekstil | 11 % | 16 % | 18 % | 17 % | 17 % | 24 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 5 % |
| Syntetisk | 28 % | 27 % | 30 % | 33 % | 36 % | 43 % |
| Ull | 5 % | 6 % | 5 % | 5 % | 6 % | 5 % |

<iframe src="../output_files/plots/pages/wm_rc_rw_rw_export_for_recycling_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT:

| År | Iterasjoner med klipping | Snitt klippet (kt) | Maks klippet (kt) | Deterministisk (kt) |
|---|---|---|---|---|
| 2024 | 2 av 1000 | 0.000 | 0.005 | 0.000 |
| 2025 | 28 av 1000 | 0.001 | 0.116 | 0.000 |

I fiberlaget (per materiale):

| År | Iterasjoner med klipping | Snitt klippet (kt) | Maks klippet (kt) | Deterministisk (kt) |
|---|---|---|---|---|
| 2024 | 34 av 1000 | 0.000 | 0.017 | 0.000 |
| 2025 | 247 av 1000 | 0.006 | 0.148 | 0.000 |

## Beregning i koden

Beregnes i `_export_for_recycling_mc` i [calculations/wm_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/wm_mc.py#L63). Dokumentasjonen i koden:

> Balance of WM.RC: textiles sent to material recycling (from domestic
> sorting, institutions and production) minus the recycled fibre sold to
> Norwegian spinning. Before Norsk Tekstilgjenvinning started in 2024
> everything was recycled abroad; from 2024 the part of the plant's fibre
> sold to European customers is exported. A negative value is not
> physical and is clipped at 0 (D34).
