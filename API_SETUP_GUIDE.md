# 🔑 API Setup Guide - Step by Step

## 📦 Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- ✅ **praw** - Reddit API
- ✅ **tweepy** - Twitter API v2  
- ✅ **google-api-python-client** - YouTube API
- ✅ **newsapi-python** - News API
- ✅ **beautifulsoup4** - Web scraping
- ✅ **requests** - HTTP client

---

## 🔑 Step 2: Get FREE API Keys (30 minutes total)

### 1. Reddit API (5 minutes) ⭐ EASIEST

**Why Reddit?** Best for fetching real comments and posts to test your rewriter!

1. Visit: https://www.reddit.com/prefs/apps
2. Scroll down, click **"Create App"** or **"Create Another App"**
3. Fill in the form:
   ```
   Name: Social Media Rewriter
   Type: ☑️ script
   Description: AI content optimizer
   About URL: (leave blank)
   Redirect URI: http://localhost:8080
   ```
4. Click **"Create app"**
5. You'll see your credentials:
   ```
   Client ID: (14 characters, under "personal use script")
   Secret: (27 characters, next to "secret")
   ```

**Add to `.env`:**
```bash
REDDIT_CLIENT_ID=your_14_char_client_id
REDDIT_CLIENT_SECRET=your_27_char_secret
```

---

### 2. YouTube Data API (5 minutes) ⭐ RECOMMENDED

**Why YouTube?** Fetch video comments and trending videos!

1. Visit: https://console.cloud.google.com/
2. Click **"Select a project"** → **"New Project"**
   - Name: "Social Media Rewriter"
   - Click **"Create"**
3. Wait 10 seconds, then select your new project
4. Click **☰ Menu** → **"APIs & Services"** → **"Library"**
5. Search for **"YouTube Data API v3"**
6. Click on it → Click **"Enable"**
7. Go to **"Credentials"** (left sidebar)
8. Click **"Create Credentials"** → **"API Key"**
9. Copy your API key (starts with `AIza...`)

**Add to `.env`:**
```bash
YOUTUBE_API_KEY=AIzaSy...your_key_here
```

**Free Quota:** 10,000 requests/day (more than enough!)

---

### 3. Twitter API v2 (10 minutes) ⚠️ Requires Approval

**Why Twitter?** Search tweets and analyze engagement!

1. Visit: https://developer.twitter.com/en/portal/dashboard
2. Sign up for **Developer Account** (Free - Essential access)
3. Answer questions:
   - Purpose: **"Exploring the API"**
   - Use case: **"Building a social media content optimizer"**
4. Verify your email
5. Create a **Project**:
   - Name: "Social Media Rewriter"
   - Environment: Development
6. Create an **App** within the project
7. Go to **"Keys and tokens"** tab
8. Click **"Generate"** under **Bearer Token**
9. **IMPORTANT:** Copy and save immediately (shown only once!)

**Add to `.env`:**
```bash
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAABear...your_token
```

**Note:** Twitter may take 1-2 hours to approve your developer account.

---

### 4. News API (2 minutes) ⭐ EASIEST

**Why News API?** Show trending headlines related to topics!

1. Visit: https://newsapi.org/register
2. Fill in the form:
   ```
   Name: Your Name
   Email: your@email.com
   ```
3. Check your email for API key
4. Copy the key (32 characters)

**Add to `.env`:**
```bash
NEWS_API_KEY=your_32_char_api_key_here
```

**Free Quota:** 100 requests/day

---

## 🛠️ Step 3: Configure .env File

Copy the example file:
```bash
cd backend
cp .env.example .env
```

Then edit `.env` and add your keys:

```bash
# AI Model
GOOGLE_API_KEY=AIzaSyBQF0aQ0gto37LUob1EzuneHwVMNqEJcME
GEMINI_MODEL=gemini-2.5-flash-lite

# Social Media APIs
REDDIT_CLIENT_ID=abc123xyz456
REDDIT_CLIENT_SECRET=abcd1234efgh5678ijkl9012
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAABearerTokenHere
YOUTUBE_API_KEY=AIzaSyABC123XYZ789
NEWS_API_KEY=1234567890abcdef1234567890abcdef
```

