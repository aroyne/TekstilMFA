# Hva er nytt sammenlignet med NORSUS? En kritisk vurdering

*Notat 2026-11-02. Sammenligner TekstilMFA med de Sadeleer & Rubach (2026), OR.18.26, og forgjengerne Rubach m.fl. (2023) og Watson m.fl. (2020). Tallene er fra `output_files/MC_summary.csv` (N = 1000), slik modellen står etter D36.*

## Utgangspunkt: hva NORSUS 2026 er

* Et øyeblikksbilde for 2025, med importtall for 2022–2025. Metoden er pivottabeller på tollkodenavn (SSB 08801), innsamlernes egne tall, KOSTRA, Mepex' plukkanalyser (7 + 4 analyser) og en spørreundersøkelse om bruktkjøp.
* Usikkerheten vises med trafikklys. Det finnes ingen tallfestet usikkerhet.
* Nyhetene i rapporten er VOEC-tallene fra Tolletaten (14,0 kt i 2025), NTGs gjenvinning og at bruktsalget mellom privatpersoner er anslått (439 t).
* Formålet er grunnlaget for produsentansvaret (vederlagsgrunnlag), ikke forskning.

## Det vi ikke kan påstå er nytt

1. **Bedre tall for 2018, 2022 og 2025.** Vi bruker de samme kildene: 08801, Mepex via NORSUS, innsamlernes tall, VOEC via NORSUS. Ankerpunktene for avfall *er* NORSUS-tallene. Bruttoimporten ligger ca. 2 kt fra deres, og eksporten av brukte tekstiler er identisk. For de siste årene reproduserer vi i hovedsak NORSUS.
2. **Metoden i seg selv.** Dynamisk, probabilistisk MFA med årgangsmodell er etablert (Bornhöft 2016, Kawecki 2021, Napolano 2025 for EU-tekstiler). flodym og Monte Carlo er verktøy, ikke et bidrag.
3. **Fiberlaget som hovedfunn.** Grunnlaget er det samme som NORSUS bruker: hovedfiberen i tollkodenavnet. Vi fordeler restpostene (PEFCR) og bruker årgangsmodellen, men årgangseffekten er ≤ 3 prosentpoeng, slik Napolano også fant. Valideringen (40–42 % syntetisk mot målt 38–48 %) ligger innenfor spredningen mellom målemetodene, så den bekrefter lite.
4. **Bredden alene.** Ull, håndstrikkegarn, usolgte varer, deponi før 2009 og mikrofibre er små flyter, og de fleste hviler på ett datapunkt eller en antakelse. Bredde er ikke et forskningsbidrag i seg selv.

## Det som kan være nytt, og hva som må til

### 1. Avviket mellom tilført og kassert: er det oppmagasinering? (sterkest)

NORSUS tolker gapet på 25 kt i 2025 (4,5 kg per innbygger) som oppmagasinering i hjemmene. Modellen vår viser at mye av gapet kommer av avgrensning og bokføring:

| Bidrag til gapet i 2025 (CL+HT+FW) | kt | Hvorfor NORSUS ikke fanger det |
|---|---|---|
| Gjeneksport av nye varer | ca. 9,6 | NORSUS trekker bare fra eksport av norskproduserte varer (7 t) |
| Forbruk i institusjoner og bedrifter (12 %) | ca. 9,8 | NORSUS regner det med i tilført, men har ikke kasseringer fra sektoren |
| Lagerendring i husholdningene (restledd) | 10 (−1 til 22) | – |

Dette er et konkret og etterprøvbart bidrag med betydning for politikken: vederlagsgrunnlaget og «avhendingsgraden» i produsentansvaret bygger på samme regnestykke.

**Det kritiske problemet:** Over tid hoper restleddet seg opp til ca. 275 kg per innbygger i 2025 (1 551 kt, 95 %-intervall 404–2 006). Lagermodellen gir ca. 97 kg (545 kt), og SIFOs garderobestudier ca. 110–140 kg klær. Enten er tilførselen for høy, eller kasseringene er for lave før 2018. Mistenkte bidrag er balansen i MA.TX (8–18 kt per år, kanskje 300+ kt akkumulert), restavfallet før 2009 og møbelputer i HT. *Oppdatert senere samme dag: Næringstallene fra SSB gir ikke grunnlag for å si at MA.TX er for høy ([notat](2026-11-02_naeringstall_mot_modellen.md)). Destruksjon og returer (D38) er en ny kandidat.* **Før dette er løst eller brutt ned, svekker det funnet om «ikke oppmagasinering»:** en anmelder vil si at den samme modellen har et lager som ikke henger sammen. Avviket kan også bli selve funnet («statistikken lukker ikke over tid, og her er hvor feilen må ligge»), men da må den nedbrytningen gjøres eksplisitt.

