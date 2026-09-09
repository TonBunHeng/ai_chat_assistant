# Angkor Verse AI - Tourism Information Service (Cambodia)

An intelligent AI Tourism Information Service specialized in Cambodia tourism built with **FastAPI**, **RAG (Retrieval-Augmented Generation)**, **Google Gemini (`gemini-3.5-flash`)**, **Ollama (`Camtour-On-Mistral-Ai:latest`)**, **SQLite**, and **Vue 3 + Vite**.

---

## AI Model Details

- **Online Cloud Model**: `gemini-3.5-flash` / `gemini-3.7-flash` (Google Gemini API with auto-failover)
- **Primary Offline Model**: `Camtour-On-Mistral-Ai:latest` (Fine-tuned model running locally via Ollama)
- **Supported Alternative Local Models**: `tripmind-ft-gguf`, `llama3.2`, `mistral`
- **Embedding & Semantic Matching**: RapidFuzz fuzzy scoring and high-dimensional semantic vector search over Cambodia tourism datasets
- **Offline Fallback**: Built-in RAG Knowledge Synthesizer engine (ensures 100% server availability even when offline)

---

## Chatbot Operating Modes & Capabilities

### 1. AI Execution Modes (Auto Orchestration)
The system automatically orchestrates between 3 execution tiers based on connectivity and availability:

| Mode | Engine / Provider | Description |
| :--- | :--- | :--- |
| 🌐 **Online Mode** | **Google Gemini** (`gemini-3.5-flash`) | Uses cloud AI along with real-time live tools (Weather, Currency, Live Events, OSM Places). |
| 💻 **Offline Mode** | **Local Ollama** (`Camtour-On-Mistral-Ai:latest`) | Runs locally without internet using Ollama, vector search, and local tourism datasets. |
| 🛡️ **Degraded / Fallback Mode** | **Local Knowledge Engine** | Activated if neither Gemini nor Ollama is reachable; synthesizes answers using cached datasets and rule-based search. |

### 2. Language Modes
- 🇰🇭 **Khmer Mode (ភាសាខ្មែរ)**: Automatic detection of Khmer script with strict 100% Khmer responses (no mixed English prose).
- 🇬🇧 **English Mode**: International mode tailored for foreign tourists and visitors.

### 3. Functional & Tool Modes (Intents)
- 🗺️ **Interactive Itinerary Planning**: Generates structured 1-to-5+ day travel schedules with cost/budget breakdown and interactive day tabs.
- ☀️ **Weather Advisory Mode**: Provides real-time weather forecasts and seasonal packing recommendations.
- 💱 **Currency Conversion Mode**: Real-time / cached USD $\leftrightarrow$ KHR (Cambodian Riel) conversion with quick denomination chips.
- ⭐ **Smart Recommendation Mode**: Ranks temples, beaches, food, and attractions based on user interest & budget.
- 🎊 **Events & Cultural Festivals Mode**: Information on Cambodian holidays (Khmer New Year, Water Festival, Pchum Ben, etc.).
- 📍 **AI Grounded Sources**: Direct verification cards for matched places with Google Maps links.
- 💡 **Suggested Topics**: Smart 2x2 topic recommendation cards with instant follow-up prompts.

### 4. UI Modes
- ☀️ **Light Theme**
- 🌙 **Dark Theme**

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
- `google-genai` & `requests` (Gemini & Ollama HTTP Integration)
- `rapidfuzz` & `numpy` (RAG Vector Search & Semantic Similarity)
- `pytest` (Automated Test Suite)

### Key Frontend Packages (`frontend/package.json`)
- `vue` & `vue-router` (Frontend UI Framework & Routing)
- `vite` (Frontend Build Tool & Dev Server)
- `axios` (HTTP API Client)
- `lucide-vue-next` (Modern Lucide Icons for Vue 3)
- `tailwindcss` (Utility-first CSS framework)

---

## How to Run the Project

### Step 1: Configure Environment Variables

In `backend/.env`:

```env
AI_MODE=online
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=Camtour-On-Mistral-Ai:latest
SIMILARITY_THRESHOLD=0.80
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

---

### Step 2: Start Ollama AI Model (Optional for Offline Mode)

If running offline with Ollama:

```bash
ollama run Camtour-On-Mistral-Ai:latest
```

---

### Step 3: Run Backend Server (FastAPI)

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

### Step 4: Run Frontend Web Application (Vue 3)

Open **Terminal 2**:

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite dev server
npm run dev
```

---

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
5. `"What is the best time of year to visit Kampot and Bokor Mountain?"`
