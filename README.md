# 💬✨ AI-Powered Social Media Content Optimizer

**"Transform your tone. Optimize your reach. Predict your impact."**

An intelligent social media assistant that rewrites comments for 2 major platforms (Reddit, YouTube) with platform-specific optimization, engagement prediction, and intelligent hashtag generation. Built with **LangChain**, **LangGraph**, **Google Gemini AI**, **FastAPI**, and **React**.

---

## 🚀 Features

### 🎨 **8 Tone Rewriting Modes**
- **Casual** 😊 — Friendly and relaxed
- **Professional** 💼 — Business-appropriate
- **Supportive** 🤗 — Encouraging and uplifting
- **Sarcastic** 😏 — Witty and ironic
- **Respectful** 🙏 — Polite and considerate
- **Empathetic** 💙 — Understanding and compassionate
- **Funny** 😂 — Humorous and entertaining
- **Motivational** 🚀 — Inspiring and energizing

### 📱 **2 Social Media Platform Integrations**
- **Reddit** 🤖 — 10K char limit, no hashtags, respectful discourse
- **YouTube** ▶️ — 10K char limit, 15 hashtags, engaging comments

### ✨ **Key Capabilities**
- **Platform-Specific Optimization** — Auto-adjusts length, hashtags, and tone per platform
- **Engagement Prediction** — Predicts virality score, likes, shares, and comments
- **Intelligent Hashtag Generation** — Creates platform-appropriate hashtags automatically
- **Character Limit Enforcement** — Ensures comments fit within platform constraints
- **Context-Aware Rewriting** — Maintains core message while transforming tone
- **Explainability Layer** — Shows why words were changed
- **Real-time Processing** — Instant rewriting with <1s response time
- **One-Click Copy** — Copy optimized content to clipboard instantly

---

## 🧠 Technical Architecture

```
┌─────────────┐      HTTP      ┌──────────────┐     LangChain    ┌─────────┐
│   React     │ ───────────────▶│   FastAPI    │ ───────────────▶│ GPT-4   │
│  Frontend   │◀─── ─────────────│   Backend    │◀─────────────────│  / 3.5  │
└─────────────┘     JSON        └──────────────┘    Response     └─────────┘
      │                                │
      │                                │
   Tailwind                      LangGraph
   Lucide Icons                  Workflow
```

### **Tech Stack**
- **Frontend**: React + TypeScript + Tailwind CSS + Vite + Lucide Icons
- **Backend**: FastAPI + LangChain + LangGraph + Python 3.12
- **AI Engine**: Google Gemini 2.0 (FREE API with generous limits)
- **NLP Tools**: TextBlob for sentiment analysis
- **State Management**: LangGraph state machine (5-node workflow)

---

## 📦 Installation

### **Prerequisites**
- Node.js 18+ and npm/yarn
- Python 3.9+
- OpenAI API key (optional — works in mock mode without it)

### **1. Clone the Repository**
```bash
git clone <your-repo-url>
cd nlp-project
```

### **2. Backend Setup**

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
copy .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run backend
python main.py
```

Backend will run on **http://localhost:8000**

### **3. Frontend Setup**

```bash
# In a new terminal, from project root:
npm install

