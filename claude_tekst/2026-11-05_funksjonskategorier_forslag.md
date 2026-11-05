# Funksjonskategorier for klær og sko i lagermodellen (forslag)

*Notat 2026-11-05. Beslutninger samme dag: 5 kategorier for klær og 4 for sko, også i historikken, impulskjøp som følsomhet for tiltak, hjemmetekstiler venter. Totalen for skapet rapporteres, og en grense for hele skapet er en senere strukturvariant. Bygger på [notatet om lagermodellen](2026-11-05_lagermodellen_hvordan_og_hvor_finkornet.md) og [tidligere arbeid med sko](2026-11-05_tidligere_arbeid_sko_B2B_relevans.md). Spennene er forslag.* **Besluttet (alle fire spørsmål ok) og implementert samme dag**, se avsnitt 7.

## 1. Prinsipp

* **Registeret endres ikke.** Flytene er fortsatt per produkt (CL, FW). Inne i lagermodellen deles hver årgang av klær og sko i kategorier etter andelene av massen i SSB 08801 (HS8) det året. Hver kategori har egne levetider. Utstrømmen og lageret summeres tilbake til produktet. Totalen for skapet rapporteres per produkt og samlet.
* **Kassering som to konkurrerende risikoer per kategori:** teknisk (slitt ut) og opplevd (umoderne, lei, vokst ut av, passer ikke). Overlevelsen er S(a) = S_teknisk(a) × S_opplevd(a), begge Weibull. `cohorts.survival` regner allerede overlevelse år for år og kan utvides til to faktorer.
* **Nivået beholdes.** Levetidene skaleres med én felles faktor per produkt, slik at den gjennomsnittlige kasseringstiden for tilførselsmiksen i 2025 er lik dagens parameter (klær 6 år, 4–9 i MC; sko 4 år, 3–6). Kategoriene endrer da fordelingen og dynamikken, ikke nivået. Hovedresultatet for historikken flytter seg lite, bortsett fra der tilførselsmiksen har endret seg over tid.

## 2. Kategorier og koblingen til HS-koder

| Kategori | HS4 (08801) | Merknad |
|---|---|---|
| **K1 Undertøy, sokker, nattøy** | 6107, 6108, 6115, 6207, 6208, 6212 | |
| **K2 Overdeler** (T-skjorter, skjorter, bluser, strikk, gensere) | 6105, 6106, 6109, 6110, 6205, 6206 | |
| **K3 Underdeler og kjoler** (bukser, jeans, skjørt, kjoler, dresser) | 6103, 6104, 6203, 6204 | |
| **K4 Yttertøy, funksjons- og sportsklær, tilbehør** | 6101, 6102, 6112, 6113, 6114, 6116, 6117, 6201, 6202, 6210, 6211, 6213–6217 | Tilbehør (votter, skjerf, slips) er lagt her (lang levetid) |
| **K5 Barneklær** | 6111, 6209 | Barneklær under andre koder havner i K1–K4 |
| **S1 Sport og fritid** | 6402.1x, 6403.1x, 6404.11 | |
| **S2 Hverdags- og pensko i lær** | 6403.5x, 6403.99 | |
| **S3 Vinter, tur og vanntett** | 6401, 6402.91, 6403.91 | Med skaft over ankelen (støvler) |
| **S4 Annet** (sandaler, tøfler, tekstilsko) | 6402.20, 6402.99, 6404.19, 6404.20, 6405 | |

Koblingen er en ny tabell, `parameters/hs_function_category.csv`, med HS8 → kategori og kilde.

## 3. Parametre per kategori (forslag til spenn)

Levetidene er **relative**. De skaleres til nivået for produktet (avsnitt 1). For hver kategori angis forholdet mellom teknisk og opplevd levetid og forholdet til snittet for produktet.

