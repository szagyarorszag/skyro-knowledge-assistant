# Skyro Knowledge Assistant

RAG prototype for internal knowledge base - answers questions from company docs.

## Architecture

This is architecture diagram:

```
┌────────────────────────────────────────────────────────┐
│               DOCUMENT INGESTION (One-time)            │
├────────────────────────────────────────────────────────┤
│                                                        │
│  PDF/DOCX/MD Files                                     │
│         │                                              │
│         ▼                                              │
│  DocumentIngester (chunk: 1000 chars, overlap: 200)    │
│         │                                              │
│         ▼                                              │
│  SentenceTransformer (all-MiniLM-L6-v2)                │
│         │                                              │
│         ▼                                              │
│  ChromaDB (384-dim vectors + metadata)                 │
│                                                        │
└────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│           QUERY PROCESSING (Runtime)             │
├──────────────────────────────────────────────────┤
│                                                  │
│  User Question + Role                            │
│         │                                        │
│         ▼                                        │
│  Embed Question (all-MiniLM-L6-v2)               │
│         │                                        │
│         ▼                                        │
│  ChromaDB Similarity Search (top-k chunks)       │
│         │                                        │
│         ▼                                        │
│  Role-based Access Filter                        │
│         │                                        │
│         ▼                                        │
│  Context + Question → Gemini 2.5 Flash           │
│         │                                        │
│         ▼                                        │
│  Answer + Sources + Chunks                       │
│                                                  │
└──────────────────────────────────────────────────┘
```

Documents (PDF, DOCX, MD) get loaded and split into chunks with some overlap so context doesn't break between pieces. Then I use all-MiniLM-L6-v2 to create embeddings locally and store them in ChromaDB.

When user asks something, the question gets embedded too and we do similarity search to find top 5 relevant chunks. These chunks + question go to Gemini 2.5 Flash which generates the answer. Also added role-based access control so different user roles see only their allowed document categories.

## Why I chose what I chose

**Embedding Model (all-MiniLM-L6-v2)**
I decided to use this local model because it's fast and doesn't cost anything to run. Yeah it's not as good as bigger models like OpenAI's text-embedding-3-large but for internal docs it works fine and I don't need to pay for API calls. Also it creates 384-dim vectors which is efficient for storage.

**Vector Store (ChromaDB)**  
ChromaDB is lightweight and easy to setup, doesn't need a server or anything. I know for production scale you'd want something like Pinecone or Weaviate but for a prototype this is perfect and deployment is super simple.

**LLM (Gemini 2.5 Flash)**
After testing 4 different models I picked Gemini 2.5 Flash as default. It's really fast (~1-2s) and quality is good enough. The free tier is generous too. Main downside is it's an external API so there's dependency and rate limits but the speed/quality/cost balance is best here.

**Chunking (1000 chars with 200 overlap)**
Standard approach that works across different document types. The 200 char overlap makes sure context doesn't get lost at boundaries. Could optimize this per doc type but honestly this works fine for most cases.

**UI (Streamlit)**
Used Streamlit because I can build functional UI fast without messing with HTML/CSS/TS. It's not production-ready for high traffic but perfect for prototyping.

## What it can do

The app handles PDF, DOCX and Markdown files. It has a chat interface with history so you can ask multiple questions. There's document-level access control where different roles (Admin, Engineering, Finance, etc.) see only their allowed categories. 

For each answer it shows sources with relevance scores and you can toggle to see the actual chunks that were retrieved. Also added feedback buttons so users can rate if answer was helpful or not(It just saves the fedbacks and does nothing) 

I built comparison and evaluation tools too - tested 4 different LLMs on 10 questions.

## Testing Results

I tested 4 different LLMs on 10 questions and evaluated them with semantic similarity and LLM-as-judge metrics.

### Response Time Comparison

| Model | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Average |
|-------|----|----|----|----|----|----|----|----|----|----|---------|
| Gemini 2.5 Flash | 6.9s | 7.3s | 5.6s | 2.0s | 4.0s | 4.6s | 5.7s | 5.5s | 14.2s | 3.4s | **5.9s** |
| Gemini 2.5 Pro | 23.1s | 20.0s | 11.0s | 13.2s | 12.1s | 19.5s | 10.7s | 17.4s | 29.2s | 31.8s | **18.8s** |
| Mistral Small 3.2 | 7.3s | 6.6s | 5.0s | 5.6s | 6.8s | 4.3s | 7.7s | 4.6s | 6.8s | 5.2s | **6.0s** |
| Llama 3.3 8B | 4.3s | 5.4s | 3.3s | 7.4s | 6.7s | 7.0s | 7.9s | 7.2s | 6.8s | 8.4s | **6.4s** |

### Quality Metrics (LLM-as-Judge by Gemini 2.5 Pro)

| Model | Faithfulness (0-10) | Coverage (0-10) | Hallucinations |
|-------|---------------------|-----------------|----------------|
| Gemini 2.5 Flash | **10.0** | **9.5** | 0 out of 10 |
| Gemini 2.5 Pro | **10.0** | **9.5** | 0 out of 10 |
| Mistral Small 3.2 | 9.0 | 8.8 | 1 out of 10 |
| Llama 3.3 8B | 8.5 | 8.4 | 2 out of 10 |

### Semantic Similarity (Weighted Avg with Retrieved Chunks)

| Model | Average Score (0-1) |
|-------|---------------------|
| Llama 3.3 8B | 0.694 |
| Gemini 2.5 Pro | 0.672 |
| Gemini 2.5 Flash | 0.663 |
| Mistral Small 3.2 | 0.643 |

**My choice: Gemini 2.5 Flash**

Both Gemini models got perfect faithfulness scores (10.0) and same coverage (9.5) with zero hallucinations. Flash is 3x faster than Pro (5.9s vs 18.8s) and comparable to Mistral/Llama (6.0s and 6.4s). But Flash has way better quality (10.0 faithfulness vs 9.0 and 8.5) with no hallucinations. Clear winner.

I tried to test Qwen and DeepSeek too but ran into API rate limits on the free tier.

## How to run

First create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create .env file with your API key:
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

Build the vector store (only need to do this once):
```bash
cd src
python vectorstore.py
```

Run the app:
```bash
streamlit run app.py
```

## If you want to test different models

You'll need OPENROUTER_API_KEY in .env too.

Compare LLMs:
```bash
python llm_comparison.py
```

Run evaluation:
```bash
python evaluate_answers.py
```

## Project structure

- `src/ingest.py` - loads and chunks documents
- `src/vectorstore.py` - creates embeddings and handles ChromaDB
- `src/rag.py` - main RAG logic with access control
- `src/app.py` - Streamlit interface
- `src/llm_comparison.py` - compares different models
- `src/evaluate_answers.py` - evaluates answers with metrics
- `skyro_dataset/data/` - sample documents
