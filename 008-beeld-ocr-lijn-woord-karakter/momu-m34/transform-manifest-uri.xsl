<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" encoding="UTF-8"/>
  
  <!-- pass the filename as parameter from command line -->
  <xsl:param name="source-file"/>
  
  <!-- base URI for this collection -->
  <xsl:param name="baseURI"
    select="'https://bretelemens.github.io/IIIF-manifest-samples/002-beeld/momu-m34/test-manifest'"/>
    

  <xsl:variable name="nrStr"
    select="substring-before(substring-after($source-file, 'HKW_M34_'), '.xml')"/> 
  
  <xsl:variable name="nr" select="number($nrStr)"/>
  
  <!-- canvas and page URIs -->
  <xsl:variable name="canvasURI" select="concat($baseURI, '/canvas/', $nr)"/>
  <xsl:variable name="pageURI" select="concat($baseURI, '/page/', $nr, '/2')"/>  


  <!-- start template  -->
  <xsl:template match="/">
    <xsl:value-of select="$pageURI"/>
  </xsl:template>
</xsl:stylesheet>
