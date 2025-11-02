import os
# Set environment variables BEFORE any imports to prevent transformers issues
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Literal, Annotated, TypedDict
import uvicorn
from datetime import datetime
from dotenv import load_dotenv

# LangChain & LangGraph imports
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema import HumanMessage, SystemMessage
    from langgraph.graph import StateGraph, END
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    print(f"⚠️  LangChain not installed - {e}")
    print("   Run: pip install -r requirements.txt")

load_dotenv()

# Import API clients and scrapers
try:
    from api_clients import social_apis
    from scrapers import web_scrapers
    API_CLIENTS_AVAILABLE = True
except ImportError as e:
    API_CLIENTS_AVAILABLE = False
    print(f"⚠️  API clients not available - {e}")
    social_apis = None
    web_scrapers = None

app = FastAPI(
    title="AI Comment Rewriter API",
    description="Transform your tone with Gemini AI + Real Social Media Data",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class RewriteRequest(BaseModel):
    comment: str
    tone: Literal["casual", "professional", "supportive", "sarcastic", "respectful", "empathetic", "funny", "motivational"]
    context: Optional[str] = None
    persona: Optional[str] = None
    platform: Optional[Literal["twitter", "linkedin", "instagram", "facebook", "reddit", "tiktok", "youtube"]] = None

class RewriteResponse(BaseModel):
    original: str
    rewritten: str
    tone: str
    persona: Optional[str]
    explanation: List[str]
    processing_time: float
    model_used: str
    sentiment_shift: Optional[Dict[str, float]] = None
    platform_info: Optional[Dict[str, Any]] = None
    suggested_hashtags: Optional[List[str]] = None
    engagement_prediction: Optional[Dict[str, Any]] = None

class ToneInfo(BaseModel):
    name: str
    description: str
    example_input: str
    example_output: str
    emoji: str

# Tone definitions
TONE_DEFINITIONS = {
    "casual": {
        "name": "Casual",
        "description": "Friendly and relaxed tone",
        "emoji": "",
        "example_input": "That movie sucked",
        "example_output": "Honestly, the movie wasnt really my thing"
    },
    "professional": {
        "name": "Professional",
        "description": "Business-appropriate communication",
        "emoji": "",
        "example_input": "That product is trash",
        "example_output": "I encountered some quality concerns with this product"
    },
    "supportive": {
        "name": "Supportive",
        "description": "Encouraging and uplifting",
        "emoji": "",
        "example_input": "Youre doing it wrong",
        "example_output": "I see what youre trying to do! Heres a suggestion that might help..."
    },
    "sarcastic": {
        "name": "Sarcastic",
        "description": "Witty and ironic",
        "emoji": "",
        "example_input": "This is the best idea ever",
        "example_output": "Oh wow, this is totally the best idea Ive ever heard"
    },
    "respectful": {
        "name": "Respectful",
        "description": "Polite and considerate",
        "emoji": "",
        "example_input": "Youre completely wrong",
        "example_output": "I respectfully disagree. Heres my perspective..."
    },
    "empathetic": {
        "name": "Empathetic",
        "description": "Understanding and compassionate",
        "emoji": "",
        "example_input": "Stop complaining",
        "example_output": "I understand this must be frustrating for you"
    },
    "funny": {
        "name": "Funny",
        "description": "Humorous and entertaining",
        "emoji": "",
        "example_input": "This update broke everything",
        "example_output": "This update just gave my app a surprise existential crisis"
    },
    "motivational": {
        "name": "Motivational",
        "description": "Inspiring and energizing",
        "emoji": "",
        "example_input": "I cant do this",
        "example_output": "Youve got this! Every expert was once a beginner. Keep pushing!"
    }
}

# LangGraph State
class RewriteState(TypedDict):
    comment: str
    tone: str
    context: Optional[str]
    persona: Optional[str]
    platform: Optional[str]
    detected_sentiment: Optional[str]
    system_prompt: Optional[str]
    user_prompt: Optional[str]
    rewritten: Optional[str]
    explanation: List[str]
    model_used: str
    platform_info: Optional[Dict[str, Any]]
    suggested_hashtags: Optional[List[str]]
    engagement_prediction: Optional[Dict[str, Any]]

# Social Media Platform Configurations
PLATFORM_CONFIGS = {
    "twitter": {
        "name": "Twitter/X",
        "char_limit": 280,
        "optimal_length": "71-100 characters",
        "hashtag_limit": 2,
        "best_tones": ["casual", "funny", "sarcastic"],
        "emoji_friendly": True,
        "thread_capable": True
    },
    "linkedin": {
        "name": "LinkedIn",
        "char_limit": 3000,
        "optimal_length": "150-300 characters",
        "hashtag_limit": 5,
        "best_tones": ["professional", "motivational", "respectful"],
        "emoji_friendly": False,
        "thread_capable": False
    },
    "instagram": {
        "name": "Instagram",
        "char_limit": 2200,
        "optimal_length": "138-150 characters",
        "hashtag_limit": 30,
        "best_tones": ["casual", "funny", "motivational"],
        "emoji_friendly": True,
        "thread_capable": False
    },
    "facebook": {
        "name": "Facebook",
        "char_limit": 63206,
        "optimal_length": "40-80 characters",
        "hashtag_limit": 3,
        "best_tones": ["casual", "supportive", "empathetic"],
        "emoji_friendly": True,
        "thread_capable": False
    },
    "reddit": {
        "name": "Reddit",
        "char_limit": 10000,
        "optimal_length": "200-500 characters",
        "hashtag_limit": 0,
        "best_tones": ["casual", "respectful", "funny"],
        "emoji_friendly": False,
        "thread_capable": True
    },
    "tiktok": {
        "name": "TikTok",
        "char_limit": 150,
        "optimal_length": "100-150 characters",
        "hashtag_limit": 5,
        "best_tones": ["funny", "casual", "motivational"],
        "emoji_friendly": True,
        "thread_capable": False
    },
    "youtube": {
        "name": "YouTube",
        "char_limit": 10000,
        "optimal_length": "100-200 characters",
        "hashtag_limit": 15,
        "best_tones": ["supportive", "funny", "respectful"],
        "emoji_friendly": True,
        "thread_capable": False
    }
}

def get_gemini_llm():
    if not LANGCHAIN_AVAILABLE:
        return None
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Warning: GOOGLE_API_KEY not found")
        return None
    
    try:
        return ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp"),
            google_api_key=api_key,
            temperature=0.7
        )
    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        return None

