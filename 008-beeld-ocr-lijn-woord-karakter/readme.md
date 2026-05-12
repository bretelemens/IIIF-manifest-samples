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
