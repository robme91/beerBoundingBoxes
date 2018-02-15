# Anleitung für das Viola-Jones Projekt

Um das Viola-Jones Projekt zu benutzen, sind mehrere Sschritte nötig die folgend erklärt werden.

## Ordnerstruktur
Die Ordnerstruktur ist entscheidend, damit alle Scripte so funktionieren wie sie sollen. Die Pfade sind relativ, aber innerhalb des Projektes müssen sie dann gleich sein.  
In den Bilder Verzeichnissen, hab ich immer eine init Datei hineingepackt, so dass im Repo eigentlichd ie Ordner zu sehen sein sollten. Falls nicht, sollte es so aussehen:
Root Verzeichnis ist hier _viola-jones_, die unwichtigen Dateien lasse ich hier weg.

* data
	* beerBottles
		* cascade
		* eval
		* negatives
		* positives
		* pred
* tools
	* create\_negative\_samples.py
	* mergejsons.py
* vj-detector.py

## Scripte und Tools ausführen
**Wichtig** ist, dass alles in der anaconda Umgebung ausgeführt werden muss, da ich nicht weiß wie ihr opencv installiert habt. In der conda prompt sind alle nötigen tools vorhanden.

### Bilder hinzufügen
Als erstes müssen die Bilder und die dazugehörigen jsons in die passenden Ordner kopiert werden. Dafür wird der Split Datensatz verwendet.

* Die _train_ Bilder und jsons kommen in den _data/beerBottles/positives_ Ordner
* Die _test_ Bilder/jsons kommen in den  _data/beerBottles/eval_ Ordner

### Trainingsfiles erzeugen
Um mit opencv zu trainieren müssen einige Dateien vorliegen. Um diese zu erzeugen sind entsprechende von uns tools geschrieben worden.

#### 1. Annotationsdatei
Es wird eine info.dat Datei benötigt, aus der Samples generiert werden können. Hierfür wird das Script _tools/mergejsons_ verwendet. 
Einfach _tools_ Verzeichnis das script ausführen. Sind alle Bilder richtig vorhanden, entsteht im Ordner _beerBottles_ anschließend eine _info.dat_ Datei.

#### 2. Negative erzeugen
Ebenfalls werden negative Bilder sowie eine passende Datei benötigt.
Erzeugen durch das _create\_negative\_samples_ Script.
Einfach im _tools_ Ordner das Script ausführen.
Anschließend sollte im _beerBottles_ Ordner eine _negatives.txt_ Datei entstanden sein und im Ordner _negatives_ die negativen Bilder liegen.

#### 3. Samples erstellen
Hierfür wird ein opencv commandline tool verwendet.
Im Ordner _beerBottles_ muss über die conda prompt folgender Befehl ausgeführt werden:

* opencv_createsamples -vec pos-samples.vec -info info.dat -num 800 -h 96 -w 30

Dabei sind die Parameter -num, -h, -w anpassbar. Der Rest sollte so bleiben.
* num sagt anzahl an samples aus die erzeugtw erden sollen
* w, h sind die Pixelmaße der Samples(Boundingboxes)

Nach dem Ausführen sollte eine Datei _pos-samples.vec_ im Ordner _beerBottles_ liegen.

### Das Training
Nachdem alle benötigten Files erzeugt wurden, kann das Training des haar classifiers gestartet werden.
Dafür muss im Ordner _beerBottles_ über die conda-shell folgende commandline ausgeführt werden:

* opencv_traincascade -data cascade -vec pos-samples.vec -bg negatives.txt -numPos 100 -numNeg 50 -numStages 30 -precalcValBufSize 512 -precalcIdxBufSize 512 -h 96 -w 30 -weightTrimRate 0.95 -mode ALL

Die Parameter sind auch hier anpassbar und es sind weitere möglich. Siehe dafür die Doku https://docs.opencv.org/3.3.0/dc/d88/tutorial_traincascade.html .

Die wichtigsten Sachen hier kurz:

* **data** gibt den Namen des Ordners an, in dem alle Trainingsartefakte gespeichert werden. Also der classifier der nachher herauskommt, sowie die logs des Trainings und die Parameter.
* Liegen die files alle wie oben beschrieben, können -vec und -bg einfach übernommen werden.
* Jetzt folgen trainingsspezifische Parameter. Die oben genannten sind Beispiel Werte aus meinem ersten tarining
* **h, w** müssen genauso angegeben werden, wie vorher beim Samples erstellen. Ansonsten gibts Fehler.

In der Konsole läuft dann das Training ab. Die Logs werden im _cascade_ Ordner gespeichert. 
Ist das Training abgeschlossen liegt auch die _cascade.xml_ Datei im _cascade_ Ordner. Diese ist der tranierte classifier, der Benutzt werden kann auf dem _eval_ Datensatz.  
Ist das training beendet und ein neues soll gestartet werden, einfach die Artefakte in den History Ordner kopieren unter einem Nummerierungsverzeichnis z.B. __cascade/history/test12_. Am besten gucken, ob im Repo die nummer schon vergeben ist. Also einfach immer weiterzählen.


### Prediction/Auswertung

Um den classifier zu evaluieren müssen für den _eval_ Datensatz die _pred_ Jsons erstellt werden. Dafür ist das _vj-detector.py_ Script im Rootverzeichnis da.
Hier muss der Pfad zum gewünschten classifieer angepasst werden. Suche nach dem Classifier anpassen _TODO_. 

Dann kann das Script ausgeführt werden. Will man die gemalten Rectangles nicht sehen, kann die show Aufrufe auskommentiert werden. Dafür einfach nach dem passenden _TODO_ suchen. (Weit unten)

Die Jsons werden im Ordner _pred_ abgespeichert. Die verwendeten Testbilder befinden sich im Ordner _eval_.

Sind alle jsons erzeugt können sie iwie mit dem Evaltool von Chris verwendet werden.


**TODO** noch die visualisierung der haar features einbauen, für die doku bestimmt nett