# Flere lag i modellen: tekstilform og materiale

*Forslag 2026-10-05. Beslutninger foreslås som D18 og D19 i SYSTEMDEFINISJON.*

## Utgangspunkt

Modellen har i dag to dimensjoner per flyt: **produktgruppe** (kolonnen `product`) og **år**. Det siste feltet i flytkoden (`-TOT`) er reservert for materiale (D4), men brukes ikke ennå. Det trengs to lag til:

1. **Tekstilform**: Hva slags tekstil flyter her? Fibre, metervare, nye produkter, brukbare brukte produkter, utslitte produkter, produksjonsavfall, mikrofibre.
2. **Materiale**: Hvilken fiber er det? PES, CO, WO og så videre.

Hvis begge legges inn som fulle dimensjoner på alle flyter, blir det flyt × produkt × form × fiber × år × MC-iterasjon. Det blir uhåndterlig i minne og i dokumentasjon, og de fleste kombinasjonene er tomme (det finnes ikke «brukbare brukte fibre»). Forslaget er derfor at de to lagene håndteres ulikt.

## 1. Tekstilform som egenskap ved flyten, ikke som dimensjon (forslag D18)

Formen er nesten alltid gitt av hvor i systemet flyten går. Fibre går bare inn i MA.FI, metervare bare inn i MA.TX, og nye produkter går fra DI.RT. Formen kan da være en **kolonne `form` i `system/flows.csv`**. Den legges ikke i resultatradene, men kan kobles på ved oppsummering og plotting.

Foreslåtte kategorier (åtte):

| Kode | Form | Eksempler på flyter |
|---|---|---|
| FIB | Fibre og garn (også råull og resirkulert fiber) | PS.WO → MA.FI, RW → MA.FI, MA.FI → MA.TX, WM.RC → MA.TX |
| FAB | Metervare og halvfabrikata | RW → MA.TX |
| NEW | Nye ferdigvarer (også usolgte) | import, salg, DI.RT → WM.RS (usolgt kassert) |
| MIX | Brukte tekstiler, usortert | innsamling, usortert eksport, CO.CO → CO.SO |
| USE | Brukte, ombrukbare | CO.SO → CO.RE, CO.RE → US.HH, eksport av sorterte ombruksfraksjoner |
| WRN | Brukte, ikke ombrukbare (utslitte, ødelagte) | CO.SO → WM.RC, sorteringsrester |
| PCW | Produksjonsavfall (kapp, spill) | MA.TX → WM.RS |
| MFR | Mikrofibre (fibre som slites løs) | vask → WM.WW → EN |

MFR kunne vært slått sammen med FIB, men holdes egen fordi mikrofibre skal kunne vises separat (METODE §7).

**Blandede flyter splittes bare der det har en verdi i seg selv.** Det gjelder to steder:

* **Restavfall fra husholdninger** (US.HH → WM.RS) deles i «brukbare tekstiler i restavfall» (USE) og «utslitte tekstiler i restavfall» (WRN). Andelen brukbart kommer fra plukkanalysene (Mepex via NORSUS) som ankerpunkter. Dette er et sentralt politisk tall: hvor mye ombrukbart blir brent?
* **Sortering** (CO.SO) gir allerede USE (til CO.RE), WRN (til gjenvinning) og rest. Det er bare navngivingen som endres.

Usortert innsamling forblir MIX. Andelen ombrukbart i den er allerede en parameter (`reuse_fraction_retained`).

Fordeler: Ingen ny kolonne i resultatene, ingen endring i massebalansesjekken, og splittingen gir vanlige flyter med egne datakilder. Ulempe: En flyt kan bare ha én form. Det tvinger fram en eksplisitt splitt der formen er blandet, men det er nettopp der vi vil ha tallet.

## 2. Materiale som lag i flytkoden, beregnet etter totalmassen (forslag D19)

Her er det motsatte tilfellet: Alle flyter har en fiberfordeling, og den endrer seg over tid (mer PES). Materialet bør derfor være et ekte lag. Det brukes laget som allerede finnes i flytkoden: `...-Sales to households-PES`.

**Prinsipp: Totalmassen beregnes som i dag (TOT). Fiberlaget er en fordeling av TOT og påvirker aldri TOT.** Det følger D8: massen kommer fra statistikk, og sammensetningen kommer fra tollkoder og modell.

