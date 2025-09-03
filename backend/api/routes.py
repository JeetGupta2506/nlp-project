from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import uuid
from datetime import datetime

from ..services.nlp_extractor import AdvancedClaimExtractor
from ..services.claim_verifier import ClaimVerificationService
from ..services.source_manager import SourceManager

router = APIRouter()

# Initialize services
extractor = AdvancedClaimExtractor()
verifier = ClaimVerificationService()
source_manager = SourceManager()

@router.post("/extract-claims")
async def extract_and_verify_claims(request: dict):
    """Extract claims from text and verify them"""
    
    start_time = datetime.now()
    text = request.get('text', '')
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text content is required")
    
    try:
        # Step 1: Extract claims using NLP
        extracted_claims = extractor.extract_claims(text)
        
        # Step 2: Verify each claim
        verified_claims = []
        
        for claim in extracted_claims:
            # Search sources for verification
            source_results = await source_manager.search_sources(
                claim.text, 
                claim.type
            )
            
            # Verify the claim
            verification = await verifier.verify_claim(
                claim.text, 
                claim.type, 
                claim.context
            )
            
            # Calculate final confidence based on sources
            if source_results:
                final_confidence = source_manager.calculate_overall_confidence(source_results)
                final_status = source_manager.determine_status(final_confidence, len(source_results))
                
                # Extract source names
                source_names = [result.get('source', 'Unknown') for result in source_results]
            else:
                final_confidence = verification['confidence']
                final_status = verification['status']
                source_names = verification.get('sources', [])
            
            verified_claim = {
                'id': str(uuid.uuid4()),
                'text': claim.text,
                'start': claim.start,
                'end': claim.end,
                'type': claim.type,
                'status': final_status,
                'confidence': int(final_confidence * 100),
                'sources': source_names,
                'evidence': verification.get('evidence', '')
            }
            
            verified_claims.append(verified_claim)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'claims': verified_claims,
            'processing_time': round(processing_time, 2),
            'total_claims': len(verified_claims),
            'metadata': {
                'text_length': len(text),
                'extraction_method': 'advanced_nlp',
                'verification_sources': len(source_manager.sources)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing claims: {str(e)}")

@router.post("/verify-claim/{claim_id}")
async def reverify_claim(claim_id: str, request: dict):
    """Re-verify a specific claim with updated parameters"""
    
    claim_text = request.get('claim_text', '')
    claim_type = request.get('claim_type', 'fact')
    
    if not claim_text:
        raise HTTPException(status_code=400, detail="Claim text is required")
    
    try:
        # Search sources
        source_results = await source_manager.search_sources(claim_text, claim_type)
        
        # Verify claim
        verification = await verifier.verify_claim(claim_text, claim_type)
        
        # Calculate confidence
        if source_results:
            confidence = source_manager.calculate_overall_confidence(source_results)
            status = source_manager.determine_status(confidence, len(source_results))
            sources = [result.get('source', 'Unknown') for result in source_results]
        else:
            confidence = verification['confidence']
            status = verification['status']
            sources = verification.get('sources', [])
        
        return {
            'claim_id': claim_id,
            'status': status,
            'confidence': int(confidence * 100),
            'sources': sources,
            'evidence': verification.get('evidence', ''),
            'updated_at': datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying claim: {str(e)}")

@router.get("/sources")
async def get_available_sources():
    """Get list of available verification sources"""
    
    sources_info = []
    for name, info in source_manager.sources.items():
        sources_info.append({
            'name': name,
            'type': info['type'],
            'reliability': info['reliability'],
            'description': f"{info['type'].title()} source with {info['reliability']*100:.0f}% reliability"
        })
    
    return {
        'sources': sources_info,
        'total_sources': len(sources_info)
    }

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'extractor': 'operational',
            'verifier': 'operational',
            'source_manager': 'operational'
        }
    }