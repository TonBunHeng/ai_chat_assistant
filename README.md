# AI Tourism Information Chatbot (Cambodia)

An intelligent AI Tourism Information Service specialized in Cambodia tourism built with **FastAPI**, **RAG (Retrieval-Augmented Generation)**, **Ollama (`Camtour-On-Mistral-Ai:latest`)**, **SQLite**, and **React + Vite**.

---

## AI Model Details

- **Primary AI Model**: `Camtour-On-Mistral-Ai:latest` (Fine-tuned model running locally via Ollama)
- **Supported Alternative Models**: `tripmind-ft-gguf`, `llama3.2`, `mistral`
- **Embedding Model**: `sentence-transformers` (`all-MiniLM-L6-v2`) for RAG vector search
- **Offline Fallback**: Built-in RAG Knowledge Synthesizer engine (ensures 100% server availability even if Ollama is restarting)

---

## Software & Package Requirements

### System Prerequisites
- **Node.js**: v18.0.0 or higher
- **Python**: v3.9.0 or higher
- **Ollama**: Download from [ollama.com](https://ollama.com) or install via Homebrew (`brew install ollama`)

### Key Python Packages (`backend/requirements.txt`)
- `fastapi` & `uvicorn[standard]` (REST API Web Framework)
- `pydantic` & `pydantic-settings` (Data Validation & Environment Management)
- `python-dotenv` (Environment Variables)
- `sentence-transformers` & `numpy` (RAG Vector Embeddings & Similarity Search)
- `requests` & `httpx` (Ollama HTTP Integration)
- `pytest` (Automated Test Suite)

### Key Frontend Packages (`frontend/package.json`)
- `react` & `react-dom` (UI Library)
- `vite` (Frontend Build Tool & Dev Server)
- `axios` (HTTP API Client)
- `lucide-react` (UI Icons)
- `tailwindcss` (Styling)

---

## How to Run the Project

### Step 1: Start Ollama AI Model

Ensure Ollama is running and start the model:

```bash
ollama run Camtour-On-Mistral-Ai:latest
```

---

### Step 2: Run Backend Server (FastAPI)

Open **Terminal 1**:

```bash
# Navigate to backend directory
cd backend

# Create & activate virtual environment (macOS / Linux)
python3 -m venv venv
source venv/bin/activate

# Install Python requirements
pip install -r requirements.txt

# Start backend server
python3 run.py
```

- **Backend API**: `http://localhost:8000`
- **Swagger Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/api/health`

---

### Step 3: Run Frontend Web Application (React)

Open **Terminal 2**:

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite dev server
npm run dev
```

## Sample Test Questions

### Khmer Questions
1. `"អង្គរវត្តនៅឯណា?"`
2. `"តើទៅសៀមរាបគួរទៅកន្លែងណាខ្លះ?"`
3. `"រៀបចំដំណើរកំសាន្តសៀមរាប 3 ថ្ងៃឲ្យខ្ញុំ"`
4. `"តើម្ហូបអាហារល្បីៗនៅកម្ពុជាមានអ្វីខ្លះ?"`
5. `"ខ្ញុំចូលចិត្តឆ្នេរសមុទ្រ តើគួរទៅកោះណា?"`

### English Questions
1. `"Where is Angkor Wat located?"`
2. `"What are the top things to do in Siem Reap?"`
3. `"Can you create a 3-day travel itinerary for Siem Reap?"`
4. `"What traditional Cambodian food should I try?"`
5. `"What is the best time of year to visit Kampot and Bokor Mountain?"`# AI_ChatBot_Support_Tourism_Information
