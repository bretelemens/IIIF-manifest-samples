# Beeld
## use case
Digitale Toegang tot alle beelden van één collectiestuk, m.n.:
* voor-/achterzijden en details van tweedimensionale werken (i.c. een schilderij, een prent)
* geheel en onderdelen van een samengesteld tweedimensionaal object (i.c. een veelluik)
* reeksen van een samengesteld tweedimensionaal object (i.c. een prentenreeks, een fotoreeks)
* geheel, verschillende aanzichten en details van een driedimensionaal object (i.c. een sculptuur, een gerbuiksvoorwerp)
* geheel en de onderdelen van een meervoudig driedimensionaal object (i.c. een theeservies) 
* alle pagina's van een boek, handschrift of tijdschrift 
## implementatie
* Het`manifest`-object representeert alle beelden van een collectiestuk.
* Het `manifest.canvas`-object representeert een specifiek beeld van collectiestuk.
* Het `manifest.canvas.page` is in dit sample redundant.
* Het `Manifest.canvas.page.annotation`-object bevat enkel de beelddata.
* De titel van het collectiestuk bevindt zich in `manifest.label`. Titels worden in viewers als hoofdlabel getoond bij het beeld.
* Een bondige beschrijving van het collectiestuk bevindt zich in `manifest.summary` en bevat een tekenreeks met een objectnaam, datering, maker en bewaarinstelling. 

* De dataverantwoordelijke voor het beeld en de metadata bevindt zich zowel in `manifest.provider`, als in elk `manifest.provider.canvas`-object. In de Viewer dient geconfigureerd te worden welk `provider`-object getoond wordt.
* De rechtenstatus bevindt zich zowel in `manifest.rights`, als in elk `manifest.canvas.rights`-object en bevat een uri voor een rightsstatements-, publiek domein- of CC0-label. In de Viewer dient geconfigureerd te worden welk `rights`-object getoond wordt.
* De naamsvermelding bevindt zich zowel in `manifest.requiredStatement`, als in `manifest.canvas.requiredStatement` en bevat een auteurs-, rechthebbende- en/of herkomstvermelding voor het collectiestuk. 
* Het referentiebeeld voor het collectiestuk bevindt zich in `manifest.thumbnail` en heeft een beeldgrootte van 133 x 175 pixel. Dit beeld wordt bvb gebruikt in zoekresultaten.
* Elk canvas bevat ook een `manifest.canvas.thumbnail` van 133 x 175 pixel dat de viewer gebruikt om door de verschillende canvas'en te browsen. 


## samples
* [003-beeld/momu-m34/manifest.json](https://github.com/bretelemens/IIIF-manifest-samples/blob/main/003-beeld/dummy-manifest.json): Brievenkopijenboek van de familie Melijn voor de periode 1707-1709. Melijn archief, Heemkundige Kring Jan Vleminck vzw, Wijnegem 
([Universal Viewer](https://www.universalviewer.dev/#?manifest=https://bretelemens.github.io/IIIF-manifest-samples/003-beeld/momu-m34/test-manifest.json&xywh=-800%2C-485%2C7417%2C5401), 
[Clover](https://samvera-labs.github.io/clover-iiif/docs/viewer/demo?iiif-content=https%3A%2F%2Fbretelemens.github.io%2FIIIF-manifest-samples%2F003-beeld%2Fmomu-m34%2Fmanifest.json), 
[Glycerine Viewer](https://demo.viewer.glycerine.io/viewer?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/003-beeld/momu-m34/manifest.json), 
[Mirador](https://projectmirador.org/embed/?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/003-beeld/momu-m34/manifest.json),
[IIIF Curation Viewer](https://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest=https://bretelemens.github.io/IIIF-manifest-samples/003-beeld/momu-m34/manifest.json&lang=en))
* [003-beeld/MPM_AR-PN-0169/manifest.json](https://github.com/bretelemens/IIIF-manifest-samples/blob/main/003-beeld/MPM_AR-PN-0169/manifest.json): Kasboek van de persoonlijke uitgaven van Balthasar II Moretus, 1641-07-01 – 1657-05-05. Uit de bibliotheekcollecties van Museum Plantin-Moretus.
([Universal Viewer](https://www.universalviewer.dev/#?manifest=https%3A%2F%2Fbretelemens.github.io%2FIIIF-manifest-samples%2F003-beeld%2FMPM_AR-PN-0169%2Fmanifest.json), 
[Clover](https://samvera-labs.github.io/clover-iiif/docs/viewer/demo?iiif-content=https%3A%2F%2Fbretelemens.github.io%2FIIIF-manifest-samples%2F003-beeld%2FMPM_AR-PN-0169%2Fmanifest.json),
[Glycerine](https://demo.viewer.glycerine.io/viewer?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/003-beeld/MPM_AR-PN-0169/manifest.json))
[Glycerine Viewer](https://demo.viewer.glycerine.io/viewer?iiif-content=https%3A%2F%2Fbretelemens.github.io%2FIIIF-manifest-samples%2F003-beeld%2FMPM_AR-PN-0169%2Fmanifest.json), ,
[IIIF Curation Viewer](https://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest=https%3A%2F%2Fbretelemens.github.io%2FIIIF-manifest-samples%2F003-beeld%2FMPM_AR-PN-0169%2Fmanifest.json&lang=en))
