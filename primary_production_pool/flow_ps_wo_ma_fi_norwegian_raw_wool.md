---
layout: default
title: Norwegian raw wool
parent: Norwegian wool (PS.WO)
grand_parent: 2. Primary production (PS)
nav_order: 1
---

# Norwegian raw wool

| | |
|---|---|
| Flytkode | `PS.WO-MA.FI-Norwegian raw wool-TOT` |
| Fra | [Norwegian wool (PS.WO)](../primary_production_pool/subpool_ps_wo.html) |
| Til | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Tekstilform | FIB – fibre og garn |
| Dimensjoner | år |
| Metode | data |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | Totalkalkylen for jordbrukssektoren (Budsjettnemnda for jordbruket/NIBIO), 1959-2026 |
| Merknad | Greasy wool as weighed in. Animalia/Norilia annual reports for checking |

## Tidsserie

<iframe src="../output_files/plots/pages/ps_wo_ma_fi_norwegian_raw_wool.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **PS.WO-MA.FI-Norwegian raw wool-TOT** er ull klippet av norske sauer, som uvasket (fettholdig) ull slik den veies inn på ullstasjonene.
- Flyten er systemets eneste innstrøm av norsk jomfrufiber.

#### Datakilder (og hvordan kildetallene er produsert)

- Totalkalkylen for jordbrukssektoren, posten «Ull» (tonn, kr/kg og verdi per år fra 1959), hentet fra NIBIOs statistikktjeneste ([Totalkalkylen](https://nibio.no/tema/landbruksokonomi/totalkalkylen)).
- Totalkalkylen utarbeides av Budsjettnemnda for jordbruket og er grunnlaget for jordbruksforhandlingene. Ullmengden bygger på innveid ull ved ullstasjonene (Norilia og Fatland Gjestal Ull) og oppdateres to ganger i året.
- Siste år i fila (2026) er budsjett og året før (2025) foreløpig regnskap. Modellen bruker 1988–2025.
- Animalias årsrapporter for ullkontrollen (FFULL) gir kvalitetsklasser og kan brukes til kontroll.

#### Antakelser

- Tallene brukes som de er, med datasettusikkerhet på ±5 % (plassholder).
- Ull som ikke veies inn (salg direkte fra gård, hjemmespinning) er ikke med.

#### Sammensetning (varetype og materiale)

- Flyten har ingen varetype.
- Materialet er ull (WO). Uvasket ull regnes som ull inkludert fett og smuss, slik at vaskesvinnet senere også er WO.

#### Tidsutvikling og sammenligninger

- Mengden lå på 4,9–5,7 kt fram til 2006 (høyest i 1994 med 5,7 kt) og har siden falt jevnt til 2,9 kt i 2025.
- Prisen per kg har vært 27–38 kr/kg siden 2000 (lavest i 2010).
- Fra 2007 eksporteres 90–100 % av ulla uvasket (se MA.FI-RW.RW-Fibre and yarn export-TOT). Ullialt-rapporten (Norges Husflidslag 2018) oppgir at omtrent 20 % av norsk ull ble brukt i Norge da prosjektet startet.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

Ull (WO). Uvasket ull regnes som ull, inkludert fett og smuss.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Ull | 100 % | 100 % | 100 % | 100 % | 100 % | 100 % |

<iframe src="../output_files/plots/pages/ps_wo_ma_fi_norwegian_raw_wool_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_norwegian_raw_wool_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L52). Dokumentasjonen i koden:

> Norwegian wool (greasy, as weighed in) from Totalkalkylen for
> jordbrukssektoren (Budsjettnemnda for jordbruket, NIBIO), the official
> agricultural account; the series starts in 1959. The last year in the
> file is a budget figure and the one before it preliminary.
