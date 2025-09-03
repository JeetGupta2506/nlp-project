from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import re
import json
import asyncio
from datetime import datetime
import uuid

app = FastAPI(title="FactCheck Pro API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ClaimExtractionRequest(BaseModel):
    text: str

class Claim(BaseModel):
    id: str
    text: str
    start: int
    end: int
    type: str  # 'date', 'number', 'entity', 'fact'
    status: str  # 'verified', 'unverified', 'false', 'pending'
    confidence: int
    sources: Optional[List[str]] = []
    evidence: Optional[str] = ""

class ClaimExtractionResponse(BaseModel):
    claims: List[Claim]
    processing_time: float

class VerificationRequest(BaseModel):
    claim_id: str
    claim_text: str

# Mock knowledge base for verification
KNOWLEDGE_BASE = {
    "iphone 16": {
        "announcement_date": "September 2024",
        "starting_price": "$829",
        "chip": "A18",
        "sources": ["Apple Press Release", "TechCrunch", "The Verge"]
    },
    "apple": {
        "ceo": "Tim Cook",
        "founded": "1976",
        "headquarters": "Cupertino, California",
        "sources": ["Apple Official Website", "SEC Filings"]
    },
    "grammarly": {
        "users": "30 million",
        "founded": "2009",
        "sources": ["Company Reports", "TechCrunch"]
    }
}

class ClaimExtractor:
    def __init__(self):
        # Date patterns
        self.date_patterns = [
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{4}\b',
            r'\b\d{1,2}\/\d{1,2}\/\d{4}\b',
            r'\b(?:Q[1-4])\s+\d{4}\b'
        ]
        
        # Number patterns
        self.number_patterns = [
            r'\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:million|billion|thousand|%|percent)\b',
            r'\$\d+(?:,\d{3})*(?:\.\d+)?\b',
            r'\b\d+(?:,\d{3})*\s*(?:users?|customers?|downloads?|sales?)\b'
        ]
        
        # Entity patterns (simplified)
        self.entity_patterns = [
            r'\b(?:iPhone|iPad|MacBook|Apple|Google|Microsoft|Amazon|Tesla|Netflix)\s*\w*\b',
            r'\b[A-Z][a-z]+\s+(?:Inc|Corp|LLC|Ltd|Company)\b',
            r'\b(?:CEO|CTO|CFO|President)\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        ]

    def extract_claims(self, text: str) -> List[Dict[str, Any]]:
        claims = []
        
        # Extract dates
        for pattern in self.date_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                claims.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'date',
                    'pattern_type': 'date'
                })
        
        # Extract numbers
        for pattern in self.number_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                claims.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'number',
                    'pattern_type': 'number'
                })
        
        # Extract entities
        for pattern in self.entity_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                claims.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'entity',
                    'pattern_type': 'entity'
                })
        
        # Remove overlapping claims (keep longer ones)
        claims = self._remove_overlaps(claims)
        
        return claims
    
    def _remove_overlaps(self, claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Sort by start position
        claims.sort(key=lambda x: x['start'])
        
        filtered_claims = []
        for claim in claims:
            # Check if this claim overlaps with any existing claim
            overlaps = False
            for existing in filtered_claims:
                if (claim['start'] < existing['end'] and claim['end'] > existing['start']):
                    # Keep the longer claim
                    if len(claim['text']) > len(existing['text']):
                        filtered_claims.remove(existing)
                    else:
                        overlaps = True
                    break
            
            if not overlaps:
                filtered_claims.append(claim)
        
        return filtered_claims

class ClaimVerifier:
    def __init__(self):
        self.knowledge_base = KNOWLEDGE_BASE
    
    async def verify_claim(self, claim_text: str, claim_type: str) -> Dict[str, Any]:
        # Simulate verification delay
        await asyncio.sleep(0.5)
        
        claim_lower = claim_text.lower()
        
        # Check against knowledge base
        for entity, data in self.knowledge_base.items():
            if entity in claim_lower:
                return await self._verify_against_entity(claim_text, claim_type, entity, data)
        
        # Default verification for unknown claims
        return {
            'status': 'unverified',
            'confidence': 60,
            'sources': ['General Knowledge Base'],
            'evidence': f'Could not find specific verification for: "{claim_text}"'
        }
    
    async def _verify_against_entity(self, claim_text: str, claim_type: str, entity: str, data: Dict[str, Any]) -> Dict[str, Any]:
        claim_lower = claim_text.lower()
        
        # Date verification
        if claim_type == 'date' and 'announcement_date' in data:
            if 'september 2024' in claim_lower and entity == 'iphone 16':
                return {
                    'status': 'verified',
                    'confidence': 95,
                    'sources': data['sources'],
                    'evidence': f'Apple officially announced the iPhone 16 in September 2024.'
                }
        
        # Price verification
        if '$' in claim_text and 'starting_price' in data:
            if '$799' in claim_text and entity == 'iphone 16':
                return {
                    'status': 'false',
                    'confidence': 90,
                    'sources': data['sources'],
                    'evidence': f'The iPhone 16 actually starts at {data["starting_price"]}, not $799.'
                }
        
        # Chip verification
        if claim_type == 'entity' and 'chip' in data:
            if 'a18' in claim_lower:
                return {
                    'status': 'verified',
                    'confidence': 98,
                    'sources': data['sources'],
                    'evidence': f'The iPhone 16 series features the {data["chip"]} chip.'
                }
        
        # Number verification
        if claim_type == 'number':
            if 'million' in claim_lower:
                if '40 million' in claim_lower and 'pre-order' in claim_lower:
                    return {
                        'status': 'unverified',
                        'confidence': 60,
                        'sources': ['Industry Reports'],
                        'evidence': 'Pre-order numbers have not been officially confirmed by Apple.'
                    }
                elif '30 million' in claim_lower and entity == 'grammarly':
                    return {
                        'status': 'verified',
                        'confidence': 85,
                        'sources': data['sources'],
                        'evidence': f'Grammarly reported approximately {data["users"]} active users.'
                    }
        
        return {
            'status': 'unverified',
            'confidence': 70,
            'sources': data['sources'],
            'evidence': f'Partial match found for {entity}, but specific claim needs verification.'
        }

# Initialize services
claim_extractor = ClaimExtractor()
claim_verifier = ClaimVerifier()

@app.get("/")
async def root():
    return {"message": "FactCheck Pro API", "version": "1.0.0"}

@app.post("/extract-claims", response_model=ClaimExtractionResponse)
async def extract_claims(request: ClaimExtractionRequest):
    start_time = datetime.now()
    
    try:
        # Extract claims using NLP pipeline
        raw_claims = claim_extractor.extract_claims(request.text)
        
        # Verify each claim
        verified_claims = []
        for raw_claim in raw_claims:
            verification_result = await claim_verifier.verify_claim(
                raw_claim['text'], 
                raw_claim['type']
            )
            
            claim = Claim(
                id=str(uuid.uuid4()),
                text=raw_claim['text'],
                start=raw_claim['start'],
                end=raw_claim['end'],
                type=raw_claim['type'],
                status=verification_result['status'],
                confidence=verification_result['confidence'],
                sources=verification_result['sources'],
                evidence=verification_result['evidence']
            )
            verified_claims.append(claim)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return ClaimExtractionResponse(
            claims=verified_claims,
            processing_time=processing_time
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing claims: {str(e)}")

@app.post("/verify-claim")
async def verify_single_claim(request: VerificationRequest):
    try:
        verification_result = await claim_verifier.verify_claim(
            request.claim_text, 
            "fact"  # Default type for manual verification
        )
        
        return {
            "claim_id": request.claim_id,
            "verification": verification_result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying claim: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)