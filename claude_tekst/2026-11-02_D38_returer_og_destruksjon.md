# D38 (forslag): Returer fra netthandel og destruksjon av usolgte varer

*Notat 2026-11-02. Beslutningsgrunnlag, ikke implementert. Kildene er samlet i tillegget til [notatet om tiltak](2026-11-02_tiltak_sirkularitet_og_MFA.md). Gjelder `RW.RW-US.HH-Direct online imports`, `DI.RT-WM.RS-Unsold goods discarded` og `DI.RT-CO.CO-Unsold goods donated` ([calculations/di_mc.py](../calculations/di_mc.py), [calculations/rw_mc.py](../calculations/rw_mc.py)).*

## Problem

1. **Usolgte varer:** Modellen har 0,2 kt kastet og 0,2 kt donert per år (2025). Begge er minimum fra undersøkelser der de største kjedene ikke svarte (Watson 2020: 95 t i 2018; Rubach 2023: 221 t i 2022). Andre anslag ligger mye høyere. Samfunnsøkonomisk analyse (2022) fant et overskudd på minst 825 t, hvorav én kjede sto for nesten 430 t. EEA (2024) anslår at 4–9 % av det som settes på markedet, destrueres ubrukt, noe som tilsvarer 4–10 kt i Norge. Den nederlandske netthandelsbransjen hevder 0,35 %.
2. **Returer fra direkte netthandel:** VOEC-tallene (0,5 / 4,8 / 3,8 / 14,0 kt i 2022–2025) er leveranser til Norge. Returer til utenlandske nettbutikker trekkes ikke fra. Returandelen er ca. 50 % hos Zalando, ca. 20 % for klær kjøpt på nett ifølge EEA, og ukjent for Temu og Shein (trolig lav).
3. **Hvor feilen havner:** Varer som destrueres av norske kjeder, blir næringsavfall og fanges ikke av plukkanalysene for husholdningsavfall. Returer forlater landet. Ingen av delene trekkes fra i dag. De havner derfor i salg til husholdningene (balansen i DI.RT) eller i tilførselen, og dermed i lageret i husholdningene.

## Forslag

| # | Endring | Metode | Parametre (forslag) |
|---|---|---|---|
| 1 | **Ny flyt `US.HH-RW.RW-Returns of direct online purchases`** (form NEW) | direkte netthandel × returandel. VOEC beholdes brutto, så tallet fra Tolletaten står uendret | `online_return_share`: PERT 0,05–0,5, mest sannsynlig 0,2 (EEA, Zalando, Bamberg). Mulig lavere fra 2024, når Temu og Shein dominerer (antakelse) |
| 2 | **Bredere fordeling for `Unsold goods discarded`** | andel av det som settes på markedet (klær, eventuelt også sko og hjemmetekstiler), ikke minimum fra undersøkelser | lognormal med median ca. 1 % og 95 %-intervall ca. 0,2–9 %. Minimum fra undersøkelsene er nedre grense og EEA er øvre. Medianen er en antakelse (overskuddet i SØA 2022 er ca. 0,8 % av klestilførselen) |
| 3 | **Returer til norske nettbutikker** | ingen egen flyt. De går tilbake til DI.RT, og det som destrueres, inngår i punkt 2 | – |
| 4 | **Ingen dobbelttelling** | `Unsold goods discarded` går til WM.RS som næringsavfall, og restavfallsankrene (plukkanalyser av husholdningsavfall) dekker det ikke | – |
| 5 | **Fra 19.7.2026 (ESPR)** | destruksjon i store foretak er forbudt. Et regimeskifte er bare aktuelt for scenarier etter 2025 | – |

## Effekt (grovt)

* Returer: ca. 3 kt i 2025 (14 kt × 0,2), mindre før 2023. Akkumulert over perioden: ca. 5 kt.
* Destruksjon: 1 % av ca. 100 kt gir ca. 1 kt per år, og ca. 35 kt over perioden. Med EEA blir det 4–9 kt per år og 150–300 kt over perioden.
* Begge reduserer lageret i husholdningene som er beregnet som restledd. Selv med EEA-nivået forklarer de bare en del av avviket (ca. 275 mot ca. 97 kg per innbygger, rundt 1 000 kt).

## Data å skaffe

* EEA (2024), *The destruction of returned and unsold textiles in Europe's circular economy*: metode, og om «en tredel av returene destrueres» stemmer.
* PostNord, *E-handel i Norden*: returandel for klær i Norge.
* Rapporteringen av destruerte mengder under ESPR (store foretak) og rapporteringen i produsentansvaret, trolig norske tall fra 2027–2028.
* Tolletaten: om VOEC-tallene er brutto (ikke justert for returer).

## Spørsmål til deg

1. Ny returflyt (punkt 1), eller nettoføring av VOEC?
2. Median for destruksjon: 1 % (antakelse), eller fortsatt minimum fra undersøkelsene med EEA bare i følsomhetsanalysen (som i D27 i dag)?
3. Skal destruksjon gjelde bare klær (som i dag), eller også sko og hjemmetekstiler?
