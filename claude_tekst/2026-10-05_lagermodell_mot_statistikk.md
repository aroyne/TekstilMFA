# Lagermodellen mot statistikken (D8)

*Notat 2026-10-05. Figur: [output_files/plots/stock_model_comparison.png](../output_files/plots/stock_model_comparison.png) (`scripts/plot_stock_model.py`). Tall: `output_files/MC_summary.csv`, 1 000 iterasjoner, frø 1.*

## Hva som sammenlignes

For klær, hjemmetekstiler og sko (CL+HT+FW) i husholdningene finnes nå to uavhengige anslag:

* **Statistikk (hovedresultatet, D8):** kassert = separat innsamling (D17) + restavfall (D15, ankerpunkter 1998, 2018, 2022, 2025 med lineær interpolasjon). Lagerendringen er restleddet: tilført − kassert.
* **Lagermodell (parallell):** innstrømsdrevet årgangsmodell i flodym. Tilført er salg, privatimport og netthandel. Levetidene er Weibull med middelverdi CL 6, HT 7 og FW 4 år (forslag, `parameters/lifetimes.csv`). Innsvinging fra 1950 på 1988-nivå (D2).

## Resultater (median, kt per år)

| År | Tilført | Kassert, statistikk | Kassert, lagermodell (95 %) | ΔLager, statistikk | ΔLager, modell |
|---|---|---|---|---|---|
| 1990 | 45 | 60 | 42 (40–44) | −15 | 3 |
| 2000 | 67 | 64 | 54 (50–58) | 3 | 13 |
| 2005 | 86 | 62 | 64 (59–69) | 24 | 22 |
| 2010 | 96 | 61 | 80 (74–88) | 35 | 16 |
| 2015 | 88 | 65 | 90 (84–95) | 23 | −2 |
| 2018 | 85 | 69 | 89 (85–94) | 17 | −4 |
| 2022 | 85 | 81 | 86 (81–90) | 4 | −1 |
| 2025 | 85 | 81 | 82 (78–87) | 6 | 2 |

Lageret i lagermodellen er ca. 98 kg per innbygger i 2018 og 85 kg i 2025. Restleddet akkumulert fra 0 i 1988 gir ca. 58 kg per innbygger. Det er ikke et nivå, fordi startlageret mangler.

## Tolkning

1. **Fra 2019 er de to anslagene enige** (forskjell 1–8 kt, overlappende intervaller). Her bygger statistikken på de tre nyeste kartleggingene. Det betyr at levetidene i forslaget er forenlige med de beste dataene.
2. **1988–2000: statistikken ligger over tilførselen.** Restleddet blir negativt (−15 kt i 1990), mens lagermodellen gir 42–54 kt kassert. Usikkerheten i statistikken er stor her (ankeret fra 1998 har ±40 %), og nedre grense nesten treffer modellen. SSB-tallet for 1998 kan være beregnet ut fra tilførselen (åpent spørsmål A1, og spørsmålet til SSB i PLAN). Det kan også være at tilførselen før 2004 er undervurdert, for eksempel fordi privatimporten er holdt på 2004-nivå.
3. **2008–2017: lagermodellen ligger klart over statistikken** (80–90 mot 61–69 kt), og intervallene overlapper ikke i 2010–2016. Restleddet får derfor et stort lageroppbygg (+25–35 kt per år), som lagermodellen ikke ser. Det finnes tre mulige forklaringer, og de kan virke sammen:
   * **Restavfallet mellom 1998 og 2018 er en rett linje uten data.** 2018-ankeret (31,6 kt, Watson 2020) er lavt sammenlignet med 2022 (48,8 kt). Det bygger på få analyser, særlig for gjenvinningsstasjonene (3 analyser, 6,1 kt mot 15,2 kt i 2022). Laitala m.fl. 2012 har plukkanalyser fra 2006–2011 med **5,6 kg tekstiler per innbygger i restavfall som hentes hjemme** (2,8–9,2). Det tilsvarer ca. 27 kt bare for henteordningen rundt 2009, før gjenvinningsstasjonene. **Dette kan bli et nytt ankerpunkt** og fylle hullet.
   * **Levetidene var lengre, eller dvalelageret vokste** i perioden med høyest tilførsel. Til sammen er det «oppmagasineringen» NORSUS peker på.
   * **Innsamlingen før 2018** er beregnet fra eksport ÷ eksportandel med ankerpunkter fra 2018 (D17). Hvis en større del ble beholdt i Norge før 2018, blir innsamlingen for lav.
4. Lagermodellen er ikke en fasit: levetidene er forslag med stor usikkerhet, og formen (Weibull 2) er en antakelse. Men intervallet i 2010–2016 dekker CL-levetider fra 4 til 9 år og overlapper likevel ikke statistikken. Avviket kan altså ikke forklares med levetidsusikkerheten alene.

## Forslag til neste steg

1. **Ankerpunkt for restavfall rundt 2009** fra Laitala m.fl. 2012: 5,6 kg per innbygger (henteordning) × folketall, pluss et tillegg for gjenvinningsstasjonene (andelen fra 2018/2022/2025). Status: litteratur, bred usikkerhet.
2. **Spørre SSB** om tekstiltallene for 1995–2011 og 1998 er beregnet ut fra tilførselen (står allerede i PLAN).
3. **Startlager (D2):** Sett restleddets startlager i 1988 lik lagermodellens lager (241 kt, ca. 57 kg per innbygger), slik at lagernivåene kan sammenlignes med garderobestudier.
4. **Følsomhet:** Kjør lagermodellen med lengre levetider for CL i 2005–2015 for å se hvor mye «dvalelager» som trengs for å forklare avviket.
