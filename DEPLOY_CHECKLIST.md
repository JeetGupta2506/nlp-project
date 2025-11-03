# 🚀 Quick Deploy Checklist

## ✅ Pre-Deployment

- [ ] Push code to GitHub
- [ ] Have all API keys ready:
  - [ ] Gemini API Key
  - [ ] Reddit Client ID & Secret
  - [ ] YouTube API Key
- [ ] Test locally to ensure everything works

## 🎨 Vercel (Frontend)

1. **Import Project**
   - Go to https://vercel.com/new
   - Connect GitHub repo
   
2. **Settings**
   - Framework: Vite
   - Build: `npm run build`
   - Output: `dist`
   
3. **Environment Variable**
   ```
   VITE_API_URL = https://your-backend.onrender.com
   ```
   (Add this AFTER deploying backend)

4. **Deploy** → Wait → Get URL

## 🐍 Render (Backend)

1. **Create Web Service**
   - Go to https://dashboard.render.com
   - Connect GitHub repo
   
2. **Settings**
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   
3. **Environment Variables**
   ```
   PYTHON_VERSION = 3.12.0
   GEMINI_API_KEY = your_key_here
   REDDIT_CLIENT_ID = your_id_here
   REDDIT_CLIENT_SECRET = your_secret_here
   REDDIT_USER_AGENT = YourApp/1.0
   YOUTUBE_API_KEY = your_key_here
   ```

4. **Deploy** → Wait 5-10 min → Copy URL

## 🔄 Connect Them

1. Copy Render backend URL
2. Go to Vercel → Settings → Environment Variables
3. Update `VITE_API_URL` with backend URL
4. Redeploy Vercel app

## ✨ Test

Visit your Vercel URL and test:
- [ ] Reddit comments fetch
- [ ] YouTube comments fetch
- [ ] Comment rewriting
- [ ] Tone selection
- [ ] Copy button

## 📌 Your URLs

**Frontend (Vercel)**: `https://______.vercel.app`

**Backend (Render)**: `https://______.onrender.com`

**Backend API Docs**: `https://______.onrender.com/docs`

---

**Note**: Render free tier spins down after 15 minutes. First request may take 30-60 seconds to wake up.
