# 📊 Financial Document Analyzer – Debug Challenge Submission

## 🚀 Overview

This project is a **Financial Document Analyzer API** built using **FastAPI and CrewAI**.
The system processes uploaded financial documents (PDFs) and provides:

* 📈 Financial Analysis
* 💰 Investment Recommendations
* ⚠️ Risk Assessment

This repository contains a **fully debugged and optimized version** of the original faulty codebase.

---

# 🐛 Bugs Found & Fixes

## 1. Invalid LLM Configuration

### ❌ Issue:

* Code used undefined `llm = llm`
* CrewAI defaulted to OpenAI → caused **401 errors**

### ✅ Fix:

* Replaced with CrewAI-native LLM:

```python
from crewai import LLM

llm = LLM(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)
```

---

## 2. Incorrect Tool Implementation

### ❌ Issue:

* Tool passed as function → caused:

```
Input should be a valid dictionary or instance of BaseTool
```

### ✅ Fix:

* Converted to `BaseTool` class:

```python
class FinancialDocumentTool(BaseTool):
    def _run(self, path: str):
```

---

## 3. Inefficient & Misleading Prompts

### ❌ Issue:

* Prompts encouraged hallucination:

  * “Make up financial data”
  * “Add fake URLs”
  * “Contradict yourself”

### ✅ Fix:

* Replaced with structured prompts:

  * Extract real financial metrics
  * Provide factual analysis
  * Return structured JSON outputs

---

## 4. CrewAI Input Handling Bug

### ❌ Issue:

```python
crew.kickoff({...})
```

### ✅ Fix:

```python
crew.kickoff(inputs={...})
```

---

## 5. OpenAI Fallback Issue

### ❌ Issue:

* CrewAI internally called OpenAI even when using Groq

### ✅ Fix:

* Used CrewAI `LLM` abstraction to explicitly define provider

---

## 6. Token Limit Errors (Groq)

### ❌ Issue:

* Large PDF input → exceeded token limit

### ✅ Fix:

* Limited:

  * Number of pages
  * Text size

---

## 7. Blocking API Requests

### ❌ Issue:

* API processed requests synchronously → slow & not scalable

### ✅ Fix:

* Implemented asynchronous processing using:

```python
FastAPI BackgroundTasks
```

---

# ⚙️ Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone <your-repo-link>
cd financial-document-analyzer
```

---

## 2️⃣ Create Environment

```bash
conda create -n assign_env python=3.11
conda activate assign_env
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Setup Environment Variables

Create `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## 5️⃣ Initialize Database

```bash
python
```

```python
from database import engine, Base
from models import Analysis

Base.metadata.create_all(bind=engine)
exit()
```

---

## 6️⃣ Run Application

```bash
uvicorn main:app --reload
```

---

## 7️⃣ Open API Docs

```
http://127.0.0.1:8000/docs
```

---

# 📡 API Documentation

## 🔹 1. Analyze Financial Document

### Endpoint:

```
POST /analyze
```

### Description:

Uploads a PDF and starts background analysis.

### Request:

* `file` → PDF document
* `query` → optional string

### Response:

```json
{
  "status": "processing",
  "message": "Your document is being analyzed in the background"
}
```

---

## 🔹 2. Get Analysis History

### Endpoint:

```
GET /history
```

### Description:

Returns all stored analysis results.

### Response:

```json
[
  {
    "id": "uuid",
    "query": "string",
    "result": "analysis output",
    "file_name": "file path"
  }
]
```

---

# 🧠 System Architecture

```
User → FastAPI → BackgroundTasks → CrewAI Agents → Database → Response
```

---

# ⚡ Improvements Made

* Fixed critical runtime errors
* Replaced poor prompts with structured ones
* Added asynchronous processing
* Integrated database storage
* Improved code structure and readability

---

# 🔮 Future Enhancements

* Celery + Redis for distributed task processing
* User authentication system
* Dashboard UI
* Vector database (RAG) integration

---

# 👨‍💻 Author

**Harshad Hole**
B.E. Artificial Intelligence & Data Science

---

# 💡 Conclusion

This project demonstrates:

* Debugging complex AI systems
* Prompt engineering
* API development with FastAPI
* Asynchronous processing design

---

⭐ Thank you for reviewing this submission!