def generate_hashtags(comment: str, platform: str, tone: str) -> List[str]:
    """Generate platform-appropriate hashtags"""
    if not platform or platform == "reddit":
        return []
    
    config = PLATFORM_CONFIGS.get(platform, {})
    limit = config.get("hashtag_limit", 3)
    
    # Extract keywords from comment
    words = comment.lower().split()
    keywords = [w.strip('.,!?') for w in words if len(w) > 5][:3]
    
    # Platform-specific hashtag strategies
    hashtag_templates = {
        "twitter": ["#{}Vibes", "#SocialMedia", "#{}Community"],
        "linkedin": ["#{}Insights", "#Professional{}", "#Leadership"],
        "instagram": ["#InstaDaily", "#{}Life", "#{}Goals"],
        "facebook": ["#{}Talk", "#Community", "#Connect"],
        "tiktok": ["#FYP", "#Viral{}", "#{}TikTok"],
        "youtube": ["#{}Content", "#Subscribe", "#YouTubeCommunity"]
    }
    
    templates = hashtag_templates.get(platform, ["#{}"])
    hashtags = []
    
    for keyword in keywords[:limit]:
        for template in templates:
            if len(hashtags) >= limit:
                break
            tag = template.format(keyword.capitalize())
            if tag not in hashtags:
                hashtags.append(tag)
    
    return hashtags[:limit]

