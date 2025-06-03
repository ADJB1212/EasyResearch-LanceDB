# EasyResearch LanceDB Prototype

## Setup

1. Install dependencies:

```bash
pip3 install -r requirements.txt
```

2. Choose embedding method:
   - **With Gemini API**: Set `GEMINI_API_KEY` environment variable
   - **Local models**: No additional setup required

## Usage

Note: A decent chunk of the pre-collected data from Hugging Face is malformed (the text of the paper was not scraped correctly)
lancedb/ currently contains a database built using the Local model method

### Build Database

**With Gemini API:**

```bash
python3 scripts/build_dbs.py
```

**With local models:**

```bash
python3 scripts/build_dbs_noAPI.py
```

This downloads ArXiv data from HuggingFace, generates embeddings, and creates a LanceDB database.

### Search Papers

**With Gemini API:**

```bash
python3 scripts/testing.py "search query"
```

**With local models:**

```bash
python3 scripts/testing_noAPI.py "search query"
```

Example:

```bash
python3 scripts/testing_noAPI.py "graph neural"
```

## Files

- `build_dbs.py` / `build_dbs_noAPI.py` - Create vector database
- `testing.py` / `testing_noAPI.py` - Query the database
- `lancedb/` - Vector database storage (created after build)

## Notes

- Local embedding model downloads ~500MB on first use
- Delete `lancedb/` directory to rebuild database
