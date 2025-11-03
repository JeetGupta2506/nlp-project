import React, { useState } from 'react';
import { Sparkles, RefreshCw, ArrowRight, Info, Hash, TrendingUp, Target, Copy, Check } from 'lucide-react';

interface Tone {
  name: string;
  description: string;
  example_input: string;
  example_output: string;
  emoji: string;
}

interface Platform {
  id: string;
  name: string;
  char_limit: number;
  optimal_length: string;
  hashtag_limit: number;
  best_tones: string[];
  emoji_friendly: boolean;
}

interface RewriteResponse {
  original: string;
  rewritten: string;
  tone: string;
  persona: string | null;
  explanation: string[];
  processing_time: number;
  model_used: string;
  platform_info?: {
    name: string;
    char_limit: number;
    current_length: number;
    within_limit: boolean;
    optimal_length: string;
  };
  suggested_hashtags?: string[];
  engagement_prediction?: {
    virality_score: number;
    predicted_likes: number;
    predicted_shares: number;
    predicted_comments: number;
    optimal_post_time: string;
    engagement_level: string;
  };
}

const App: React.FC = () => {
  const [comment, setComment] = useState("Bruh this product is trash ");
  const [selectedTone, setSelectedTone] = useState("professional");
  const [selectedPlatform, setSelectedPlatform] = useState<string | null>("reddit");
  const [result, setResult] = useState<RewriteResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [tones, setTones] = useState<Tone[]>([]);
  const [platforms, setPlatforms] = useState<Record<string, Platform>>({});
  const [copied, setCopied] = useState(false);
  const [fetchingComments, setFetchingComments] = useState(false);
  const [realComments, setRealComments] = useState<any[]>([]);
  const [showComments, setShowComments] = useState(false);
  const [subreddit, setSubreddit] = useState("technology");
  const [youtubeVideoId, setYoutubeVideoId] = useState("");

  React.useEffect(() => {
    // Fetch tones
    fetch('http://localhost:8000/tones')
      .then(res => res.json())
      .then(data => setTones(data))
      .catch(err => {
        console.error('Failed to fetch tones:', err);
        setTones([
          { name: 'Casual', description: 'Friendly and relaxed', example_input: '', example_output: '', emoji: '😊' },
          { name: 'Professional', description: 'Business-appropriate', example_input: '', example_output: '', emoji: '💼' },
          { name: 'Supportive', description: 'Encouraging', example_input: '', example_output: '', emoji: '🤗' },
          { name: 'Sarcastic', description: 'Witty and ironic', example_input: '', example_output: '', emoji: '😏' },
          { name: 'Respectful', description: 'Polite', example_input: '', example_output: '', emoji: '🙏' },
          { name: 'Empathetic', description: 'Understanding', example_input: '', example_output: '', emoji: '💙' },
          { name: 'Funny', description: 'Humorous', example_input: '', example_output: '', emoji: '😂' },
          { name: 'Motivational', description: 'Inspiring', example_input: '', example_output: '', emoji: '🚀' }
        ]);
      });

    // Fetch platforms
    fetch('http://localhost:8000/platforms')
      .then(res => res.json())
      .then(data => setPlatforms(data))
      .catch(err => console.error('Failed to fetch platforms:', err));
  }, []);

  const handleRewrite = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/rewrite', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          comment,
          tone: selectedTone,
          context: null,
          persona: null,
          platform: selectedPlatform
        })
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Rewrite failed:', error);
      alert('Failed to rewrite comment. Make sure the backend is running on port 8000.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchRedditComments = async () => {
    setFetchingComments(true);
    try {
      const response = await fetch(`http://localhost:8000/api/comments/reddit?query=${encodeURIComponent(subreddit)}&limit=10`);
      const data = await response.json();
      console.log('Reddit API Response:', data);
      
      if (data.error) {
        alert(`Error: ${data.error}`);
        setRealComments([]);
      } else if (data.comments && data.comments.length > 0) {
        setRealComments(data.comments);
        setShowComments(true);
      } else {
        alert('No comments found. Try a different search term.');
        setRealComments([]);
      }
    } catch (err) {
      console.error('Failed to fetch Reddit comments:', err);
      alert('Failed to fetch Reddit comments. Make sure backend is running.');
    } finally {
      setFetchingComments(false);
    }
  };

  const fetchYouTubeComments = async () => {
    setFetchingComments(true);
    try {
      let url;
      
      if (youtubeVideoId) {
        // Check if it looks like a video ID (11 chars, alphanumeric with - and _)
        const videoIdPattern = /^[a-zA-Z0-9_-]{11}$/;
        
        if (videoIdPattern.test(youtubeVideoId)) {
          // It's a video ID
          url = `http://localhost:8000/api/comments/youtube?video_id=${youtubeVideoId}&limit=10`;
        } else {
          // It's a search query
          url = `http://localhost:8000/api/comments/youtube?query=${encodeURIComponent(youtubeVideoId)}&limit=10`;
        }
      } else {
        // Empty - use trending
        url = `http://localhost:8000/api/comments/youtube/trending?limit=10`;
      }
      
      const response = await fetch(url);
      const data = await response.json();
      console.log('YouTube API Response:', data);
      
      if (data.error) {
        alert(`Error: ${data.error}`);
        setRealComments([]);
      } else if (data.comments && data.comments.length > 0) {
        setRealComments(data.comments);
        setShowComments(true);
      } else {
        alert('No comments found. Try a different video or check API keys.');
        setRealComments([]);
      }
    } catch (err) {
      console.error('Failed to fetch YouTube comments:', err);
      alert('Failed to fetch YouTube comments. Make sure backend is running.');
    } finally {
      setFetchingComments(false);
    }
  };

  const useComment = (commentText: string) => {
    setComment(commentText);
    setShowComments(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCopy = async () => {
    if (result?.rewritten) {
      await navigator.clipboard.writeText(result.rewritten);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const getPlatformEmoji = (platformId: string) => {
    const emojis: Record<string, string> = {
      reddit: '🤖',
      youtube: '▶️'
    };
    return emojis[platformId] || '🌐';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50">
      <div className="max-w-5xl mx-auto px-6 py-12">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="w-10 h-10 text-purple-600" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Social Media Rewriter
            </h1>
          </div>
          <p className="text-xl text-gray-600">Transform your tone for any platform. Express smarter. 🚀</p>
        </div>

        {/* Platform Selector */}
        <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-purple-600" />
            Choose Your Platform
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
            {Object.entries(platforms).map(([id, platform]) => (
              <button
                key={id}
                onClick={() => setSelectedPlatform(id)}
                className={`p-4 rounded-xl border-2 transition-all duration-200 ${
                  selectedPlatform === id
                    ? 'border-blue-500 bg-blue-50 shadow-md'
                    : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
                }`}
              >
                <div className="text-3xl mb-2">{getPlatformEmoji(id)}</div>
                <div className="font-semibold text-gray-900 text-sm">{platform.name}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Fetch Real Comments Section */}
        <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            Fetch Real Comments from Social Media
          </h3>
          <div className="grid md:grid-cols-2 gap-6">
            {/* Reddit Section */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <span className="text-2xl">🤖</span>
                <h4 className="font-semibold text-gray-800">Reddit Search</h4>
              </div>
              <input
                type="text"
                value={subreddit}
                onChange={(e) => setSubreddit(e.target.value)}
                placeholder="Search keyword (e.g., AI, gaming, cooking)"
                className="w-full p-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400"
              />
              <p className="text-xs text-gray-500">💡 Enter any topic to find related Reddit comments</p>
              <button
                onClick={fetchRedditComments}
                disabled={fetchingComments}
                className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {fetchingComments ? <RefreshCw className="w-4 h-4 animate-spin" /> : <ArrowRight className="w-4 h-4" />}
                Search Reddit
              </button>
            </div>

            {/* YouTube Section */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <span className="text-2xl">▶️</span>
                <h4 className="font-semibold text-gray-800">YouTube</h4>
              </div>
              <input
                type="text"
                value={youtubeVideoId}
                onChange={(e) => setYoutubeVideoId(e.target.value)}
                placeholder="Video ID or search 'AI news' or 'funny cats'"
                className="w-full p-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500/20 focus:border-red-400"
              />
              <p className="text-xs text-gray-500 mt-1">💡 Enter video ID (dQw4w9WgXcQ), search by name, or leave empty for trending!</p>
              <button
                onClick={fetchYouTubeComments}
                disabled={fetchingComments}
                className="w-full bg-red-600 text-white px-4 py-3 rounded-lg hover:bg-red-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {fetchingComments ? <RefreshCw className="w-4 h-4 animate-spin" /> : <ArrowRight className="w-4 h-4" />}
                Fetch from YouTube
              </button>
            </div>
          </div>

          {/* Display Fetched Comments */}
          {showComments && realComments.length > 0 && (
            <div className="mt-6 border-t pt-6">
              <h4 className="font-semibold text-gray-800 mb-3">📝 Found {realComments.length} comments - Click to use:</h4>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {realComments.map((comment, idx) => (
                  <button
                    key={idx}
                    onClick={() => useComment(comment.text || comment.body)}
                    className="w-full text-left p-4 bg-gray-50 hover:bg-blue-50 rounded-lg border border-gray-200 hover:border-blue-300 transition-all group"
                  >
                    <div className="flex items-start gap-3">
                      <span className="text-sm text-gray-500 font-mono">#{idx + 1}</span>
                      <div className="flex-1">
                        <p className="text-gray-800 line-clamp-2 group-hover:text-blue-900">{comment.text || comment.body}</p>
                        {comment.post_title && (
                          <p className="text-xs text-gray-500 mt-1">From: {comment.post_title}</p>
                        )}
                        {comment.video_title && (
                          <p className="text-xs text-gray-500 mt-1">Video: {comment.video_title}</p>
                        )}
                        <div className="flex items-center gap-3 mt-2 text-xs text-gray-500">
                          <span>👤 {comment.author || comment.author_display_name || 'Anonymous'}</span>
                          {comment.score && <span>⬆️ {comment.score}</span>}
                          {comment.like_count && <span>❤️ {comment.like_count}</span>}
                        </div>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <span className="text-lg"></span>
              </div>
              <h2 className="text-xl font-semibold text-gray-900">Original Comment</h2>
            </div>
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Type your comment here..."
              className="w-full h-40 p-4 border border-gray-200 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-purple-500/20 focus:border-purple-400 transition-all"
            />
            <p className="text-sm text-gray-500 mt-2">{comment.length} characters</p>
          </div>

          {result && (
            <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-2xl shadow-lg p-6 border border-purple-100">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-4 h-4 text-white" />
                </div>
                <h2 className="text-xl font-semibold text-gray-900">Rewritten</h2>
                <span className="ml-auto text-sm text-purple-600 font-medium">{result.tone}</span>
                <button
                  onClick={handleCopy}
                  className="ml-2 p-2 hover:bg-white rounded-lg transition-all"
                  title="Copy to clipboard"
                >
                  {copied ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4 text-gray-600" />}
                </button>
              </div>
              <div className="bg-white rounded-xl p-4 min-h-[160px] border border-purple-200">
                <p className="text-gray-800 text-lg leading-relaxed">{result.rewritten}</p>
              </div>
              
              {/* Hashtags */}
              {result.suggested_hashtags && result.suggested_hashtags.length > 0 && (
                <div className="mt-4 flex items-center gap-2 flex-wrap">
                  <Hash className="w-4 h-4 text-blue-500" />
                  {result.suggested_hashtags.map((tag, idx) => (
                    <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                      {tag}
                    </span>
                  ))}
                </div>
              )}

              {/* Engagement Prediction */}
              {result.engagement_prediction && (
                <div className="mt-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-xl p-4 border border-green-200">
                  <div className="flex items-center gap-2 mb-3">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                    <h3 className="font-semibold text-gray-900">Engagement Prediction</h3>
                    <span className={`ml-auto px-3 py-1 rounded-full text-sm font-bold ${
                      result.engagement_prediction.engagement_level === 'High' ? 'bg-green-200 text-green-800' :
                      result.engagement_prediction.engagement_level === 'Medium' ? 'bg-yellow-200 text-yellow-800' :
                      'bg-gray-200 text-gray-800'
                    }`}>
                      {result.engagement_prediction.engagement_level}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                    <div className="bg-white rounded-lg p-3">
                      <div className="text-gray-600">Virality</div>
                      <div className="text-2xl font-bold text-purple-600">{result.engagement_prediction.virality_score}%</div>
                    </div>
                    <div className="bg-white rounded-lg p-3">
                      <div className="text-gray-600">❤️ Likes</div>
                      <div className="text-2xl font-bold text-pink-600">{result.engagement_prediction.predicted_likes}</div>
                    </div>
                    <div className="bg-white rounded-lg p-3">
                      <div className="text-gray-600">🔄 Shares</div>
                      <div className="text-2xl font-bold text-blue-600">{result.engagement_prediction.predicted_shares}</div>
                    </div>
                    <div className="bg-white rounded-lg p-3">
                      <div className="text-gray-600">💬 Comments</div>
                      <div className="text-2xl font-bold text-green-600">{result.engagement_prediction.predicted_comments}</div>
                    </div>
                  </div>
                  <div className="mt-3 text-sm text-gray-600">
                    ⏰ {result.engagement_prediction.optimal_post_time}
                  </div>
                </div>
              )}

              {/* Platform Info */}
              {result.platform_info && (
                <div className="mt-4 flex items-center justify-between text-sm text-gray-600 bg-white rounded-lg p-3 border border-gray-200">
                  <span>
                    📏 Length: {result.platform_info.current_length}/{result.platform_info.char_limit} 
                    {result.platform_info.within_limit ? ' ✅' : ' ⚠️ Too long!'}
                  </span>
                  <span className="text-xs text-gray-500">
                    Optimal: {result.platform_info.optimal_length}
                  </span>
                </div>
              )}

              <div className="mt-4 space-y-2">
                {result.explanation.map((exp, idx) => (
                  <div key={idx} className="flex items-start gap-2 text-sm text-gray-600">
                    <Info className="w-4 h-4 mt-0.5 text-purple-500 flex-shrink-0" />
                    <span>{exp}</span>
                  </div>
                ))}
                <p className="text-xs text-gray-400 mt-2">
                  Processed in {result.processing_time.toFixed(3)}s • {result.model_used}
                </p>
              </div>
            </div>
          )}
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Choose Your Tone</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {tones.map((tone) => (
              <button
                key={tone.name.toLowerCase()}
                onClick={() => setSelectedTone(tone.name.toLowerCase())}
                className={`p-4 rounded-xl border-2 transition-all duration-200 ${
                  selectedTone === tone.name.toLowerCase()
                    ? 'border-purple-500 bg-purple-50 shadow-md'
                    : 'border-gray-200 hover:border-purple-300 hover:bg-gray-50'
                }`}
              >
                <div className="text-3xl mb-2">{tone.emoji}</div>
                <div className="font-semibold text-gray-900">{tone.name}</div>
                <div className="text-xs text-gray-500 mt-1">{tone.description}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="flex justify-center">
          <button
            onClick={handleRewrite}
            disabled={isLoading || !comment.trim()}
            className="group flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 text-white text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin" />
                Rewriting...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                Rewrite Comment
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
        </div>

        <div className="mt-12 bg-gradient-to-r from-purple-100 to-blue-100 rounded-2xl p-6 border border-purple-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-3"> How It Works</h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm text-gray-700">
            <div className="flex items-start gap-2">
              <span className="text-2xl">1</span>
              <div>
                <strong>Write or paste</strong> your comment in the text box
              </div>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-2xl">2</span>
              <div>
                <strong>Select a tone</strong> that matches your intent
              </div>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-2xl">3</span>
              <div>
                <strong>Get AI-powered</strong> rewrite instantly
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
