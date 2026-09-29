# Spørsmål og valg fra fase 2 (kjerneflyter)

*2026-09-29. Samlet mens du var borte. Der det trengtes en beslutning, har jeg valgt det jeg anbefaler og bygget det slik at det er lett å endre. Hvert punkt sier hva som er gjort, og hva jeg trenger fra deg.*

**Status:** Alle 13 kjerneflyter (P1) er implementert og kjører i MC for 1988–2025. Massebalansen sjekkes i hver iterasjon, og testene går gjennom (11). Resultater: `output_files/MC_summary.csv`.

**Figur:** [output_files/plots/core_household_flows.png](../output_files/plots/core_household_flows.png) viser tilført, innsamlet, restavfall og lagerendring for husholdningene med 95 %-intervall. Laget av `scripts/plot_core_flows.py`. Bruddet i restavfallet før 2018 (A1) er godt synlig.

---

## A. Viktigst – påvirker resultatene mye

### A1. Restavfall før 2018: SSBs tall for 1990-tallet ser ut til å være beregnet ut fra tilførsel
SSBs tekstilregnskap oppgir klær i avfallet: 34,8 kt (1991) og 47,2 kt (1998). Netto import av klær fra 08801 var **34,5 kt og 46,6 kt** de samme årene. Tallene er nesten identiske. Det tyder sterkt på at SSB i praksis satte avfall ≈ tilførsel (varetilførselsmetoden), selv om teksten sier at de valgte avfallsstatistikken.

**Implementert (D15 som besluttet):** Ankerpunkt 1998 = 58,5 kt restavfall for CL+HT+FW, omregnet fra SSB med ±40 %. Verdien holdes konstant før 1998 og interpoleres lineært til 31,6 kt i 2018.

**Konsekvens:**

| | 1990 | 1995 | 1998 | 2005 | 2010 | 2015 | 2018 |
|---|---|---|---|---|---|---|---|
| Tilført til husholdninger (kt) | 45,1 | 55,6 | 61,6 | 85,7 | 96,3 | 88,0 | 85,8 |
| Restavfall, D15 | 58,5 | 58,5 | 58,5 | 49,1 | 42,3 | 35,6 | 31,6 |
| Lagerendring, D15 | **−14,9** | −7,0 | −4,1 | 23,9 | 34,8 | 22,9 | 16,5 |
| Restavfall, alternativ (fast forhold restavfall/tilført fra 2018) | 16,6 | 20,5 | 22,7 | 31,5 | 35,4 | 32,4 | 31,6 |
| Lagerendring, alternativ | 27,0 | 31,0 | 31,7 | 41,4 | 41,7 | 26,1 | 16,5 |

Samlet lagerendring 1988–2017 blir **+282 kt med D15** og **+987 kt med alternativet**. Begge er vanskelige å forsvare. Med D15 krymper lageret på 1990-tallet. Med alternativet vokser det med ca. 180 kg per person. Rapportene selv finner et avvik mellom tilført og avhendet på 7–28 kt per år. Det tyder på at restavfall + innsamling ikke fanger opp alle kasseringer (næringsliv, andre kanaler, oppmagasinering).

**Spørsmål:**
1. Skal SSB-ankeret for 1998 beholdes som nivå (D15), eller bare brukes til andeler (deponi mot forbrenning), slik vi gjorde med 05281?
2. Hvis det ikke brukes som nivå: hvilken regel skal gjelde før 2018? Alternativer: (a) fast forhold til tilført (tabellen over), (b) fast restavfall per innbygger fra 2018, (c) lagermodellen (bryter med D8, men bare der det ikke finnes uavhengige data).
3. Vil du spørre SSB om tekstilregnskapet 1990–1998 var basert på tilførsel? Det kan tas sammen med spørsmålet om 05281.

### A2. Direkte netthandel: 2018-anslaget passer ikke med VOEC-tallene
D7 er implementert slik notatet foreslo: 0 i 2000, 3,3 kt i 2018 (Watson 2020 / Virke), og Tolletatens VOEC-tall for 2022–2025 (0,5 / 4,8 / 3,8 / 14,0 kt). Det gir et **fall fra 3,3 kt i 2018 til 0,5 kt i 2022**, som neppe er reelt. To mulige forklaringer:
- 2018-tallet (3,2 mrd NOK) gjelder all netthandel fra utlandet, også pakker over 350 kr, som allerede er deklarert og ligger i 08801. Da er det dobbelttelling.
- VOEC-tallene for 2022 er ufullstendige, fordi overgangsordningen for 350-kronersgrensen varte til 1.1.2024.

**Spørsmål:** Skal 2018-ankeret fjernes, slik at flyten går fra 0 (rundt 2010?) til VOEC-tallene fra 2022? Min anbefaling er ja, og at 2018-tallet omtales som et diskusjonspunkt.

### A3. Innsamling: justert formel for D17
D17 sa «innsamlet = eksport ÷ eksportandel». I 2022 og 2025 er eksporten av brukte tekstiler (31,6 og 34,3 kt) **større** enn det innsamlerne rapporterer (29,6 og 33,7 kt). Eksportandelen blir da over 1, og balansen i CO.CO går negativ.

**Implementert i stedet:** innsamlet = eksport + andel som beholdes i Norge. Andelen som beholdes er et ankerpunkt: 3,3 % (2018), 2,9 % (2022), 5,8 % (2025), konstant før 2018. Av det som beholdes, går en andel til bruktbutikk (54 %, 95 %, 82 %), og resten til restavfall.

