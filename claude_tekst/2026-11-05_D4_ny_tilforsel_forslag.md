# Fase D, trinn 4: lavere tilførsel av nytt materiale som mål (forslag og vurdering av nyhet)

*Notat 2026-11-05. Bygger på trinn 1–3, [lagerdiagnosen](2026-11-02_C_lagerdiagnose.md), [opphopningen](2026-11-05_opphopning_hos_forbruker.md) og [datagrunnlaget](2026-11-05_lagerets_datagrunnlag_og_nevnerproblemet.md). Nettsøk, ikke systematisk. Funn om nyhet er derfor foreløpige.* **Besluttet og implementert samme dag** (punkt 1–5 ja, alle tiltakene L6–L9 med, klimaindikatoren venter), se resultatene i avsnitt 8.

## 1. Hvorfor modellen må endres

Målet i sirkulærøkonomien er lavere tilførsel av nytt materiale, ikke mer ombruk eller gjenvinning i seg selv. I trinn 1–3 er tilførselen gitt utenfra (2025-nivå per innbygger × befolkning × trend). Tiltakene kan derfor ikke senke kjøpene, bortsett fra avgiften (L5). Konsekvensen så vi i L3: Lengre levetid uten færre kjøp gir fullere garderober (+110 kt i 2050) og bare en midlertidig nedgang i kasseringene (−12 % i 2035, −1 % i 2050).

## 2. Forslag: kjøpene følger av behovet (lagerdrevet modell) for CL+HT+FW

**Prinsippet:** Husholdningene har et ønsket lager i bruk S*(t) (kg per innbygger × befolkning). Nye kjøp er det som trengs for å holde lageret der:

> nye kjøp(t) = [S*(t) − S*(t−1)] + utstrømmen fra lageret(t) − d × bruktkjøp(t)

* **Utstrømmen** kommer fra årgangsmodellen (levetider per årgang, som i dag).
* **d er erstatningsgraden for brukt**: hvor mange nye plagg ett kjøpt brukt plagg erstatter. Den delen av bruktkjøpene som ikke erstatter nytt (1 − d), kommer i tillegg til lageret og kasseres senere.
* **Rebound r**: en andel av reduksjonen i kjøp som kommer tilbake som andre kjøp (eller tyngre og dyrere plagg). Den legges til de nye kjøpene.
* Årgangsmodellen må løses år for år, fordi kjøpene i år avhenger av utstrømmen, og utstrømmen avhenger av tidligere kjøp. Det er en enkel løkke med flodym sin overlevelsesmatrise, eller `StockDrivenDSM` med bruktkjøp som eget tillegg.

**Kalibrering i 2025:**
* **S\*(2025)** settes til lagermodellens lager i 2025 (ca. 101 kg per innbygger, 69–135 i MC). Restleddet (ca. 210 kg) er trolig for høyt (datagrunnlaget). Hvilket nivå som er riktig, blir en usikker faktor (X14).
* **Kjøpene i 2025** i modellen ganges med en faktor som gjør at de treffer faktisk tilførsel i 2025 (ca. 88 kt nye varer til husholdningene, CORE). Det er det samme grepet som skaleringen av kasseringene (s).
* **Kasseringer:** utstrømmen × s er det statistikken fanger. Resten, (1 − s) × utstrømmen, går til D42-flyten (næringsavfall og grovavfall). Det erstatter balanseregelen fra D42 og gir et fysisk konsistent bilde: Lageret følger S\*, og gapet er en fast andel av kasseringene.

**Hva som ikke endres:** historikken, de andre varegruppene, institusjonene (tilførselsdrevet som nå), alt etter kassering og fiberlaget.

**Begge formuleringene beholdes.** Tilførselsdrevet (trinn 1–3) og lagerdrevet (trinn 4) kjøres i de samme scenariene som to modellstrukturer. Det er i seg selv et funn: Hvilke konklusjoner om tiltak avhenger av hvordan etterspørselen er modellert?

## 3. Nye usikre faktorer

