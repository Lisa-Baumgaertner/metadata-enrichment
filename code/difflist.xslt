<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">
    <xsl:template match="difference">
        <html>
            <body>
                <h2>Difference List</h2>
                <table border="1">
                    <xsl:apply-templates/> 
                </table>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="org">
        <tr bgcolor="#BDECFD">
            <th style="text-align:center">Organisation <xsl:value-of select="@xml:id"/></th>
        </tr>
        <tr>
            <!--<xsl:for-each select="difference/org">-->
            <td>xml:id</td>
            <td><xsl:value-of select="@xml:id"/></td>
        </tr>
        <xsl:for-each select="orgName">
            <tr>
                <xsl:choose>
                    <xsl:when test="@wd='alternative'">
                        <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                        <td bgcolor="#BDFDEA"><xsl:value-of select="@full"/></td>
                        <td bgcolor="#BDFDEA"><xsl:value-of select="text()"/></td>  
                    </xsl:when>
                    <xsl:otherwise>
                        <td><xsl:value-of select ="local-name()"/></td>
                        <td><xsl:value-of select ="@full"/></td>
                        <td><xsl:value-of select="text()"/></td>
                    </xsl:otherwise>
                </xsl:choose>
            </tr> 
        </xsl:for-each>
        <xsl:for-each select="event">
            <tr>
                <xsl:choose>
                    <xsl:when test="@wd='alternative'">
                        <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                        <td  bgcolor="#BDFDEA"><xsl:value-of select="@from"/></td>
                        <td  bgcolor="#BDFDEA"><xsl:value-of select="@to"/></td>
                        <td bgcolor="#BDFDEA"><xsl:value-of select="label/text()"/></td>
                    </xsl:when>
                    <xsl:otherwise>
                        <td><xsl:value-of select ="local-name()"/></td>
                        <td><xsl:value-of select="@from"/></td>
                        <td><xsl:value-of select="@to"/></td>
                        <td><xsl:value-of select ="label/text()"/></td>
                    </xsl:otherwise>
                </xsl:choose>
            </tr>
        </xsl:for-each>
        <xsl:for-each select="idno">
            <tr>
                <xsl:choose>
                    <xsl:when test="@wd='alternative'">
                       <!-- <td><xsl:value-of select ="local-name()"/>  &#160; &#160; &#160;  <xsl:value-of select ="@type"/></td>-->
                        <xsl:choose>
                            <xsl:when test="@subtype">
                                <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                                <td bgcolor="#BDFDEA"><xsl:value-of select ="@subtype"/></td>
                                <!--<td><xsl:value-of select ="@subtype/text()"/></td>-->
                                <td  bgcolor="#BDFDEA"><xsl:value-of select="text()"/> &#160;</td> 
                                    <!--<xsl:value-of select="label/text()"/></td>-->
                             </xsl:when>   
                                <xsl:otherwise>
                                    <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                                    <td bgcolor="#BDFDEA"><xsl:value-of select ="@type"/></td>
                                    <!--<td><xsl:value-of select ="@type/text()"/></td>-->
                                    <td  bgcolor="#BDFDEA"><xsl:value-of select="text()"/> &#160;</td>
                                        <!--<xsl:value-of select="label/text()"/></td>-->
                                   </xsl:otherwise>
                            
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        
                        <xsl:choose>
                            <xsl:when test="@subtype">
                                <td><xsl:value-of select ="local-name()"/></td>
                                <td><xsl:value-of select ="@subtype"/></td>
                                <!--<td><xsl:value-of select ="@subtype/text()"/></td>-->
                                <td><xsl:value-of select="text()"/> &#160; </td>
                                    
                                
                            </xsl:when>   
                            <xsl:otherwise>
                                <td><xsl:value-of select ="local-name()"/></td>
                                <td><xsl:value-of select ="@type"/></td>
                                <!--<td><xsl:value-of select ="@type/text()"/></td>-->
                                <td><xsl:value-of select="text()"/> &#160; </td>
                                    
                                
                            </xsl:otherwise>
                            
                        </xsl:choose>
                    </xsl:otherwise>
                </xsl:choose>
            </tr>
        </xsl:for-each>
            