Fremgangsmåte:

1. **Tilført sammensetning** per produkt og år: 08801 på HS6/HS8 gir hovedfiber for store deler av klesimporten (6109.10 bomull, 6110.30 kjemiske fibre osv.). En ny kolonne `main_fibre` i `hs_mapping.csv` (på 6-sifret nivå) og en matrise *hovedfiber → fiberandeler* (et plagg klassifisert som bomull er ikke 100 % bomull) gir tilført sammensetning. Varer uten fiber i koden får produktgruppens standardfordeling fra `fibre_composition.csv`. Trenden over tid kommer da fra handelsdataene, ikke fra en antatt trend.
2. **Ikke-tekstile deler som eget materiale (NT).** Knapper, glidelåser og skosåler blir laget `NT`, i stedet for den separate `nontextile_share_*`-beregningen. Da gjelder TOT = sum av fibre + NT, og tekstilmassen er bare TOT − NT. Det forenkler D4.
3. **Blanding gjennom prosessene.** Hver prosess blander innstrømmene sine, og utstrømmene får blandingens sammensetning. Unntaket er flyter med fiberspesifikke overføringskoeffisienter, for eksempel mikrofibre (avhenger av fiber), gjenvinning (bare visse fibre er egnet) og ull til MA.FI.
4. **Lagre forsinker sammensetningen.** Det som kasseres fra US.HH i 2025, ble kjøpt for år siden. Sammensetningen av kasseringene hentes fra årgangene i lagermodellen (tilført sammensetning × levetidsfordeling), og massen fra statistikken. Det forklarer en del av forskjellen mellom tilført (NORSUS 2026: 32 % syntetisk) og kassert (Syversen 2023: 44 % syntetisk), og den forskjellen kan valideres.
5. **CORE- og ALL-radene** (innsamling og avfall er ikke delt på produkt) får sammensetningen fra blandingen i US.HH. Det er nettopp der fiberlaget gir ny informasjon.

**Gjennomføring i koden:** En egen modul `calculations/layers.py` kjøres etter alle poolene i hver iterasjon. Den leser TOT-radene og skriver fiberrader. Poolmodulene endres ikke.

To ting må på plass samtidig:

* **Massebalansen må sjekkes per lag.** `balances.py` grupperer i dag på (prosess, år). Hvis fiberrader legges til uten endring, telles massen dobbelt (TOT + sum av fibre), og sjekken feiler. Den må gruppere på (prosess, år, lag).
* **Minne.** I dag er det ca. 40 flyter × 8 produkter × 38 år ≈ 12 000 rader per iterasjon, lagret som dict-er. Med 10 lag blir det over 100 millioner rader ved 1 000 iterasjoner. Forslag: fiberlaget slås på med et flagg (`--layers fibre`), og fiberradene oppsummeres per iterasjon (løpende persentiler eller lagring som numpy-matrise per flyt) i stedet for å samles som dict-er.

Fibertyper: De ni i `fibre_composition.csv` (PES, PA, PAC, PP, EL, CO, WO, CV, OTH) pluss NT. Det kan reduseres til fem grupper for rapportering (syntetisk, bomull, ull, regenerert cellulose, annet + NT) uten å endre beregningen.

## 3. Produktdimensjonen

Den beholdes som i dag. Den svake siden er at den stopper ved salg (etter det er det CORE). Tekstilform og fiber erstatter ikke produktdimensjonen, men fiberlaget gir delvis det samme innsynet nedstrøms. Å dele innsamling og restavfall på produktgruppe (klær vs. hjemmetekstiler) er en egen sak som kan tas senere, med andeler fra plukkanalysene.

## Foreslått rekkefølge

1. **Kolonnen `form` i `flows.csv`** med test i `test_system_register.py` (gyldige koder, og ingen tom form). Liten jobb, ingen endring i resultatene.
2. **Splitte restavfall fra husholdninger i USE og WRN**, med andelen ombrukbart som ankerpunkter fra plukkanalysene (2018, 2022, 2025). Først må det sjekkes hva rapportene faktisk oppgir.
3. **Hovedfiber fra HS-kodene**: kolonnen `main_fibre` i `hs_mapping.csv` og tilført fibersammensetning per produkt og år. Kan kontrolleres mot NORSUS 2026 (41 % bomull, 32 % syntetisk) før noe annet bygges.
4. **`layers.py`** med blanding gjennom prosesser, NT som materiale, balansesjekk per lag og flagget `--layers fibre`.
5. **Årgangssammensetning fra lagermodellen** for kasseringene, og validering mot Syversen 2023.

