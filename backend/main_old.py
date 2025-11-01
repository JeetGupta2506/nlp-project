from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
from datetime import datetime
from dotenv import load_dotenv

# LangChain & LangGraph imports
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import Graph, END

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Comment Rewriter API",
    description="Transform your tone. Express smarter. 💬✨",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Claim(BaseModel):
    id: str
    text: str
    start: int
    end: int
    type: str  # 'date', 'number', 'entity', 'fact'
    status: str  # 'verified', 'unverified', 'false', 'pending'
    confidence: int
    sources: Optional[List[str]] = []
    evidence: Optional[str] = None

class TextAnalysisRequest(BaseModel):
    content: str

class TextAnalysisResponse(BaseModel):
    claims: List[Claim]
    processing_time: float
    total_claims: int

class ClaimVerificationRequest(BaseModel):
    claim_id: str
    action: str  # 'confirm' or 'correct'

# Mock data for demonstration
MOCK_SOURCES = [
    "Wikipedia", "BBC News", "Reuters", "Associated Press", "FactCheck.org",
    "Snopes", "PolitiFact", "Google Fact Check", "News API", "Company Reports"
]

MOCK_EVIDENCE = [
    "Information verified through multiple reliable sources",
    "Data confirmed by official company statements",
    "Fact-checked against government databases",
    "Verified through independent news sources",
    "Confirmed by expert analysis"
]

def extract_dates(text: str) -> List[dict]:
    """Extract date claims from text"""
    claims = []
    date_patterns = [
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{4}\b',
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',
        r'\b\d{1,2}-\d{1,2}-\d{4}\b'
    ]
    
    for pattern in date_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            confidence = random.randint(70, 95)
            status = 'verified' if confidence > 85 else 'unverified'
            
            claims.append({
                'id': f'date-{len(claims)}',
                'text': match.group(),
                'start': match.start(),
                'end': match.end(),
                'type': 'date',
                'status': status,
                'confidence': confidence,
                'sources': random.sample(MOCK_SOURCES, random.randint(1, 3)),
                'evidence': random.choice(MOCK_EVIDENCE)
            })
    
    return claims

def extract_numbers(text: str) -> List[dict]:
    """Extract numerical claims from text"""
    claims = []
    number_patterns = [
        r'\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:million|billion|thousand|%|dollars?|\$)\b',
        r'\$\d+(?:,\d{3})*(?:\.\d+)?\b',
        r'\b\d+(?:,\d{3})*(?:\.\d+)?%\b'
    ]
    
    for pattern in number_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            if len(match.group()) > 3:  # Only significant numbers
                confidence = random.randint(60, 90)
                status = 'verified' if confidence > 80 else 'unverified'
                
                claims.append({
                    'id': f'number-{len(claims)}',
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'number',
                    'status': status,
                    'confidence': confidence,
                    'sources': random.sample(MOCK_SOURCES, random.randint(1, 2)),
                    'evidence': random.choice(MOCK_EVIDENCE)
                })
    
    return claims

def extract_entities(text: str) -> List[dict]:
    """Extract entity claims from text (simplified NER)"""
    claims = []
    entity_patterns = [
        r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc|Corp|Company|LLC|Ltd)\b',  # Companies
        r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:CEO|President|Director|Manager)\b',  # Titles
        r'\b(?:iPhone|iPad|MacBook|Samsung|Google|Microsoft|Apple|Tesla|Amazon)\b',  # Tech brands
        r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:chip|processor|CPU|GPU)\b'  # Tech products
    ]
    
    for pattern in entity_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            confidence = random.randint(75, 95)
            status = 'verified' if confidence > 85 else 'unverified'
            
            claims.append({
                'id': f'entity-{len(claims)}',
                'text': match.group(),
                'start': match.start(),
                'end': match.end(),
                'type': 'entity',
                'status': status,
                'confidence': confidence,
                'sources': random.sample(MOCK_SOURCES, random.randint(1, 3)),
                'evidence': random.choice(MOCK_EVIDENCE)
            })
    
    return claims

