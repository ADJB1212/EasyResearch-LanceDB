from sentence_transformers import SentenceTransformer
import lancedb
import numpy as np
from huggingface_hub import hf_hub_download
import torch
import pyarrow as pa
import pandas as pd
import os
from tqdm import tqdm

# Load local embedding model
model = SentenceTransformer("all-mpnet-base-v2")


def getEmbedding(text):
    """Generate embeddings using local sentence-transformers model"""
    embedding = model.encode(text)
    return embedding.tolist()


file_path = hf_hub_download(
    repo_id="HuieL/arxiv_graph", filename="arxiv.pt", repo_type="dataset"
)

data = torch.load(file_path, weights_only=False)

titles = [str(t) for t in data["title"]]
abstracts = [str(a) for a in data["abstract"]]
arxivIds = [str(aid) for aid in data["arxiv_id"]]

# Combine title + abstract
documents = [f"{title}\n\n{abstract}" for title, abstract in zip(titles, abstracts)]

embeddings = [getEmbedding(doc) for doc in tqdm(documents, desc="Embedding documents")]

# print(documents[0])
db = lancedb.connect("./lancedb")
df = pd.DataFrame({"arxivId": arxivIds, "text": documents, "vector": embeddings})

table = db.create_table("test_arxiv", data=df, mode="overwrite")

table = db.open_table("test_arxiv")

# View as pandas DataFrame
df2 = table.to_pandas()


# Verify everything went well
queryText = "graph neural networks"
queryEmbedding = getEmbedding(queryText)

results = table.search(queryEmbedding).limit(3).to_pandas()
for _, row in results.iterrows():
    print("Arxiv ID:", row["arxivId"])
    print("Similarity Score:", row["_distance"])
    print("Text:", row["text"])
