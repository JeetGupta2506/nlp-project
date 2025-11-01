from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Literal, Annotated
import uvicorn
import os
from datetime import datetime
from dotenv import load_dotenv

# LangChain & LangGraph imports
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema import HumanMessage, SystemMessage
    from langgraph.graph import StateGraph, END
    from typing_extensions import TypedDict
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    print(f"Warning: LangChain not installed - {e}")

load_dotenv()

app = FastAPI(
    title="AI Comment Rewriter API",
    description="Transform your tone with Gemini AI",
    version="2.0.0"
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

class RewriteResponse(BaseModel):
    original: str
    rewritten: str
    tone: str
    persona: Optional[str]
    explanation: List[str]
    processing_time: float
    model_used: str
    sentiment_shift: Optional[Dict[str, float]] = None

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
    detected_sentiment: Optional[str]
    system_prompt: Optional[str]
    user_prompt: Optional[str]
    rewritten: Optional[str]
    explanation: List[str]
    model_used: str

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

def create_rewrite_workflow():
    workflow = StateGraph(RewriteState)
    
    workflow.add_node("detect_tone", detect_tone_node)
    workflow.add_node("create_prompt", create_prompt_node)
    workflow.add_node("generate_rewrite", generate_rewrite_node)
    workflow.add_node("explain_changes", explain_changes_node)
    
    workflow.set_entry_point("detect_tone")
    workflow.add_edge("detect_tone", "create_prompt")
    workflow.add_edge("create_prompt", "generate_rewrite")
    workflow.add_edge("generate_rewrite", "explain_changes")
    workflow.add_edge("explain_changes", END)
    
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
                "detected_sentiment": None,
                "system_prompt": None,
                "user_prompt": None,
                "rewritten": None,
                "explanation": [],
                "model_used": "unknown"
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
                model_used=result["model_used"]
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
    
    print("\\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