| # | Faktor | Spenn | Begrunnelse |
|---|---|---|---|
| X14 | Ønsket lager 2025 | 70–135 kg per innbygger | MC-intervallet for lagermodellen (69–135), garderobedata 55–110 kg klær per voksen |
| X15 | Ønsket lager per innbygger, trend uten tiltak | −1 til +1 % per år til 2035 | Ingen data om vekst i garderobene (Klepp & Laitala 2015, via Watson m.fl. 2018) |
| X16 | Erstatningsgrad for brukt (d) | 0,1–0,85 | Farrant m.fl. (2010): 60–85 % (85 % er et «best guess»). Spørreundersøkelser: 10–60 % (LCA-studie 2025). Studier fra Malawi, Mozambique og Angola: 28–90 %. Det finnes også tegn på at bruktkjøp kommer i tillegg til nytt (positiv korrelasjon, PNAS Nexus 2025) |
| X17 | Rebound (r) | 0–100 % av reduksjonen | Yerushalmi & Saha (2025, BSE) finner globalt «backfire», ca. 155 % i kroner. En agentbasert studie finner nedgang i nye kjøp til tross for rebound. Over 100 % testes som strukturkjøring |
| X18 | Andel av holdbarheten som brukes | 20–100 % | Lengre teknisk levetid gir ikke nødvendigvis lengre bruk. Brukeren bestemmer når plagget kastes («nurture» hos Krych & Pettersen 2025) |

X1–X13 og effektene fra trinn 3 beholdes.

## 4. Mål

| Mål | Definisjon | Forslag til terskel |
|---|---|---|
| **M-ny: Ny tilførsel per innbygger** | Nye CL+HT+FW til husholdningene (salg + privatimport + netthandel − returer), kg per innbygger | **−30 % i 2035 sammenlignet med 2025** (ca. 16 → 11 kg) |
| **M-jomfru: Jomfruelig fiber** | Ny tilførsel × tekstilandel × (1 − resirkulert innhold), etter fibertype (fiberlaget) | −30 % i 2035 |
| M-utland: Fortrengt nytt i utlandet | Eksportert ombruk × d | Rapporteres for seg (ingen terskel) |
| Kasseringer, forbrenning, innsamlingsgrad | Som i trinn 3 | Som i trinn 3 |

Hot or Cool Institute (2022) sier at kjøpene av nye klær i de fleste høyinntektsland må ned til omtrent 2010-nivå. Kildene oppgir tall per plagg som spriker (5 nye plagg per år eller en garderobe på 85 plagg). Det må sjekkes i originalen. For Norge var 2010 en topp i tilførselen, så et prosentmål sammenlignet med 2025 er tydeligere.

## 5. Tiltak med dette målet

| # | Tiltak | Virkemåte i lagerdrevet modell | Effekt (usikker) |
|---|---|---|---|
| L3 | Holdbarhet (ESPR) | Lengre levetid for nye klær fra 2029 gir færre kjøp | +10–50 % × X18 |
| L5 | Avgift eller tiltak mot ultrarask mote | Lavere ønsket lager (S\*) fra 2028 | −10 til −30 % |
| **L6** | **Ombruk i Norge** (støtte, krav om ombrukskanaler, momsfritak) | Større bruktmarked (X13 opp), og bruktkjøp erstatter nytt med d | Markedet × 1,5–3 |
| **L7** | **Reparasjon** (støtte, rett til reparasjon) | Lengre levetid for hele lageret fra 2027, ikke bare for nye årganger | +5–20 % |
| **L8** | **Utleie og deling** | Lavere S\* og samme bruk | −5 til −15 % |
| **L9** | **Krav til resirkulert innhold** (ESPR) | Bare M-jomfru: resirkulert andel av ny fiber | 5–25 % i 2035 |
| L-alle | Alle | | |

L1, L2 og L4 fra trinn 3 virker ikke på ny tilførsel i en lagerdrevet modell. De tas med for å vise nettopp det.

L7 er en periodeeffekt: Levetiden for plagg som allerede er i bruk, endres også. Årgangsfaktoren i `use_cohorts` dekker bare årgangseffekter, så L7 må tilnærmes som lengre levetid for årgangene fra 2018 og senere, eller gjøres med en enkel modell for alder og periode.

## 6. Spørsmål

