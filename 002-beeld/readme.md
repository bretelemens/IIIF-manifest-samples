# Beeld
## use case
Digitale Toegang tot alle beelden van één collectiestuk, m.n.:
* voor-/achterzijden en details van tweedimensionale werken (i.c. een schilderij, een prent)
* geheel en onderdelen van een samengesteld tweedimensionaal object (i.c. een veelluik)
* reeksen van een samengesteld tweedimensionaal object (i.c. een prentenreeks, een fotoreeks)
* geheel, verschillende aanzichten en details van een driedimensionaal object (i.c. een sculptuur, een gerbuiksvoorwerp)
* geheel en de onderdelen van een meervoudig driedimensionaal object (i.c. een theeservies) 
* alle pagina's van een boek, handschrift of tijdschrift 
## implementation notes
* Het Manifest representeert alle beelden van een collectiestuk.
* Manifest/labe bevat de titel van het collectiestuk. De titel kan in verschillende talen getoond worden. Elk titel heeft een taalcode. Deze titels worden in de viewer als titel getoond bij het beeld.
* * Het Manifest/Canvas representeert een specifiek beeld van collectiestuk.
* De Manifest/Canvas/Page is in dit sample redundant.
* De Manifest/Canvas/Page/Annotation representeert enkel een beeld.


## samples
* momu: Brievenkopijenboek van de familie Melijn voor de periode 1707-1709. Melijn archief, Heemkundige Kring Jan Vleminck vzw, Wijnegem ([Universal Viewer](https://www.universalviewer.dev/#?manifest=https://bretelemens.github.io/IIIF-manifest-samples/002-beeld/momu-m34/test-manifest.json&xywh=-800%2C-485%2C7417%2C5401), [Clover](https://samvera-labs.github.io/clover-iiif/docs/viewer/demo?iiif-content=https%3A%2F%2Fbretelemens.github.io%2FIIIF-manifest-samples%2F002-beeld%2Fmomu-m34%2Ftest-manifest.json), Mirador)