Det følger ideen i D17 (eksport som årlig hovedserie), men innsamlingen i modellen blir litt høyere enn innsamlernes egne tall, fordi eksporten også dekker aktører utenfor nettverket.

**Spørsmål:** Er denne tolkningen av D17 ok?

### A4. Eksport av restavfall (D11) – implementert etter at listen ble skrevet
SSB 13035 (KOSTRA) gir andelen av restavfallet som eksporteres: 16 % (2015), 16 % (2018), 13 % (2022), 12 % (2025). Andelen brukes på alle tekstiler i WM.RS, også fra næringslivet. Det gir 10–14 kt tekstiler per år eksportert til forbrenning i utlandet siden 2012.
- **Før 2015 finnes ingen offisielle tall.** Jeg har antatt 0 i 2005 og lineær økning til 2015-nivået. Har du en kilde, for eksempel Miljødirektoratets tall for grensekryssende avfall eller svensk importstatistikk?
- Handelsstatistikken (HS 3825.10) fanger ikke opp denne eksporten (bare 0–27 kt i alt per år).
- SSB 13035 har også «Tekstiler til ombruk» fra kommunene (13–21 kt per år, 2015–2025). Den serien er ikke brukt ennå, men kan være en kontroll av innsamlingen.

## B. Forenklinger jeg har gjort (bør bekreftes)

### B1. Produktgrupper etter salg
Import, eksport og salg beregnes per produktgruppe (CL, HT, FW, CA, SA, TA, OM). Innsamling, restavfall, sortering og bruktsalg har bare en samlet verdi for CL+HT+FW (merket `CORE`), fordi statistikken ikke skiller mellom dem. Avfallsbehandlingen (deponi og forbrenning) er merket `ALL`. **Ok?**

### B2. Varer uten avfallsstatistikk kastes samme år som de kjøpes
Tepper, presenninger/telt og andre konfeksjonerte varer (CA, TA, OM), og **alt** som brukes av næringsliv og offentlig sektor (US.IC), har ingen kasseringsstatistikk. De er foreløpig satt til å kastes samme år som de tilføres, altså uten lagerendring, og gå til restavfall. Sekker (SA) følger D13.
- For CA er dette tvilsomt, fordi tepper har lang levetid. Alternativet er lagermodellen, men den mangler levetidsparametre (se C1).
- **Spørsmål:** Ok som foreløpig løsning, eller skal disse gruppene bruke lagermodellen når levetidene er på plass (et unntak fra D8, fordi det ikke finnes offisielle data)?

### B3. Andel til næringsliv og offentlig sektor
Satt til **12 %** (PERT 8–15 %) for alle produkter unntatt sekker, etter den danske fordelingen som alle de norske rapportene bruker. Nederland har ca. 8 % arbeidstøy. **Ok?**

### B4. Grensehandel
- Påslaget fra tollverdi til utsalgspris er satt til **2,5** (PERT 1,8–3,5). Det er en ren antakelse. Har du en kilde, for eksempel SSBs prisstatistikk eller en bransjekilde?
- Før 2004 holdes massen på 2004-nivå (D16).
- Resultat: ca. 0,9 kt per år før pandemien, 0,1 kt i 2020 og 0,4–0,5 kt i 2023–2025.

### B5. Ikke implementert ennå (planlagt P2/P3)
Norsk produksjon (MA), usolgte varer, materialgjenvinning som egen flyt (ligger nå i «sorting residues»), mikrofibre, og innsamling fra næringslivet.

## C. Mangler data eller kilder

### C1. Levetider for den parallelle lagermodellen
`parameters/lifetimes.csv` er tom. Lagermodellen er ferdig kodet og testet, men kan ikke kjøres før vi har levetider. Kandidater (må leses i fulltekst): Laitala & Klepp 2020 (Sustainability 12, 9151), Kawecki m.fl. 2021 (RCR 173, 105733) og Napolano m.fl. 2024 (RCR). Disse ble blokkert for nedlasting. **Kan du legge PDF-ene i `litteratur/` eller i Zotero?**

### C2. Startlager (D2)
Lagerendringen er beregnet, men ikke lagernivået, fordi det krever et startlager i 1988. Forslaget i D2 var innsvinging med lagermodellen, og det venter på C1.

### C3. Usikkerheter satt som plassholdere
- SSB 08801: ±5 % (plassholder)
- Grensehandel: ±10 % (plassholder)
- Plukkanalyser (restavfall): ±30 %, begrunnet med Nørup 2019 (standardavvik 35–50 %), tørr/fuktig vekt (opptil 20 %) og representativitet (Syversen 2023)
- VOEC: ±50 % («veiledende»)
- Pedigree-basert usikkerhet (fase 4) skal erstatte plassholderne.

## D. Mindre ting
- D1. Syversen 2023 (2021) og NORSUS 2023 (2022) har **nøyaktig samme** restavfall (48 809 t), fordi begge bruker samme Mepex-database. Bare 2022 er brukt som ankerpunkt, så de ikke telles dobbelt.
- D2. Ankerpunktene trekkes uavhengig av hverandre i MC. Det overdriver trolig variasjonen fra år til år mellom ankerårene. Korrelasjon kan legges inn senere.
- D3. `output_files/MC_summary.csv` ligger i git. Skal resultatfiler ligge i git (som i NitrogenBudsjett), eller lages på nytt lokalt?
