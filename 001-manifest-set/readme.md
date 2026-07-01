# manifest set
## use case
Toegang tot alle beelden uit een bepaalde verzameling, m.n.:
* lijst met alle manifesten voor collectiestukken uit een specifieke bewaarinstelling
* lijst met alle manifesten voor collectiestukken voor een specifieke query in DAMS
## implementation notes
* collecties van meer dan 250 collectiestukken worden opgedeeld in subcollecties.
## samples
[001-manifest-set/rubenshuis/collection.json](https://github.com/bretelemens/IIIF-manifest-samples/blob/main/001-manifest-set/rubenshuis/collection.json): Alle manifests voor collectiestukken beheerd door Rubenshuis in een iiif-collection object 
* Deze sample bevat 3169 manifests in 1 collection, wat zeer traag laadt. Clover lijkt daar het best mee om te kunnen.
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
[001-manifest-set/rubenshuis/paged-collection.json](https://github.com/bretelemens/IIIF-manifest-samples/blob/main/001-manifest-set/rubenshuis/paged-collection.json): Alle manifests voor collectiestukken beheerd door Rubenshuis verspreid over 13 IIIF sub-collections en toegankelijk via een IIIF top-level collection 
* De sample bevat 3169 manifests, verspreid over 13 subcollecties van max 250 manifests
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

[001-manifest-set/mpm-woodcuts/paged-collection.json](https://github.com/bretelemens/IIIF-manifest-samples/blob/main/001-manifest-set/mpm-woodcuts/paged-collection.json): Alle manifests voor afdrukken van houtblokken in Museum-Plantin-Moretus verspreid over 37 IIIF sub-collections en toegankelijk via een IIIF top-level collection 
* Deze sample bevat 13793 manifests, verspreid over 37 subcollecties
* Universal viewer werkt wel bij deze sample (nog onduidelijk waarom). beelden laden niet.
* Glycerine laadt enkel de eerste subcollectie
* Mirador werkt volledig en laadt ook beelden
* Curation Viewer accepteert de collectie niet

([Universal Viewer](https://www.universalviewer.dev/#?manifest=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/mpm-woodcuts/paged-collection.json), 
[Clover](https://samvera-labs.github.io/clover-iiif/docs/viewer/demo?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/mpm-woodcuts/paged-collection.json), 
[Glycerine Viewer](https://demo.viewer.glycerine.io/viewer?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/mpm-woodcuts/paged-collection.json), 
[Mirador](https://projectmirador.org/embed/?iiif-content=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/mpm-woodcuts/paged-collection.json),
[IIIF Curation Viewer](https://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest=https://bretelemens.github.io/IIIF-manifest-samples/001-manifest-set/mpm-woodcuts/paged-collection.json))