1. **Modellen:** Lagerdrevet for CL+HT+FW, med begge formuleringene som strukturusikkerhet. Er det riktig?
2. **D42 i lagerdrevet modell:** (1 − s) × utstrømmen, i stedet for balanseregelen. Er det greit?
3. **Faktorene X14–X18 og spennene.** Spesielt erstatningsgraden (0,1–0,85) og rebound (0–100 %, med «backfire» over 100 % som egen kjøring).
4. **Terskel:** −30 % ny tilførsel per innbygger i 2035?
5. **Tiltakene L6–L9:** Hvilke skal med? L9 krever at fiberlaget kjøres (ok, det gjøres allerede).

---

## 7. Hva er nytt sammenlignet med litteraturen?

### Metodisk

| Element | Finnes fra før | Vårt bidrag |
|---|---|---|
| Lagerdrevet (tjenestedrevet) dynamisk MFA | Etablert for bygg, kjøretøy og metaller (Müller 2006; Pauliuk & Müller 2014). Verktøy med «nature/nurture»-levetider (Krych & Pettersen 2025, oppvaskmaskiner). | **For tekstiler har vi ikke funnet noen lagerdrevet MFA** (søket er ikke systematisk). EU-modellene er tilførselsdrevne (Napolano m.fl. 2025, Kawecki m.fl. 2021). Vermeyen m.fl. (2025) foreslår eksplisitt en lager- og flytmodell for garderober. Nytt bruksområde, ikke ny metode. |
| Erstatningsgrad og rebound | LCA av ombruk (Farrant m.fl. 2010 og senere). Økonomiske rebound-modeller (Yerushalmi & Saha 2025). Agentbaserte modeller. «Circular economy rebound» (Zink & Geyer 2017, JIE) | Erstatning og rebound som **flyter i en nasjonal MFA**, med effekt på lager og avfall over tid. Lite brukt i MFA, så det er et reelt, men moderat bidrag. |
| Tiltak under dyp usikkerhet (EMA) i MFA | Weijenberg m.fl. (2026, PET-flasker) | Første anvendelse på tekstiler vi kjenner til, med tiltakseffekter som usikre faktorer (som Weijenberg etterlyser) og **forsinkelse gjennom lageret**, som PET-modellen ikke har. |
| **To formuleringer av etterspørselen som strukturusikkerhet** | Strukturusikkerhet drøftes i MFA, men vi har ikke funnet studier som kjører tilførselsdrevet og lagerdrevet modell side om side for tiltak | **Mest originalt metodisk:** Viser hvilke konklusjoner som skyldes modellvalget. Eksempel: Holdbarhet ser ineffektivt ut i tilførselsdrevet modell, men effektivt i lagerdrevet. |
| Statistikk som fasit i historikken, lagermodell som diagnose, kalibrering av lagerdrevet fremtid mot både statistikk og lagermodell | Restledd (Millward-Hopkins 2023, ett år), lagermodeller (EU, Kina) | Koblingen fra en 37-årig avstemming til en lagerdrevet fremtid er så vidt vi vet ny. Den gjør også at usikkerheten om lagernivået (som vi ikke kan fastslå) føres inn i fremtiden som en eksplisitt faktor (X14). |

### Perspektiv

* **Fra sirkularitetsgrad til absolutt tilførsel.** Kritikken av sirkularitetsmål er velkjent i industriell økologi (Zink & Geyer 2017, Haas m.fl. 2015, Hot or Cool 2022). Det nye er ikke perspektivet, men at vi **tallfester konflikten for et nasjonalt tekstilsystem**: Tiltak som løfter innsamling og ombruk (L1, L2) kan nå sine sirkularitetsmål uten å redusere ny tilførsel, mens holdbarhet og suffisiens (L3, L5, L8) kan gjøre det motsatte.
* **Kobling til konferansetemaet:** Endelige ressurser, suffisiens og Brundtland (rettferdig fordeling av forbruk, eksporten av brukt til lavinntektsland, fortrengt nytt i utlandet) passer «A Shared Space for Humans and Nature» bedre enn innsamlingsgrader.
* **Politisk:** Produsentansvaret i EU måles på innsamling og behandling, ikke på tilførsel. En analyse som viser at målene i produsentansvaret kan nås uten at tilførselen går ned, er relevant for revisjonen av målene (WFD 2025/1892 legger opp til at Kommisjonen vurderer mål).

### Begrensninger for nyhetsverdien

