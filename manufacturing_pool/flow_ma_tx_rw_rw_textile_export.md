---
layout: default
title: Textile export
parent: Textile and apparel manufacturing (MA.TX)
grand_parent: 3. Manufacturing (MA)
nav_order: 2
---

# Textile export

| | |
|---|---|
| Flytkode | `MA.TX-RW.RW-Textile export-TOT` |
| Fra | [Textile and apparel manufacturing (MA.TX)](../manufacturing_pool/subpool_ma_tx.html) |
| Til | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år |
| Metode | data |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | SSB 08801 (fabric export: woven fabric in HS 50-55, HS 58 and 60) |
| Merknad | Fabric only. Exports of finished products stay with DI.RT, because the trade statistics do not separate re-export from Norwegian production (D6) |

## Tidsserie

<iframe src="../output_files/plots/pages/ma_tx_rw_rw_textile_export.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **MA.TX-RW.RW-Textile export-TOT** er eksport av metervare (vevnader i HS 50–55, HS 58 og 60).
- Eksport av ferdigvarer føres fra DI.RT, fordi handelsstatistikken ikke skiller gjeneksport fra norsk produksjon (D6).

#### Datakilder (og hvordan kildetallene er produsert)

- SSB tabell 08801, nettovekt i kg (se RW.RW-MA.FI-Fibre and yarn import-TOT).

#### Antakelser

- All eksport av metervare kommer fra norsk industri. Noe kan være gjeneksport.

#### Sammensetning (varetype og materiale)

- Ingen varetype.
- Materialet er hovedfiberen i HS-koden. I 1990 var eksporten 54 % bomull og 40 % syntetisk. I 2022 var den 71 % ull, trolig ullstoff fra norske veverier.

#### Tidsutvikling og sammenligninger

- Eksporten økte fra 2,8 kt i 1988 til 6,6 kt i 1998, falt til under 1 kt i 2015–2022 og steg til 2,4 kt i 2025. Økningen i 2025 kommer fra trikotasjestoff (HS 60, 1,75 kt) og bør undersøkes.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

Hovedfiberen fra HS-koden (metervare, FA).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 54 % | 36 % | 24 % | 13 % | 8 % | 2 % |
| Regenerert cellulose | 1 % | 2 % | 1 % | 1 % | 2 % | 0 % |
| Andre fibre | 0 % | 0 % | 0 % | 2 % | 1 % | 0 % |
| Syntetisk | 40 % | 58 % | 63 % | 13 % | 18 % | 69 % |
| Ull | 5 % | 5 % | 12 % | 71 % | 71 % | 29 % |

<iframe src="../output_files/plots/pages/ma_tx_rw_rw_textile_export_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_textile_export_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L184). Dokumentasjonen i koden:

> Registered exports of fabric, SSB 08801 (woven fabric in HS 50-55, HS 58
> and 60). Exports of finished goods are counted from DI.RT, because the
> trade statistics do not separate re-export from Norwegian production
> (D6).
