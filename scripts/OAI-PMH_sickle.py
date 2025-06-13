from sickle import Sickle
import pandas as pd
from datetime import datetime 
import lancedb
import pickle
from load_dotenv import load_dotenv
from google import genai
import os
from tqdm import tqdm


load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def getEmbedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents=text,
    )
    return response.embeddings[0].values

def combine_title_and_abstract(row):
    return f"{row['title']}\n\n{row['abstract']}"


#load seen ids
try:
    with open("./seen_ids.pkl", "rb") as file:
        seen_ids = pickle.load(file)

except FileNotFoundError:
    seen_ids = set()
    
    
 
 #get records from oai 
 
sickle = Sickle("https://oaipmh.arxiv.org/oai")
records = sickle.ListRecords(metadataPrefix="arXiv") 

data = []

for i, record in enumerate(records):
    if i > 3:
        break
    
    metadata = record.metadata
    
    if metadata:
        
        id = metadata.get("id", [None])[0]

        if(id and id not in seen_ids):
            
            seen_ids.add(id)
            
            title = metadata.get("title", [""])[0]
            abstract = metadata.get("abstract", [""])[0]


            data.append({
                "arxiv_id": id,
                "title": title,
                "abstract": abstract,
            })


df = pd.DataFrame(data)
#add to lance

db = lancedb.connect("./lancedb")

# Combine title + abstract
documents = df.apply(combine_title_and_abstract, axis=1).tolist()

embeddings = [getEmbedding(doc) for doc in tqdm(documents, desc="Embedding documents")]


df.drop(["title", "abstract"], axis=1, inplace=True)

df['text'] = documents
df['embeddings'] = embeddings

table = db.open_table("test_sync_daily")

table.add(data=df)

# View as pandas DataFrame
df2 = table.to_pandas()
print(df2)

with open("./seen_ids.pkl", "wb") as file:
    pickle.dump(seen_ids, file)
        
        
