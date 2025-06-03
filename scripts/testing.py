from google import genai
import lancedb
import numpy as np
from huggingface_hub import hf_hub_download
import torch
import pyarrow as pa
import pandas as pd
import sys
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def getEmbedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents=text,
    )
    return response.embeddings[0].values


db = lancedb.connect("./lancedb")
table = db.open_table("test_arxiv")


queryText = sys.argv[1]
queryEmbedding = getEmbedding(queryText)

results = table.search(queryEmbedding).limit(3).to_pandas()
for _, row in results.iterrows():
    print("Arxiv ID:", row["arxivId"])
    print("Euclidean Distance:", row["_distance"])  # Lower = more similar
    print("Text:", row["text"])