# Start frontend
npm run dev
```

Frontend will run on **http://localhost:5173**

---

## 🎮 Usage

### **Quick Start**

1. **Open** http://localhost:5173 in your browser
2. **Type or paste** your comment in the text box
3. **Select a tone** from the 8 available options
4. **Click "Rewrite Comment"** and see the magic! ✨

### **Example Transformations**

| Original | Tone | Rewritten |
|----------|------|-----------|
| "Bruh this product is trash 😤" | Professional | "I encountered some quality concerns with this product" |
| "That movie sucked" | Casual | "Honestly, the movie wasn't really my thing" |
| "You're doing it wrong" | Supportive | "I see what you're trying to do! Here's a suggestion..." |
| "This is the best idea ever" | Sarcastic | "Oh wow, this is *totally* the best idea I've ever heard 🙄" |

---

## 🧪 API Documentation

### **Base URL**
```
http://localhost:8000
```

### **Endpoints**

#### `GET /`
Health check and API info

#### `GET /tones`
Returns available tone options with examples

#### `POST /rewrite`
Rewrite a comment with specified tone

**Request Body:**
```json
{
  "comment": "This product is terrible",
  "tone": "professional",
  "context": "Product review",
  "persona": "influencer"
}
```

**Response:**
```json
{
  "original": "This product is terrible",
  "rewritten": "I encountered several quality issues with this product",
  "tone": "professional",
  "persona": "influencer",
  "explanation": [
    "Removed harsh language to be more constructive",
    "Adjusted phrasing to match professional tone"
  ],
  "processing_time": 0.234,
  "model_used": "gpt-4"
}
```

---

## 🔧 Configuration

### **Environment Variables (.env)**

```bash
# Required for AI features
OPENAI_API_KEY=sk-your-key-here

# Optional
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo
API_HOST=0.0.0.0
API_PORT=8000
```

### **Running Without OpenAI API Key**

The app works in **mock mode** without an API key! Perfect for:
- Testing the UI
- Development
- Demos

Simply run without setting `OPENAI_API_KEY` and it will use template-based rewriting.

---

## 🎯 LangGraph Workflow

The rewriting process uses a **LangGraph state machine**:

```
┌───────────────┐
│  Detect Tone  │ (Analyze original comment)
└───────┬───────┘
        │
┌───────▼────────┐
│ Create Prompt  │ (Build LLM prompt with tone/persona)
└───────┬────────┘
        │
┌───────▼─────────┐
│ Generate Rewrite│ (Call LLM or use mock)
└───────┬─────────┘
        │
┌───────▼──────────┐
│ Explain Changes  │ (Generate explanation)
└──────────────────┘
```

Each node is modular and can be extended with:
- Sentiment analysis
- Context understanding
- User preference learning
- Multi-language support

---

## 📁 Project Structure

```
nlp-project/
├── backend/
│   ├── main.py              # FastAPI + LangGraph backend
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   └── .env                 # Your config (gitignored)
├── src/
│   ├── App.tsx              # React main component
│   ├── main.tsx             # React entry point
│   └── index.css            # Tailwind styles
├── package.json             # Node dependencies
├── vite.config.ts           # Vite configuration
├── tailwind.config.js       # Tailwind configuration
└── README.md                # This file
```

---

## 🚧 Development

### **Running Tests**
```bash
# Backend tests (add pytest later)
cd backend
pytest

# Frontend (add vitest later)
npm test
```

### **Code Formatting**
```bash
# Backend
black main.py

# Frontend
npm run format
```

---

## 🎨 Future Enhancements

- [ ] **Vector DB Integration** — Store past rewrites for personalization
- [ ] **Multi-language Support** — Translate + rewrite
- [ ] **Browser Extension** — One-click rewriting on any site
- [ ] **Advanced Personas** — Comedian, debater, influencer modes
- [ ] **Sentiment Analysis** — Detect emotional tone automatically
- [ ] **A/B Testing** — Compare multiple rewrites
- [ ] **Export Options** — Copy, share, or save rewrites

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License — feel free to use this project for personal or commercial purposes.

---

## 🙏 Acknowledgments

Built with:
- [LangChain](https://langchain.com) — LLM framework
- [LangGraph](https://github.com/langchain-ai/langgraph) — State machine workflows
- [FastAPI](https://fastapi.tiangolo.com) — Modern Python web framework
- [React](https://react.dev) — UI framework
- [Tailwind CSS](https://tailwindcss.com) — Styling
- [OpenAI](https://openai.com) — GPT models

---

## 💡 Vision

**Empower online users, creators, and brands to express themselves positively and effectively** — making social platforms more constructive, inclusive, and emotionally intelligent.

---

**Made with ❤️ and ✨ by the NLP Project Team**

*Transform your tone. Express smarter.*
