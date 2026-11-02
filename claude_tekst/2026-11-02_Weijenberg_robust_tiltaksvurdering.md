# Weijenberg m.fl. (2026): robust tiltaksvurdering i MFA, og hva vi kan bruke

*Notat 2026-11-02. Weijenberg, N., Auping, W. L., Lensen, S., Schwarz, A. & Thonemann, N. (2026). Robust policy evaluation in material flow analysis under deep uncertainty. Journal of Industrial Ecology 30(5). [doi:10.1007/s44498-026-00170-5](https://doi.org/10.1007/s44498-026-00170-5), CC BY 4.0. Kode: GitHub `nweijenb2001/emfma`. Lest fra forlagets side (de siste ca. 30 % av teksten, i hovedsak referanser og tillegg, er ikke lest). Ligger i Zotero.*

## Hva artikkelen gjør

* **Hovedpoeng:** Når data er knappe, kan vanlig probabilistisk usikkerhetsanalyse (MC med valgte fordelinger) gi inntrykk av mer kunnskap enn det finnes. Forfatterne foreslår å slutte å lete etter det mest sannsynlige utfallet av et tiltak, og i stedet finne tiltak som fungerer godt nok over hele spennet av plausible framtider (dyp usikkerhet, exploratory modeling and analysis, EMA).
* **Rammeverk i fem trinn:** problemformulering med tiltak og mål (XLRM: eksterne faktorer, tiltak, relasjoner, mål), systemdefinisjon, usikkerhet fra eksperter (laveste og høyeste troverdige verdi, med data holdt tilbake til en andre runde for å unngå forankring), robusthet og sårbarhet, og presentasjon.
* **Overføringskoeffisienter med sum lik 1:** Spennene hentes inn med et regneark som håndhever summen. Trekkene gjøres fra en avkuttet, flat Dirichlet-fordeling med blokkvis Gibbs-sampling (Park & Lee 2022). Det bevarer summen uten normalisering, som forfatterne viser at forskyver fordelingene.
* **Robusthetsmål (Kwakkel m.fl. 2016):** tilfredsstillelse (andel scenarier der et mål nås, for eksempel at sekundærmateriale er over 30 % av forbruket), anger (avstand til beste tiltak i samme scenario) og statistiske mål som feilrate og verste utfall.
* **Sårbarhet:** Spearman-korrelasjon mellom hver usikker faktor og hvert mål, med signifikanstest. Ingen PRIM eller scenario discovery.
* **Eksempel:** PET-flasker i Nederland 2025–2030, 43 prosesser, 136 usikre faktorer og én ekspert. Åtte tiltak er modellert som ±10 % på berørte koeffisienter, som er en antakelse. Med 500 scenarier × 9 alternativer er absolutte robusthetstall ustabile mellom kjøringer, men rangeringen av tiltakene er stabil.
* **Begrensninger de selv peker på:** Det er tungt å hente inn ekspertvurderinger (117 spørsmål var nær grensen), Spearman fanger ikke samspill, og usikkerheten i selve tiltakseffekten er ikke med. Studien er ment som demonstrasjon.

## Relevans for TekstilMFA

### 1. Den viktigste lærdommen: to typer usikkerhet, to metoder

Artikkelen gir et godt grunnlag for et skille som passer prinsippet vårt om at data er fasiten:

| | Historikken 1988–2025 (fase A–C) | Framtid og tiltak (fase D–E) |
|---|---|---|
| Hva er usikkert | Feil i data og parametre som det finnes empiri for | Forbruk, levetider, eksportmarkeder, tiltakseffekter: ingen data |
| Metode | MC med fordelinger fra kildetype og kalibreringspunkter (fase A) | EMA: flate, vide plausible spenn, mange scenarier, robusthetsmål |
| Hva rapporteres | Median og 95 %-intervall per flyt | Hvilke tiltak som holder i flest framtider, og hvilke faktorer de er sårbare for |

For historikken er MC fortsatt riktig, fordi usikkerheten der kan begrunnes med data. Kritikken treffer likevel våre parametre av type 4 (ekspertanslag uten data), for eksempel institusjonsandelen, gjenbruksandelen av det som holdes tilbake, `ntg_fibre_domestic_share` og levetidene. For dem gir PERT med en modus et inntrykk av kunnskap vi ikke har. Forslag til fase A: parametre av type 4 får flat (uniform) fordeling innenfor spennet, og ikke PERT eller triangulær. Det er et lite, forsvarlig avvik fra fordelingsregelen i NitrogenBudsjett.

### 2. Fase E (tiltak): rammeverket passer

* **XLRM** er en god mal for tiltaksnotatet: tiltakene (L) fra listen A1–D, målene (M) som innsamlingsgrad, andel gjenbruk i Norge, eksport av usortert, restavfall per innbygger og grunnlaget for produsentansvaret, og de eksterne faktorene (X) fra fase D.
* **Robusthetsmål:** Tilfredsstillelse passer til krav med terskler (for eksempel innsamlingsmål i produsentansvaret). Anger passer til å sammenligne tiltak.
* **Svakheten deres er vår mulighet:** Tiltakene er modellert som ±10 % uten begrunnelse. Vi bør begrunne tiltakseffekten fra kilder (for eksempel fransk produsentansvar, svenske innsamlingstall) og la den være en usikker faktor selv.
* **Vår fordel:** Lagermodellen gir forsinkelsen mellom tiltak og kasseringer, som PET-modellen (kort levetid) ikke trenger.

### 3. Sum lik 1 i vår modell

* Vi løser det i dag mest ved at én flyt er restleddet (det som ikke går andre veier), slik at summen alltid stemmer. Det gir skjeve fordelinger for restleddet, men ingen normalisering.
* **Unntak:** Produktandelene i norsk produksjon trekkes med gap-støy og normaliseres etterpå ([calculations/ma_mc.py:247](../calculations/ma_mc.py#L247)). Det er akkurat det artikkelen advarer mot. Effekten er liten (flyten er 1–5 kt), men den bør nevnes i docstringen, eller løses med Dirichlet hvis vi går gjennom flyten igjen.
* I fase D vil det komme flere fordelinger på flere veier (sortering til gjenbruk, materialgjenvinning og rester, eksportmarkeder). Der er avkuttet Dirichlet en god løsning, og koden deres kan brukes som referanse.

### 4. Bidrags- og sårbarhetsanalyse

* Spearman krever lagrede trekk. Elastisitetsmetoden fra NitrogenBudsjett (A0) gjør det ikke, og gir variansbidrag i stedet for rangkorrelasjon. For historikken holder vi oss til A0.
* For fase E trengs lagrede trekk uansett (robusthetsmålene regnes per scenario). Da er Spearman, eller bedre en variansbasert metode, billig å legge til.

### 5. Det vi ikke bør ta over

* Ekspertinnhenting med over 100 spørsmål. Vi har få eksperter og mange kilder. Spennene bør komme fra litteratur og data der det finnes, og ekspertvurdering bare for de faktorene som sårbarhetsanalysen peker ut.
* Å holde import og relasjoner faste. For tekstiler er tilførselen selve drivkraften og må variere.

## Forslag til endringer i planen

1. Fase A2: parametre av type 4 (ekspertanslag eller antakelse) får flat fordeling innenfor spennet.
2. Fase D og E: EMA med robusthetsmål (tilfredsstillelse, anger, feilrate) som metode, med XLRM som struktur for tiltaksnotatet. Avkuttet Dirichlet for koeffisienter med sum lik 1.
3. Flagg normaliseringen av produktandelene i `ma_mc.py` som kjent svakhet.