def predict_engagement(comment: str, tone: str, platform: str) -> Dict[str, Any]:
    """Predict engagement metrics based on comment characteristics"""
    if not platform:
        return {}
    
    config = PLATFORM_CONFIGS.get(platform, {})
    comment_len = len(comment)
    
    # Simple heuristic-based engagement prediction
    base_score = 50  # baseline
    
    # Length optimization
    if platform == "twitter" and 71 <= comment_len <= 100:
        base_score += 20
    elif platform == "linkedin" and 150 <= comment_len <= 300:
        base_score += 15
    
    # Tone matching
    if tone in config.get("best_tones", []):
        base_score += 15
    
    # Emoji bonus
    emoji_count = sum(1 for c in comment if ord(c) > 127000)
    if emoji_count > 0 and config.get("emoji_friendly"):
        base_score += 10
    
    # Question bonus (drives engagement)
    if "?" in comment:
        base_score += 10
    
    virality_score = min(100, base_score)
    
    return {
        "virality_score": virality_score,
        "predicted_likes": int(virality_score * 1.5),
        "predicted_shares": int(virality_score * 0.5),
        "predicted_comments": int(virality_score * 0.3),
        "optimal_post_time": "Best time: 9-11 AM or 7-9 PM (local time)",
        "engagement_level": "High" if virality_score > 70 else "Medium" if virality_score > 40 else "Low"
    }

def optimize_for_platform(comment: str, platform: str) -> str:
    """Optimize comment for specific platform"""
    if not platform:
        return comment
    
    config = PLATFORM_CONFIGS.get(platform, {})
    char_limit = config.get("char_limit", 5000)
    
    # Truncate if too long
    if len(comment) > char_limit:
        comment = comment[:char_limit-3] + "..."
    
    return comment

def detect_tone_node(state: RewriteState) -> RewriteState:
    try:
        from textblob import TextBlob
        blob = TextBlob(state["comment"])
        polarity = blob.sentiment.polarity
        
        if polarity < -0.3:
            state["detected_sentiment"] = "negative"
        elif polarity > 0.3:
            state["detected_sentiment"] = "positive"
        else:
            state["detected_sentiment"] = "neutral"
    except:
        state["detected_sentiment"] = "neutral"
    
    return state

def create_prompt_node(state: RewriteState) -> RewriteState:
    tone_info = TONE_DEFINITIONS.get(state["tone"], TONE_DEFINITIONS["casual"])
    
    system_prompt = f"""You are an expert at rewriting social media comments to match specific tones.

TARGET TONE: {tone_info["name"]} - {tone_info["description"]}

EXAMPLE:
Input: "{tone_info["example_input"]}"
Output: "{tone_info["example_output"]}"

RULES:
1. Keep the core message intact
2. Match the {tone_info["name"]} tone precisely
3. Be natural and authentic
4. Keep it concise (social media appropriate)
5. Return ONLY the rewritten comment without quotes or extra text"""

    context_str = f"\\nCONTEXT: {state.get('context')}" if state.get("context") else ""
    persona_str = f"\\nWrite in the style of: {state.get('persona')}" if state.get("persona") else ""
    
    user_prompt = f"""Rewrite this comment in a {tone_info["name"]} tone:{context_str}{persona_str}

Original comment: {state["comment"]}

Rewritten comment:"""
    
    state["system_prompt"] = system_prompt
    state["user_prompt"] = user_prompt
    return state

