<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:alto="http://www.loc.gov/standards/alto/ns-v4#">

  <xsl:output method="text" encoding="UTF-8"/>
  <!-- pass the filename as parameter from command line -->
  <xsl:param name="source-file"/>
  <!--volgnummer canvas uit de bestandsnaam halen. this is meant to extract the number from e.g. HKW_M34_0001.xml -->
    
    <xsl:variable name="nr"
  select="string(number(replace($source-file, '^HKW_M34_(\\d+)\\.xml$', '$1')))" />
  <!-- canvas uri vormen   -->
  <xsl:variable name="canvasURI">
    <xsl:text>https://bretelemens.github.io/IIIF-manifest-samples/002-beeld/momu-m34/test-manifest/canvas/</xsl:text>
    <xsl:value-of select="$nr"/>
  </xsl:variable>
  <!-- page uri vormen -->
  <xsl:variable name="pageURI">
    <xsl:text>https://bretelemens.github.io/IIIF-manifest-samples/002-beeld/momu-m34/test-manifest/page/</xsl:text>
    <xsl:value-of select="$nr"/>
    <xsl:text>/2</xsl:text>
  </xsl:variable>
  <!--
    The ALTO may have been generated from the TIFF, if so the jp2 or IIIF image might be a different size.
    If so use the following ratios to reduce the TIFF coordinates to the IIIF image coordinates:
  -->
  <xsl:param name="xRatio" select="3"/>
  <xsl:param name="yRatio" select="3"/>

  <!-- start json-ld template
  -->
  <xsl:variable name="quote">'</xsl:variable>
  <xsl:variable name="doublequote">"</xsl:variable>

  <!-- entry point -->
  <xsl:template match="/">
    <xsl:text>{</xsl:text>
    <xsl:text>
  "@context":</xsl:text>
    <xsl:value-of select="$doublequote"/>
    <xsl:text>http://iiif.io/api/presentation/3/context.json</xsl:text>
    <xsl:value-of select="$doublequote"/>
    <xsl:text>,
  "id":</xsl:text>
    <xsl:value-of select="$doublequote"/>
    <xsl:value-of select="$pageURI"/>
    <xsl:value-of select="$doublequote"/>
    <xsl:text>,
  "type":</xsl:text>
    <xsl:value-of select="$doublequote"/>
    <xsl:text>AnnotationPage</xsl:text>
    <xsl:value-of select="$doublequote"/>
    <xsl:text>,
  "items":[
</xsl:text>

    <xsl:for-each
      select="/alto:alto/alto:Layout/alto:Page/alto:PrintSpace//alto:TextBlock//alto:TextLine">

      <xsl:text>    {</xsl:text>
      <xsl:text>
      "id":</xsl:text>
      <xsl:value-of select="$doublequote"/>
      <xsl:value-of select="$pageURI"/>
      <xsl:text>/</xsl:text>
      <xsl:value-of select="position()"/>
      <xsl:value-of select="$doublequote"/>

      <xsl:text>,
      "type":</xsl:text>
      <xsl:value-of select="$doublequote"/>
      <xsl:text>Annotation</xsl:text>
      <xsl:value-of select="$doublequote"/>

      <xsl:text>,
      "motivation":</xsl:text>
      <xsl:value-of select="$doublequote"/>
      <xsl:text>supplementing</xsl:text>
      <xsl:value-of select="$doublequote"/>

      <xsl:text>,
      "body":{
        "type":</xsl:text>
      <xsl:value-of select="$doublequote"/>
      <xsl:text>TextualBody</xsl:text>
      <xsl:value-of select="$doublequote"/>

      <xsl:text>,
        "format":</xsl:text>
      <xsl:value-of select="$doublequote"/>
      <xsl:text>text/plain</xsl:text>
      <xsl:value-of select="$doublequote"/>

      <xsl:text>,
        "value":</xsl:text>

      <!-- build the text content of the line -->
      <xsl:variable name="line-text">
        <xsl:apply-templates mode="text"/>
      </xsl:variable>

      <!-- escape backslashes and quotes -->

      <xsl:variable name="step1">
        <xsl:call-template name="replace-string">
          <xsl:with-param name="text" select="normalize-space($line-text)"/>
          <xsl:with-param name="replace" select="'\'"/>
          <xsl:with-param name="with" select="'\\'"/>
        </xsl:call-template>
      </xsl:variable>

<!--
      <xsl:variable name="step2">
        <xsl:call-template name="replace-string">
          <xsl:with-param name="text" select="$step1"/>
          <xsl:with-param name="replace" select='"'/>
          <xsl:with-param name="with" select="concat('\', '"')"/>
        </xsl:call-template>
      </xsl:variable>

      <xsl:value-of select="$doublequote"/>
      <xsl:value-of select="$step2"/>
      <xsl:value-of select="$doublequote"/>
-->
      <!-- target region -->
      <xsl:text>,
      "target":</xsl:text>
      <xsl:value-of select="$doublequote"/>
      <xsl:value-of select="$canvasURI"/>
      <xsl:text>#xywh=</xsl:text>
      <xsl:value-of select="floor(@HPOS div $xRatio)"/>
      <xsl:text>,</xsl:text>
      <xsl:value-of select="floor(@VPOS div $yRatio)"/>
      <xsl:text>,</xsl:text>
      <xsl:value-of select="floor(@WIDTH div $xRatio)"/>
      <xsl:text>,</xsl:text>
      <xsl:value-of select="floor(@HEIGHT div $yRatio)"/>
      <xsl:value-of select="$doublequote"/>


      <xsl:text>
    }
  }
    </xsl:text>

      <!-- comma after each item except the last -->
      <xsl:if test="position() != last()">
        <xsl:text>,</xsl:text>
      </xsl:if>

      <xsl:text>
</xsl:text>
    </xsl:for-each>

    <xsl:text>  ]
}
</xsl:text>
  </xsl:template>

  <!-- extract text content for a TextLine -->
  <xsl:template match="alto:String" mode="text">
    <xsl:value-of select="@CONTENT"/>
  </xsl:template>

  <xsl:template match="alto:SP" mode="text">
    <xsl:text> </xsl:text>
  </xsl:template>

  <!--
    general recursive template to replace a substring
  -->
  <xsl:template name="replace-string">
    <xsl:param name="text"/>
    <xsl:param name="replace"/>
    <xsl:param name="with"/>

    <xsl:choose>
      <xsl:when test="contains($text, $replace)">
        <xsl:value-of select="substring-before($text, $replace)"/>
        <xsl:value-of select="$with"/>
        <xsl:call-template name="replace-string">
          <xsl:with-param name="text"
            select="substring-after($text, $replace)"/>
          <xsl:with-param name="replace" select="$replace"/>
          <xsl:with-param name="with" select="$with"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$text"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
