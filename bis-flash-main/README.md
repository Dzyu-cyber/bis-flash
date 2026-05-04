# 🛡️ BIS Standards Recommendation Engine (Flash Coders)

> **Winner-Grade RAG Pipeline** for the Bureau of Indian Standards x Sigma Squad AI Hackathon 2026.

This project delivers a high-performance, low-latency, and zero-hallucination recommendation engine designed to help Micro and Small Enterprises (MSEs) identify applicable BIS regulations in seconds.

## 🚀 Performance Benchmarks (Public Test Set)

| Metric | Target | **Our Result** | Status |
| :--- | :--- | :--- | :--- |
| **Hit Rate @3** | > 80% | **100.00%** | ✅ Exceeded |
| **MRR @5** | > 0.70 | **0.8833** | ✅ Exceeded |
| **Avg Latency** | < 5.0s | **~4.1s** | ✅ Exceeded |

---

## ⚡ Quick Start (For Judges)

We have prioritized **Seamless Replication**. Use the automated setup script to prepare the environment in one go.

### 1. Instant Environment Setup
```bash
# Installs dependencies, caches quantized models, and initializes index
python setup_env.py
```

### 2. Mandatory Inference (Automated Metrics)
```bash
# Run the entry-point for automated evaluation
python inference.py --input data/public_test_set.json --output team_results.json --no-expand

# Run the provided evaluation script to verify 100% accuracy
python eval_script.py --results team_results.json
```

### 3. Interactive Web UI
```bash
# Launch the premium POC interface
streamlit run src/app.py
```

---

## 🏗️ System Architecture & Innovations

### 1. Two-Stage Optimized Retrieval
*   **Stage 1 (Hybrid Recall)**: Combines Semantic Search (BGE-Small) with Keyword/ID Metadata filtering to ensure zero recall loss.
*   **Stage 2 (Neural Precision)**: Uses a `MiniLM-L6` CrossEncoder to rerank candidates with human-level accuracy.

### 2. CPU Dynamic Quantization (Innovation)
Both the embedding model and the neural reranker are **dynamically quantized (INT8)**. This reduces latency by ~40%, allowing the full pipeline to run on standard consumer CPUs without requiring a dedicated GPU.

### 3. Master-ID Recovery & Part-Boosting
To eliminate hallucinations (Rule 4.2), our engine cross-references all results against a master standard list. We implement **Part-Specificity Boosting**, which correctly distinguishes between different sections of a standard (e.g., IS 1489 Part 1 vs Part 2) based on technical descriptors.

---

## 📁 Repository Structure
```
mse-engine/
├── src/                # Core RAG Logic (Retriever, Generator, Pipeline)
├── chroma_db/          # Persistent Vector Store
├── data/               # Public test set and ground truth results
├── setup_env.py        # Automated environment replicator
├── inference.py        # Mandatory judge entry-point
├── eval_script.py      # Mandatory evaluation script
├── presentation.pdf    # 8-Slide technical deck
└── requirements.txt    # Project dependencies
```

---

## 🛠️ Technical Stack
*   **Vector DB**: ChromaDB
*   **Embeddings**: `BAAI/bge-small-en-v1.5` (Quantized)
*   **Reranker**: `cross-encoder/ms-marco-MiniLM-L-6-v2` (Quantized)
*   **LLM**: Google Gemini 2.0 Flash (For expansion & rationales)

---
*Developed by Flash Coders for the Bureau of Indian Standards x Sigma Squad AI Hackathon 2026.*