def generate_rewrite_node(state: RewriteState) -> RewriteState:
    llm = get_gemini_llm()
    
    if llm is None:
        state["rewritten"] = mock_rewrite(state["comment"], state["tone"])
        state["model_used"] = "mock-fallback"
        return state
    
    try:
        messages = [
            SystemMessage(content=state["system_prompt"]),
            HumanMessage(content=state["user_prompt"])
        ]
        response = llm.invoke(messages)
        state["rewritten"] = response.content.strip().strip('"').strip("'")
        state["model_used"] = "gemini-2.0-flash-exp"
    except Exception as e:
        print(f"Gemini error: {e}")
        state["rewritten"] = mock_rewrite(state["comment"], state["tone"])
        state["model_used"] = "mock-error-fallback"
    
    return state

def explain_changes_node(state: RewriteState) -> RewriteState:
    explanations = []
    original = state["comment"].lower()
    rewritten = state["rewritten"].lower()
    tone = state["tone"]
    
    if any(word in original for word in ["trash", "suck", "terrible", "awful"]):
        explanations.append("Removed harsh language for constructive tone")
    if "wrong" in original or "stupid" in original:
        explanations.append("Softened criticism to maintain respect")
    if len(rewritten) > len(original) * 1.3:
        explanations.append("Added context and clarity")
    if state.get("detected_sentiment") == "negative" and tone in ["supportive", "empathetic"]:
        explanations.append(f"Shifted from negative to {tone} sentiment")
    
    if not explanations:
        explanations.append(f"Adjusted phrasing to match {tone} tone")
    
    state["explanation"] = explanations
    return state

def platform_optimization_node(state: RewriteState) -> RewriteState:
    """Optimize for specific social media platform"""
    platform = state.get("platform")
    
    if platform:
        # Optimize length
        state["rewritten"] = optimize_for_platform(state["rewritten"], platform)
        
        # Add platform info
        state["platform_info"] = {
            **PLATFORM_CONFIGS.get(platform, {}),
            "current_length": len(state["rewritten"]),
            "within_limit": len(state["rewritten"]) <= PLATFORM_CONFIGS.get(platform, {}).get("char_limit", 5000)
        }
        
        # Generate hashtags
        state["suggested_hashtags"] = generate_hashtags(
            state["rewritten"], 
            platform, 
            state["tone"]
        )
        
        # Predict engagement
        state["engagement_prediction"] = predict_engagement(
            state["rewritten"],
            state["tone"],
            platform
        )
    
    return state

def create_rewrite_workflow():
    workflow = StateGraph(RewriteState)
    
    workflow.add_node("detect_tone", detect_tone_node)
    workflow.add_node("create_prompt", create_prompt_node)
    workflow.add_node("generate_rewrite", generate_rewrite_node)
    workflow.add_node("explain_changes", explain_changes_node)
    workflow.add_node("platform_optimization", platform_optimization_node)
    
    workflow.set_entry_point("detect_tone")
    workflow.add_edge("detect_tone", "create_prompt")
    workflow.add_edge("create_prompt", "generate_rewrite")
    workflow.add_edge("generate_rewrite", "explain_changes")
    workflow.add_edge("explain_changes", "platform_optimization")
    workflow.add_edge("platform_optimization", END)
    
    return workflow.compile()

def mock_rewrite(comment: str, tone: str) -> str:
    templates = {
        "casual": lambda c: f"Hey, {c.lower().rstrip('!.')}",
        "professional": lambda c: f"I would like to note that {c.lower().rstrip('!.')}.",
        "supportive": lambda c: f"I hear you! {c} Youre doing great!",
        "sarcastic": lambda c: f"Oh wow, {c.lower().rstrip('!.')} totally",
        "respectful": lambda c: f"I respectfully share that {c.lower().rstrip('!.')}.",
        "empathetic": lambda c: f"I understand where youre coming from. {c}",
        "funny": lambda c: f"{c} (but make it meme-worthy)",
        "motivational": lambda c: f"{c} Youve got this! Keep pushing!"
    }
    return templates.get(tone, lambda c: c)(comment)

rewrite_workflow = create_rewrite_workflow() if LANGCHAIN_AVAILABLE else None

