import feedparser
import pickle 
import os
from google import genai
import lancedb
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

def getEmbedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents=text,
    )
    return response.embeddings[0].values



feed = feedparser.parse("http://export.arxiv.org/rss/cs.LG") 

try:
    with open("./seen_ids.pkl", "rb") as file:
        seen_ids = pickle.load(file)

except FileNotFoundError:
    seen_ids = set()
    
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

titles = []
abstracts = []
arxivIds = []

for paper in feed.entries:
    if paper["id"] not in seen_ids:
        titles.append(paper["title"])
        abstracts.append(paper["summary"])
        arxivIds.append(paper["id"])
        seen_ids.add(paper["id"])
    

    
# Combine title + abstract
documents = [f"{title}\n\n{abstract}" for title, abstract in zip(titles, abstracts)]


embeddings = [getEmbedding(doc) for doc in tqdm(documents, desc="Embedding documents")]

# print(documents[0])
db = lancedb.connect("./lancedb")
df = pd.DataFrame({"arxivId": arxivIds, "text": documents, "vector": embeddings})

table = db.open_table("test_arxiv")

table.add(data=df)

# View as pandas DataFrame
df2 = table.to_pandas()
print(df2)

with open("./seen_ids.pkl", "wb"):
    pickle.dump(seen_ids, file)

    