# Nachtbericht 19. November 2026

Die Arbeit kompiliert ohne Fehler und ohne kaputte Verweise (179 Seiten). Nichts ist committet.

## 1. Was über Nacht gelaufen ist

| Lauf | Ergebnis | Ordner |
|---|---|---|
| Tiefe 5, finale Konfiguration, Training, Intensität 0,8/1,2, voll generativ, E3 | Aussagen unverändert (Details unten) | `simulation_e3/runs/depth5_20261118` |
| E5 mit Tiefe 5 für ±1 und any | Regel 1 gilt auch bei Tiefe 5 | `depth5_20261118/e5`, `night_20261119` |
| ProSiT nur mit der Korrektur aus 1.0.5 | Korrektur nötig, aber nicht ausreichend | `simulation_e3/runs/night_20261119` |
| Regressionstest „alle Schalter aus“ auf HM 0.7 | identisch (2 Seeds, je 600 Fälle) | `hm07orig_20261115/regression_check_hm07.json` |

**Tiefe 5 in Kürze.**
- **Besser:** Niveau (CTD 6,8 statt 8,0 im Test) und Ausfahrt (12,9 bei 12,4 beobachtet).
- **Schlechter:** Rückstaus unter starker Last. Bei 150+ LKW 68,5 statt 58 Minuten, bei Intensität 1,2 im Mittel 78 Minuten.
- **Auswahlregel:** Auf dem Training gewinnt weiter Tiefe 3 (Summe der Profilabstände 6,9 gegenüber 7,5).
- **Annahmekriterien:** dieselben zwei Schwellen verfehlt.
- **E5:** Stunden über 35 −7,0 / −8,3 / −11,9 Prozentpunkte. Besuche mit verlegter Lieferung 7,9 bis 9,8 Minuten kürzer, alle Intervalle ohne null.

**ProSiT nur mit der 1.0.5-Korrektur.**
- Der Stau an einem Block verschwindet.
- Median 24 statt 33 Minuten, keine Reaktion auf Last (Spearman −0,18).
- Mit drei LKW am Block wartet ein LKW 0 statt 16 Minuten.
- Ein Stopp dauert immer 8 Minuten.
- Bis zu 7 LKW an einem Block (mit eingespielten Ankünften bis zu 10).

## 2. Was in der Arbeit geändert wurde

- **Kapitel 2.6:**
  - Formulierungen aus der ProSiT-Doku übernommen, etwa „rule-aware“, bedingte Modelle, „queue delay after a resource becomes free“, No-rules-Modus und inkrementelles Lernen.
  - 2.6.5 hat jetzt acht Eigenschaften.
  - Ein Einordnungsabsatz: Die Eigenschaften folgen aus dem Design für Ressourcen, die nacheinander arbeiten. Kapazität 1 ist dort richtig.
  - Die Version 1.0.5 ist erwähnt.
- **Kapitel 4:**
  - Absatz „Sensitivity to the tree depth“ in E4.
  - Der Lauf „nur Korrektur 1.0.5“ ist beschrieben.
  - Robustheit in E5 um Tiefe 5 ergänzt.
- **Kapitel 5:**
  - 5.3: neue Begründung für Tiefe 3 (Standard laut Doku, Tiefe 5 als Sensitivitätsanalyse).
  - 5.4: die vier Erweiterungen als präzise Liste.
  - Neuer Absatz „Definitions“ mit formalen Definitionen (Wartezeit ab erster freier Spur, Schlange, Lastmerkmal, Verschiebung beim Start).
  - „holds three trucks“ statt „serves three trucks“.
- **Kapitel 6:**
  - 6.5.1 korrigiert (siehe Punkt 4).
  - Neuer Unterabschnitt 6.5.8 „Sensitivity to the Tree Depth“ mit Tabelle `rq2_depth5`.
  - Absatz zu ProSiT 1.0.5 in 6.5.4.
  - Ein Satz in der Antwort auf RQ2.
- **Diskussion:**
  - Die datenbasierten Teile tragen das Ergebnis.
  - Neuer Absatz: Die Erweiterungen sind keine Kalibrierung, mit Literaturbelegen.
  - Kran-Granularität: Ein Ereignis „Kran beginnt“ würde ProSiTs Logik passend machen.
  - Absatz „Waiting and queue in the simulation model“ (Construct Validity).
  - Tiefe 5 in „Conditions of the result“.
- **Fazit:**
  - Neuer Beitrag C3 (Befunde zu datenbasierter Simulation unter physischen Grenzen).
  - Limitationen nach Art gegliedert: Framework, Daten, Evaluation, Domänenwissen.
  - Future Work neu: Jeder Punkt greift genau eine Limitation auf.