@app.get("/")
async def root():
    return {
        "message": "AI Comment Rewriter API - Powered by Gemini",
        "version": "2.0.0",
        "status": "running",
        "langchain_available": LANGCHAIN_AVAILABLE,
        "gemini_available": get_gemini_llm() is not None,
        "endpoints": {
            "rewrite": "/rewrite",
            "tones": "/tones",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "AI Comment Rewriter API",
        "ai_engine": "Google Gemini",
        "langchain": LANGCHAIN_AVAILABLE,
        "gemini_configured": get_gemini_llm() is not None
    }

@app.get("/tones")
async def get_tones() -> List[ToneInfo]:
    return [
        ToneInfo(
            name=td["name"],
            description=td["description"],
            example_input=td["example_input"],
            example_output=td["example_output"],
            emoji=td["emoji"]
        )
        for td in TONE_DEFINITIONS.values()
    ]

@app.get("/platforms")
async def get_platforms():
    """Get all supported social media platforms with their configurations"""
    return {
        platform: {
            **config,
            "id": platform
        }
        for platform, config in PLATFORM_CONFIGS.items()
    }

@app.post("/rewrite", response_model=RewriteResponse)
async def rewrite_comment(request: RewriteRequest):
    start_time = datetime.now()
    
    if not request.comment.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")
    
    try:
        if rewrite_workflow and LANGCHAIN_AVAILABLE:
            initial_state: RewriteState = {
                "comment": request.comment,
                "tone": request.tone,
                "context": request.context,
                "persona": request.persona,
                "platform": request.platform,
                "detected_sentiment": None,
                "system_prompt": None,
                "user_prompt": None,
                "rewritten": None,
                "explanation": [],
                "model_used": "unknown",
                "platform_info": None,
                "suggested_hashtags": None,
                "engagement_prediction": None
            }
            
            result = rewrite_workflow.invoke(initial_state)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return RewriteResponse(
                original=request.comment,
                rewritten=result["rewritten"],
                tone=request.tone,
                persona=request.persona,
                explanation=result["explanation"],
                processing_time=processing_time,
                model_used=result["model_used"],
                platform_info=result.get("platform_info"),
                suggested_hashtags=result.get("suggested_hashtags"),
                engagement_prediction=result.get("engagement_prediction")
            )
        else:
            rewritten = mock_rewrite(request.comment, request.tone)
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return RewriteResponse(
                original=request.comment,
                rewritten=rewritten,
                tone=request.tone,
                persona=request.persona,
                explanation=[f"Adjusted phrasing to match {request.tone} tone (mock mode)"],
                processing_time=processing_time,
                model_used="mock"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rewriting failed: {str(e)}")

# ============================================================================
# NEW ENDPOINTS: REAL API & WEB SCRAPING
# ============================================================================

@app.get("/api/status")
async def get_api_status():
    """Get status of all connected APIs"""
    if not API_CLIENTS_AVAILABLE or social_apis is None:
        return {
            "apis_available": False,
            "message": "API clients not installed. Run: pip install praw tweepy google-api-python-client newsapi-python"
        }
    
    return {
        "apis_available": True,
        "status": social_apis.get_status(),
        "scrapers_available": web_scrapers is not None
    }

@app.get("/api/reddit/trending")
async def get_reddit_trending(subreddit: str = "popular", limit: int = 10):
    """Fetch trending posts from Reddit"""
    if not API_CLIENTS_AVAILABLE or not social_apis:
        # Fallback to scraping
        if web_scrapers:
            posts = web_scrapers.fetch_reddit_content(subreddit, limit)
            return {"source": "scraper", "posts": posts}
        return {"error": "APIs and scrapers not available"}
    
    if social_apis.reddit.available:
        posts = social_apis.reddit.get_trending_posts(subreddit, limit)
        return {"source": "api", "posts": posts}
    else:
        # Fallback to scraper
        if web_scrapers:
            posts = web_scrapers.fetch_reddit_content(subreddit, limit)
            return {"source": "scraper", "posts": posts}
        return {"error": "Reddit API and scraper not available"}

@app.get("/api/youtube/trending")
async def get_youtube_trending(region: str = "US", limit: int = 10):
    """Fetch trending YouTube videos"""
    if not API_CLIENTS_AVAILABLE or not social_apis or not social_apis.youtube.available:
        return {"error": "YouTube API not available. Add YOUTUBE_API_KEY to .env"}
    
    videos = social_apis.youtube.get_trending_videos(region, limit)
    return {"source": "api", "videos": videos}

@app.get("/api/youtube/comments/{video_id}")
async def get_youtube_comments(video_id: str, limit: int = 20):
    """Fetch comments from a YouTube video"""
    if not API_CLIENTS_AVAILABLE or not social_apis or not social_apis.youtube.available:
        return {"error": "YouTube API not available"}
    
    comments = social_apis.youtube.get_video_comments(video_id, limit)
    return {"source": "api", "comments": comments}

@app.get("/api/twitter/search")
async def search_twitter(query: str, limit: int = 10):
    """Search recent tweets"""
    if not API_CLIENTS_AVAILABLE or not social_apis or not social_apis.twitter.available:
        return {"error": "Twitter API not available. Add TWITTER_BEARER_TOKEN to .env"}
    
    tweets = social_apis.twitter.search_recent_tweets(query, limit)
    return {"source": "api", "tweets": tweets}

@app.get("/api/news/headlines")
async def get_news_headlines(category: str = "technology", country: str = "us"):
    """Fetch top news headlines"""
    if not API_CLIENTS_AVAILABLE or not social_apis or not social_apis.news.available:
        return {"error": "News API not available. Add NEWS_API_KEY to .env"}
    
    articles = social_apis.news.get_top_headlines(category, country)
    return {"source": "api", "articles": articles}

@app.get("/api/trending/hashtags/{platform}")
async def get_trending_hashtags(platform: str):
    """Fetch trending hashtags for a specific platform"""
    if not API_CLIENTS_AVAILABLE or not web_scrapers:
        return {"error": "Scrapers not available"}
    
    hashtags = web_scrapers.fetch_trending_hashtags(platform)
    return {"platform": platform, "hashtags": hashtags, "source": "scraper"}

@app.post("/api/analyze/url")
async def analyze_social_url(url: str):
    """Extract metadata from social media URL"""
    if not API_CLIENTS_AVAILABLE or not web_scrapers:
        return {"error": "Scrapers not available"}
    
    metadata = web_scrapers.analyze_url(url)
    return {"url": url, "metadata": metadata}

@app.get("/api/content/sample/{platform}")
async def get_content_sample(platform: str, limit: int = 5):
    """Fetch sample content from any platform"""
    if not API_CLIENTS_AVAILABLE or not social_apis:
        return {"error": "APIs not available"}
    
    content = social_apis.fetch_content_sample(platform, limit)
    return {"platform": platform, "content": content}

if __name__ == "__main__":
    print("\\n Starting AI Comment Rewriter API...")
    print(f" LangChain Available: {LANGCHAIN_AVAILABLE}")
    
    gemini_llm = get_gemini_llm()
    print(f" Gemini Available: {gemini_llm is not None}")
    
    if gemini_llm:
        print(f" Model: {os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')}")
        print(" Ready to rewrite with AI!")
    else:
        print("  Running in MOCK mode - set GOOGLE_API_KEY for AI features")
        print("   Get your FREE key at: https://makersuite.google.com/app/apikey")
    
    if API_CLIENTS_AVAILABLE and social_apis:
        print(f"\\n Social Media APIs:")
        status = social_apis.get_status()
        for api_name, available in status.items():
            icon = "✅" if available else "❌"
            print(f"  {icon} {api_name.capitalize()}: {'Connected' if available else 'Not configured'}")
    
    print("\\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