* **Søket er ikke systematisk.** En lagerdrevet tekstilmodell kan finnes, for eksempel i systemdynamikk eller i avhandlinger. Det bør sjekkes i Scopus før påstanden brukes.
* **Resultatene vil i stor grad bestemmes av antakelser** (d, r, X18). Bidraget er å vise hvilke av dem som avgjør utfallet (sårbarhet), ikke å si hva effekten er.
* **Bare masse.** Uten miljøindikatorer kan vi ikke si om tilførselen som fortrenges, er bomull eller polyester. Fiberlaget gjør det mulig å koble på livsløpsfaktorer senere.

### Vurdering

Bidraget er **moderat til godt nytt** som en samlet ramme:
* en avstemming over 37 år
* en lagerdrevet fremtid kalibrert mot den
* tiltak under dyp usikkerhet med erstatning og rebound
* to formuleringer av etterspørselen som strukturusikkerhet

Ingen enkeltdel er en ny metode. Det sterkeste nye er sammenligningen av de to formuleringene og tallfestingen av konflikten mellom sirkularitetsmål og absolutt tilførsel. Begge passer godt for ISIE under Material and Resource Systems eller Cross-Cutting Methods.

## Kilder (søk 2026-11-05)

* Vermeyen m.fl. (2025), Behind Closed Doors: Examining the Stock of Clothing in Individuals' Wardrobes, J. Circular Economy. https://circulareconomyjournal.org/wp-content/uploads/2025/02/Vermeyen_et_al_Behind-Closed-Doors-Examining-the-Stock-of-Clothing-in-Individuals-Wardrobes.pdf
* Krych & Pettersen (2025), The «nature» and «nurture» of product lifetimes in dynamic stock modeling, J. Ind. Ecol. https://link.springer.com/article/10.1111/jiec.13586
* Napolano m.fl. (2025), Dynamic probabilistic MFA of textile in the EU, RCR. https://www.sciencedirect.com/science/article/pii/S0921344924004816
* Farrant, Olsen & Wangel (2010), Environmental benefits from reusing clothes, Int. J. LCA (sitert via sekundærkilder, ikke lest). https://www.researchgate.net/publication/226848184_Environmental_benefits_from_reusing_clothes
* LCA av sirkulære forretningsmodeller for klær (2025), Int. J. LCA: erstatningsgrad 10–60 % fra spørreundersøkelser. https://link.springer.com/article/10.1007/s11367-025-02468-1
* Erstatningsgrader i Malawi, Mozambique og Angola. https://www.researchgate.net/publication/333901508_Replacement_rates_for_second-hand_clothing_and_household_textiles_-_A_survey_study_from_Malawi_Mozambique_and_Angola
* Bruktkjøp og nye kjøp, positiv korrelasjon (2025). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12504660/
* Yerushalmi & Saha (2025), Quantifying the rebound effect of the textiles and clothing sector, Bus. Strat. Env. https://www.open-access.bcu.ac.uk/16601/1/20250729_ACCEPTED_Yerushalmi_Saha_-_2025_BSE_Circular_Economy_Rebound_Effect_in_Clothing.pdf
* Agentbasert modell av ombruk og rebound i tekstiler. https://link.springer.com/chapter/10.1007/978-3-032-31712-4_49
* Hot or Cool Institute (2022), Unfit, Unfair, Unfashionable. https://hotorcool.org/unfit-unfair-unfashionable
* Zink, T. & Geyer, R. (2017), Circular Economy Rebound, J. Ind. Ecol. 21(3) (ikke hentet i dette søket).

## 8. Implementering og resultater (2026-11-05)

