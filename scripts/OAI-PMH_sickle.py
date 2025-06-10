from sickle import Sickle
import pandas as pd

sickle = Sickle("https://oaipmh.arxiv.org/oai")


records = sickle.ListRecords(metadataPrefix="arXiv") 


data = []

for i, record in enumerate(records):
    if i > 4:
        break
    
    metadata = record.metadata
    
    if metadata:
        data.append({
            "id": metadata.get("id", None)[0],
            "title": metadata.get("title", None)[0],
            "abstract": metadata.get("abstract", None)[0]
        })
        


df = pd.DataFrame(data)

df.to_csv("sickle_test", index=False )
        
        
