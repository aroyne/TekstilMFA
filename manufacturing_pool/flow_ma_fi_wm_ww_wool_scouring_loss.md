---
layout: default
title: Wool scouring loss
parent: Fibre and yarn production (MA.FI)
grand_parent: 3. Manufacturing (MA)
nav_order: 4
---

# Wool scouring loss

| | |
|---|---|
| Flytkode | `MA.FI-WM.WW-Wool scouring loss-TOT` |
| Fra | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Til | [Wastewater treatment (WM.WW)](../waste_management_pool/subpool_wm_ww.html) |
| Tekstilform | BYP – biprodukt, ikke tekstil |
| Dimensjoner | år |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | Greasy wool scoured in Norway (Totalkalkylen + SSB 08801 greasy wool trade, period means) x loss share (Norwegian Wool Book) |
| Merknad | Grease, suint and dirt, not textile. WM.WW has a temporary stock until its outflows are implemented |

## Tidsserie

<iframe src="../output_files/plots/pages/ma_fi_wm_ww_wool_scouring_loss.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **MA.FI-WM.WW-Wool scouring loss-TOT** er fett (lanolin), ullsvette, smuss og plantemateriale som vaskes ut når uvasket ull vaskes i Norge. Massen er ikke tekstil (form BYP) og går med vaskevannet til avløpsrensing.
- WM.WW har foreløpig et midlertidig lager som tar imot flyten, til utstrømmene fra avløpsrensing er implementert (D24).

#### Datakilder (og hvordan kildetallene er produsert)

- Uvasket ull vasket i Norge: norsk ull (Totalkalkylen) + import − eksport av uvasket ull (SSB 08801, HS 5101.11 og 5101.19, og 5101.30 når prisen per kg viser at det er uvasket ull). Utledet i `scripts/derive_wool_scouring_anchors.py`.
- Svinnandel: Norwegian Wool Book (Flokk) oppgir at omtrent en tredjedel av vekten forsvinner ved vasking.

#### Antakelser

- Årsbalansen svinger mye fordi klipping, lagring og eksport faller i ulike år (den er negativ i 2017). Derfor brukes snitt over perioder med stabil eksportandel: 2,8 kt (1988–1995), 2,2 kt (1996–2000), 1,3 kt (2001–2006) og 0,3 kt (2007–2025) uvasket ull. Usikkerheten er standardfeilen til snittet (6–18 %).
- Svinnandelen er 0,33 (0,20–0,45, PERT).
- I fiberlaget regnes uvasket ull som ull inkludert fettet, så svinnet er WO.

#### Sammensetning (varetype og materiale)

- Ingen varetype. Materialet er WO (se antakelsene).

#### Tidsutvikling og sammenligninger

- Svinnet var 0,9 kt per år rundt 1990 og har vært 0,09 kt per år fra 2007, da nesten all norsk ull ble eksportert uvasket.
- Sandnes Garn og Hillesvåg vasker fortsatt noe ull selv, blant annet ull fra gammelnorsk sau og ull til kontraktspinning. Det passer med de omtrent 0,3 kt uvasket ull per år etter 2007.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

Ull (WO), fordi uvasket ull regnes som ull inkludert fettet.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Ull | 100 % | 100 % | 100 % | 100 % | 100 % | 100 % |

<iframe src="../output_files/plots/pages/ma_fi_wm_ww_wool_scouring_loss_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_wool_scouring_loss_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L88). Dokumentasjonen i koden:

> Grease, suint and dirt removed when greasy wool is scoured in Norway,
> sent with the scouring water to wastewater treatment. The greasy wool
> scoured in Norway is Norwegian wool plus imports minus exports of greasy
> wool, as a mean over periods because the annual balance is dominated by
> the timing of shearing, storage and export (anchors derived by
> scripts/derive_wool_scouring_anchors.py): about 2.8 kt in 1988-1995,
> 2.2 kt in 1996-2000, 1.3 kt in 2001-2006 and 0.3 kt from 2007, when
> nearly all Norwegian wool is exported greasy. Exports declared as
> carbonised wool in 1996-2000 and 2002 are counted as greasy, because
> they are priced like greasy wool. The loss share is about a third of the
> greasy weight.