---

## 🧪 Step 4: Test the APIs

Start the backend:
```bash
cd backend
python main.py
```

You should see:
```
✅ Reddit API connected
✅ YouTube API connected
✅ Twitter API connected
✅ News API connected
```

If you see ⚠️ warnings, that API key is missing or incorrect.

---

## 🎯 Step 5: Test Each Endpoint

### Test Reddit:
```bash
curl http://localhost:8000/api/reddit/trending?subreddit=AskReddit&limit=5
```

### Test YouTube:
```bash
curl http://localhost:8000/api/youtube/trending?region=US&limit=5
```

### Test Twitter:
```bash
curl "http://localhost:8000/api/twitter/search?query=AI&limit=5"
```

### Test News:
```bash
curl "http://localhost:8000/api/news/headlines?category=technology"
```

### Test API Status:
```bash
curl http://localhost:8000/api/status
```

---

## 🚀 What You Can Do Now

### 1. **Fetch Real Reddit Posts**
```python
# Frontend: Click "Fetch from Reddit"
# Backend fetches actual posts from r/AskReddit
# User selects a post → auto-fills comment box
# Rewrites it with AI!
```

### 2. **Show Trending Topics**
```javascript
// Display trending content in sidebar:
- Top Reddit posts (r/popular)
- YouTube trending videos
- Twitter trending topics
- Latest tech news
```

### 3. **Analyze Real Comments**
```python
# Fetch YouTube video comments
# Let user select one
# Rewrite it for different platform
# Compare engagement predictions
```

### 4. **Smart Hashtag Suggestions**
```python
# Instead of generic hashtags:
❌ #QualityVibes

# Use real trending hashtags:
✅ #AITrends (scraped, 45K posts)
✅ #TechNews (API, 23K tweets)
```

---

## 🎓 Priority Setup Recommendations

### **Start with these 2 (10 minutes):**
1. ✅ **Reddit API** - Easiest, most useful
2. ✅ **YouTube API** - Second easiest

### **Add later (optional):**
3. ⏳ **Twitter API** - Requires approval (1-2 hours wait)
4. ⏳ **News API** - Nice to have, not critical

---

## 🐛 Troubleshooting

### **"Reddit API not connected"**
- Check `REDDIT_CLIENT_ID` is correct (14 chars)
- Check `REDDIT_CLIENT_SECRET` is correct (27 chars)
- Make sure no quotes around values in .env

### **"YouTube API quota exceeded"**
- Free tier: 10,000 units/day
- Each video list = 100 units
- Reset daily at midnight PST

### **"Twitter Bearer Token invalid"**
- Token must start with `AAAAAAAAAAAAA...`
- Make sure you copied the entire token
- Check for extra spaces

### **"ImportError: No module named 'praw'"**
```bash
pip install -r requirements.txt
```

---

## 📊 API Limits (Free Tier)

| API | Free Limit | Enough For |
|-----|-----------|-----------|
| Reddit | Unlimited (60 req/min) | ✅ Production ready |
| YouTube | 10,000 units/day | ✅ ~100 video requests |
| Twitter | 500K tweets/month | ✅ More than enough |
| News | 100 req/day | ⚠️ Development only |

---

## 🎉 Next Steps

Once APIs are configured:

1. **Test New Endpoints**
   ```bash
   python quick_test.py  # Will test all APIs
   ```

2. **Update Frontend**
   - Add "Fetch from Reddit" button
   - Show trending topics sidebar
   - Display real engagement metrics

3. **Deploy Online**
   - Add API keys to Render environment variables
   - Test in production

---

## 💡 Pro Tips

1. **Reddit is most useful** - Start here first!
2. **YouTube has best free limits** - 10K requests/day
3. **Twitter requires approval** - Apply early, takes 1-2 hours
4. **News API is limited** - Use sparingly (100/day)
5. **Scraping is fallback** - Works without API keys

---

**Your APIs are ready! 🚀**

Now you can fetch **real social media data** to make your rewriter even more powerful!
