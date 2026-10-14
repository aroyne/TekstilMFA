---
layout: default
title: Secondhand sales to households
parent: Second-hand retail (CO.RE)
grand_parent: 6. Collection and sorting (CO)
nav_order: 1
---

# Secondhand sales to households

| | |
|---|---|
| Flytkode | `CO.RE-US.HH-Secondhand sales to households-TOT` |
| Fra | [Second-hand retail (CO.RE)](../collection_and_sorting_pool/subpool_co_re.html) |
| Til | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Tekstilform | USE – brukte, ombrukbare |
| Dimensjoner | år × produktgruppe |
| Metode | balance |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Balance of CO.RE |
| Merknad | Re-enters the in-use stock |

## Tidsserie

<iframe src="../output_files/plots/pages/co_re_us_hh_secondhand_sales_to_households.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **CO.RE-US.HH-Secondhand sales to households-TOT** er brukte tekstiler solgt fra innsamlernes bruktbutikker tilbake til husholdningene.
- Uformell ombruk (Finn, Tise, arv) er ikke med. Den regnes som lengre levetid i husholdningene (D9).

#### Datakilder (og hvordan kildetallene er produsert)

- Flyten er balansen i CO.RE: alt som sorteres til bruktbutikk, selges.

#### Antakelser

- Usolgte varer i bruktbutikk er ikke med ennå.

#### Sammensetning (varetype og materiale)

- Bare CORE, med blandingen av det som samles inn fra husholdningene (utstrømmen fra årgangsmodellen) og donerte usolgte klær.

#### Tidsutvikling og sammenligninger

- Flyten er liten sammenlignet med salget av nye varer: under 1 kt per år fram til 2021, 1,0 kt i 2022 og 1,9 kt i 2025. Den omfatter også importerte brukte klær.
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
| Bomull | 51 % | 48 % | 44 % | 40 % | 37 % | 36 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 13 % | 15 % | 18 % | 18 % | 17 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 2 % |
| Syntetisk | 28 % | 27 % | 30 % | 33 % | 36 % | 37 % |
| Ull | 5 % | 6 % | 5 % | 5 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/co_re_us_hh_secondhand_sales_to_households_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_secondhand_sales_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L80). Dokumentasjonen i koden:

> Balance of CO.RE: everything sorted for second-hand sale is sold.
