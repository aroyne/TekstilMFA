# Fase D, trinn 3: tiltak i de samme scenariene (forslag)

*Notat 2026-11-05. Bygger på [tiltaksnotatet](2026-11-02_tiltak_sirkularitet_og_MFA.md), [Weijenberg m.fl. 2026](2026-11-02_Weijenberg_robust_tiltaksvurdering.md), [designnotatet](2026-11-02_D_fremtidsmodul_design.md) og [trinn 2](2026-11-05_D2_scenarier_forslag.md). Ingenting er implementert. Årstall og innhold i regelverket bør sjekkes mot rettsteksten før de brukes i en publikasjon.*

## Opplegg

* **Tiltakene (L)** kjøres i hvert av de 1 000 scenariene fra trinn 2 og i referansebanen. Det gir 1 001 × (antall tiltak + 1) kjøringer, ca. 5–6 minutter med fiberlaget.
* **Tiltakseffekten er en usikker faktor** (Weijenberg-svakheten vi ville unngå). Hvert tiltak har en effekt med et spenn begrunnet fra kilder, og effekten trekkes per scenario med latin hypercube (eget frø). Hvert tiltak får samme trekk i alle kombinasjoner der det inngår. Da er forskjellen mellom tiltakene i ett scenario bare tiltaket.
* **Robusthetsmål per tiltak:** tilfredsstillelse (andel scenarier der et mål med terskel nås), anger (hvor langt tiltaket er fra det beste tiltaket i samme scenario, som 90-persentil over scenariene) og feilrate (1 − tilfredsstillelse).
* **Sårbarhet:** hvilke X og hvilke tiltakseffekter som avgjør om et tiltak når målet (Spearman som i trinn 2, og andelen feil i øvre og nedre tredjedel av hver faktor).

## Tiltakene

| # | Tiltak | Fra | Hvordan i modellen | Effekt (usikker faktor) | Begrunnelse |
|---|---|---|---|---|---|
| L0 | Ingen nye tiltak | – | Scenarioet fra trinn 2 | – | Referanse |
| L1 | **Produsentansvar med innsamlingsmål** (WFD 2025/1892, norsk forskrift foreslått fra 2027) | 2027, full effekt 2032 | Innsamlingsandelen av registrerte kasseringer øker fra scenarioets 2025-nivå (X7) med +E1. Det tas fra brukbart og utslitt i restavfallet, mest fra brukbart (forholdet E1b). | E1: +5 til +25 prosentpoeng. E1b: 50–90 % av økningen kommer fra brukbart | Norge har allerede ca. 45 %, blant de høyeste i Europa. Nederland har mål om 50 % forberedt til ombruk eller gjenvunnet innen 2025 og 75 % innen 2030 under UPV Textiel (bør sjekkes). Frankrike har hatt produsentansvar siden 2007 og har ca. en tredjedel av det som settes på markedet samlet inn (bør sjekkes). Øvre grense: det brukbare i restavfallet (18 kt) tilsvarer ca. +20 pp. |
| L2 | **Sortering før eksport** (WFD 2025/1892, art. 22) | 2028 | Andelen av innsamlet som sorteres i Norge (X8) øker til E2 i 2032. Resten eksporteres som før. Utfallet av sorteringen følger scenarioets X9. | E2: 30–80 % sortert i Norge | **Se spørsmål 2.** 92 % av eksporten av 6309+6310 (34 kt i 2025) går til EU-land (Polen 16,9, Tyskland 5,1, Bulgaria 3,3, Litauen 2,2 kt …) og sorteres der. Hvis sortering i et annet EØS-land oppfyller kravet, er effekten på norske flyter nesten null, og L2 blir et «strengt» alternativ der sorteringen må skje i Norge. Eksportreglene for avfall (WSR fra 21.5.2027) berører bare ca. 2 kt som går utenfor OECD (Pakistan, Ukraina, Emiratene, Filippinene). |
| L3 | **Holdbarhet** (ESPR, delegert akt for klær ca. 2027, virkning ca. 2029) | 2029 | Levetiden for nye årganger av klær (CL) ganges med 1 + E3. Hjemmetekstiler og sko er ikke med i første runde. | E3: +5 til +30 % | Ingen grenseverdier er kjent. WRAP (2017): ni måneder lengre levetid for halvparten av klærne gir 4–10 % lavere fotavtrykk. Det svarer til ca. +10 % i gjennomsnitt. Kravene gjelder bare nye varer, så effekten kommer forsinket gjennom lageret. |
| L4 | **Forbud mot destruksjon** (ESPR art. 25) | 19.7.2026 for store foretak, 2030 for mellomstore | Usolgte varer som kastes (1,1 kt i 2025), går til donasjon (CO.CO) i stedet. Andelen som omfattes, er E4. | E4: 50–90 % i 2027, 80–100 % fra 2030 | Allerede vedtatt. Liten flyt med dagens data (D38: 0,2–8 kt). |
| L123 | L1 + L2 + L3 (+ L4) | | Alt sammen | De samme trekkene | Pakken som er i gang i EU |

