"""
Social Media API Clients
Integrates with Reddit, Twitter, YouTube, and News APIs
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# REDDIT API CLIENT (Using PRAW)
# ============================================================================

class RedditClient:
    """Fetch posts and comments from Reddit"""
    
    def __init__(self):
        try:
            import praw
            self.client = praw.Reddit(
                client_id=os.getenv("REDDIT_CLIENT_ID"),
                client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                user_agent="SocialMediaRewriter/1.0"
            )
            self.available = True
            logger.info("✅ Reddit API connected")
        except Exception as e:
            self.available = False
            logger.warning(f"⚠️  Reddit API unavailable: {e}")
    
    def get_trending_posts(self, subreddit: str = "AskReddit", limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch trending posts from a subreddit"""
        if not self.available:
            return []
        
        try:
            posts = []
            subreddit_obj = self.client.subreddit(subreddit)
            
            for post in subreddit_obj.hot(limit=limit):
                posts.append({
                    "id": post.id,
                    "title": post.title,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "url": post.url,
                    "author": str(post.author),
                    "created_utc": post.created_utc,
                    "selftext": post.selftext[:500] if post.selftext else "",
                    "subreddit": subreddit
                })
            
            logger.info(f"✅ Fetched {len(posts)} posts from r/{subreddit}")
            return posts
        
        except Exception as e:
            logger.error(f"❌ Reddit error: {e}")
            return []
    
    def get_top_comments(self, post_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetch top comments from a Reddit post"""
        if not self.available:
            return []
        
        try:
            submission = self.client.submission(id=post_id)
            submission.comment_sort = "top"
            submission.comments.replace_more(limit=0)
            
            comments = []
            for comment in submission.comments[:limit]:
                comments.append({
                    "id": comment.id,
                    "body": comment.body,
                    "score": comment.score,
                    "author": str(comment.author),
                    "created_utc": comment.created_utc
                })
            
            return comments
        
        except Exception as e:
            logger.error(f"❌ Error fetching comments: {e}")
            return []


# ============================================================================
# TWITTER API CLIENT (Using Tweepy for Twitter API v2)
# ============================================================================

class TwitterClient:
    """Fetch trending topics and tweets from Twitter"""
    
    def __init__(self):
        try:
            import tweepy
            bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
            if bearer_token:
                self.client = tweepy.Client(bearer_token=bearer_token)
                self.available = True
                logger.info("✅ Twitter API connected")
            else:
                self.available = False
                logger.warning("⚠️  Twitter Bearer Token not found")
        except Exception as e:
            self.available = False
            logger.warning(f"⚠️  Twitter API unavailable: {e}")
    
    def get_trending_topics(self, location_id: int = 1) -> List[Dict[str, Any]]:
        """Fetch trending topics (Note: Requires Twitter API v2 elevated access)"""
        if not self.available:
            return []
        
        # Note: Trending topics require elevated access in Twitter API v2
        # For now, we'll return mock data or use search for popular tweets
        logger.warning("⚠️  Trending topics require Twitter API elevated access")
        return []
    
    def search_recent_tweets(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search recent tweets by query"""
        if not self.available:
            return []
        
        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=["created_at", "public_metrics", "author_id"]
            )
            
            results = []
            if tweets.data:
                for tweet in tweets.data:
                    results.append({
                        "id": tweet.id,
                        "text": tweet.text,
                        "created_at": str(tweet.created_at),
                        "metrics": {
                            "likes": tweet.public_metrics.get("like_count", 0),
                            "retweets": tweet.public_metrics.get("retweet_count", 0),
                            "replies": tweet.public_metrics.get("reply_count", 0)
                        }
                    })
            
            logger.info(f"✅ Found {len(results)} tweets for '{query}'")
            return results
        
        except Exception as e:
            logger.error(f"❌ Twitter search error: {e}")
            return []


# ============================================================================
# YOUTUBE API CLIENT
# ============================================================================