def extract_names(text: str) -> List[dict]:
    """Extract personal names and identity claims from text"""
    claims = []
    name_patterns = [
        r'\b(?:My name is|I am|I\'m)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',  # "My name is John"
        r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is my name\b',  # "John is my name"
        r'\b(?:I am|I\'m)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',  # "I am John"
        r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+here\b',  # "John here"
    ]
    
    for pattern in name_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            if len(match.groups()) > 0:
                name = match.group(1)
                confidence = random.randint(70, 90)
                status = 'unverified'  # Names are typically unverified
                
                claims.append({
                    'id': f'name-{len(claims)}',
                    'text': name,
                    'start': match.start(1),
                    'end': match.end(1),
                    'type': 'entity',
                    'status': status,
                    'confidence': confidence,
                    'sources': ['User Input', 'Personal Information'],
                    'evidence': 'Personal name claim requires verification'
                })
    
    return claims

def extract_facts(text: str) -> List[dict]:
    """Extract factual claims from text"""
    claims = []
    fact_patterns = [
        r'\b(?:announced|launched|released|introduced|confirmed|stated|said)\b[^.]*\.',
        r'\b(?:according to|reports|sources|data shows|research indicates)\b[^.]*\.',
        r'\b(?:successful|record|highest|lowest|first|last)\b[^.]*\.'
    ]
    
    for pattern in fact_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            if len(match.group()) > 20:  # Only substantial facts
                confidence = random.randint(50, 85)
                status = 'unverified' if confidence < 70 else 'verified'
                
                claims.append({
                    'id': f'fact-{len(claims)}',
                    'text': match.group().strip(),
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'fact',
                    'status': status,
                    'confidence': confidence,
                    'sources': random.sample(MOCK_SOURCES, random.randint(1, 2)),
                    'evidence': random.choice(MOCK_EVIDENCE)
                })
    
    return claims

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FactCheck Pro API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze": "/analyze",
            "verify": "/verify",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "FactCheck Pro API"
    }

@app.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """Analyze text and extract claims"""
    start_time = datetime.now()
    
    if not request.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    
    # Extract different types of claims
    all_claims = []
    all_claims.extend(extract_dates(request.content))
    all_claims.extend(extract_numbers(request.content))
    all_claims.extend(extract_entities(request.content))
    all_claims.extend(extract_names(request.content))
    all_claims.extend(extract_facts(request.content))
    
    # Remove duplicates and sort by position
    unique_claims = []
    seen_positions = set()
    
    for claim in all_claims:
        position_key = (claim['start'], claim['end'])
        if position_key not in seen_positions:
            seen_positions.add(position_key)
            unique_claims.append(claim)
    
    # Sort by start position
    unique_claims.sort(key=lambda x: x['start'])
    
    # Convert to Claim objects
    claims = [Claim(**claim) for claim in unique_claims]
    
    processing_time = (datetime.now() - start_time).total_seconds()
    
    return TextAnalysisResponse(
        claims=claims,
        processing_time=processing_time,
        total_claims=len(claims)
    )

@app.post("/verify")
async def verify_claim(request: ClaimVerificationRequest):
    """Verify or correct a claim"""
    if request.action not in ['confirm', 'correct']:
        raise HTTPException(status_code=400, detail="Action must be 'confirm' or 'correct'")
    
    # In a real application, this would update a database
    # For now, we'll just return a success message
    return {
        "claim_id": request.claim_id,
        "action": request.action,
        "status": "success",
        "message": f"Claim {request.claim_id} has been {request.action}ed",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/stats")
async def get_stats():
    """Get API statistics"""
    return {
        "total_requests": random.randint(1000, 5000),
        "successful_analyses": random.randint(800, 4500),
        "average_processing_time": round(random.uniform(0.5, 2.0), 2),
        "uptime": "99.9%",
        "last_updated": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
