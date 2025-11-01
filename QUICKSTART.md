# 🚀 Quick Start Guide - AI Comment Rewriter with Gemini

## ✅ What's Working Now

Your project now has:
- ✅ **LangChain** integration (v0.3.13)
- ✅ **LangGraph** state machine (v0.2.60)
- ✅ **Google Gemini AI** (FREE API - gemini-2.0-flash-exp)
- ✅ **Sentiment Detection** with TextBlob
- ✅ **8 Tone Rewriting Modes**
- ✅ **FastAPI Backend** running on port 8000
- ✅ **React Frontend** with Tailwind CSS

---

## 🔑 Get Your FREE Gemini API Key

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

### Set Up Your API Key

Open `backend/.env` and replace:
```
GOOGLE_API_KEY=YOUR_KEY_HERE
```

With:
```
GOOGLE_API_KEY=AIzaSy... (your actual key)
```

**That's it!** Gemini is FREE and more generous than OpenAI!

---

## 🎮 How to Run

### Backend (Already Running!)
```powershell
cd backend
python main.py
```

Backend is now live at: **http://localhost:8000**

### Frontend
```powershell
npm run dev
```

Frontend will open at: **http://localhost:5173**

---

## 🧪 Test the API

### Check Health
```powershell
curl http://localhost:8000/health
```

### Test Rewriting (Mock Mode - works without API key)
```powershell
curl -X POST http://localhost:8000/rewrite -H "Content-Type: application/json" -d '{
  "comment": "Bruh this product is trash",
  "tone": "professional"
}'
```

### With Gemini API (after adding key)
Once you add your `GOOGLE_API_KEY`, restart the backend and the same request will use real AI!

---

## 🎨 LangGraph Workflow

Your backend uses a **4-node state machine**:

```
┌─────────────────┐
│ 1. Detect Tone  │  (TextBlob sentiment analysis)
└────────┬────────┘
         │
┌────────▼─────────┐
│ 2. Create Prompt │  (Build Gemini prompt with tone examples)
└────────┬─────────┘
         │
┌────────▼──────────┐
│ 3. Generate Text  │  (Call Gemini API or mock fallback)
└────────┬──────────┘
         │
┌────────▼──────────┐
│ 4. Explain Changes│  (Why words were changed)
└───────────────────┘
```

**See it in action:** `backend/main.py` lines 157-172

---

## 🎯 Available Tones

| Tone | Emoji | Example |
|------|-------|---------|
| Casual | 😊 | "Bruh this is trash" → "Hey, this isn't really my thing" |
| Professional | 💼 | "This sucks" → "I encountered some concerns" |
| Supportive | 🤗 | "You're wrong" → "I see your point! Here's another perspective..." |
| Sarcastic | 😏 | "Great idea" → "Oh wow, totally the best idea ever 🙄" |
| Respectful | 🙏 | "That's stupid" → "I respectfully disagree..." |
| Empathetic | 💙 | "Stop complaining" → "I understand this is frustrating" |
| Funny | 😂 | "Bug again" → "The app is having an existential crisis 😅" |
| Motivational | 🚀 | "I can't" → "You've got this! Keep pushing! 💪" |

---

## 📊 What Makes This Special

### 1. **Real AI with LangChain**
Not just templates - actual intelligent rewriting with:
- Context understanding
- Tone preservation
- Natural language generation

### 2. **LangGraph State Machine**
Professional workflow management:
- Modular nodes (easy to extend)
- State tracking
- Error handling

### 3. **Sentiment Analysis**
Detects if original comment is:
- Negative (-0.3 to -1.0)
- Neutral (-0.3 to 0.3)
- Positive (0.3 to 1.0)

### 4. **Explainability**
Shows **why** it changed certain words:
- "Removed harsh language"
- "Softened criticism"
- "Added context"

---

## 🔧 Next Steps

### Immediate (Do Now!)

1. **Add Gemini API Key** ⭐
   - Get it from https://makersuite.google.com/app/apikey
   - Paste into `backend/.env`
   - Restart backend

2. **Test with Real AI**
   - Try all 8 tones
   - Compare results with mock mode
   - See the explainability feature

### Quick Wins (This Weekend!)

3. **Add Copy Button** (30 mins)
   - One-click copy rewritten text
   - Toast notification: "Copied!"

4. **Save History** (1 hour)
   - localStorage for last 10 rewrites
   - "View History" sidebar

5. **Character Counter** (30 mins)
   - Show Twitter (280), LinkedIn (3000) limits
   - Red text when over limit

### Portfolio Enhancements

6. **Deploy Online** (2 hours)
   - Backend: Render.com (free tier)
   - Frontend: Vercel (free)
   - Share live demo link!

7. **Browser Extension** (4-6 hours)
   - Chrome extension that adds "Rewrite" button to Twitter/LinkedIn
   - Right-click menu integration
   - Instant portfolio booster! ⭐⭐⭐⭐⭐

---

## 🐛 Troubleshooting

### "Gemini Available: False"
**Problem:** API key not found  
**Fix:** Add `GOOGLE_API_KEY` to `backend/.env`

### "Module not found"
**Problem:** Missing dependencies  
**Fix:**
```powershell
cd backend
pip install -r requirements.txt
```

### Frontend won't connect
**Problem:** Backend not running  
**Fix:** Make sure backend is running on port 8000

### Rate Limit Error
**Problem:** Too many requests  
**Fix:** Gemini has generous free limits (60 requests/minute). Wait a minute or upgrade to paid tier.

---

## 📁 Project Structure

```
nlp-project/
├── backend/
│   ├── main.py               # LangChain + LangGraph + Gemini
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # Your API keys (gitignored)
│   └── .env.example          # Template
├── src/
│   ├── App.tsx               # React frontend
│   ├── main.tsx
│   └── index.css
├── IMPROVEMENTS.md           # 17 improvement ideas
├── README.md                 # Full documentation
└── QUICKSTART.md             # This file!
```

---

## 💡 Tips for Best Results

### Prompt Engineering
The system works best with:
- Clear, complete sentences
- Social media style (casual tone)
- 5-100 words (sweet spot)

### Tone Selection
- **Professional:** Work emails, LinkedIn
- **Casual:** Friends, Twitter
- **Empathetic:** Customer support
- **Funny:** Social media engagement

### Context Field (Optional)
Add context for better results:
```json
{
  "comment": "This doesn't work",
  "tone": "professional",
  "context": "Replying to a customer bug report"
}
```

---

## 🎓 Learning Resources

### LangChain
- Docs: https://python.langchain.com/
- Tutorials: https://python.langchain.com/docs/tutorials/

### LangGraph
- Docs: https://langchain-ai.github.io/langgraph/
- Examples: https://github.com/langchain-ai/langgraph/tree/main/examples

### Gemini
- Docs: https://ai.google.dev/tutorials/python_quickstart
- Models: https://ai.google.dev/models/gemini

---

## 🚀 Ready to Ship!

Your project is now production-ready with:
- ✅ Professional AI architecture
- ✅ State machine workflows
- ✅ Free, powerful AI model
- ✅ Clean, documented code

**Next:** Add your API key and start rewriting! 🎉

---

**Questions?** Check `IMPROVEMENTS.md` for 17 enhancement ideas!