Steg 1–3 kan gjøres uavhengig av hverandre. Steg 4 avhenger av 3, og 5 av 4.

## Åpne Python-pakker som kan gjøre deler av dette

Vurdert 2026-10-05 (kildekoden til flodym er lest).

| Pakke | Hva den gjør | Passer for oss? |
|---|---|---|
| **flodym** (PIK, github.com/pik-piam/flodym, MIT, v1.0, JOSS 2026) | Ny implementasjon av ODYM. Navngitte dimensjoner (`FlodymArray`), og **hver flyt har sine egne dimensjoner**. Årgangsbaserte lagermodeller (innstrøms- og lagerdrevet; Weibull, lognormal, normal, fast). Massebalansesjekk per prosess. Datainnlesing og Sankey. | Best match. Løser fiberlaget, årgangssammensetningen og balansen per lag. **Har ikke Monte Carlo.** |
| ODYM (Pauliuk & Heeren 2020) | Forløperen til flodym. Samme idé, eldre API. | Nei, flodym erstatter den. |
| dpmfa (Bornhöft m.fl. 2016, EMPA, PyPI) | Dynamisk probabilistisk MFA med innebygd MC. Brukt i EU-tekstil-DPMFA og plast-DPMFA-ene. | MC er bra, men den har én masse per flyt og ingen dimensjonshåndtering. Vi har allerede en egen MC-motor. |

**Hvordan flodym løser det vi trenger:**

* **Ulike dimensjoner per flyt.** Import kan være (år, produkt, fiber), innsamling (år, fiber) og mikrofibre (år, fiber). Når en prosess har flyter med ulike dimensjoner, sjekkes balansen på dimensjonene alle flytene har felles. CORE-problemet i dag (produkt forsvinner etter salg) blir da en vanlig modelleringsbeslutning, ikke en spesialregel.
* **Fiberlaget** blir en dimensjon `m` på flytene, ikke ti ganger så mange rader. Sammensetningsmatrisen ganges inn med `FlodymArray`.
* **Årgangssammensetning (steg 5)** følger med lagermodellen, fordi lageret er (år, årgang, produkt, fiber).
* **Monte Carlo kan bli en dimensjon** `s` (iterasjon). Levetidsparametrene kan variere over lagerets dimensjoner, så hver iterasjon kan få egen levetid. Da kjøres alle iterasjonene som én vektorisert beregning i stedet for en Python-løkke. Det løser også minneproblemet med dict-rader. *Dette er ikke testet, og det må prøves på et lite eksempel før vi bygger på det.*

**Hva vi beholder selv:** trekking og parametertabeller (`sampling.py`, `params.py`, ankerpunkter), datainnlasting, systemregisteret i `system/*.csv`, D8-logikken (masse fra statistikk, lagermodell parallelt) og dokumentasjonen per flyt.

**Konvensjonene i CLAUDE.md er ikke et hinder (avklart 2026-10-05):** Rader med `comment` og `data_sources` var et krav fra den offisielle rapporteringsfilen i NitrogenBudsjett, og gjelder ikke her. Datakilder og metode dokumenteres i koden og på en md-side per flyt. CLAUDE.md er oppdatert. Med flodym er en flyt en matrise, og manglende år blir NaN i matrisen.

**Forslag til kombinasjon, i to trinn:**

1. **Prototype uten å røre poolene.** Steg 4–5 over (`layers.py`) bygges med flodym. Den leser TOT-resultatene fra dagens modell, bygger et flodym-system med fiberdimensjon og årgangslager, og sjekker balansen. Da får vi prøvd pakken på det den er best på, og kan sammenligne med dagens TOT-resultater.
2. **Full overgang bare hvis prototypen er god.** Poolene flyttes én etter én til flodym-flyter, og flodym tar over `stock_model.py` og `balances.py`. Prøv MC som dimensjon `s` i dette trinnet.

## Resultat av prototypen (trinn 1)