### Hva som er gjort
* `DEMAND_MODES = ('supply', 'stock')` i `calculations/future.py`. Den tilførselsdrevne formuleringen er uendret (referansebanen er lik trinn 1).
* Under den lagerdrevne formuleringen (`stock_driven_purchases`) regnes kjøpene av CL+HT+FW+YA år for år. Ønsket lager er lagermodellens lager i 2025 per innbygger × befolkning × X15 × (L5, L8). Overlevelsen kommer fra `cohorts.survival` med X4b, L3 × X18 og L7. Bruktkjøp × X16 trekkes fra, og X17 legger til rebound sammenlignet med samme scenario uten tiltak. Bruktkjøpene inngår i lagermodellen. Kjøp og bruktsalg løses iterativt (toleranse 10⁻⁶ kt).
* **Kalibrering:** Lagermodellens lager krympet litt i 2025, så det ønskede lageret ville gitt et hopp i kjøpene i 2026 (92 mot 89 kt). En faktor per produkt (ca. 0,96) gjør at kjøpene i 2026 er lik 2025-nivået per innbygger. Faktoren er den samme med og uten tiltak, fordi ingen tiltak virker i 2026.
* **X14 (ønsket lager i 2025)** følger av X4 og er ikke en egen faktor. Det må være lik lagermodellens lager i 2025, ellers hopper kjøpene i 2026. X4 gir ca. 100–175 kg per innbygger.
* **D42** er (1 − s) × utstrømmen under den lagerdrevne formuleringen.
* **Hvordan tiltakene virker i de to formuleringene:**
  * L5 og L8 senker kjøpene med tilførselsdrevet etterspørsel og det ønskede lageret med lagerdrevet.
  * L3 og L7 endrer levetiden i begge formuleringene. Bare med lagerdrevet etterspørsel påvirker det kjøpene.
  * L6 ganger bruktmarkedet i Norge (X13) med 1,5–3.
  * L9 påvirker bare jomfruelig fiber.
* **X2 (forbrukstrenden) brukes ikke for CORE med lagerdrevet etterspørsel.** X15 er det tilsvarende.
* `future_policies.py` kjører 1 001 scenarier × 11 alternativer × 2 formuleringer over 8 prosesser (ca. 6 min, uten fiberlaget). Jomfruelig fiber regnes fra tekstilandelen per produkt i 2025. Råtabellen har bare nøkkelårene 2030, 2035, 2040 og 2050.
* Trinn 2 er kjørt på nytt med X15–X18 i utvalget. Det endrer alle trekkene, men ikke bildet (417 av 1 000 scenarier med lagervekst under X5).

### Resultater (1 000 scenarier)

**Endring i ny tilførsel per innbygger sammenlignet med L0 i samme scenario og samme formulering (median, 2035):**

| | L1 | L2 | L3 | L5 | L6 | L7 | L8 | L9 | Alle |
|---|---|---|---|---|---|---|---|---|---|
| Tilførselsdrevet | 0 % | 0 % | 0 % | −20 % | 0 % | 0 % | −6 % | 0 % | −26 % |
| Lagerdrevet | −0,3 % | −0,7 % | **−4 %** (−10 til −1) | −14 % | 0 % | **−7 %** (−14 til −1) | −4 % | 0 % | −32 % (**−47 til −5**) |

Jomfruelig fiber: L9 −15 %, alle tiltakene −38 % (tilførselsdrevet) og −43 % (lagerdrevet) i 2035.

**Andel scenarier som når målet (−30 % per innbygger i 2035 sammenlignet med 2025):**

| | L0 | L5 | L8 | L9 | Alle |
|---|---|---|---|---|---|
| Ny tilførsel, tilførselsdrevet | 0 % | 32 % | 3 % | 0 % | 49 % |
| Ny tilførsel, lagerdrevet | 0 % | 1 % | 0 % | 0 % | 44 % |
| Jomfruelig fiber, tilførselsdrevet | 0 % | 32 % | 6 % | 22 % | 82 % |
| Jomfruelig fiber, lagerdrevet | 0 % | 1 % | 0 % | 2 % | 75 % |

