# manifest set
## use case
Toegang tot alle beelden uit een bepaalde verzameling, m.n.:
* lijst met alle manifesten voor collectiestukken uit een specifieke bewaarinstelling (bvb. alle beelden van alle collectiestukken uit het Rubenshuis)
* lijst met alle manifesten voor collectiestukken voor een specifieke query in DAMS (bvb alle beelden van alle houtblokken uit Museum Plantin-Moretus)
## implementation notes
* een 'paging' methode is niet beschikbaar in IIIF presentation API v3. Aanbevolen is verschillende collecties hierarchisch te organiseren.
* Ofwel alle manifesten in eem collectie
* Ofwel manifesten per 250 in aparte subcollecties verpakken en die subcollectie vindbaar maken via een top-level colletion (cf. paged-collection).
## samples
[001-manifest-set/rubenshuis/collection.json](https://github.com/bretelemens/IIIF-manifest-samples/blob/main/001-manifest-set/rubenshuis/collection.json) 

Alle 3169 manifests voor collectiestukken beheerd door Rubenshuis in 1 collection. 
* Universal Viewer laadt de manifest, maar laadt geen beelden. > Komt omdat de collection de manifesten die opgehaald worden in DAM! nog image uri's bevatten met dams.antwerpen.be als domein.
* Clover Viewer laadt de manifest, maar laadt geen beelden.
* Glycerine Viewer laadt de manifest, maar laadt geen beelden.
* Mirador laadt de manifest, maar laadt geen beelden.
* Curation Viewer accepteert de collectie niet.
(
([Universal Viewer](https://www.universalviewer.dev/#?manifest=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/rubenshuis/collection.json), 
[Clover](https://samvera-labs.github.io/clover-iiif/docs/viewer/demo?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/rubenshuis/collection.json), 
[Glycerine Viewer](https://demo.viewer.glycerine.io/viewer?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/rubenshuis/collection.json), 
[Mirador](https://projectmirador.org/embed/?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/rubenshuis/collection.json),
[IIIF Curation Viewer](https://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/rubenshuis/collection.json))

[001-manifest-set/rubenshuis/paged-collection.json](https://github.com/bretelemens/IIIF-manifest-samples/blob/main/001-manifest-set/rubenshuis/paged-collection.json) 

Alle 3169 manifests voor collectiestukken beheerd door Rubenshuis verspreid over 13 IIIF sub-collections van maximum 250 manifests en toegankelijk via een IIIF top-level collection 
* universal viewer laadt niet.
* Clover laadt niet
* Glycerine laadt enkel de eerste subcollectie
* Mirador linkt niet door naar subcollections. 
* Curation Viewer accepteert de collectie niet.
([Universal Viewer](https://www.universalviewer.dev/#?manifest=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/rubenshuis/paged-collection.json), 
[Clover](https://samvera-labs.github.io/clover-iiif/docs/viewer/demo?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/rubenshuis/paged-collection.json), 
[Glycerine Viewer](https://demo.viewer.glycerine.io/viewer?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/rubenshuis/paged-collection.json), 
[Mirador](https://projectmirador.org/embed/?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/rubenshuis/paged-collection.json),
[IIIF Curation Viewer](https://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/rubenshuis/paged-collection.json))

[001-manifest-set/mpm-woodcuts/paged-collection.json](https://github.com/bretelemens/IIIF-manifest-samples/blob/main/001-manifest-set/mpm-woodcuts/paged-collection.json)

Alle 13793 manifests voor afdrukken van houtblokken in Museum-Plantin-Moretus verspreid over 37 IIIF sub-collections van maximum 250 manifests en toegankelijk via een IIIF top-level collection 
* Universal viewer werkt wel bij deze sample (nog onduidelijk waarom). beelden laden niet.
* Glycerine laadt enkel de eerste subcollectie
* Mirador werkt volledig en laadt ook beelden
* Curation Viewer accepteert de collectie niet

([Universal Viewer](https://www.universalviewer.dev/#?manifest=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/mpm-woodcuts/paged-collection.json), 
[Clover](https://samvera-labs.github.io/clover-iiif/docs/viewer/demo?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/mpm-woodcuts/paged-collection.json), 
[Glycerine Viewer](https://demo.viewer.glycerine.io/viewer?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/mpm-woodcuts/paged-collection.json), 
[Mirador](https://projectmirador.org/embed/?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/mpm-woodcuts/paged-collection.json),
[IIIF Curation Viewer](https://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/mpm-woodcuts/paged-collection.json))


