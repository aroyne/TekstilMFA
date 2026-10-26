---
layout: default
title: Yarn to textile manufacturing
parent: Fibre and yarn production (MA.FI)
grand_parent: 3. Manufacturing (MA)
nav_order: 1
---

# Yarn to textile manufacturing

| | |
|---|---|
| Flytkode | `MA.FI-MA.TX-Yarn to textile manufacturing-TOT` |
| Fra | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Til | [Textile and apparel manufacturing (MA.TX)](../manufacturing_pool/subpool_ma_tx.html) |
| Tekstilform | FIB – fibre og garn |
| Dimensjoner | år |
| Metode | balance |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | Balance of MA.FI; SSB 10455 (Prodcom, yarn produced in large enterprises 2008-) for checking |
| Merknad | – |

## Tidsserie

<iframe src="../output_files/plots/pages/ma_fi_ma_tx_yarn_to_textile_manufacturing.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **MA.FI-MA.TX-Yarn to textile manufacturing-TOT** er fiber og garn som går fra spinning og fiberbearbeiding (MA.FI) til veving, strikking og konfeksjon i Norge (MA.TX).

#### Datakilder (og hvordan kildetallene er produsert)

- Flyten er balansen i MA.FI og har ingen egen datakilde. Inn går norsk ull (Totalkalkylen), import av fiber og garn (SSB 08801) og fra 2024 gjenvunnet fiber fra NTG. Ut går eksport av fiber og garn (08801), vaskesvinn og håndstrikkegarn (SSB varetall og Prodcom).
- Til kontroll: Prodcom (SSB 10455) har noen år med produksjon av ikke-detaljpakket garn (13.10.50.10: 0,14–0,21 kt).

#### Antakelser

- Fiber og garn som verken eksporteres eller blir håndstrikkegarn, brukes i MA.TX samme år (ingen lagerendring i MA.FI).
- En negativ balanse er ikke-fysisk og klippes til 0. Det har ikke skjedd i TOT. I fiberlaget klippes ull i enkelte trekk i 1989 og 2000 (se under).

#### Sammensetning (varetype og materiale)

- Ingen varetype.
- Materialet er balansen per materiale. Syntetisk utgjør omtrent halvparten (51 % i 1990, 56 % i 2022). Bomull falt fra 32 % til 3 %, og ull økte fra 5 % til 25 %.
- Ullbalansen er stram i 1989 og 2000, fordi nesten all norsk ull ble eksportert. Ved høye trekk av svinnandel og håndstrikkegarn blir ull negativt og klippes til 0.

#### Tidsutvikling og sammenligninger

- Flyten falt fra 12–13 kt rundt 1990 til omtrent 4–6 kt etter 2010. Det følger nedgangen i norsk tekstilindustri.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

Balansen i MA.FI per materiale, klippet til 0.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 32 % | 22 % | 5 % | 6 % | 3 % | 4 % |
| Regenerert cellulose | 11 % | 10 % | 1 % | 2 % | 1 % | 1 % |
| Andre fibre | 1 % | 5 % | 12 % | 7 % | 14 % | 12 % |
| Syntetisk | 51 % | 58 % | 67 % | 59 % | 57 % | 61 % |
| Ull | 6 % | 5 % | 15 % | 27 % | 24 % | 23 % |

<iframe src="../output_files/plots/pages/ma_fi_ma_tx_yarn_to_textile_manufacturing_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

I fiberlaget (per materiale):

| År | Iterasjoner med klipping | Snitt klippet (kt) | Maks klippet (kt) | Deterministisk (kt) |
|---|---|---|---|---|
| 1989 | 1 av 1000 | 0.000 | 0.035 | 0.000 |
| 2000 | 18 av 1000 | 0.002 | 0.285 | 0.000 |

## Beregning i koden

Beregnes i `_yarn_to_manufacturing_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L160). Dokumentasjonen i koden:

> Balance of MA.FI: Norwegian wool, imported fibre and yarn and recycled
> fibre minus exports, the scouring loss and hand knitting yarn sold
> through retail.
> A negative balance is not physical and is clipped at 0; the clipped
> mass is recorded and reported on the flow page.
