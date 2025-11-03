# 🚀 Deployment Guide - Vercel + Render

This guide will help you deploy the Social Media Rewriter project with:
- **Frontend** on Vercel
- **Backend** on Render

---

## 📋 Prerequisites

1. GitHub account
2. Vercel account (sign up at https://vercel.com)
3. Render account (sign up at https://render.com)
4. Your API keys ready:
   - Google Gemini API key
   - Reddit API credentials
   - YouTube API key

---

## 🔧 Step 1: Prepare Your Repository

### 1.1 Push to GitHub

```powershell
# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Prepare for deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 1.2 Add .gitignore

Make sure you have a `.gitignore` file to exclude sensitive data:

```
# Environment variables
.env
.env.local
backend/.env

# Dependencies
node_modules/
backend/__pycache__/
backend/venv/

# Build outputs
dist/
build/

# IDE
.vscode/
.idea/
```

---

## 🎨 Step 2: Deploy Frontend to Vercel

### 2.1 Deploy via Vercel Dashboard

1. Go to https://vercel.com/new
2. Click "Import Project"
3. Select your GitHub repository
4. Configure the project:
   - **Framework Preset**: Vite
   - **Root Directory**: `./` (leave as root)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### 2.2 Add Environment Variables

In Vercel dashboard → Settings → Environment Variables:

- **Variable Name**: `VITE_API_URL`
- **Value**: `https://your-backend-url.onrender.com` (you'll get this from Step 3)

### 2.3 Deploy

Click "Deploy" and wait for the build to complete.

---

## 🐍 Step 3: Deploy Backend to Render

### 3.1 Create a New Web Service

1. Go to https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `nlp-project-backend`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3.2 Add Environment Variables

In Render dashboard → Environment:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.12.0` |
| `GEMINI_API_KEY` | Your Gemini API key |
| `REDDIT_CLIENT_ID` | Your Reddit client ID |
| `REDDIT_CLIENT_SECRET` | Your Reddit client secret |
| `REDDIT_USER_AGENT` | `YourApp/1.0` |
| `YOUTUBE_API_KEY` | Your YouTube API key |

### 3.3 Deploy

1. Click "Create Web Service"
2. Wait for the deployment to complete (5-10 minutes)
3. Copy your backend URL: `https://your-backend-url.onrender.com`

---

## 🔄 Step 4: Update Frontend with Backend URL

### 4.1 Update Vercel Environment Variable

1. Go to Vercel dashboard → Your project → Settings → Environment Variables
2. Update `VITE_API_URL` with your Render backend URL:
   - `https://your-backend-url.onrender.com`
3. Redeploy your frontend (Vercel → Deployments → Redeploy)

---

## ✅ Step 5: Verify Deployment

### 5.1 Test Backend

Visit: `https://your-backend-url.onrender.com/docs`

You should see the FastAPI interactive documentation.

### 5.2 Test Frontend

Visit your Vercel URL: `https://your-project.vercel.app`

Test the features:
1. ✅ Fetch Reddit comments
2. ✅ Fetch YouTube comments
3. ✅ Rewrite comments with different tones
4. ✅ Check engagement predictions

---

## 🐛 Troubleshooting

### Frontend Issues

**Problem**: API calls fail with CORS errors
- **Solution**: Make sure your backend's CORS settings allow your Vercel domain
- In `backend/main.py`, verify `allow_origins=["*"]` is set

**Problem**: Environment variable not working
- **Solution**: 
  1. Check variable name starts with `VITE_`
  2. Redeploy after adding/changing variables
  3. Clear browser cache

### Backend Issues

**Problem**: Build fails on Render
- **Solution**: Check Python version matches requirements
- Verify all packages in `requirements.txt` are compatible

**Problem**: API returns 500 errors
- **Solution**: Check Render logs (Dashboard → Logs)
- Verify all environment variables are set correctly

**Problem**: Reddit/YouTube API fails
- **Solution**: 
  1. Verify API credentials are correct
  2. Check API quotas/limits
  3. Ensure credentials have proper permissions

---

## 🔐 Security Best Practices

1. ✅ Never commit `.env` files to GitHub
2. ✅ Use environment variables for all secrets
3. ✅ Rotate API keys regularly
4. ✅ Monitor API usage and set up alerts
5. ✅ Use HTTPS for all API calls

---

## 📊 Monitoring

### Vercel Analytics
- Go to Vercel dashboard → Analytics
- Monitor page views, performance, and errors

### Render Metrics
- Go to Render dashboard → Metrics
- Monitor CPU, Memory, and HTTP response times

---

## 🔄 Continuous Deployment

Both Vercel and Render automatically deploy when you push to GitHub:

```powershell
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Vercel and Render will auto-deploy
```

---

## 💰 Cost Considerations

### Vercel (Free Tier)
- ✅ Unlimited personal projects
- ✅ Automatic SSL certificates
- ✅ Global CDN
- ⚠️ 100GB bandwidth/month

### Render (Free Tier)
- ✅ 750 hours/month
- ✅ Automatic SSL
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ Cold start time: 30-60 seconds

**Tip**: For production, consider upgrading to paid plans for better performance.

---

## 📞 Support

If you encounter issues:

1. Check Vercel documentation: https://vercel.com/docs
2. Check Render documentation: https://render.com/docs
3. Review application logs in both dashboards
4. Verify environment variables are set correctly

---

## 🎉 You're Done!

Your Social Media Rewriter is now live on:
- **Frontend**: `https://your-project.vercel.app`
- **Backend**: `https://your-backend-url.onrender.com`

Share your project with the world! 🚀
