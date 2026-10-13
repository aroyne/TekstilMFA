# Gjennomgang av DI.RT (engros og butikk)

*2026-10-13. Tredje subpool i gjennomgangen flyt for flyt. Beslutningen står som D27 i [SYSTEMDEFINISJON](../docs/SYSTEMDEFINISJON.md).*

## Flytene

| Flyt | Status før | Beslutning |
|---|---|---|
| Import av ferdigvarer (RW → DI.RT) | 08801, implementert | Uendret. Små varelinjer under 1 000 kr (SSB 99.60.1000, ca. 7 kt klær i 2024) holdes utenfor (D14). |
| Eksport av ferdigvarer (DI.RT → RW) | 08801, implementert | Uendret. Gjeneksport kan ikke skilles fra norsk produksjon (D6). |
| Salg til institusjoner og bedrifter (DI.RT → US.IC) | 12 % (8–15 %), dansk fordeling via Watson 2020 og Rubach 2023 | Uendret. Ingen norsk statistikk funnet. Offentlige innkjøp (DFØ/Doffin) og vaskeribransjen gir ikke masse. |
| Salg til husholdninger (DI.RT → US.HH) | Balanse | Usolgte varer trekkes nå fra. |
| **Usolgte varer gitt til innsamlere (DI.RT → CO.CO)** | planlagt | **Implementert.** 0,6 kt i 2018 og 0,2 kt i 2022 per kt klesimport, så flyten følger klesimporten. Trekkes fra innsamlingen fra husholdningene. |
| **Usolgte varer kastet (DI.RT → WM.RS)** | planlagt | **Implementert.** Minimumstall fra undersøkelsene: 95 t i 2018 og 221 t i 2022, per kt klesimport. |

## Kildene for usolgte varer

- **Watson m.fl. (2020), kapittel 3.1.8:** 44 produsenter og forhandlere svarte, og 16 oppga mengder (116 t). 82 % av dette gikk til forbrenning (95 t) og 11 % til innsamlere. Én innsamler oppga at den mottok omtrent 600 t fra forhandlere i 2018, blant annet fra noen av de største kjedene. Watson konkluderer med at volumet er minst 714 t, men sannsynligvis høyere, og at donasjonene neppe er mye høyere enn 600 t.
- **Rubach m.fl. (2023), kapittel 3.3.4:** 56 svarte fullstendig. De rapporterte 337 t, hvorav 116 t donert, 93 t til materialgjenvinning og 110 t annet. Innsamlerne oppga omtrent 200 t mottatt.
- **de Sadeleer & Rubach (2026):** ingen tall for usolgte varer.
- **EEA (2024) / ETC CE Report 2024/4:** 4–9 % av tekstilene som settes på markedet i Europa, destrueres uten å ha vært brukt (264–594 kt per år i EU). For Norge ville det tilsvare 4–10 kt per år. Det er en europeisk modellberegning og brukes bare i følsomhetsanalysen.

## Resultater (median, N = 1000)

| | 1988 | 2000 | 2008 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Usolgt gitt til innsamlere | 0,32 | 0,53 | 0,72 | 0,62 | 0,22 | 0,19 |
| Usolgt kastet | 0,06 | 0,10 | 0,13 | 0,12 | 0,27 | 0,23 |
| Innsamlet fra husholdninger | 0,3 | 8,2 | 16,3 | 36,9 | 32,3 | 36,1 |

Innsamlingen fra husholdningene ligger fortsatt over kartleggingene (31,7 kt i 2018, 29,6 kt i 2022, 33,7 kt i 2025). Donasjonene forklarer bare en liten del av forskjellen.

## I fiberlaget

Det som går gjennom CO (eksport av brukte tekstiler, sortering i Norge, bruktbutikk), har nå blandingen av det som samles inn fra husholdningene (utstrømmen av årgangsmodellen) og donerte usolgte klær (tilførselssammensetningen). Da balanserer CO.CO per materiale.
