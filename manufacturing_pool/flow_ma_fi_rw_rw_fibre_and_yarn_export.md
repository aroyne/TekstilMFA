---
layout: default
title: Fibre and yarn export
parent: Fibre and yarn production (MA.FI)
grand_parent: 3. Manufacturing (MA)
nav_order: 3
---

# Fibre and yarn export

| | |
|---|---|
| Flytkode | `MA.FI-RW.RW-Fibre and yarn export-TOT` |
| Fra | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Til | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Tekstilform | FIB – fibre og garn |
| Dimensjoner | år |
| Metode | data |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | SSB 08801 (HS 50-55 fibre and yarn export, incl. greasy wool 5101; high-tenacity filament yarn excluded) |
| Merknad | Greasy wool is 90-100 % of Norwegian wool since 2007. Yarn export may include re-export of yarn spun abroad |

## Tidsserie

<iframe src="../output_files/plots/pages/ma_fi_rw_rw_fibre_and_yarn_export.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **MA.FI-RW.RW-Fibre and yarn export-TOT** er eksport av tekstilfiber og garn (HS 50–55, unntatt vevd metervare og garn i detaljopplegg), med de samme kodene utenfor omfanget som importen (D22).
- Flyten domineres av uvasket norsk ull (HS 5101.11 og 5101.19), som for det meste vaskes i Bradford i England.

#### Datakilder (og hvordan kildetallene er produsert)

- SSB tabell 08801 (se RW.RW-MA.FI-Fibre and yarn import-TOT).
- Eksport deklarert som karbonisert ull (5101.30) i 1996–2000 og 2002 er trolig uvasket ull. Prisen per kg er som for uvasket ull, mottakerlandet er Storbritannia, og eksporten av uvasket ull faller like mye de årene. Varenummeret påvirker ikke denne flyten, men brukes i vaskesvinnet (MA.FI-WM.WW-Wool scouring loss-TOT).

#### Antakelser

- Handelsstatistikken skiller ikke gjeneksport fra norsk produksjon. Garn som norske garnmerker får spunnet i utlandet og videreselger, telles både som import og eksport. Det utlignes i balansen til MA.FI, men eksportflyten overvurderer da hvor mye garn som er spunnet i Norge.

#### Sammensetning (varetype og materiale)

- Flyten har ingen varetype.
- Materialet er hovedfiberen i HS-koden. Andelen ull økte fra 74 % i 1990 til 96 % i 2022, da bomull og syntetisk forsvant fra eksporten.

#### Tidsutvikling og sammenligninger

- Eksporten lå på 4,3–6,2 kt fram til 2015 og har falt til omtrent 3 kt i 2020–2025, i takt med mindre norsk ull.
- Andelen av norsk ull som eksporteres uvasket, økte fra 50–60 % rundt 1990 til over 90 % fra 2007. Det betyr at nesten ingen norsk ull vaskes i Norge lenger.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

Hovedfiberen fra HS-koden (fiber og garn, FY).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 17 % | 3 % | 1 % | 0 % | 0 % | 1 % |
| Regenerert cellulose | 6 % | 4 % | 1 % | 0 % | 0 % | 0 % |
| Andre fibre | 1 % | 0 % | 1 % | 0 % | 0 % | 1 % |
| Syntetisk | 2 % | 2 % | 2 % | 2 % | 4 % | 3 % |
| Ull | 74 % | 91 % | 96 % | 98 % | 96 % | 96 % |

<iframe src="../output_files/plots/pages/ma_fi_rw_rw_fibre_and_yarn_export_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_fibre_and_yarn_export_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L76). Dokumentasjonen i koden:

> Registered exports of fibre and yarn, SSB 08801 (HS 50-55 except woven
> fabric and retail yarn). Dominated by greasy Norwegian wool (HS 5101.11
> and 5101.19), which since 2007 is 90-100 % of Norwegian wool. Yarn
> exports may include re-export of yarn spun abroad for Norwegian brands,
> which the trade statistics do not separate from domestic production.