<!--        <tr bgcolor="#696564"> <td>&#160; </td> <td> &#160; </td><td> &#160; </td></tr>-->
        
        
        
    </xsl:template>
    
    
    <xsl:template match="person">
        <tr bgcolor="#BDECFD">
            <th style="text-align:center">Person <xsl:value-of select="@xml:id"/></th>
        </tr>
        <tr>
            <!--<xsl:for-each select="difference/org">-->
            <td>xml:id</td>
            <td><xsl:value-of select="@xml:id"/></td>  
        </tr>
        
        <xsl:for-each select="persName">
            <xsl:for-each select="surname">
            <tr>
                <xsl:choose>
                    <xsl:when test="@wd='alternative'">
                        <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                        <td bgcolor="#BDFDEA"><xsl:value-of select="text()"/></td>
                    </xsl:when>
                    <xsl:otherwise>
                        <td><xsl:value-of select ="local-name()"/></td>
                        <td><xsl:value-of select ="text()"/></td>
                    </xsl:otherwise>
                </xsl:choose>
            </tr>
            </xsl:for-each>
            <xsl:for-each select="forename">
                <tr>
                    <xsl:choose>
                        <xsl:when test="@wd='alternative'">
                            <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                            <td bgcolor="#BDFDEA"><xsl:value-of select="text()"/></td>
                        </xsl:when>
                        <xsl:otherwise>
                            <td><xsl:value-of select ="local-name()"/></td>
                            <td><xsl:value-of select ="text()"/></td>
                        </xsl:otherwise>
                    </xsl:choose>
                </tr>
            </xsl:for-each>
        </xsl:for-each>
        
        <xsl:for-each select="sex">
            <tr>
                <xsl:choose>
                    <xsl:when test="@wd='alternative'">
                        <xsl:choose>
                            <xsl:when test="@value">
                                <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                                <td bgcolor="#BDFDEA"><xsl:value-of select ="@value"/></td>
                                <!--<td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>-->
                               <td bgcolor="#BDFDEA"><xsl:value-of select="text()"/></td>
                            </xsl:when>
                           
                        <xsl:otherwise>
                            <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                            <td bgcolor="#BDFDEA"></td>
                            <td bgcolor="#BDFDEA"><xsl:value-of select ="text()"/></td>
                        </xsl:otherwise>
                    </xsl:choose>
                
           
            </xsl:when>
                    
              <xsl:otherwise>
                  <xsl:choose>
                      <xsl:when test="@value">
                          <td><xsl:value-of select ="local-name()"/></td>
                          <td><xsl:value-of select ="@value"/></td>
                          <td><xsl:value-of select="text()"/></td>
                          <!--</xsl:choose>--> 
                      </xsl:when>
                      
                      
                      <xsl:otherwise>
                          <td><xsl:value-of select ="local-name()"/></td>
                          <td></td>
                          <td><xsl:value-of select ="text()"/></td>
                      </xsl:otherwise>
                  </xsl:choose>
              </xsl:otherwise>
        </xsl:choose>
            </tr>
        </xsl:for-each>
        
        <xsl:for-each select="birth">
            <tr>
                <xsl:choose>
                    <xsl:when test="@wd='alternative'">
                        <td bgcolor="#BDFDEA"><xsl:value-of select="local-name()"/></td>
                        <td bgcolor="#BDFDEA"><xsl:value-of select="@when"/></td>
                        
                        
                        <xsl:for-each select="placeName">
                            <xsl:choose>
                                <xsl:when test="@wd='alternative'">
                                    <!--<xsl:when test="<xsl:value-of select="placeName/@wd='alternative'"/>"</xsl>-->
                                    <td bgcolor="#BDFDEA"><xsl:value-of select="text()"/></td>
                                </xsl:when>
                                
                                <xsl:otherwise>
                                    <td><xsl:value-of select="text()"/></td>
                                </xsl:otherwise>
                            </xsl:choose>
                            
                        </xsl:for-each>
                        <!--<xsl:choose>
                            <xsl:when test="placeName/@wd='alternative'">
                            <!-\-<xsl:when test="<xsl:value-of select="placeName/@wd='alternative'"/>"</xsl>-\->
                                <td bgcolor="#BDFDEA"><xsl:value-of select="placeName/text()"/></td>
                                
                            </xsl:when>
                            <xsl:otherwise>
                                <td><xsl:value-of select="placeName/text()"/></td>
                            </xsl:otherwise>
                        </xsl:choose>-->
                    </xsl:when>
                    
                    <xsl:otherwise>
                        <td><xsl:value-of select="local-name()"/></td>
                        <td><xsl:value-of select="@when"/></td>
                       <!-- <td><xsl:value-of select="placeName/text()"/></td>-->
                        <xsl:for-each select="placeName">
                            <xsl:choose>
                                <xsl:when test="@wd='alternative'">
                                    <!--<xsl:when test="<xsl:value-of select="placeName/@wd='alternative'"/>"</xsl>-->
                                    <td bgcolor="#BDFDEA"><xsl:value-of select="text()"/></td>
                                </xsl:when>
                                
                                <xsl:otherwise>
                                    <td><xsl:value-of select="text()"/></td>
                                </xsl:otherwise>
                            </xsl:choose>
                            
                        </xsl:for-each>
                        
                    </xsl:otherwise>
                </xsl:choose>
            </tr>
        </xsl:for-each>
        
        <xsl:for-each select="death">
            <tr>
                <xsl:choose>
                    <xsl:when test="@wd='alternative'">
                        <td bgcolor="#BDFDEA"><xsl:value-of select="local-name()"/></td>
                        <td bgcolor="#BDFDEA"><xsl:value-of select="@when"/></td>
                        
                        <xsl:for-each select="placeName">
                            <xsl:choose>
                                <xsl:when test="@wd='alternative'">
                                    <!--<xsl:when test="<xsl:value-of select="placeName/@wd='alternative'"/>"</xsl>-->
                                    <td bgcolor="#BDFDEA"><xsl:value-of select="text()"/></td>
                                </xsl:when>
                                
                                <xsl:otherwise>
                                    <td><xsl:value-of select="text()"/></td>
                                </xsl:otherwise>
                            </xsl:choose>
                            
                        </xsl:for-each>
                        <!--<xsl:choose>
                            <xsl:when test="placeName/@wd='alternative'">
                                <!-\-<xsl:when test="<xsl:value-of select="placeName/@wd='alternative'"/>"</xsl>-\->
                                <td bgcolor="#BDFDEA"><xsl:value-of select="placeName/text()"/></td>
                                
                            </xsl:when>
                            <xsl:otherwise>
                                <td><xsl:value-of select="placeName/text()"/></td>
                            </xsl:otherwise>
                        </xsl:choose>-->
                    </xsl:when>
                    
                    <xsl:otherwise>
                        <td><xsl:value-of select="local-name()"/></td>
                        <td><xsl:value-of select="@when"/></td>
                        
                        <xsl:for-each select="placeName">
                            <xsl:choose>
                                <xsl:when test="@wd='alternative'">
                                    <!--<xsl:when test="<xsl:value-of select="placeName/@wd='alternative'"/>"</xsl>-->
                                    <td bgcolor="#BDFDEA"><xsl:value-of select="text()"/></td>
                                </xsl:when>
                                
                                <xsl:otherwise>
                                    <td><xsl:value-of select="text()"/></td>
                                </xsl:otherwise>
                            </xsl:choose>
                            
                        </xsl:for-each>
                        
                    </xsl:otherwise>
                        <!--<td><xsl:value-of select="placeName/text()"/></td>-->
                    <!--</xsl:otherwise>-->
                </xsl:choose>
            </tr>
        </xsl:for-each>
        
        
        <xsl:for-each select="occupation">
            <tr>
                <xsl:choose>
                    <xsl:when test="@wd='alternative'">
                        <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                        
                        <td  bgcolor="#BDFDEA"><xsl:value-of select="@xml:lang"/></td>
                        <td bgcolor="#BDFDEA"><xsl:value-of select="text()"/></td>
                    </xsl:when>
                    <xsl:otherwise>
                        <td><xsl:value-of select ="local-name()"/></td>
                        
                        <td><xsl:value-of select="@xml:lang"/></td>
                        <td><xsl:value-of select ="text()"/></td>
                    </xsl:otherwise>
                </xsl:choose>
            </tr>
        </xsl:for-each>   
        
        <xsl:for-each select="education">
            <tr>
                <xsl:choose>
                    <xsl:when test="@wd='alternative'">
                        <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                        <td  bgcolor="#BDFDEA"><xsl:value-of select="@xml:lang"/></td>
                        <td bgcolor="#BDFDEA"><xsl:value-of select="text()"/></td>
                    </xsl:when>
                    <xsl:otherwise>
                        <td><xsl:value-of select ="local-name()"/></td>
                        <td><xsl:value-of select="@xml:lang"/></td>
                        <td><xsl:value-of select ="text()"/></td>
                    </xsl:otherwise>
                </xsl:choose>
            </tr>
        </xsl:for-each>   
        
        
        
        
        
        
        
        
        
        
        <xsl:for-each select="affiliation">
            <tr>
                <xsl:choose>
                    <xsl:when test="@wd='alternative'">
                        <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                        
                        <td  bgcolor="#BDFDEA"><xsl:value-of select="@ref"/></td>
                        <td bgcolor="#BDFDEA"><xsl:value-of select="text()"/></td>
                    </xsl:when>
                    <xsl:otherwise>
                        <td><xsl:value-of select ="local-name()"/></td>
                        
                        <td><xsl:value-of select="@ref"/></td>
                        <td><xsl:value-of select ="text()"/></td>
                    </xsl:otherwise>
                </xsl:choose>
                
            </tr>
            
        </xsl:for-each>   
        
        
        <xsl:for-each select="idno">   
            <tr>
                <xsl:choose>
                    <xsl:when test="@wd='alternative'">
                        <!-- <td><xsl:value-of select ="local-name()"/>  &#160; &#160; &#160;  <xsl:value-of select ="@type"/></td>-->
                        <xsl:choose>
                            <xsl:when test="@subtype">
                                <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                                <td bgcolor="#BDFDEA"><xsl:value-of select ="@subtype"/></td>
                                <!--<td><xsl:value-of select ="@subtype/text()"/></td>-->
                                <td  bgcolor="#BDFDEA"><xsl:value-of select="text()"/> &#160;</td> 
                                <!--<xsl:value-of select="label/text()"/></td>-->
                            </xsl:when>   
                            <xsl:otherwise>
                                <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                                <td bgcolor="#BDFDEA"><xsl:value-of select ="@type"/></td>
                                <!--<td><xsl:value-of select ="@type/text()"/></td>-->
                                <td  bgcolor="#BDFDEA"><xsl:value-of select="text()"/> &#160;</td>
                                <!--<xsl:value-of select="label/text()"/></td>-->
                            </xsl:otherwise>
                            
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:choose>
                            <xsl:when test="@subtype">
                                <td><xsl:value-of select ="local-name()"/></td>
                                <td><xsl:value-of select ="@subtype"/></td>
                                <!--<td><xsl:value-of select ="@subtype/text()"/></td>-->
                                <td><xsl:value-of select="text()"/> &#160; </td>
                                
                                
                            </xsl:when>   
                            <xsl:otherwise>
                                <td><xsl:value-of select ="local-name()"/></td>
                                <td><xsl:value-of select ="@type"/></td>
                                <!--<td><xsl:value-of select ="@type/text()"/></td>-->
                                <td><xsl:value-of select="text()"/> &#160; </td>
                                
                                
                            </xsl:otherwise>
                            
                        </xsl:choose>
                    </xsl:otherwise>
                </xsl:choose>
            </tr>  
        </xsl:for-each>
        
        <xsl:for-each select="figure">
            <tr>
                <xsl:choose>
                    <xsl:when test="@wd='alternative'">
                        <td bgcolor="#BDFDEA"><xsl:value-of select ="local-name()"/></td>
                        <td bgcolor="#BDFDEA"></td>
                        <td  bgcolor="#BDFDEA"><xsl:value-of select="graphic/@url"/></td>
                        <!--<td bgcolor="#BDFDEA"><xsl:value-of select="text()"/></td>-->
                    </xsl:when>
                    <xsl:otherwise>
                        <td><xsl:value-of select ="local-name()"/></td>
                        <td></td>
                        <td><xsl:value-of select="graphic/@url"/></td>
                        <!--<td><xsl:value-of select ="text()"/></td>-->
                    </xsl:otherwise>
                </xsl:choose>
            </tr>
    </xsl:for-each>    
    </xsl:template>
</xsl:stylesheet>