Tekstilavgift og tiltak mot ultrarask mote (C1, C2) tas ikke med nå. Rekkefølgen fra designnotatet var produsentansvar, sortering og holdbarhet, og avgiften kommer etterpå. De kan legges til som L5 med en effekt på forbruket per innbygger (−5 til −20 % fra 2028).

## Mål med terskler (for tilfredsstillelse)

Det finnes nesten ingen tallfestede norske mål. Tersklene er derfor forslag og må bestemmes (spørsmål 1):

| Mål | Forslag til terskel | Retning | Hvorfor |
|---|---|---|---|
| Innsamlingsgrad 2035 | ≥ 50 % | høyere er bedre | Runde tall nær nederlandske mål. Viser om produsentansvaret løfter graden over dagens nivå |
| Andel eksportert usortert 2035 | ≤ 50 % | lavere er bedre | Formålet med sortering før eksport |
| Ombruk i Norge 2035 | ≥ 2 × 2025 (ca. 4 kt) | høyere er bedre | Ombruk er øverst i avfallshierarkiet |
| Tekstiler til forbrenning 2035 | ≤ 2025-nivå (ca. 106 kt) | lavere er bedre | Formålet med innsamlingen |
| Kassert fra husholdningene 2040 | ≤ 2025-nivå | lavere er bedre | Holdbarhet og forbruk |

Anger regnes for alle målene uten terskel, som avstand til beste tiltak i samme scenario.

## Det modellen må ha i tillegg

* Klassen `Policy` med tiltakene og trekkene av effektene. `Reference` tar `(scenario, policy)`, og flytfunksjonene leser begge. L0 skal gi nøyaktig trinn 2 (test).
* Levetid per årgang og produkt (L3 bare for CL). `cohort_factor` støtter det allerede.
* For L1: at innsamlingen tas fra brukbart og utslitt i restavfallet. D42-flyten (næringsavfall og grovavfall) påvirkes ikke, se spørsmål 3.
* Resultater i `output_files/future_policies*.csv`. Et plott med tilfredsstillelse og anger per tiltak, og vifter per tiltak for innsamlingsgrad og forbrenning.

## Spørsmål

1. **Terskler:** Er de fem tersklene over gode å starte med, eller finnes det mål du vil bruke (for eksempel fra forskriftsforslaget eller samfunnsoppdraget)?
2. **Sortering før eksport (L2):** Skal L2 bety at sorteringen må skje i Norge («streng», 30–80 %)? Eller skal vi modellere at sortering i EØS teller, slik at L2 i praksis bare berører eksporten utenfor EU (ca. 2 kt)? Forslag: begge, som L2-streng og L2-EØS.
3. **Produsentansvar og D42:** Skal økt innsamling også kunne nå tekstilene som i dag går som næringsavfall og grovavfall (D42-flyten), for eksempel ved at kommunene og produsentene samler inn ved flytting og dødsbo? Eller gjelder den bare husholdningsavfallet (anbefalt for nå, fordi D42-flyten ikke er observert)?
4. **Destruksjonsforbudet (L4):** Skal det være med i alle tiltakene, siden det er vedtatt? Da blir L0 «vedtatt politikk» og ikke «ingen nye tiltak». Eller skal det være et eget tiltak (anbefalt, slik at L0 fortsatt er lik trinn 2)?
5. **Avgift og ultrarask mote (L5):** Nå eller senere?
