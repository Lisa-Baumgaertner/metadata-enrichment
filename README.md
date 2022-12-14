# Abstract

In previous years there have been many corpora of parliamentary proceedings created. One of the most extensive projects, covering a wide range of languages and European parliaments , is the [ParlaMint project](https://github.com/clarin-eric/ParlaMint)  (Erjavec et al., 2022). The corpora of this project share a uniform encoding and already include metadata, which is not yet equally rich across the individual corpora.
This thesis seeks to investigate, if an automated process for enriching the missing corpus metadata with the help of the knowledge base Wikidata is viable. <br/>
Beyond the enrichment of metadata, the paper aims to provide two forms of cross-checking using Wikidata. 
The first form of cross-checking includes adding pages on the knowledge base, for persons of the corpora who were found to not yet have a entry on the knowledge base. The data which is added to the knowledge base is the metadata given in the corpora before the enrichment process performed in this thesis. <br/>
The second form of cross-checking entails a comparison of corpus data to data from the knowledge base, to check the data for inconsistencies. This is performed on the corpus metadata pre-enrichment. The differences are noted and visualized using a XSLT stylesheet, where they can be accessed and used further for manual corrections.

# General
**code folder**: contains the programs for the three parts of my thesis.  <br />
**input folder**: contains the corpus files of the ParlaMint project for easier access when testing the code.  <br />
**output folder**: contains the output/ the ParlaMint corpora after running my metadata enrichment program on them.  <br />
**validation folder**: contains the RelaxNG validation files of the ParlaMint project for easy access.

# Metadata Enrichment
- file in 'code' folder called: **xmltree.py** <br/>
- requires python [SPARQLWrapper](https://github.com/RDFLib/sparqlwrapper) and [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) <br/>
- requires [jing](https://relaxng.org/jclark/jing.html) for the validation <br/>

call on command line with:
`python xmltree.py --infile ParlaMint-XX.xml --validation ParlaMint-teiCorpus.rng`
where **--outfile** parameter is optional.
if parameter **--outfile** is not specified the enriched corpus file is automatically written to a file named: **ParlaMint-XX_out.xml**

in the case of wanting to run on **linguistically annotated** corpus file use: <br/>
`python xmltree.py --infile ParlaMint-XX.ana.xml --validation ParlaMint-teiCorpus.ana.rng`

- if all used files are not contained in the same directory, full paths are required.

# Pywikibot
- file in 'code' folder called: **person_bot.py** <br/>
- requires python [SPARQLWrapper](https://github.com/RDFLib/sparqlwrapper) <br/>
- requires [pywikibot](https://github.com/wikimedia/pywikibot) <br/>
- the pywikibot requires configuration and username and password to the Wikidata site, a guide can be found [here](https://www.wikidata.org/wiki/Wikidata:Pywikibot_-_Python_3_Tutorial/Setting_up_Shop)

running the person_bot.py: <br/>
In the **pywikibot** **core** folder, with the person_bot.py file and the ParlaMint-XX-languagecode.txt (this file is created in xmltree.py) copied into the core directory <br/>
`python person_bot.py --infile ParlaMint-XX-nowikiid_xx.txt`


# List of Differences
- file in 'code' folder called: **differencesxml.py**
- requires python [SPARQLWrapper](https://github.com/RDFLib/sparqlwrapper) and [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) <br/>

call from command line using: <br/>
`python differencesxml.py --infile ParlaMint-XX.xml --outfile outfile.xml --style difflist.xslt` <br/>
where all parameters are required to run the program. <br/>
**outfile.xml** can be named however the user wants, but should have **.xml** extension.

- difflist.xslt should be in same folder as the other files or specified with path.
