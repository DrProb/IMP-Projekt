# Imp Projekt Leo, Paul, Darragh
**IMP Projekt am ende des Jahres**

**Beschreibung:** 

Bei unserem Spiel handelt es sich im Prinzip um "Mensch Ärgere Dich Nicht", allerdings haben wir das Spiel insofern verändert, dass sobald man eine Figur schlägt, ein Kampf ausgelöst wird, welcher solchen aus Spielen wie "Final Fantasy" oder "Expedition 33" ähnelt. Bei diesen Kämpfen hat man drei verschiedene Angriffe, einen normalen Angriff, welcher keinen der "FP" genannten Ressourcen verbraucht und entsprechend wenig Schaden verursacht, einen schweren Angriff, der 1 FP verbraucht und stärker ist, und einen Spezialangriff, der am meisten Schaden verursacht, aber entsprechend 3 FP verbraucht. Sobald man vom Gegner angegriffen wird, hat man die Möglichkeit, diesen Angriff abzuwehren, was mithilfe von gutem Timing erfolgt, indem man einen sich bewegenden grünen Balken zum richtigen Zeitpunkt stoppen muss. Je nachdem, wie gut dies gelingt, wird unterschiedlich viel Schaden abgewehrt. Die Story des Spiels lautet wie Folgt: Eines Tages wurde das Königreich von Linus Torvalds heimgesucht und verfiel dessen Unheil. Die Bewohner des Königreichs wurden von Linus gefangen genommen und zu seinen Untertanan gemacht. Unter ihnen sind Herr Lenz-Faktenverweigerer, ein einstiger Gelehrter, der nun alles nicht seinem Weltbild entsprechende gekonnt leugnet, Georgbär, früher ein Friedlicher bewohner der Wälder, der nun agressiv mit schweren Flaschen nach fremden wirft, Friedrich Schmerz, ein ehemaliger Politiker, der nun bei allen angehörigen der Opposition, aber auch bei allen anderen Feinden starke Schmerzen verursacht, und die drei Weisen Oleg, Fassan und Ayale, die nun jegliche Feinde des Linus Torvalds mit deren eigenen Mitteln in die Knie zwingen. Nur noch der Krieger Aaron ist mithilfe der Magie, die er bei seinen Reisen nach Tibet und seinem langjährigen Training bei DanPost, dem stärksten gelehrten des Landes, lernte, in der Lage, die Untertanen Torvalds' so wie ihn selbst zu besiegen und Frieden zurück ins Land zu bringen.
Besagter Aaron setzt sich aus uns, die 3 Entwickler dieses Spiels zusammen. Der Name in Ehren unseres Freundes Aaron, der leider nicht am Projekt teilnehmen konnte, Das Schalke-Trikot in Anlehnung an Leos Liebe für besagten Verein, die Gitarre und das Gesicht in Anlehnung an Pauls Verehrung des Gitarristen Eddie Van Halen und die Vodkaflasche in Anlehnung an Darraghs unkontrollierbaren Alkoholismus (das ist ein Witz) sowie der Gesichtsausdruck in Anlehnung an Darraghs Wut (das leider nicht).

**Teammitglieder:**

Wie bereits Gesagt waren an diesem Projekt Leo Scheller, Darragh Käßer und Paul Herweh beteiligt. Ersterer übernahm die Aufgabe des Mensch-Ärgere-Dich-nicht Teils des Spiels, sowie die Intergration von Darraghs und Pauls Code in seinen Code, welcher leztenendes das Fertige Produkt wurde, und letzte "Aufräumarbeiten" in Spiel und Code (Edit von Leo: Letzte Aufräumarbeiten ist bodenlos ich grinde hier während du auf einem Konzert chillst, und dann ist hier auch noch JEDES DRITTE WORT falsch geschrieben. Nomen schreibt man GROß!!! NAME SCHREIBT MAN OHNE H (Entschuldigen Sie Frau Rolli, das musste raus.)). Paul schrieb den Code für die Kämpfe und die verschiedenen Alleinstellungsmerkmale dieser. Darragh war für die Animationen in den Kämpfen des Spiels zuständig sowie, zusammen mit Paul, dem Beheben der Bugs in besagten Kämpfen zuständig.

