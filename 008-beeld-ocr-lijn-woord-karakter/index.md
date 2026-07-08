# Reproducties met ge-OCR’de tekst per lijn, woord of karakter als web annotation

## [008-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json](https://github.com/bretelemens/IIIF-manifest-samples/blob/main/08-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json)
Brievenkopijenboek van de familie Melijn voor de periode 1707-1709. Melijn archief, Heemkundige Kring Jan Vleminck vzw, Wijnegem 

([Universal Viewer](https://www.universalviewer.dev/#?manifest=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json), 
[Clover](https://samvera-labs.github.io/clover-iiif/docs/viewer/demo?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json), 
[Glycerine Viewer](https://demo.viewer.glycerine.io/viewer?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json), 
[Mirador](https://projectmirador.org/embed/?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json),
[IIIF Curation Viewer](https://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/momu-m34/referenced-manifest.json&lang=en))

* Alto files geproduceerd met Transcribus in /alto directory. Ocr text getagd per lijn.
* OCR Annotation Pages geproduceerd met/scripts/transform.xsl of alto_to_ocr.py

## [008-beeld-ocr-lijn-woord-karakter/EHC_519618/manifest.json](https://github.com/bretelemens/IIIF-manifest-samples/blob/main/008-beeld-ocr-lijn-woord-karakter/EHC_519618/manifest.json)
Antwerpsch straatnamenboek. lijstvanaldestraatnamen, oude en nieuwe, met hun beteekenis, reden, oorsprong en veranderingen, 1926.Erfgoedbibliotheek Hendrik Conscience.

([Universal Viewer](https://www.universalviewer.dev/#?manifest=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/EHC_519618/manifest.json), 
[Clover](https://samvera-labs.github.io/clover-iiif/docs/viewer/demo?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/EHC_519618/manifest.json),
[Mirador](https://projectmirador.org/embed/?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/EHC_519618/manifest.json)
[Glycerine Viewer](https://demo.viewer.glycerine.io/viewer?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/EHC_519618/manifest.json)
[IIIF Curation Viewer](https://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/EHC_519618/manifest.json))


## [008-beeld-ocr-lijn-woord-karakter/EHC_e772/manifest.json](https://github.com/bretelemens/IIIF-manifest-samples/blob/main/008-beeld-ocr-lijn-woord-karakter/EHC_e722/manifest.json)
Madame de Pompadour, 1881. Erfgoedbibliotheek Hendrik Conscience.

([Universal Viewer](https://www.universalviewer.dev/#?manifest=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/EHC_e772/manifest.json), 
[Clover](https://samvera-labs.github.io/clover-iiif/docs/viewer/demo?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/EHC_e772/manifest.json),
[Mirador](https://projectmirador.org/embed/?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/EHC_e772/manifest.json)

## use case
*	Vindbaarheid van de tekst uit uit een beeld als tekstlaag over het beeld (json web annotations).

## implementation notes
* OCR text per lijn, gelocaliseerd met coordinaten en gecodeerd in ALTO-xml v4.
* OCR text gempt naar annotation page per pagina en in een apart json bestand. Bestandsnaam: "page-[canvas nr].json".
* Coordinaten gecodeerd met een FragmentSelector als suffix bij de canvas uri in het `target` object.
* OCr annotation page: `items.motivation` has default value "supplementing".
* OCR annotation page: `items.body.typs` has default value "TextualBody".
* OCR annotation pages in `/ocr`.
* Oorspronkelijke ALTO xml bestanden in `/alto`.
* Referenties naar OCR annotation page in `annotations`. OCR text wordt getoond in IIIF viewers.
* Referenties naar downloadbaar ALTO bestand in `rendering`.
  