### 2. Tidsserien 1988–2025

Ingen norsk tekstil-MFA har tidsserier, og internasjonalt finnes det få nasjonale tekstil-MFA-er med 30+ år. **Men:** Bare handelssiden er årlige data. Avfallssiden har ankerpunkter i 1991, 1998, 2009, 2018, 2022 og 2025. 1998-tallet kan være modellberegnet av SSB, og 2009 bygger på Oslo-analyser. Trender i kasseringer før 2018 vil derfor i stor grad være interpolasjon og D30-usikkerhet. Det må sies tydelig, og det er tilførselssiden (VOEC-bruddet, klesimport per innbygger, kg per plagg) som tåler å stå som trendfunn.

### 3. Metodevalg som korrigerer NORSUS

Hvert av disse er små, men samlet utgjør de et poeng om datakvalitet:
* **Innsamling fra eksporten (D31):** NORSUS finner selv at SSBs eksport er 5,6 kt større enn det innsamlerne rapporterer, men bruker innsamlernes tall.
* **Institusjonsandelen:** NORSUS bruker fortsatt den danske 12 % (siden 2019). Eurostat TEC gir en nedre grense på 3–4 % for import direkte til næringslivet (D36).
* **Gjeneksport** (se over).
* **VOEC som brudd i serien:** økningen fra 2024 til 2025 kan komme av registreringen like mye som av forbruket.

### 4. Tallfestet usikkerhet

Dette er nytt for Norge og kan bli nyttig: hvilke parametre styrer usikkerheten i lageret, i innsamlingsgraden og i vederlagsgrunnlaget? **Men:** Grensene er i dag stort sett ekspertanslag. Pedigree-matrisen (Laner 2016) og følsomhetsanalysen (Spearman) er planlagt, men ikke gjort. Uten dem er MC-intervallene lette å avfeie som vilkårlige.

### 5. Åpen og oppdaterbar modell

Kode, register og dokumentasjon per flyt er åpne, mens NORSUS bruker Excel-pivot og ikke publiserer regnearkene. Produsentansvaret starter i 2027 og gir nye rapporteringsdata. En modell som kan oppdateres årlig og gi en sammenlignbar referanse bakover i tid, er en reell styrke for en dataartikkel (J. Ind. Ecol. data/software, Scientific Data), men neppe nok for en vanlig forskningsartikkel.

## Mulige artikler, rangert

1. **«Placed on market minus discarded is not hoarding»**: dekomponering av gapet og 37 års avstemming mellom restledd, lagermodell og garderobestudier. Krever at det høye lageret brytes ned. Lengst kommet: å estimere levetider og dvalelager fra data (Krych & Pettersen 2025) i stedet for å anta dem.
2. **Hva offisiell statistikk kan bære for overvåking av produsentansvaret**: datakvalitet og følsomhet (6309-klassifisering, VOEC, KOSTRA mot Mepex, institusjonsandel, gjeneksport), tallfestet med MC og Spearman. Krever fase 4.
3. **Data- og programvareartikkel**: åpen nasjonal tekstil-MFA 1988–2025. Lavest terskel og minst nytt.

Svake vinkler: fiberlaget alene, mikrofibre (skalert fra Mepex 2014) og ull og håndstrikk (nisje, få data).

## Før noe sendes inn

* Løs eller dekomponer lageret på 275 kg per innbygger (MA.TX-balansen først).
* Følsomhetsanalyse og pedigree for usikkerheten.
* Sjekk litteraturen for nasjonale tekstil-MFA-er med tidsserier (NL CBS-lagre, Sverige, Finland, UK), slik at påstanden om «første» holder.
* Avklar med SSB om tekstiltallene for 1998 og 1995–2011 er modellberegnet.
