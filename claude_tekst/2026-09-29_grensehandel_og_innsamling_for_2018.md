# Grensehandel (privatimport) og innsamling før 2018

*Notat 2026-09-29. Oppfølging av [datainventaren](2026-09-29_datainventar_P1-flyter.md), flyt 3 og 6.*

## 1. Grensehandel – `RW.RW-US.HH-Private imports`

**Offisielle kilder (SSB, lagret i `data_files/SSB_grensehandel_05678_14221.csv`):**
* 05678: Grensehandel, handlebeløp (mill. kr) på **dagsturer**, 2004–2022 (avsluttet serie), uten varegrupper.
* 14221: Grensehandel etter varegruppe, 2023–2025. «Klær og sko, også til trening»: 496 / 509 / 458 mill. kr (5,3 / 4,6 / 4,1 % av varekurven).
* Den nye serien (14044, 14221 m.fl.) starter i 2023. Metodebruddet mellom seriene er ikke undersøkt.

| mill. kr | 2004 | 2010 | 2015 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| Grensehandel i alt | 8 804 | 10 525 | 14 109 | 16 041 | 1 968 | 2 500 | 10 376 | 9 346 | 11 032 | 11 279 |
| herav klær og sko | – | – | – | – | – | – | – | 496 | 509 | 458 |

**Størrelsesorden:** Beløpene er utsalgspriser i Sverige, inkludert mva. Importverdien i 08801 er ca. 470 NOK/kg for klær (2023–2025, tollverdi). Utsalgsprisen per kg er trolig 2–3 ganger høyere. Da blir 0,5 mrd NOK ≈ **0,2–0,5 kt per år**, under 1 % av den registrerte klesimporten.

**Forslag til metode (P1 → reelt P3 på grunn av størrelsen):**
* 2023–2025: SSB-beløp for klær og sko, delt på utsalgspris per kg (NOK/kg fra 08801 × påslagsfaktor, som blir en parameter med vid usikkerhet).
* 2004–2022: totalbeløpet × klesandel (gjennomsnitt 2023–2025, ca. 4,7 %, med usikkerhet). Pandemien (2020–2021) kommer automatisk med gjennom totalbeløpet.
* Før 2004: totalbeløpet holdes på 2004-nivået i faste priser, eller skaleres med KPI. Stor usikkerhet, men flyten er liten.
* **Ikke dekket:** Klær kjøpt på ferie- og forretningsreiser med overnatting. Det finnes ingen SSB-tabell for dette (sjekket i API-søk). Det omtales som et diskusjonspunkt, i tråd med prinsippet om offisielle kilder.

## 2. Innsamling før 2018 – `US.HH-CO.CO-Separate collection from households`

Nesten alt som samles inn eksporteres (85–97 %), og SSB 08801 gir eksport av brukte tekstiler (HS 6309, og filler i 6310) for **hvert år 1988–2025**:

| kt | 1990 | 1995 | 1998 | 2000 | 2005 | 2010 | 2015 | 2018 | 2020 | 2022 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Eksport 6309 | 1,2 | 3,9 | 6,7 | 8,3 | 12,1 | 18,0 | 27,6 | 36,3 | 33,6 | 31,4 | 32,9 |
| Eksport 6310 | 0,2 | 0,1 | 0,2 | 0,2 | 0,3 | 0,5 | 0,9 | 0,2 | 0,5 | 0,2 | 1,5 |

**Sammenligning med innsamlingstallene i ankerårene:**

| År | Eksport 6309+6310 | Innsamlet (kilde) | Forhold |
|---|---|---|---|
| 1998 | 6,9 kt | ca. 8,5 kt gjenvunnet/ombrukt (SSB tekstilregnskap: 8 % av 106 kt) | ≈ 0,8 |
| 2018 | 36,5 kt | 31,7 kt uten sko og vesker; 30,7 kt eksportert (Watson 2020). Comtrade 36,3 kt inkludert sko og vesker | ≈ 1,15 (≈ 1,0 med sko) |
| 2022 | 31,6 kt | 29,6 kt (NORSUS 2023) | ≈ 1,07 |
| 2025 | 34,4 kt | 33,7 kt innsamlet; SSB-eksport 34,3 kt (NORSUS 2026) | ≈ 1,02 |

Eksporten inkluderer sko og vesker. Det passer med vårt omfang, der sko (FW) er med. Den inkluderer også eksportører utenfor innsamlernettverket (NORSUS: 5,6 kt mer i SSB enn innsamlerne rapporterer i 2025).

**Forslag til metode:**
* Innsamlet(t) = eksport av 6309+6310 fra 08801(t) ÷ eksportandel(t) + usolgte varer donert og lignende.
* Eksportandelen er en tidsavhengig parameter med ankerpunkter: 2018 (Watson: 30,7 / 31,7 ≈ 0,97), 2022 (NORSUS 2023: ≈ 0,85, verifiseres), 2025 (NORSUS 2026). 1998 fra SSBs tekstilregnskap hvis tabellene kan hentes.
* Da er innsamlingen forankret i en offisiell årlig serie (08801), og ankerpunktene fra rapportene kalibrerer forholdet. Det følger D8/D15-prinsippet.
* Samme serie gir direkte `CO.CO-RW.RW-Export of unsorted collected textiles` (og `CO.SO-RW.RW` når sortert og usortert kan skilles).
* Veksten fra 1,2 kt (1990) til 36 kt (2018) er et tydelig historisk signal. En stor del av diskusjonen i artikkelen kan handle om dette.

## Kilder
* SSB tabell 05678 og 14221 (Grensehandel), hentet fra API 2026-09-29.
* SSB tabell 08801, se `DATA_SOURCES.md`.
* SSB, [Avfallsregnskap, tekstiler, 1990–1998](https://www.ssb.no/natur-og-miljo/statistikker/avfregntekstil/hvert-2-aar/2001-08-01).
* Watson m.fl. (2020), NORSUS OR 52.20; de Sadeleer & Rubach (2026), NORSUS OR.18.26.
