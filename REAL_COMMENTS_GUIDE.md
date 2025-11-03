# 🎯 Real Comments Integration Guide

## ✨ What's New?

You can now **fetch real comments** from Reddit and YouTube and rewrite them with AI!

## 🚀 How to Use

### 1. Start the Servers

**Terminal 1 - Backend:**
```powershell
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```powershell
npm run dev
```

### 2. Fetch Real Comments

#### 📱 From Reddit:
1. Enter a subreddit name (e.g., "AskReddit", "technology", "funny")
2. Click "Fetch from Reddit"
3. Browse through real comments from that subreddit
4. Click any comment to use it for rewriting

#### 🎥 From YouTube:
1. **Option A:** Leave video ID empty to get comments from **trending videos**
2. **Option B:** Enter a specific video ID (e.g., "dQw4w9WgXcQ" from URL `youtube.com/watch?v=dQw4w9WgXcQ`)
3. Click "Fetch from YouTube"
4. Browse through real comments
5. Click any comment to use it for rewriting

### 3. Rewrite Real Comments

1. After clicking a comment, it automatically fills the "Original Comment" box
2. Select your desired tone (Professional, Casual, Funny, etc.)
3. Select target platform (Twitter, LinkedIn, Instagram, etc.)
4. Click "Rewrite with AI"
5. Get AI-rewritten version with hashtags and engagement predictions!

## 📊 New API Endpoints

### Fetch Reddit Comments
```
GET /api/comments/reddit?subreddit=AskReddit&limit=10
```

**Response:**
```json
{
  "platform": "reddit",
  "subreddit": "AskReddit",
  "comments": [
    {
      "id": "abc123",
      "text": "This is a real comment",
      "score": 150,
      "author": "username",
      "post_title": "What's your favorite movie?"
    }
  ],
  "count": 10
}
```

### Fetch YouTube Comments
```
GET /api/comments/youtube?video_id=dQw4w9WgXcQ&limit=10
```

**Response:**
```json
{
  "platform": "youtube",
  "video_id": "dQw4w9WgXcQ",
  "comments": [
    {
      "id": "xyz789",
      "text": "Great video!",
      "like_count": 50,
      "author_display_name": "John Doe"
    }
  ],
  "count": 10
}
```

### Fetch Comments from Trending Videos
```
GET /api/comments/youtube/trending?limit=10
```

## 🎨 UI Features

### Comment Display:
- **Author name** with 👤 icon
- **Score/Likes** with ⬆️ or ❤️ icons
- **Post/Video title** for context
- **Click to use** - Instantly loads comment for rewriting
- **Scrollable list** - Browse through multiple comments
- **Numbered items** - Easy to track

### Visual Indicators:
- 🤖 Reddit icon
- ▶️ YouTube icon
- ⏳ Loading spinner while fetching
- ✅ Success highlights when hovering

## 💡 Use Cases

### 1. **Social Media Manager**
- Fetch comments from your brand's social media
- Rewrite negative comments professionally
- Turn casual comments into marketing content

### 2. **Content Creator**
- Get inspiration from trending comments
- Rewrite comments for different platforms
- Create engaging responses

### 3. **Marketing Team**
- Analyze real audience sentiment
- Transform user feedback into testimonials
- Optimize messaging for different platforms

### 4. **Research & Analysis**
- Study real communication patterns
- Test tone transformations on actual data
- Compare platform-specific language styles

## 🔧 Backend Implementation

### New Endpoints Added:
1. `/api/comments/reddit` - Fetch Reddit comments
2. `/api/comments/youtube` - Fetch YouTube comments by video ID
3. `/api/comments/youtube/trending` - Fetch from trending videos
4. `/api/rewrite/batch` - Rewrite multiple comments at once

### Updated Reddit Client:
- Enhanced `get_top_comments()` to work with subreddits
- Automatically fetches from multiple hot posts
- Returns formatted comment data with context

### YouTube Integration:
- Fetch comments from specific videos
- Fetch comments from trending videos
- Includes video titles for context

## 📝 Example Workflow

```
1. Open http://localhost:5173
2. Choose "Fetch from Reddit"
3. Enter "technology"
4. Click "Fetch from Reddit"
5. See 10 real comments from r/technology
6. Click a comment about AI
7. Select "Professional" tone
8. Select "LinkedIn" platform
9. Click "Rewrite with AI"
10. Get LinkedIn-optimized version with:
    - Professional language
    - Relevant hashtags (#AI #Technology)
    - Engagement predictions
    - Character count for LinkedIn
```

## 🎯 Next Steps

1. **Test with different subreddits:**
   - r/AskReddit (questions & discussions)
   - r/technology (tech news)
   - r/funny (humor)
   - r/programming (technical)

2. **Test with YouTube:**
   - Leave video ID empty for trending
   - Or use specific video IDs

3. **Try different tones:**
   - Rewrite casual Reddit comments professionally
   - Make formal YouTube comments more friendly
   - Add humor to serious comments

4. **Experiment with platforms:**
   - See how the same comment changes for Twitter vs LinkedIn
   - Compare Instagram optimization vs Facebook

## 🚨 Troubleshooting

**No comments showing?**
- Make sure backend is running (`python main.py`)
- Check Reddit API credentials in `.env`
- Try a different subreddit (some may be private)

**YouTube not working?**
- Verify `YOUTUBE_API_KEY` in `.env`
- Check video ID is correct (11 characters)
- Try trending option instead

**Comments won't load into textarea?**
- Click directly on the comment card
- Scroll to top to see the loaded comment
- Try a different comment

## 🎉 Features Summary

✅ Fetch real Reddit comments from any subreddit
✅ Fetch real YouTube comments from any video
✅ Fetch from trending YouTube videos
✅ One-click to use any comment
✅ Visual comment browser with metadata
✅ Author, score, and context information
✅ Seamless integration with rewriter
✅ Works with all 7 platforms
✅ Works with all 8 tones

**Enjoy rewriting real social media comments with AI! 🚀**
