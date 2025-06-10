
'''
https://oaipmh.arxiv.org/oai -> base endpoint
one of the followin verbs (response):
 Identify, ListMetadataFormats, ListSets, ListRecords, ListIdentifiers, GetRecord 

choose metadata format (request) -> oai_dc (dublin core),
                     -> arXiv -> arxiv speicifc format
                     -> arXivRaw -> interla arXiv format 
                     

(you can also do an incremental one, so from=2025-06-1 means papers that have been modified from that date or added, etc)
                     
assemble, so https://oaipmh.arxiv.org/oai?verb=ListRecords&metadataPrefix=arXiv


resumption token, just add on at end with &resumptionToken=<token>
'''

import requests
import xml.etree.ElementTree as ET
import pandas as pd
import sickle 


url = "https://oaipmh.arxiv.org/oai?verb=ListRecords&metadataPrefix=arXiv"

response = requests.get(url).content

root = ET.fromstring(response)


ns = {
    'oai': 'http://www.openarchives.org/OAI/2.0/',
    'arxiv': 'http://arxiv.org/OAI/arXiv/'
}



ids = []
titles = []
abstracts = []

max_papers = 5

count =0

for record in root.findall('.//oai:record', ns):
    
    if count >= max_papers:
        break
    
    paper = {}
    
    metadata = record.find("oai:metadata", ns)
    arxiv_meta = metadata.find("arxiv:arXiv", ns)
    
    id = arxiv_meta.find(".//arxiv:id" ,ns)
    title = arxiv_meta.find(".//arxiv:title", ns)
    abstract = arxiv_meta.find(".//arxiv:abstract", ns)
    
    ids.append(id.text) if id is not None else None
    titles.append(title.text) if title is not None else None
    abstracts.append(abstract.text) if abstract is not None else None


    count += 1
    

    
df = pd.DataFrame({
    "arxiv_id": ids, 
    "title": titles,
    "abstract": abstracts
})

df.to_csv("test_oai", index=False)
    
    

    

