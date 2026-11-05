# Kan vi koble livsløpsdata (LCA) på strømmene? Gir det mening innenfor usikkerheten?

*Notat 2026-11-05. Vurdering før trinn 4. Nettsøk, ikke systematisk. Faktorene er størrelsesordener og må hentes fra primærkilder (PEFCR Apparel & Footwear, EF 3.1-datasett, JRC, EEA) før de brukes.*

## Kort svar

**Ja for klima, med forbehold. Nei, eller bare illustrativt, for vann, arealbruk, biologisk mangfold og toksisitet.**

* **Absolutte tall** for klima blir usikre med en faktor 2–3. Det er likevel nyttig som størrelsesorden og kan kontrolleres mot EEA.
* **Forskjeller mellom tiltak** blir robuste, fordi de i hovedsak bestemmes av endringen i ny tilførsel. Den samme faktoren for produksjon gjelder alle tiltakene i et scenario, så usikkerheten i faktoren skalerer forskjellene, men snur dem ikke.
* **Risikoen for «hva som helst»** ligger i tre ting: valg av godskriving (for ombruk, gjenvinning og energi fra forbrenning), påvirkningskategorier med svake data, og opprinnelsen til fiberen. Den kan begrenses med et stramt oppsett (se under).

## 1. Hvordan påvirkningen fordeler seg

Klimafotavtrykket for tekstiler kan skrives omtrent slik:

> påvirkning ≈ Σ ny tilførsel × faktor for produksjon + Σ forbrenning × faktor for avfall − godskriving (ombruk, gjenvinning, energi)

| Ledd | Størrelse (Norge, CL+HT+FW, 2025) | Faktor | Usikkerhet i faktoren |
|---|---|---|---|
| **Produksjon av nye varer** | ca. 88 kt nye varer | 14–78 kg CO₂e/kg plagg i studier, typisk 15–35. EEA gir ca. 18 kg/kg (270 kg CO₂e per person for ca. 15 kg tekstiler) | **Faktor 2–5.** Styres av strømmiks i farging og etterbehandling, garnfinhet og systemgrense |
| **Forbrenning av syntetisk fiber** | ca. 100 kt forbrent × ca. 45 % syntetisk | ca. 2,3 kg fossil CO₂/kg polyester (karboninnhold 62,5 % × 44/12) | **Lav.** Det er kjemi. Bomull og ull gir biogent CO₂ |
| **Godskriving for energi fra forbrenning** | Fjernvarme i Norge | Avhenger av hva varmen erstatter (strøm, bio, annen avfallsforbrenning) | **Svært høy, og et metodevalg** |
| **Godskriving for ombruk** | Ombruk × erstatningsgrad × faktor for produksjon | Samme som produksjon × d (0,1–0,85) | **Styres av d**, som allerede er en usikker faktor |
| **Godskriving for gjenvinning** | Under 1 kt i dag | Spart jomfruelig fiber minus gjenvinningsprosessen | Fiberleddet er bare ca. 10–30 % av fotavtrykket for et plagg, så gevinsten per kg er liten |

**Grovt for Norge:**
* Produksjonen gir 88 kt × 15–35 kg/kg ≈ 1,3–3,1 Mt CO₂e, eller ca. 230–550 kg per innbygger. EEA gir 270 kg for EU.
* Fossil CO₂ fra forbrenning av syntetisk fiber er ca. 0,1 Mt, altså ca. 3–8 % av produksjonen.

**Konsekvens:** Produksjonen av nye varer dominerer klimaregnskapet med en faktor 10–20. Klima blir derfor i stor grad ny tilførsel ganget med en faktor. Det er et argument for trinn 4, ikke mot det: Det viser at ny tilførsel er det riktige målet, og at innsamling og sortering har liten klimaeffekt med mindre de fortrenger ny produksjon.

## 2. Hvor LCA kan endre konklusjoner (og hvor ikke)

| Tiltak | Endres rangeringen av at vi tar med klima? | Hvorfor |
|---|---|---|
| L1 produsentansvar, L2 sortering i Norge, L4 destruksjonsforbud | **Nei.** Effekten er liten | Endrer mest hvor avfallet behandles. L2 flytter forbrenning av rester til Norge, men leddet er lite og ville skjedd i utlandet uansett. Globalt er det nøytralt |
| L3 holdbarhet, L5 avgift, L7 reparasjon, L8 deling (lagerdrevet modell) | **Nei, men størrelsen får mening** | Klimaeffekten er omtrent proporsjonal med endringen i ny tilførsel |
| L6 ombruk | **Ja, delvis** | Effekten avhenger helt av erstatningsgraden d. LCA gjør tydelig at ombruk uten erstatning ikke gir noe |
| L9 resirkulert innhold | **Ja, men lite** | Gevinsten gjelder bare fiberleddet |
| X12 fiberblandingen (mer syntetisk) | **Ja, for avfallet og for kategorier utenom klima** | Mer syntetisk gir mer fossil CO₂ ved forbrenning, men mindre vann og areal i produksjonen. Her er det reelle avveininger |

