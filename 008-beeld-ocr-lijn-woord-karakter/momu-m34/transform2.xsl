<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:alto="http://www.loc.gov/standards/alto/ns-v4#">

  <xsl:output method="text" encoding="UTF-8"/>
  
  <xsl:param name="source-file"/>
  <xsl:param name="xRatio" select="3"/>
  <xsl:param name="yRatio" select="3"/>
  
  <!-- Extract number from filename (XSLT 1.0 compatible) -->
  <xsl:variable name="nr">
    <xsl:call-template name="extract-number">
      <xsl:with-param name="text" select="$source-file"/>
    </xsl:call-template>
  </xsl:variable>
  
  <xsl:variable name="canvasURI">https://bretelemens.github.io/IIIF-manifest-samples/002-beeld/momu-m34/test-manifest/canvas/<xsl:value-of select="$nr"/></xsl:variable>
  
  <xsl:variable name="pageURI">https://bretelemens.github.io/IIIF-manifest-samples/002-beeld/momu-m34/test-manifest/page/<xsl:value-of select="$nr"/>/2</xsl:variable>

  <!-- Main template -->
  <xsl:template match="/">
    <xsl:text>{"@context":"http://iiif.io/api/presentation/3/context.json","id":"</xsl:text>
    <xsl:value-of select="$pageURI"/>
    <xsl:text>","type":"AnnotationPage","items":[</xsl:text>
    
    <xsl:for-each select="/alto:alto/alto:Layout/alto:Page/alto:PrintSpace//alto:TextLine">
      <xsl:text>{"id":"</xsl:text>
      <xsl:value-of select="$pageURI"/>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="position()"/>
      <xsl:text>","type":"Annotation","motivation":"supplementing","body":{"type":"TextualBody","format":"text/plain","value":"</xsl:text>
      
      <!-- Extract and escape text -->
      <xsl:variable name="text">
        <xsl:apply-templates select=".//alto:String | .//alto:SP" mode="text"/>
      </xsl:variable>
      <xsl:call-template name="escape-json">
        <xsl:with-param name="text" select="normalize-space($text)"/>
      </xsl:call-template>
      
      <xsl:text>"},"target":"</xsl:text>
      <xsl:value-of select="$canvasURI"/>
      <xsl:text>#xywh=</xsl:text>
      <xsl:value-of select="floor(@HPOS div $xRatio)"/>
      <xsl:text>,</xsl:text>
      <xsl:value-of select="floor(@VPOS div $yRatio)"/>
      <xsl:text>,</xsl:text>
      <xsl:value-of select="floor(@WIDTH div $xRatio)"/>
      <xsl:text>,</xsl:text>
      <xsl:value-of select="floor(@HEIGHT div $yRatio)"/>
      <xsl:text>"}</xsl:text>
      
      <xsl:if test="position() != last()">,</xsl:if>
    </xsl:for-each>
    
    <xsl:text>]}</xsl:text>
  </xsl:template>

  <!-- Extract text content -->
  <xsl:template