- **Abstract:** „criteria“ statt „checks“, ein Satz zur datenbasierten Linie und zu Tiefe 5.
- **Anhang F:** neuer Abschnitt „Implementation of the Extensions“ mit den Funktionsnamen, dazu neue Zeilen in der Quellentabelle.
- **Front Matter:** neue Seite „Use of Generative AI“ (Entwurf) und Literatureintrag `Anthropic2026Claude`.

## 3. Einordnung der Erweiterungen aus Sicht eines Theorie-Profs

**Ist das Modelloptimierung statt Aufzeigen einer Limitation?** Nein, wenn es so dargestellt wird wie jetzt:
- Die Limitationen sind die Befunde. Sie werden gezeigt:
  - in 2.6.5 aus dem Code;
  - in E3 als Leistung von reinem ProSiT;
  - in E4 durch Ersetzen eines Teils nach dem anderen;
  - mit der Kontrolle „alle Schalter aus = ProSiT“.
- Die Erweiterungen sind der Nachweis. Jede wird einzeln zurückgenommen, und jede wird gebraucht.
- Kalibriert wird nichts. Alle Parameter bleiben aus dem Training gelernt, die Auswahl erfolgt auf dem Training nach einer vorab festgelegten Regel. Geändert wird die Bedeutung von Kapazität, Wartezeit und Bedienzeit, nicht deren Werte.
- In der BPS-Forschung ist das übliche Praxis, etwa extraneous delays bei Chapela-Campa und Dumas oder RIMS. Masterarbeiten wie die von Hoang oder Berat werten Werkzeuge ohne Eingriff aus. Die Situation hier, dass das Werkzeug nicht passt, gibt es dort nicht.
- Der neue 1.0.5-Lauf ist das stärkste Argument. Die offizielle Korrektur des Entwicklers bestätigt einen Befund, reicht aber allein nicht.

**Wo die Arbeit Limitationen und Future Work jetzt verknüpft:** 2.6.5 → E4 → Diskussion 7.3 (vier Arten) → Fazit (dieselben vier Arten) → Future Work (ein Punkt pro Art).

**Wahrscheinliche Fragen und wo die Antwort steht:**
- *Warum nicht Tiefe 5?* 5.3 und 6.5.8. Die Trainingsregel wählt Tiefe 3, Tiefe 5 ändert keine Aussage.
- *Ist das noch ProSiT?* Anhang F. Paket unverändert, gelernt wird mit ProSiTs Funktionen, alle Schalter aus ergibt ein identisches Log.
- *Warum wird eingespielt?* Kapitel 4, „Conditional replay“, mit Law und Özdemir et al.
- *Was ist der Beitrag zum Process Mining?* C3. Die Konformitätsmetriken sagen das Simulationsverhalten nicht voraus, weil die Gewichte die Markierung nicht sehen. Die Ressourcensemantik von ProSiT passt nicht zu Ressourcen mit mehreren Plätzen.
- *Formale Semantik?* 5.4, Absatz „Definitions“. Dazu der Stop Guard als Data-Petri-Netz-Guard mit Bezug auf Felli, de Leoni und Montali.

## 4. Offen, du musst entscheiden oder prüfen

1. **Begutachtung durch das Terminal.** Du hattest gesagt, sie sei „nicht wirklich passiert“. Diese Stellen behaupten sie aber noch:
   - Diskussion 7.5 (Begutachtung per E-Mail am 12. November);
   - Antwort auf RQ3 in Kapitel 6 und im Fazit („The terminal judged the result plausible“);
   - Abstract („found the result plausible“);
   - Fazit, Limitation „Domain knowledge“.

   Ich habe sie nicht geändert, weil ich nicht weiß, was davon stattgefunden hat. Bitte klären.
2. **Seite „Use of Generative AI“.** Gegen die Regeln in Padua prüfen und an deine tatsächliche Nutzung anpassen. Ich kenne nur das Modell dieser Sitzungen.
3. **WOFLAN in ProM.** Der Text sagt jetzt, die Soundness sei in ProM geprüft. Die Skripte nutzten PM4Py. Bitte sicherstellen, dass du die 19 Netze auch in ProM geprüft hast.
4. **Wartung der Blöcke.** „According to the terminal“ steht ohne Datum. Wenn du eins hast, wird daraus eine „personal communication“.
5. **Kapitel 3 heißt jetzt „Event Log Construction“.** Bitte bestätigen.
6. **Grenzfälle im Anhang:** Tabelle E.1 (allgemeine ProSiT-Parameter, doppelt zu 2.6.1) und Abbildung A.2 (Teile der TTT pro Stunde). Behalten oder streichen?

## 5. Korrigierter Fehler

In 6.5.1 stand, alle auf unveränderten Daten neu trainierten Parameter seien identisch. Für HM 0.7 stimmt das nicht ganz. Abweichend sind 3 von 37 Bäumen bei LL und HO2, mit minimalen Unterschieden. Alle Wartezeit-Bäume und alle RMG-Bäume sind identisch. Der Text sagt das jetzt genau so.