| Kategori | Relativ kasseringstid (snitt = 1) | Andel kasseringer som skyldes slitasje | Andel slitasje som kan repareres | Følsomhet for avgift og deling (snitt = 1) |
|---|---|---|---|---|
| K1 Undertøy, sokker | 0,5–0,8 | 0,6–0,9 | 0–0,1 | 0,2–0,6 |
| K2 Overdeler | 0,8–1,1 | 0,3–0,6 | 0,1–0,3 | 1,2–1,8 |
| K3 Underdeler, kjoler | 1,0–1,3 | 0,4–0,7 | 0,3–0,6 | 0,8–1,2 |
| K4 Yttertøy, funksjon | 1,4–2,0 | 0,3–0,6 | 0,4–0,7 | 0,5–0,9 |
| K5 Barneklær | 0,3–0,6 | 0,1–0,3 (de vokser ut av dem) | 0,1–0,3 | 0,6–1,0 |
| S1 Sport og fritid | 0,6–1,0 | 0,5–0,8 | 0,05–0,3 | 1,0–1,5 |
| S2 Lær, hverdag og pen | 1,0–1,5 | 0,3–0,6 | 0,4–0,8 | 0,7–1,1 |
| S3 Vinter, tur | 1,5–2,5 | 0,2–0,5 (umoderne før utslitt) | 0,3–0,7 | 0,4–0,8 |
| S4 Annet | 0,5–1,0 | 0,4–0,7 | 0–0,2 | 1,0–1,6 |

Grunnlag:
* **Relativ kasseringstid:** WRAP (2021) gir aktiv bruk i snitt 3,3 år, over 5 år for frakker, jakker og yttertøy, og under 3 år for undertøy, sokker og leggings. Valuing our clothes (2012) gir frakker 4,6, kjoler 3,6, gensere 3,5, jeans 3,4, T-skjorter 2,8 og snittet 3,3 år. For sko bruker vi forholdene fra agentmodellen (ISEE 2025): tursko har lang teknisk og opplevd levetid, og pensko og sportssko kort.
* **Andel kasseringer som skyldes slitasje:** Laitala viser i sin oversikt at kvalitet og størrelse er de vanligste årsakene og mote sjeldnere (én studie: 4 % for «umoderne»), men at to av tre plagg kasseres før de er utslitt. WRAP (2021) finner at uegnethet (smak, passform) dominerer for plagg som ikke brukes. Agentmodellen viser at slitesterke sko kasseres fordi de oppleves som utdaterte. Andelen avgjør hvor mye holdbarhet (L3) og reparasjon (L7) kan gi. **X18 erstattes av den.**
* **Andel som kan repareres:** Det finnes ingen tall for husholdninger. Spennene er skjønn. Registreringen av kassasjonsårsaker i B2B kan gi et anslag når det er avklart hvordan den kan brukes.
* **Følsomhet for tiltak (impulskjøp):** Den ganger effekten av L5 (avgift) og L8 (deling) per kategori. Den normaliseres slik at gjennomsnittet vektet med massen er 1, så samlet effekt er sammenlignbar med trinn 4. Rangeringen følger hvor mye impulskjøp og mote det er (YouGov og WRAP: «kjøpt på impuls» og «lei av den»), mens tallene er skjønn.

**Formparameter:** 2 for teknisk og 1,5 for opplevd levetid, siden mote og smak er mer spredt. Begge er usikre faktorer i en strukturkjøring.

## 4. Hvordan tiltakene virker per kategori

* **L3 holdbarhet:** Bare teknisk levetid, og bare klær (ESPR, første runde). Kategoriene der få plagg kasseres fordi de er slitt ut (K2, S3), får liten effekt.
* **L7 reparasjon:** Periodeeffekt på den tekniske risikoen. Gevinsten er effektstørrelsen × andelen som kan repareres i kategorien.
* **L5 og L8:** Det ønskede lageret (lagerdrevet) eller kjøpene (tilførselsdrevet) per kategori, med effekten × følsomheten.
* **X4b (ultrarask mote):** Bare opplevd levetid, og bare K2, K3 og S1.

## 5. Kalibrering og kontroll

