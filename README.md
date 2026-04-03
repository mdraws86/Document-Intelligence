# Document Intelligence

## Blogpost
Please consider to read also my [blogpost](https://medium.com/p/d2ef9133b9f7/edit) on Medium.

---

## 📜 Authors and Licensing

- Author: Martin Draws
- License: [MIT License](https://opensource.org/license/mit).

---

## 📌 Project Motivation

Extracting structured information from contracts sounds straightforward—until you actually try it.

Real-world contracts are messy:
- inconsistent structure
- missing sections
- ambiguous language
- mixed formats (including scanned documents)

This project explores a key question:

> Can a reliable contract intelligence system be built **locally**, without external APIs?

Instead of relying on rigid rules, this project uses a **Retrieval Augmented Generation (RAG)** approach combined with structured outputs to extract meaningful and reusable data from contracts.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/document-intelligence.git
cd document-intelligence
```

Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
```

Install dependencies:

```bash
pip install -r requirements.txt
```

⚠️ This project uses:
Ollama for local LLM hosting (qwen2.5:14b)
Hugging Face embeddings (BAAI/bge-base-en-v1.5)
FAISS for vector similarity search

---

## 📂 Project Structure & File Descriptions

```markdown
.
├── data/ # PDF contract files (Kaggle dataset)
├── notebooks/ # Jupyter notebooks for experimentation
├── src/ # Core Python modules
│ ├── llm_settings.py # Contract extraction schemas and helper functions
│ └── wrangle_data.py # PDF loading, chunking, retriever, embeddings
├── models/ # Optional local LLM models (via Ollama)
├── outputs/ # Extracted structured contract data
├── README.md
└── requirements.txt
```

### Key Components

- **Data ingestion** → Loads and preprocesses contract data  
- **Chunking** → Splits documents into meaningful sections  
- **Retrieval** → Finds relevant contract parts  
- **LLM extraction** → Extracts structured information  
- **Schema enforcement** → Ensures consistent output format  

---

## 📊 Dataset

This project uses a synthetic contract dataset from [Kaggle](https://www.kaggle.com/datasets/juniorbueno/synthetic-data-contracts).

The dataset provides structured examples that simulate real-world contract variability.

---

## 🤝 How to Interact with the Project

1. Place PDF contracts in the `data/` directory.
2. Open the Jupyter notebook and run the pipeline.
3. The pipeline will:
   - Load PDFs and split into meaningful text chunks
   - Create a FAISS retriever using Hugging Face embeddings
   - Query the retriever for relevant sections
   - Use **qwen2.5:14b via Ollama** for structured extraction
   - Return JSON matching the `ContractExtraction` schema
4. Extracted data will be saved in the `outputs/` folder.

---

## 🧠 Approach / Tech Stack

- **LLM:** Qwen2.5:14b (local, via Ollama)  
- **Embeddings:** BAAI/bge-base-en-v1.5 (via Hugging Face)  
- **Vector Store:** FAISS for similarity search  
- **PDF Processing:** PyPDF2 for text extraction  
- **Pipeline Framework:** LangChain Core + Community modules  
- **Schema Validation:** Pydantic v2 for structured output  
- **Text Splitting:** RecursiveCharacterTextSplitter for chunking  

This setup ensures **fully local execution**, **structured output**, and **reproducible contract extraction**.

### Why not rule-based systems?

| Approach   | Works well when…        |
|------------|-------------------------|
| Rule-based | Structure is consistent |
| RAG + LLM  | Structure is messy      |

---

### Structured Extraction

Instead of free-form outputs, the system enforces a schema:

| Without structure    | With structure      |
|---------------------|---------------------|
| Inconsistent output | Predictable format  |
| Hard to reuse       | Easy to integrate   |
| Ambiguous           | Clear expectations  |

This transforms the model from a **text generator** into a **structured data extractor**.

---

### Importance of Retrieval

Rather than processing full documents, we only want to take into account relevant chunks.
This leads to improvements both in accuray and efficiency.

---

## 🚀 Features

- Fully local execution (no external APIs)
- Retrieval-Augmented Generation (RAG)
- Structured outputs (schema-based extraction)
- Modular and extensible pipeline

---

## 🧪 Hardware & Performance Notes

This project was developed and tested on a **MacBook Pro with an Apple M2 chip**.  
The workflow emphasizes **fully local execution**, no external APIs are required.

However, hardware can significantly affect performance:

- On Apple Silicon (M‑series), Ollama runs natively and may leverage the Metal API for GPU support, but in many cases it primarily uses the **CPU**, even on M‑series hardware.  
  Real‑world GPU acceleration on Apple Silicon with Ollama can be limited or inconsistent. 

- For **true GPU acceleration** with Ollama, dedicated GPUs like **NVIDIA cards (CUDA ≥5.0)** offer the best performance.

- **AMD GPU support** is available via ROCm on Linux/Windows systems, but is generally more experimental or limited compared to NVIDIA support.

As a result, while the system *does* run locally on Apple Silicon, performance may vary depending on whether hardware acceleration is available.

---

## 📈 Results & Insights

### What worked well

- RAG significantly improved extraction quality  
- Structured outputs increased usability  
- Local setup ensured full data privacy  

### What could be improved

- Evaluation on real-world contracts  
- OCR support for scanned documents  
- Retrieval optimization  

---

## 🙏 Acknowledgements

- Kaggle dataset providers  
- Ollama for local LLM deployment (qwen2.5:14b)  
- Hugging Face for embeddings and model access (BAAI/bge-base-en-v1.5)  
- FAISS for fast vector similarity search  
- Open-source contributions in document intelligence and RAG systems

---

## 💡 Final Thoughts

Building a contract intelligence system locally is not only possible—

it’s practical.

The key is not complexity, but:
- structure
- relevance
- and thoughtful system design