## 3. Kategorier utenom klima: høy risiko for «hva som helst»

* **Vann og arealbruk:** Bomull dominerer. Resultatet avhenger av hvor bomullen er dyrket (vanning, vannmangel), og det vet vi ikke. Handelsstatistikken viser hvor plagget er laget, ikke hvor fiberen kommer fra. Spennet kan bli en størrelsesorden.
* **Biologisk mangfold:** Faktorene for arealbruk finnes i EF 3.1, men er usikre og avhenger av hvor fiberen kommer fra. Det er fristende fordi konferansetemaet handler om natur, men resultatene blir lett vilkårlige.
* **Toksisitet og kjemikalier:** Faktorene er usikre med flere størrelsesordener. Data om kjemikalier mangler for de fleste fiberkjeder.
* **Mikroplast:** Fiberlaget gir utslipp (D37), men det finnes ingen etablerte faktorer for påvirkning. Det kan rapporteres som masse, ikke som påvirkning.

## 4. Anbefalt oppsett (om vi gjør det)

1. **Bare klima (GWP100), i tillegg til masse og jomfruelig fiber.** Eventuelt vann og areal for bomull som illustrasjon, merket slik.
2. **Faktorer per fibergruppe** (SYN, CO, WO, CV, OTH) **og trinn** (fiber, garn og stoff, farging og etterbehandling, konfeksjon) fra én konsistent kilde, PEFCR A&F eller EF 3.1. Fiberlaget gir allerede massen per fibergruppe.
3. **Faktorene som usikre faktorer i scenariene**, med flate spenn (for eksempel × 0,5–2 rundt den sentrale verdien). **Samme trekk for alle tiltakene i et scenario.** Da faller usikkerheten i faktoren bort i forskjellene, og det kan vises.
4. **Godskriving rapporteres for seg og ikke nettet.** Det gjelder ombruk (× d), gjenvinning og energi fra forbrenning. Hovedtallet er «produksjon av ny tilførsel + fossil CO₂ fra forbrenning i Norge».
5. **Kontroll:** Fotavtrykket per innbygger skal være av samme størrelse som EEAs 270 kg CO₂e per person (EU, 2020).
6. **Formidling:** Absolutte tall som spenn. Hovedbudskapet er forskjellene mellom tiltakene og andelen av fotavtrykket som skyldes produksjon av nye varer.

## 5. Vurdering

* **Det gir mening for klima.** Konklusjonene om tiltak blir robuste, fordi produksjonen dominerer og faktoren er felles for alle tiltakene. Usikkerheten i faktoren gjør de absolutte tallene usikre, men ikke rangeringen.
* **Det gir lite ny informasjon om rangeringen.** Klima følger i stor grad ny tilførsel. Merverdien er størrelsesordenen og koblingen til konferansetemaet. Den viktigste innsikten er at innsamling og sortering betyr lite for klima når de ikke fortrenger ny produksjon.
* **Det kan gi «hva som helst»** hvis godskriving nettes inn i hovedtallet, eller hvis vann, areal, biologisk mangfold og toksisitet tolkes kvantitativt uten kunnskap om hvor fiberen kommer fra. Det bør unngås.
* **Arbeid:** ca. en halv økt etter trinn 4. Det trengs en tabell med faktorer (med kilde) og en funksjon som regner klima per scenario og tiltak fra fiberlaget.

## Kilder (søk 2026-11-05)

* EEA, What are the environmental impacts of textiles? (FAQ): 2020 ca. 270 kg CO₂e, 391 kg råvarer, 400 m² areal og 9 m³ vann per person. Ca. 15 kg tekstiler per person (6,0 kg klær, 6,1 kg hjemmetekstiler, 2,7 kg sko). https://www.eea.europa.eu/en/about/contact-us/faqs/what-are-the-environmental-impacts-of-textiles
* EEA (2022), Textiles and the environment: the role of design in Europe's circular economy. https://www.eea.europa.eu/publications/textiles-and-the-environment-the
* Sammenlignende LCA av T-skjorter (viskose, lyocell, bomull, polyester), Sustainability 2026: bomull 14,1 kg CO₂e/kg, polyester 19,6–78,3 kg CO₂e/kg i andre studier. https://www.mdpi.com/2071-1050/18/8/4070
* LCA av blandingsstoff av polyester og ull, Energies 2024: farging og etterbehandling ca. 20–24 kg CO₂e/kg produkt. https://www.mdpi.com/1996-1073/17/2/312