Hovedpunkter:
1. **Tiltakene for sirkularitet senker ikke ny tilførsel.** Produsentansvaret (L1) løfter innsamlingsgraden over 50 % i ca. 88 % av scenariene. Sortering i Norge (L2) fjerner den usorterte eksporten i alle scenarier. Ombruk (L6) øker bruktsalget. Effekten på ny tilførsel er under 1 %, også når bruktkjøp erstatter nytt. Bruktsalget i Norge (2–6 kt) er lite sammenlignet med kjøpene (ca. 90 kt). **Sirkularitetsmålene kan altså nås uten at målet i sirkulærøkonomien nås.**
2. **Holdbarhet (L3) og reparasjon (L7) virker bare i den lagerdrevne formuleringen,** og moderat: ca. −4 og −7 % i 2035 og −6 og −9 % i 2050. Holdbarhetskravet gjelder bare klær fra 2029, og bare en del av den tekniske levetiden brukes (X18). **Formuleringen av etterspørselen avgjør om dette er et tiltak eller ikke.** Når tilførselen er gitt, ser holdbarhet virkningsløs ut. Når kjøpene følger behovet, virker det, men forsinket.
3. **Avgift og suffisiens (L5, L8) virker i begge formuleringene**, men mindre i den lagerdrevne, der rebound tar igjen noe (−14 mot −20 %).
4. **Bare kombinasjonen kan nå −30 %**, i ca. halvparten av scenariene. Med lagerdrevet etterspørsel er **rebound den viktigste faktoren** (ρ = −0,69), foran trenden i ønsket lager (−0,39) og effekten av avgiften (+0,21). Spennet er −47 til −5 %. Med full rebound forsvinner nesten hele effekten.
5. **Uten tiltak avhenger utgangspunktet av formuleringen.** I den lagerdrevne gir kortere levetid for nye årganger (X4b, ultrarask mote) flere kjøp (16,7 mot 15,0 kg per innbygger i 2035). Uten tiltak er ny tilførsel i den lagerdrevne formuleringen styrt av trenden i ønsket lager (ρ = −0,86) og av X4b (+0,38).
6. **Krav til resirkulert innhold (L9)** senker jomfruelig fiber med ca. 15 %, men ikke ny tilførsel.

### Forbehold
* Erstatningsgrad, rebound og X18 er antakelser med vide spenn. Bidraget er å vise hvilke av dem som avgjør utfallet, ikke å anslå selve effekten.
* L7 når bare nye årganger fra 2027. Reparasjon av plagg som allerede er i bruk, er ikke med, så effekten er undervurdert.
* Institusjonene og varene utenom CORE er fortsatt tilførselsdrevne. Eksport, usolgte varer og norsk produksjon skaleres med husholdningsmarkedet (en tilnærming).
* Det er bare masse. Klima kan kobles på etterpå (vurdert i [eget notat](2026-11-05_LCA_kobling_vurdering.md)).

### Reparasjon som periodeeffekt (endret samme dag)
* L7 gjaldt først bare nye årganger fra 2027. Nå senker reparasjonen risikoen for å kassere i en gitt alder for **alle plagg i bruk**, også de som er kjøpt tidligere. Effekten fases inn i 2027–2032. Overlevelsen bygges opp år for år i `cohorts.survival(period_factor=...)`. Med faktor 1 er den lik Weibull-modellen (test, avvik 10⁻¹⁵).
* **Effekt på ny tilførsel med lagerdrevet etterspørsel:** −7 % i 2030, **−10 % i 2035 (−17 til −2)** og −9 % i 2050, mot −7 % i 2035 tidligere. Med tilførselsdrevet etterspørsel er det fortsatt ingen effekt på kjøpene. Registrerte kasseringer går ned med ca. 10 % i 2030 og 7 % i 2035.
* Alle tiltakene samlet gir −35 % (−50 til −5) i 2035 med lagerdrevet etterspørsel og −26 % med tilførselsdrevet. Målet om −30 % per innbygger nås i ca. 50 % av scenariene i begge formuleringene.

### Kjent svakhet: overgangen i 2028–2030 med lagerdrevet etterspørsel
Når L5 og L8 senker det ønskede lageret med 10–30 % over 2028–2030, slutter husholdningene nesten å kjøpe til lageret har krympet. Ny tilførsel faller med −35 % i 2030 (L5) og −46 % for alle tiltakene, med 5-persentil −83 %. Det henger sammen fysisk, men er urealistisk som atferd. Effekten i 2035 og 2050 påvirkes lite. **Forslag:** La reduksjonen i ønsket lager fases inn over 2027–2035 med lagerdrevet etterspørsel, slik at garderoben krymper gjennom naturlig avgang.

### Med funksjonskategorier (D43, samme dag)
Holdbarhet og reparasjon er beregnet på nytt med konkurrerende tekniske og opplevde levetider per kategori, der andelen kassert på grunn av slitasje er bundet til Mepex. Effekten på ny tilførsel med lagerdrevet etterspørsel er nå −2 % (L3) og −2,4 % (L7) i 2035, mot −4 og −10 % uten kategorier. Alle tiltakene gir −28 %. Se [notatet om kategoriene](2026-11-05_funksjonskategorier_forslag.md), avsnitt 8.
