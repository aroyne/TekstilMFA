---
layout: default
title: Unsold goods donated
parent: Wholesale and retail (DI.RT)
grand_parent: 4. Distribution (DI)
nav_order: 5
---

# Unsold goods donated

| | |
|---|---|
| Flytkode | `DI.RT-CO.CO-Unsold goods donated-TOT` |
| Fra | [Wholesale and retail (DI.RT)](../distribution_pool/subpool_di_rt.html) |
| Til | [Separate collection (CO.CO)](../collection_and_sorting_pool/subpool_co_co.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | Watson et al. 2020 (one collector received about 600 t from retailers in 2018); Rubach et al. 2023 (collectors received about 200 t in 2022) |
| Merknad | Clothing only. Per kt of clothing imports in the anchor years, so it follows the clothing imports (D27). Mostly exported with HS 6309, so it is subtracted from collection from households |

## Tidsserie

<iframe src="../output_files/plots/pages/di_rt_co_co_unsold_goods_donated.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **DI.RT-CO.CO-Unsold goods donated-TOT** er usolgte klær som produsenter og forhandlere gir til innsamlere (dødt lager, returer og varer som tas ut av sortimentet).
- Varene sendes for det meste til land der merket ikke har butikker, og eksporteres derfor med de brukte tekstilene (HS 6309).

#### Datakilder (og hvordan kildetallene er produsert)

- 2018: én innsamler mottok omtrent 600 t usolgte tekstiler fra produsenter og forhandlere, blant annet fra noen av de største kjedene (Watson m.fl. 2020, kapittel 3.1.8). Watson vurderer at donasjonene neppe er mye høyere.
- 2022: innsamlerne oppga at de mottok omtrent 200 t (Rubach m.fl. 2023, kapittel 3.3.4).
- Begge tallene kommer fra kartleggingene til NORSUS, som bygger på spørreundersøkelser blant innsamlere, produsenter og forhandlere.

#### Antakelser

- Mengden uttrykkes per kt klesimport i ankerårene, og forholdstallet interpoleres. Før 2018 følger flyten klesimporten med 2018 som referanse, og etter 2022 med 2022 som referanse (D27).
- Usikkerhet: −20 / +50 % i 2018 og −50 / +100 % i 2022.
- Alt regnes som klær.
- Mengden trekkes fra innsamlingen fra husholdningene, fordi den eksporteres sammen med de innsamlede tekstilene.

#### Sammensetning (varetype og materiale)

- Bare klær.
- Materialet er sammensetningen til tilførselen av klær samme år (import og norske ferdigvarer).

#### Tidsutvikling og sammenligninger

- Flyten er liten: 0,3–0,4 kt rundt 1990, 0,6–0,7 kt i 2008–2018 og omtrent 0,2 kt fra 2022.
- Fallet fra 2018 til 2022 kan skyldes at andre aktører har tatt over, eller at tallene kommer fra ulike innsamlere. Det er ikke avklart.
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

<iframe src="../output_files/plots/pages/di_rt_co_co_unsold_goods_donated_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_unsold_goods_donated_mc` i [calculations/di_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/di_mc.py#L36). Dokumentasjonen i koden:

> Unsold clothing that producers and retailers give to collectors. One
> collector received about 600 t in 2018, including from some of the
> largest retailers (Watson et al. 2020), and collectors reported about
> 200 t in 2022 (Rubach et al. 2023). Most of it is exported to countries
> where the brand has no shops, i.e. with the export of used textiles
> (HS 6309), so it is subtracted from collection from households.
>
> `_per_clothing_import`: Array (year, product) with the anchored mass (kt) in clothing: the mass
> per kt of clothing imports in the anchor years, interpolated, times the
> clothing imports of each year.