class YouTubeClient:
    """Fetch video comments and trending videos from YouTube"""
    
    def __init__(self):
        try:
            from googleapiclient.discovery import build
            api_key = os.getenv("YOUTUBE_API_KEY")
            if api_key:
                self.client = build("youtube", "v3", developerKey=api_key)
                self.available = True
                logger.info("✅ YouTube API connected")
            else:
                self.available = False
                logger.warning("⚠️  YouTube API key not found")
        except Exception as e:
            self.available = False
            logger.warning(f"⚠️  YouTube API unavailable: {e}")
    
    def get_trending_videos(self, region_code: str = "US", max_results: int = 10) -> List[Dict[str, Any]]:
        """Fetch trending videos"""
        if not self.available:
            return []
        
        try:
            request = self.client.videos().list(
                part="snippet,statistics",
                chart="mostPopular",
                regionCode=region_code,
                maxResults=max_results
            )
            response = request.execute()
            
            videos = []
            for item in response.get("items", []):
                videos.append({
                    "id": item["id"],
                    "title": item["snippet"]["title"],
                    "channel": item["snippet"]["channelTitle"],
                    "views": int(item["statistics"].get("viewCount", 0)),
                    "likes": int(item["statistics"].get("likeCount", 0)),
                    "comments": int(item["statistics"].get("commentCount", 0)),
                    "published_at": item["snippet"]["publishedAt"]
                })
            
            logger.info(f"✅ Fetched {len(videos)} trending videos")
            return videos
        
        except Exception as e:
            logger.error(f"❌ YouTube error: {e}")
            return []
    
    def get_video_comments(self, video_id: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """Fetch top comments from a YouTube video"""
        if not self.available:
            return []
        
        try:
            request = self.client.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results,
                order="relevance"
            )
            response = request.execute()
            
            comments = []
            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "text": comment["textDisplay"],
                    "author": comment["authorDisplayName"],
                    "likes": comment["likeCount"],
                    "published_at": comment["publishedAt"]
                })
            
            logger.info(f"✅ Fetched {len(comments)} comments from video {video_id}")
            return comments
        
        except Exception as e:
            logger.error(f"❌ Error fetching comments: {e}")
            return []


# ============================================================================
# NEWS API CLIENT
# ============================================================================

class NewsAPIClient:
    """Fetch trending news headlines"""
    
    def __init__(self):
        try:
            from newsapi import NewsApiClient
            api_key = os.getenv("NEWS_API_KEY")
            if api_key:
                self.client = NewsApiClient(api_key=api_key)
                self.available = True
                logger.info("✅ News API connected")
            else:
                self.available = False
                logger.warning("⚠️  News API key not found")
        except Exception as e:
            self.available = False
            logger.warning(f"⚠️  News API unavailable: {e}")
    
    def get_top_headlines(self, category: str = "technology", country: str = "us") -> List[Dict[str, Any]]:
        """Fetch top news headlines"""
        if not self.available:
            return []
        
        try:
            response = self.client.get_top_headlines(
                category=category,
                country=country,
                page_size=10
            )
            
            articles = []
            for article in response.get("articles", []):
                articles.append({
                    "title": article["title"],
                    "description": article.get("description", ""),
                    "url": article["url"],
                    "source": article["source"]["name"],
                    "published_at": article["publishedAt"]
                })
            
            logger.info(f"✅ Fetched {len(articles)} headlines")
            return articles
        
        except Exception as e:
            logger.error(f"❌ News API error: {e}")
            return []


# ============================================================================
# UNIFIED API MANAGER
# ============================================================================

class SocialMediaAPIs:
    """Unified manager for all social media API clients"""
    
    def __init__(self):
        self.reddit = RedditClient()
        self.twitter = TwitterClient()
        self.youtube = YouTubeClient()
        self.news = NewsAPIClient()
        
        # Status summary
        self.status = {
            "reddit": self.reddit.available,
            "twitter": self.twitter.available,
            "youtube": self.youtube.available,
            "news": self.news.available
        }
        
        available_count = sum(self.status.values())
        logger.info(f"📊 API Status: {available_count}/4 APIs available")
    
    def get_status(self) -> Dict[str, bool]:
        """Get availability status of all APIs"""
        return self.status
    
    def fetch_content_sample(self, platform: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetch sample content from specified platform"""
        if platform == "reddit" and self.reddit.available:
            return self.reddit.get_trending_posts(limit=limit)
        elif platform == "twitter" and self.twitter.available:
            return self.twitter.search_recent_tweets("trending", max_results=limit)
        elif platform == "youtube" and self.youtube.available:
            return self.youtube.get_trending_videos(max_results=limit)
        elif platform == "news" and self.news.available:
            return self.news.get_top_headlines()
        else:
            return []


# ============================================================================
# INITIALIZE GLOBAL API MANAGER
# ============================================================================

# Create global instance (will be imported by main.py)
social_apis = SocialMediaAPIs()
