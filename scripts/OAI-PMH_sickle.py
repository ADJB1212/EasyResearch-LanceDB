from sickle import Sickle
import pandas as pd

sickle = Sickle("https://oaipmh.arxiv.org/oai")


records = sickle.ListRecords(metadataPrefix="arXiv") 

ids = []
titles = []
abstracts = []

for i, record in enumerate(records):
    if i > 4:
        break
    
    if record.metadata:
        ids.append(record.metadata["id"][0] if record.metadata["id"][0] is not None else None)
        titles.append(record.metadata["title"][0] if record.metadata["title"][0] is not None else None)
        abstracts.append(record.metadata["abstract"][0] if record.metadata["abstract"][0] is not None else None)
        


df = pd.DataFrame({
    "id": ids, 
    "title": titles,
    "abstract": abstracts
})

df.to_csv("sickle_test")
        
        