* **Nivå:** Den gjennomsnittlige kasseringstiden per produkt er lik dagens parameter, som i avsnitt 1.
* **Sammensetning av kasseringene:** Mepex (Syversen m.fl. 2023) har kasseringene fordelt på overdeler (tynne og tykke), underdeler, yttertøy, barn, sport og arbeid, og sko. Når tilførselen er nesten flat, følger sammensetningen av kasseringene sammensetningen av tilførselen. Sammenligningen kontrollerer derfor først og fremst koblingen fra HS-koder til kategorier, og bare svakt levetidene.
* **Sammensetning av lageret:** Garderobestudiene (Klepp, Laitala og Haugrønning, antall plagg per type) begrenser de relative levetidene sterkere, fordi lageret av en kategori er tilførsel × levetid. Det krever vekt per plagg per kategori (08801 har stykk og kg per HS-kode) og tallene fra OsloMet (henvendelsen er allerede listet).
* **Historikken:** Tilførselsmiksen har endret seg, for eksempel med mer trikotasje og sportstøy. Den gjennomsnittlige levetiden for klær kan derfor endre seg over tid uten at en trend legges inn. Effekten på lagerdiagnosen rapporteres.

## 5b. Tilstanden til kasseringene: brukbart eller ødelagt (lagt til etter innspill)

Årsaken til kasseringen bestemmer om plagget kan brukes igjen:
* **Kassert på grunn av opplevd levetid** (umoderne, lei, vokst ut av, passer ikke) er **brukbart**.
* **Kassert på grunn av teknisk levetid** (slitt ut, skadet) er **brukbart bare hvis det repareres**. Den delen som kan repareres, er brukbar (Mepex regner «litt slitt, feil som enkelt kan fikses» som brukbart, tilstand 2). Resten er **ødelagt** og går til gjenvinning eller restavfall.

Andelen ødelagt per kategori er da: andel kassert på grunn av slitasje × (1 − andel som kan repareres).

**Data (Syversen m.fl. 2023, tabell 23, andel brukbart, vektet, alle strømmene):**

| Kategori hos Mepex | Brukbart | Ødelagt | Vår kategori |
|---|---|---|---|
| Overdeler A (tynn) og B (tykk) | 80 % og 86 % | 14–20 % | K2 |
| Underdeler | 77 % | 23 % | K3 |
| Yttertøy | 71 % | 29 % | K4 |
| Sport, fritid, overall, arbeidstøy | 72 % | 28 % | K4 |
| Barn og baby | 85 % | 15 % | K5 |
| Klær annet (intimplagg, sokker, regntøy) | 58 % | 42 % | K1 |
| Sko | 56 % | 44 % | S1–S4 |
| Tekstilboks / restavfall HH / restavfall GVS | 81 / 66 / 64 % | | Utvalget ved innsamling |

**Konsekvenser for parametrene i avsnitt 3:** Andelen kassert på grunn av slitasje blir bundet av data. For overdeler, med 17 % ødelagt og 10–30 % som kan repareres, er den bare ca. 0,2–0,25. Spennet i avsnitt 3 (0,3–0,6) er for høyt og må strammes inn mot Mepex. Holdbarhet (L3) betyr da mindre for overdeler. Undertøy og sokker (ca. 0,45–0,5) og sko (ca. 0,5–0,6) har høyere andel kassert på grunn av slitasje, og der virker holdbarhet og reparasjon mer.

**Bruk i modellen:**
* **Historikken:** Tilstanden regnes per kategori og år og kontrolleres mot Mepex 2021–2022 og mot andelen brukbart i restavfallet for 2018, 2022 og 2025 (D18). Flytene er fortsatt fra data (D8). Tilstanden er kalibrering og diagnose.
* **Fremtiden:**
  * Andelen brukbart i restavfallet (brukbart mot slitt) og det maksimale ombruket fra sorteringen følger tilstanden. X9 for ombruk blir begrenset av andelen brukbart i det som samles inn, og X13 er fortsatt grensen for markedet.
  * Innsamlingen tar bare litt mer av det brukbare (81 % mot 64–66 %). Den forskjellen holdes fra data.
