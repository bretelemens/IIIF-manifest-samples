# Beeld met ge-OCR’de tekst van één lijn, woord of karakter als webannotation

## use case
*	Vindbaarheid van de tekst uit uit een beeld als tekstlaag over het beeld (json web annotations).

## implementation notes
Annotation met een link naar een tekstbestand met de ge-OCR’de tekst van één lijn, woord of karakter op het beeld
* annotations/annotation page/annotation/body
* motivation:supplementing
*	type= TextualBody   of id: uri naar het tekstbestand
* target: uri naar canvas met een Fragmentselector voor de preciese locatie van de tekst in het beeld	

## samples
* [008-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json](https://github.com/bretelemens/IIIF-manifest-samples/blob/main/08-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json): Brievenkopijenboek van de familie Melijn voor de periode 1707-1709. Melijn archief, Heemkundige Kring Jan Vleminck vzw, Wijnegem 
([Universal Viewer](https://www.universalviewer.dev/#?manifest=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json), 
[Clover](https://samvera-labs.github.io/clover-iiif/docs/viewer/demo?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json), 
[Glycerine Viewer](https://demo.viewer.glycerine.io/viewer?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json), 
[Mirador](https://projectmirador.org/embed/?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json),
[IIIF Curation Viewer](https://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json&lang=en))