Kode: [prototype/fibre_layer_flodym.py](../prototype/fibre_layer_flodym.py). Hovedfiber per HS-kode: [parameters/hs_main_fibre.csv](../parameters/hs_main_fibre.csv), bygget med [scripts/build_hs_main_fibre.py](../scripts/build_hs_main_fibre.py). Resultater: `output_files/prototype_fibre_shares.csv`.

**Oppsett:** Grunnlaget er den deterministiske kjøringen (iterasjon 0) av alle poolene. TOT-flytene for CL+HT+FW i husholdningene fordeles på åtte hovedfiberklasser. Tilførselen får sammensetningen til registrert import per produkt og år. Kasseringene beholder massen fra statistikken (D8), men får sammensetningen fra en parallell årgangsmodell av US.HH (flodym `InflowDrivenDSM`, Weibull). Alt nedstrøms arver sammensetningen. Lagerendringen er restleddet per fiber, og flodym sjekker massebalansen per prosess. Levetidene er ikke satt ennå, så modellen kjøres med tre scenarier (kort, middels, lang; klær 3, 5 og 8 år). Det er scenarier, ikke parameterverdier.

**Det som fungerte:**

* Systemet med 7 prosesser, 13 flyter (noen med dimensjonene år × produkt × fiber, andre med år × fiber) og ett lager balanserer i alle år og scenarier. Flytene kan ha samme navn som i `flows.csv`.
* Hovedfiber fra varetekstene stemmer med NORSUS 2026: Klær 2025 har 40 % bomull og 33 % kjemiske fibre (NORSUS: 41 % og 32 %).
* Koden ble kort: Selve fiberlaget og årgangsmodellen er ca. 100 linjer.

**Hva prototypen viser (CL+HT+FW, andel av masse):**

| | Tilført 2021 | Kassert 2021 (kort / middels / lang levetid) |
|---|---|---|
| Bomull | 34,5 % | 34,1 / 35,9 / 38,4 % |
| Kjemiske fibre (SYN+ART+MMF) | 27,3 % | 27,6 / 26,4 / 24,3 % |
| Ull | 3,1 % | 3,4 / 3,3 / 3,2 % |
| Fiber ukjent (RES+UNK) | 35,0 % | 34,9 / 34,3 / 33,9 % |

* **Årgangseffekten er reell, men liten.** Med lang levetid har kasseringene ca. 3 prosentpoeng mindre kjemiske fibre enn tilførselen, fordi de ble kjøpt da andelen var lavere. Sammensetningen i importen endrer seg for sakte til at forsinkelsen betyr mye.
* **Årgangseffekten forklarer altså ikke** at Syversen 2023 fant 44 % syntetisk i det som kastes. Den mest sannsynlige forklaringen er at de syntetiske fibrene skjuler seg i RES+UNK (ca. 35 %): restposter som «T-shirts of textile materials (excl. cotton)», belagte plagg og sko. Hvis rundt to tredjedeler av RES+UNK er syntetisk, havner vi nær 44 %.
* **Neste forbedring er derfor ikke mer modellering, men en matrise for RES/UNK**, altså hvilke fibre restpostene og kodene uten fiber inneholder per produkt (fra plukkanalyser med fibersortering eller JRC). Sko trenger egen behandling, fordi ingen koder oppgir fiber.

**Det som mangler i flodym, og som vi må bygge selv:**

* **Monte Carlo.** Prototypen er deterministisk. Iterasjoner som egen dimensjon `s` er ikke prøvd.
* **Kobling til flytsidene.** Generatoren for md-sidene (fase 5) må hente flytene fra flodym-systemet og metadata fra `flows.csv`. Det er en liten jobb, fordi flytnavnene kan være de samme som kodene i registeret.
* **Tidskonvensjon (besluttet som D20).** Flyter er summer per kalenderår, og lageret er nivået ved årsslutt. Innstrømmen regnes som om den kom midt i året (flodym-standard). `stock_model.py` regner med årets start og blir erstattet.

## Spørsmål til beslutning

* Er de åtte formkategoriene riktige? Spesielt: Skal usolgte varer være NEW (som foreslått) eller egen kategori? Skal skadede, men reparerbare produkter regnes som USE?
* Skal NT erstatte `nontextile_share_*` (forslag) eller ligge ved siden av?
* Skal fiberlaget rapporteres med ni fibre eller fem grupper?
* Skal vi gå over til flodym fullt ut (trinn 2)? Prototypen er laget, og radkonvensjonen er ikke lenger et hinder.