* **Tiltak som endrer tilstanden:** Reparasjon (L7) gjør at færre plagg kasseres som ødelagte, og at flere blir værende i bruk. Holdbarhet (L3) gir færre utslitte. Kortere opplevd levetid (X4b) gir flere brukbare kasseringer. Det øker potensialet for ombruk, men ikke nødvendigvis ombruket.
* At noe er brukbart, betyr ikke at det blir brukt igjen. Det faktiske ombruket bestemmes av sorteringen og markedet.

## 6. Kostnad og rekkefølge

1. Koblingen fra HS8 til kategori og andelene av tilførselen per år (en ny datafunksjon, test på at andelene summerer til 1).
2. Overlevelse med to risikoer per kategori i `cohorts.py` (test på at én kategori med opplevd levetid uendelig gir dagens Weibull).
3. Undergrupper i lagermodellen for CL og FW, i historikken (us_mc og fiberlaget) og i fremtiden (future.py, lagerdrevne kjøp per kategori).
4. Tiltak per kategori og nye usikre faktorer (spennene over, trukket med latin hypercube).
5. Tilstanden til kasseringene (5b) og kalibrering av andelen kassert på grunn av slitasje mot Mepex tabell 23.
6. Kontroll mot Mepex og eventuelt garderobedata, dokumentasjon og ny kjøring.

Anslått arbeid er 1–2 økter.

## Spørsmål

1. **Kategoriene og HS-koblingen:** Er det greit at tilbehør legges i K4, og at barneklær bare fanges via 6111 og 6209?
2. **Spennene i avsnitt 3:** Er de rimelige? Andelen kasseringer som skyldes slitasje kalibreres nå mot andelen ødelagt hos Mepex (5b), gitt andelen som kan repareres. Er det riktig at den bindes slik, og ikke settes fritt?
3. **Nivået:** Er det greit at kategoriene skaleres til dagens gjennomsnittlige levetid per produkt, så de endrer fordelingen og ikke nivået?
4. **Usikkerheten:** Skal parametrene per kategori være usikre faktorer i fremtidsscenariene (ca. 36 nye) og ha fordelinger i MC for historikken? Alternativet er faste midtverdier med en strukturkjøring.

## Kilder

* WRAP (2021), Clothing longevity and measuring active use. https://www.wrap.ngo/sites/default/files/2021-04/Clothing%20Longevity%20Report.pdf
* WRAP (2012), Valuing our clothes. https://www.wrap.ngo/sites/default/files/2021-01/WRAP-valuing-our-clothes-2012-07-11.pdf
* Laitala, K. (2014), Consumers' clothing disposal behaviour, a synthesis of research results. https://www.researchgate.net/publication/265690075_Consumers'_clothing_disposal_behaviour_-_a_synthesis_of_research_results
* Laitala & Klepp (2021), Clothing longevity: the relationship between the number of users, how long and how many times garments are used. https://clothingresearch.oslomet.no/wp-content/uploads/sites/1026/2025/04/Laitala-et-al_2021_Clothing-longevity-The-relationship.pdf
* Klepp, Laitala & Wiedemann (2020), Clothing lifespans: what should be measured and how. https://www.mdpi.com/2071-1050/12/15/6219
* YouGov, Bored with your clothes? https://yougov.com/en-gb/articles/3807-bored-your-clothes
* Røyne & Simon (2025), ISEE, agentbasert modell for sko (eget arbeid, OneDrive)
* Syversen m.fl. (2023), Dypdykk i materialstrømmene for tekstiler fra husholdninger i Norge, Mepex

## 7. Implementering (2026-11-05)

* `calculations/categories.py`:
  * kobling fra HS til kategori, med test på at alle koder for klær og sko er dekket
  * andeler per år
  * levetider per enhet fra relativ levetid, andel ødelagt og andel som kan repareres (tabellert invers for andelen slitasje og gjennomsnittet)
  * følsomhet for tiltak
  * `household_core_cohorts`
