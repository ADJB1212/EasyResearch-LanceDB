from sentence_transformers import SentenceTransformer
import lancedb
import numpy as np
from huggingface_hub import hf_hub_download
import torch
import pyarrow as pa
import pandas as pd
import os
import sys
from tqdm import tqdm

# Load local embedding model
model = SentenceTransformer("all-mpnet-base-v2")


def getEmbedding(text):
    """Generate embeddings using local sentence-transformers model"""
    embedding = model.encode(text)
    return embedding.tolist()


db = lancedb.connect("./lancedb")
table = db.open_table("test_arxiv")


queryText = sys.argv[1]
queryEmbedding = getEmbedding(queryText)

results = table.search(queryEmbedding).limit(3).to_pandas()
for _, row in results.iterrows():
    print("Arxiv ID:", row["arxivId"])
    print("Euclidean Distance:", row["_distance"])  # Lower = more similar
    print("Text:", row["text"])
