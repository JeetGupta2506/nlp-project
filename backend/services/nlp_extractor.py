import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class ExtractedClaim:
    text: str
    start: int
    end: int
    type: str
    confidence: float
    context: str

class AdvancedClaimExtractor:
    """
    Advanced NLP-based claim extractor using regex patterns and heuristics.
    In production, this would use spaCy, transformers, or other NLP libraries.
    """
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.entity_keywords = self._load_entity_keywords()
    
    def _initialize_patterns(self) -> Dict[str, List[str]]:
        return {
            'dates': [
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
                r'\b\d{4}\b',
                r'\b\d{1,2}\/\d{1,2}\/\d{4}\b',
                r'\b(?:Q[1-4])\s+\d{4}\b',
                r'\b(?:in|during|since|by)\s+\d{4}\b',
                r'\b(?:early|mid|late)\s+\d{4}\b'
            ],
            'numbers': [
                r'\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:million|billion|thousand|%|percent)\b',
                r'\$\d+(?:,\d{3})*(?:\.\d+)?\b',
                r'\b\d+(?:,\d{3})*\s*(?:users?|customers?|downloads?|sales?|orders?)\b',
                r'\b\d+(?:\.\d+)?\s*(?:GB|TB|MB|KB)\b',
                r'\b\d+(?:\.\d+)?\s*(?:hours?|minutes?|seconds?|days?|weeks?|months?|years?)\b'
            ],
            'entities': [
                r'\b(?:iPhone|iPad|MacBook|Apple|Google|Microsoft|Amazon|Tesla|Netflix|Meta|Facebook|Twitter|X|Instagram|TikTok|YouTube)\s*\w*\b',
                r'\b[A-Z][a-z]+\s+(?:Inc|Corp|LLC|Ltd|Company|Corporation)\b',
                r'\b(?:CEO|CTO|CFO|President|Director|Manager)\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b',
                r'\b[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b(?=\s+(?:said|announced|reported|stated|claimed))'
            ],
            'facts': [
                r'\b(?:announced|launched|released|introduced|unveiled)\s+.{10,50}\b',
                r'\b(?:reported|stated|claimed|said)\s+that\s+.{10,100}\b',
                r'\b(?:increased|decreased|grew|fell|rose|dropped)\s+by\s+\d+.{0,20}\b'
            ]
        }
    
    def _load_entity_keywords(self) -> Dict[str, List[str]]:
        return {
            'companies': ['apple', 'google', 'microsoft', 'amazon', 'meta', 'tesla', 'netflix', 'grammarly'],
            'products': ['iphone', 'ipad', 'macbook', 'android', 'windows', 'alexa', 'tesla model'],
            'people': ['tim cook', 'elon musk', 'satya nadella', 'sundar pichai'],
            'locations': ['cupertino', 'seattle', 'redmond', 'mountain view', 'austin']
        }
    
    def extract_claims(self, text: str) -> List[ExtractedClaim]:
        claims = []
        
        # Extract different types of claims
        for claim_type, patterns in self.patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    claim = ExtractedClaim(
                        text=match.group().strip(),
                        start=match.start(),
                        end=match.end(),
                        type=claim_type.rstrip('s'),  # Remove plural
                        confidence=self._calculate_confidence(match.group(), claim_type),
                        context=self._get_context(text, match.start(), match.end())
                    )
                    claims.append(claim)
        
        # Remove overlapping claims
        claims = self._remove_overlaps(claims)
        
        # Filter out low-confidence claims
        claims = [claim for claim in claims if claim.confidence > 0.5]
        
        return claims
    
    def _calculate_confidence(self, claim_text: str, claim_type: str) -> float:
        """Calculate confidence score based on claim characteristics"""
        base_confidence = 0.7
        
        # Boost confidence for specific patterns
        if claim_type == 'dates':
            if re.search(r'\b\d{4}\b', claim_text):
                base_confidence += 0.2
        elif claim_type == 'numbers':
            if any(unit in claim_text.lower() for unit in ['million', 'billion', '$']):
                base_confidence += 0.15
        elif claim_type == 'entities':
            if any(entity in claim_text.lower() for entities in self.entity_keywords.values() for entity in entities):
                base_confidence += 0.25
        
        return min(base_confidence, 0.95)
    
    def _get_context(self, text: str, start: int, end: int, window: int = 50) -> str:
        """Get surrounding context for a claim"""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        return text[context_start:context_end].strip()
    
    def _remove_overlaps(self, claims: List[ExtractedClaim]) -> List[ExtractedClaim]:
        """Remove overlapping claims, keeping the most confident ones"""
        claims.sort(key=lambda x: x.start)
        
        filtered_claims = []
        for claim in claims:
            overlaps = False
            for i, existing in enumerate(filtered_claims):
                if (claim.start < existing.end and claim.end > existing.start):
                    # Keep the more confident claim
                    if claim.confidence > existing.confidence:
                        filtered_claims[i] = claim
                    overlaps = True
                    break
            
            if not overlaps:
                filtered_claims.append(claim)
        
        return filtered_claims