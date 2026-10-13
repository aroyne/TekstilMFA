---
layout: default
title: Unsold goods discarded
parent: Wholesale and retail (DI.RT)
grand_parent: 4. Distribution (DI)
nav_order: 4
---

# Unsold goods discarded

| | |
|---|---|
| Flytkode | `DI.RT-WM.RS-Unsold goods discarded-TOT` |
| Fra | [Wholesale and retail (DI.RT)](../distribution_pool/subpool_di_rt.html) |
| Til | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | Watson et al. 2020 (retailers reported 95 t incinerated in 2018); Rubach et al. 2023 (retailers reported 337 t handled in 2022, of which 116 t donated); EEA 2024 (4-9 % of textiles put on the market destroyed) for sensitivity only |
| Merknad | Clothing only. Survey minimums, as the large chains did not report; per kt of clothing imports in the anchor years (D27) |

## Tidsserie

<iframe src="../output_files/plots/pages/di_rt_wm_rs_unsold_goods_discarded.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **DI.RT-WM.RS-Unsold goods discarded-TOT** er usolgte klær som produsenter og forhandlere sender til forbrenning eller materialgjenvinning, i stedet for å selge eller gi dem bort.

#### Datakilder (og hvordan kildetallene er produsert)

- 2018: forhandlerne som oppga mengder (16 av 44 som svarte), sendte 95 t til forbrenning (Watson m.fl. 2020).
- 2022: produsenter og forhandlere rapporterte 337 t usolgte tekstiler, hvorav 116 t donert. Resten (221 t) gikk til materialgjenvinning (93 t), annet (110 t) og forbrenning (Rubach m.fl. 2023).
- Tallene er minimum, fordi de største kjedene ikke ville oppgi mengder.
- Til sammenligning anslår EEA (2024) at 4–9 % av tekstilene som settes på markedet i Europa, destrueres uten å ha vært brukt. For Norge ville det tilsvare 4–10 kt per år. Det anslaget brukes bare til følsomhetsanalyse og diskusjon.

#### Antakelser

- Minimumstallene fra undersøkelsene er hovedresultatet (D27). Mengden uttrykkes per kt klesimport i ankerårene, på samme måte som donasjonene.
- Usikkerheten er skjevfordelt oppover (−20 / +200 %).
- Materialgjenvinning er ikke skilt ut ennå (WM.RC er ikke implementert), så alt går til WM.RS.

#### Sammensetning (varetype og materiale)

- Bare klær.
- Materialet er sammensetningen til tilførselen av klær samme år.

#### Tidsutvikling og sammenligninger

- Flyten er 0,06–0,13 kt per år fram til 2018 og omtrent 0,25 kt fra 2022. Det reelle nivået er trolig høyere.
- EUs økodesignforordning (ESPR) forbyr store virksomheter å destruere usolgte klær og sko. Det kan redusere flyten framover.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Klær | 100 % | 100 % | 100 % | 100 % | 100 % | 100 % |

### Materiale (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 62 % | 52 % | 57 % | 45 % | 46 % | 47 % |
| Regenerert cellulose | 3 % | 3 % | 3 % | 4 % | 4 % | 3 % |
| Ikke-tekstil | 2 % | 2 % | 2 % | 2 % | 2 % | 2 % |
| Andre fibre | 0 % | 1 % | 1 % | 0 % | 1 % | 1 % |
| Syntetisk | 30 % | 37 % | 32 % | 42 % | 42 % | 41 % |
| Ull | 4 % | 6 % | 6 % | 7 % | 6 % | 7 % |

<iframe src="../output_files/plots/pages/di_rt_wm_rs_unsold_goods_discarded_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_unsold_goods_discarded_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L49). Dokumentasjonen i koden:

> Unsold clothing that producers and retailers send to incineration or
> recycling, as minimums from surveys where the largest retailers did not
> report: 95 t incinerated in 2018 (Watson et al. 2020) and 221 t handled
> other than by donation in 2022 (Rubach et al. 2023). Material recycling
> is not split out yet, so all of it goes to WM.RS. The EEA (2024)
> estimates that 4-9 % of textiles put on the market in Europe are
> destroyed unused, which would be 4-10 kt a year in Norway; that is used
> for sensitivity and discussion only.
>
> `_per_clothing_import`: Array (year, product) with the anchored mass (kt) in clothing: the mass
> per kt of clothing imports in the anchor years, interpolated, times the
> clothing imports of each year.