**Setup-Anleitung:**
1. Installieren Sie Visual Studio Code, Git und Python (https://code.visualstudio.com/, https://www.python.org/downloads/, https://git-scm.com/downloads)
2. Installieren Sie Pygame, indem Sie Visual Studio Code öffnen und im Terminal "pip install pygame" eingeben
3. Erstellen Sie irgendwo auf ihrem Computer einen neuen Ordner
4. Rechtsklicken Sie in besagtem Ordner, gehen sie auf "Weitere Optionen" und wählen sie "in Git Bash öffnen"
5. Schreiben Sie in Git Bash folgenden Befehl "git clone https://github.com/DrProb/IMP-Projekt"
6. Geben sie im Terminal in Visual Studio Code den Befehl "python Programmcode.py" ein

**Übersicht über die Aufgabe:**

Teil 1: GitHub
Inwiefern wir GitHub verwendet haben ist sehr leicht zu erklären. Da wir alle 3 wärend der Bearbeitungszeit dieses Projekts unserere GFSen hielten, jedoch zu unterschiedlichen Zeitpunkten, mussten wir uns zeitlich so abstimmen, dass jeder zu unterschiedlichen Zeiten Arbeitet. Wir legten unsere eigenen Branches an, in denen wir zuerst die uns zugeteilten Teile (besagte Verteilung wurde oben näher erklärt) des Projektes erledigten, wie gesagt zu unterschiedlichen Zeiten. Nach ungefähr 2 Wochen waren Darragh und Paul soweit, dass sie ihre Codes - Darragh machte die Animationen für die Kämpfe von Paul - zusammenführen konnten, was in einem extra dafür vorgesehenen Branch geschah. Wenige Tage später hat Leo Darragh und Pauls Code auch schon in seinen integriert. Dies Geschah im Leo-Branch. Nachdem dies getan war, mussten wir nur noch kleinere Grafik-Bugs beheben (Edit: Wutköder von Paul, ich musste noch so viele Dinge machen), Musik sowie Bilder für Gegner und Spieler, also keine Animationen, hinzufügen. Bei der Musik handelt es sich übrigens in erster Linie um 8-Bit Versionen von älteren Rock-und Popsongs, mit Ausnahme der Musik aus dem Losing-Screen, die Paul selbst schrieb und Aufnahm. 
Teil 2: Datenbanken
Datenbanken kamen in 2 verschiedenen Situationen zum Einsatz. Zum einen werden bei den Kämpfen die Alleinstellungsmerkmale der Bosse, wie die Anzahl der HP, die speziellen Fähgkeiten, die Bilder etc. aus Datenbanken abgerufen, um zu verhindern, dass es am ende effektiv 5 verschiedene Kampf-Codes gibt, die zu 80% identisch zueinander wären. Zum anderen wird mithilfe von Datenbanken eine Speicher-Funktion ermöglicht. Dies geschieht, indem die Positionen der Gegner- und Spielersteine auf dem Mensch-ärgere-dich-nicht-Brett in Datenbanken eingetragen werden, um zu ermöglichen, dass man, sollte das Spiel geschlossen werden, weiterspielen kann, ohne den zuvor erlangten Fortschritt zu verlieren. 

**Steuerung:**

Da Paul uns dieses README als fertig verkaufen wollte, und jetzt auf einem Steve Vai Konzert ist, aber vergessen hat die Steuerung zu erklären, schreibe ich (Leo) jetzt noch ganz kurz eine kurze Erklärung dieser:

Während des Mensch Ärgere dich Nichts:
- Leertaste: Würfeln
- Linksklick auf sich drehende Spielfiguren: Zug ausführen
- STRG+R: Spiel zurücksetzen

Während des Turn-Based-Combat Fights:
- Rechtsklick: Menü Öffnen/Wechseln
- Pfeiltaste oben/unten: Aktion wählen
- Enter: Aktion bestätigen
- Leertaste: Blocken (Wenn Blockmodus aktiv)