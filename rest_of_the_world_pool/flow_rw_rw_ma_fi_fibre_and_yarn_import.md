---
layout: default
title: Fibre and yarn import
parent: Rest of the world (RW.RW)
grand_parent: 1. Rest of the world (RW)
nav_order: 1
---

# Fibre and yarn import

| | |
|---|---|
| Flytkode | `RW.RW-MA.FI-Fibre and yarn import-TOT` |
| Fra | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Til | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Tekstilform | FIB – fibre og garn |
| Dimensjoner | år |
| Metode | data |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | SSB 08801 (HS 50-55 fibre and yarn; woven fabric and retail yarn excluded) |
| Merknad | HS 56, high-tenacity filament yarn (5402.10/11/19/20), nylon net twine (5402.61), other single synthetic filament yarn (5402.49) and polypropylene staple fibre (5503.40) are outside the scope: they go to ropes, nets, nonwovens and technical products. Retail yarn goes to DI.RT as product YA |

## Tidsserie

<iframe src="../output_files/plots/pages/rw_rw_ma_fi_fibre_and_yarn_import.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **RW.RW-MA.FI-Fibre and yarn import-TOT** er import av tekstilfiber og garn til norsk spinning og tekstilindustri: rå, vasket og karbonisert ull, ulltopper, bomull, stapelfiber og filamentgarn (HS 50–55).
- Flyten omfatter ikke vevd metervare (RW.RW-MA.TX-Fabric import-TOT) eller garn i detaljopplegg til håndstrikking (produkt YA i RW.RW-DI.RT-Finished textile products import-TOT).
- HS 56 (vatt, filt, fiberduk, tau, nett) og garn til tau, nett og tekniske produkter er utenfor omfanget (D22): høyfast filamentgarn (5402.10/11/19/20), tvunnet nylongarn (5402.61), annet enkelt syntetisk filamentgarn (5402.49) og polypropylen stapelfiber (5503.40).

#### Datakilder (og hvordan kildetallene er produsert)

- SSB tabell 08801, utenrikshandel med varer etter varenummer (HS8) og land, nettovekt i kg. 1988–2022 fra den fulle 08801-fila i NitrogenBudsjett og 2023–2025 fra SSBs API.
- Handelsstatistikken bygger på tolldeklarasjoner. Nettovekten er varens vekt uten emballasje, slik importøren deklarerer den.

#### Antakelser

- All registrert import av fiber og garn går til norsk industri (MA.FI). Garn som videreforhandles uten bearbeiding, går gjennom MA.FI og ut igjen som eksport.
- Datasettusikkerhet ±5 % (plassholder), fullt korrelert mellom år og flyter fra 08801.

#### Sammensetning (varetype og materiale)

- Flyten har ingen varetype.
- Materialet er hovedfiberen i HS-koden. I 1990 var importen 44 % syntetisk, 33 % bomull, 11 % regenerert cellulose og 10 % ull. I 2022 var den 51 % syntetisk, 32 % ull, 13 % andre fibre (blant annet kokos, abaka og sisal i 5305) og 3 % bomull.

#### Tidsutvikling og sammenligninger

- Importen falt fra 15,4 kt i 1988 til 7,7 kt i 2005 og har ligget på 5–6 kt siden 2010.
- Fallet kommer særlig fra bomull og regenerert cellulose, som forsvant med nedleggingen av spinnerier og veverier på 1990- og 2000-tallet.
- Polyester stapelfiber (5503.20) har ligget stabilt på 2,3–3,1 kt per år. Den brukes trolig som fyll i dyner og puter.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

Hovedfiberen fra HS-koden (fiber og garn, FY).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 33 % | 20 % | 5 % | 5 % | 3 % | 2 % |
| Regenerert cellulose | 11 % | 10 % | 2 % | 2 % | 1 % | 1 % |
| Andre fibre | 1 % | 4 % | 10 % | 6 % | 13 % | 11 % |
| Syntetisk | 44 % | 49 % | 57 % | 52 % | 51 % | 54 % |
| Ull | 10 % | 16 % | 27 % | 36 % | 32 % | 33 % |

<iframe src="../output_files/plots/pages/rw_rw_ma_fi_fibre_and_yarn_import_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_fibre_and_yarn_import_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L66). Dokumentasjonen i koden:

> Registered imports of fibre and yarn, SSB 08801 (HS 50-55 except woven
> fabric and retail yarn). Includes raw, scoured and carbonised wool and
> tops returning after scouring abroad.
