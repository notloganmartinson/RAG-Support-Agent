# Institutional-Grade Support Agent

An air-gapped, high-precision ReAct-inspired support agent designed for B2B financial software environments. This project demonstrates a production-ready RAG pipeline that prioritizes accuracy, security, and institutional reliability.

## 🚀 Key Features

*   **Hybrid RAG Pipeline**: Combines semantic vector search (ChromaDB) with metadata filtering to ensure only relevant, trusted data reaches the LLM.
*   **Surgical Context Extraction**: Eliminates "context stuffing" by extracting only the specific resolution steps (the "needle") from historical logs.
*   **PII Scrubber**: Automatically detects and masks sensitive information (Emails, Client IDs, ISINs) before processing, ensuring GDPR/SOC2 compliance.
*   **Live System Bridge**: Integrates with production monitors to provide real-time status updates (e.g., API outages) alongside historical fixes.
*   **Self-Improving Feedback Loop**: Allows human agents to verify resolutions, which prioritizes those fixes for future queries.

## 📊 Performance & Reliability

This agent is verified using an automated **Evaluation Framework**. It achieves **100% accuracy** in extracting technical parameters from historical data.

| Category | Query Snippet | Accuracy | Status |
| :--- | :--- | :--- | :--- |
| **Calculation** | Sharpe ratio anomalies... | 100.0% | **PASS** |
| **API** | Direct API timeouts... | 100.0% | **PASS** |
| **UI/Crash** | Intermittent tab crashes... | 100.0% | **PASS** |

## 🛠️ Tech Stack

*   **LLM**: Qwen2.5:3b (Running locally via Ollama)
*   **Vector DB**: ChromaDB
*   **Embeddings**: `all-MiniLM-L6-v2` (Local)
*   **Framework**: Custom Python RAG (No LangChain/LlamaIndex for maximum transparency)
*   **UI**: Rich-enhanced CLI

## 🏃 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Agent**:
   ```bash
   python chat.py
   ```

3. **Run Evaluations**:
   ```bash
   python evaluator.py
   ```

## 🔒 Security & Privacy

This system is designed to be **completely air-gapped**. No data is sent to external APIs (OpenAI, Anthropic, etc.). All embeddings and LLM inferences happen locally on your hardware.