* `cohorts.competing_survival` og `cohorts.unit_cohorts`: konkurrerende risikoer, periodeeffekt og ødelagte kasseringer. Testet mot Weibull uten opplevd levetid.
* 38 parametre i `global_parameters.csv`, trukket flatt i MC. Andelen ødelagt har ±25 % rundt Mepex. Hjemmetekstiler: 32 % ødelagt (Mepex «Husholdning»). Garn: 24 % (antatt lik klær).
* **Endrede spenn:**
  * Andelen som kan repareres, må være under 1 − andelen ødelagt. For yttertøy er den derfor 0,3–0,6, og for sko 0,05–0,3 (sport), 0,15–0,4 (lær, vinter) og 0–0,2 (annet). En kombinasjon som ikke går opp, gir feilmelding.
  * L7 er nå opptaket av reparasjon (0,2–0,8): andelen av feilene som kan repareres og som faktisk repareres.
* **Historikken:** Fiberlaget og vaskeutslippet fra institusjonene bruker kategoriene. Andelen brukbart i kasseringene er 70 % (klær 75 %, sko 55 %, hjemmetekstiler 68 %), mot 72 %, 76 %, 56 % og 68 % hos Mepex. Ny utgang: `US.HH-US.HH-Stock model broken discards-TOT`.
* **Fremtiden:** `Reference` bygger enhetsoppsettet. Lagerdrevne kjøp regnes per enhet. Tilstanden til kasseringene skalerer andelen brukbart i restavfallet og ombruket fra sorteringen. X18 er fjernet. Kategoriparametrene er usikre faktorer i scenariene.
* **Gjenstår:**
  * Kalibrering mot sammensetningen av lageret (garderobedata fra OsloMet).
  * Grense for hele skapet som strukturvariant.
  * Fibersammensetning per kategori (nå har kategoriene sammensetningen til produktet).

## 8. Resultater med kategoriene (1 000 scenarier, 2026-11-05)

* **Historikken (MC, N = 1 000):** Lagermodellens lager i 2025 er 571 kt (389–758), mot 566 kt uten kategorier, fordi nivået er kalibrert. 30 % av kasseringene er ødelagte (27 av 92 kt). Restleddet er 1 174 kt (446–1 823). MC tar nå 626 s, mot 110 s. Lagermodellen med kategorier regnes to ganger per iterasjon (fiberlaget og `us_mc`) og bør bufres.
* **Effekt på ny tilførsel per innbygger, lagerdrevet etterspørsel**, sammenlignet med L0 i samme scenario:

| | 2035 uten kategorier | **2035 med kategorier** | 2050 med kategorier |
|---|---|---|---|
| L3 holdbarhet | −4 % | **−2 %** (−4 til −0,3) | −4 % |
| L7 reparasjon | −10 % | **−2,4 %** (−4,7 til −0,6) | −2 % |
| L5 avgift | −14 % | −14 % | −15 % |
| L8 deling | −4 % | −4 % | −5 % |
| Alle | −35 % | **−28 %** (−43 til −5) | −31 % |

* **Holdbarhet og reparasjon virker mindre** når andelen kassert på grunn av slitasje er bundet til tilstandsdataene fra Mepex. De fleste klær kasseres før de er utslitt (overdeler: ca. 20 % på grunn av slitasje). Da kan lengre teknisk levetid og reparasjon bare nå en liten del av kasseringene. Det stemmer med funnet i den agentbaserte modellen for sko (ISEE 2025): Slitesterke sko kasseres fordi de oppleves som utdaterte.
* Andelen brukbart i kasseringene øker litt med tiltakene, fra 71 % (L0) til 73–75 % (L3, L7, alle) i 2035–2050. Det gir litt mer å ombruke.
* Målet om −30 % ny tilførsel per innbygger i 2035 nås med alle tiltakene i 40 % (lagerdrevet) og 49 % (tilførselsdrevet) av scenariene. Rebound (ρ = −0,61) og trenden i ønsket lager (−0,46) avgjør.
