#  Smart Agent System for Strategy Validation

A lightweight AI system that uses local LLMs and autonomous agents to analyze and verify Polish municipal strategy documents (PDFs). Combines Retrieval-Augmented Generation (RAG), multi-agent coordination (CrewAI), and semantic understanding (LangChain) for document classification and fact extraction.

---

## 🚀 What It Does

-  Downloads and processes **PDF strategy documents** from the web
-  Uses **LLM + RAG** to extract relevant facts from the content
-  Uses **autonomous agents** to verify:
  - Whether the PDF is a **valid development strategy**
  - The **date range** of the strategy (e.g., 2021–2030)
  - The **governing administrative unit** (e.g., Gmina, Powiat)

---

## 🧩 Tech Stack

| Area                  | Tools/Libs                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| Retrieval & RAG       | `LangChain`, `FAISS`, `HuggingFaceEmbeddings`, `sentence-transformers`     |
| Language Model        | `Gemma 3B` via `transformers` (local, no OpenAI required)                   |
| Agents & Coordination | `CrewAI`                                                                    |
| PDF Scraping          | `Playwright`, `aiohttp`, `aiofiles`                                        |
| Core Language         | Python 3.10+                                                                |

---

## 🧠 RAG Pipeline

The RAG module loads PDF documents and allows LLM agents to answer questions based on embedded vector similarity.




