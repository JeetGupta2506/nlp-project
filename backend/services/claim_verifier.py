import asyncio
from typing import Dict, Any, List
import re

class ClaimVerificationService:
    """
    Service for verifying claims against multiple sources.
    In production, this would integrate with Wikipedia API, news APIs, 
    vector databases, and other verification sources.
    """
    
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.verification_rules = self._load_verification_rules()
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        return {
            "apple": {
                "products": {
                    "iphone 16": {
                        "announcement_date": "September 12, 2024",
                        "starting_price": "$829",
                        "chip": "A18",
                        "pre_orders": "unconfirmed"
                    }
                },
                "leadership": {
                    "ceo": "Tim Cook"
                },
                "company_info": {
                    "founded": "1976",
                    "headquarters": "Cupertino, California"
                },
                "sources": ["Apple Press Release", "Apple.com", "SEC Filings"]
            },
            "grammarly": {
                "metrics": {
                    "users": "30 million",
                    "founded": "2009"
                },
                "sources": ["Company Reports", "Grammarly Blog"]
            },
            "market_data": {
                "smartphone_sales_2024": "1.2 billion",
                "ai_market_size": "$150 billion",
                "sources": ["IDC", "Gartner", "Statista"]
            }
        }
    
    def _load_verification_rules(self) -> Dict[str, Any]:
        return {
            "price_tolerance": 0.05,  # 5% tolerance for price claims
            "date_exact_match": True,
            "number_significant_digits": 2
        }
    
    async def verify_claim(self, claim_text: str, claim_type: str, context: str = "") -> Dict[str, Any]:
        """Main verification method"""
        
        # Simulate API call delay
        await asyncio.sleep(0.3)
        
        claim_lower = claim_text.lower()
        
        # Route to specific verification methods
        if claim_type == 'date':
            return await self._verify_date_claim(claim_text, context)
        elif claim_type == 'number':
            return await self._verify_number_claim(claim_text, context)
        elif claim_type == 'entity':
            return await self._verify_entity_claim(claim_text, context)
        elif claim_type == 'fact':
            return await self._verify_fact_claim(claim_text, context)
        
        return self._default_verification(claim_text)
    
    async def _verify_date_claim(self, claim_text: str, context: str) -> Dict[str, Any]:
        """Verify date-related claims"""
        claim_lower = claim_text.lower()
        context_lower = context.lower()
        
        # iPhone 16 announcement date
        if 'september 2024' in claim_lower and 'iphone' in context_lower:
            return {
                'status': 'verified',
                'confidence': 95,
                'sources': self.knowledge_base['apple']['sources'],
                'evidence': 'Apple officially announced the iPhone 16 on September 12, 2024.'
            }
        
        # General year verification
        year_match = re.search(r'\b(20\d{2})\b', claim_text)
        if year_match:
            year = int(year_match.group(1))
            current_year = 2024
            
            if year <= current_year:
                confidence = 80 if year == current_year else 90
                return {
                    'status': 'verified',
                    'confidence': confidence,
                    'sources': ['General Knowledge'],
                    'evidence': f'Year {year} is within valid historical range.'
                }
        
        return self._default_verification(claim_text, 'date')
    
    async def _verify_number_claim(self, claim_text: str, context: str) -> Dict[str, Any]:
        """Verify numerical claims"""
        claim_lower = claim_text.lower()
        context_lower = context.lower()
        
        # Pre-order numbers
        if 'million' in claim_lower and 'pre-order' in context_lower:
            if '40 million' in claim_lower:
                return {
                    'status': 'unverified',
                    'confidence': 60,
                    'sources': ['Industry Reports'],
                    'evidence': 'Pre-order numbers have not been officially confirmed by Apple.'
                }
        
        # Price verification
        price_match = re.search(r'\$(\d+(?:,\d{3})*)', claim_text)
        if price_match and 'iphone' in context_lower:
            price = int(price_match.group(1).replace(',', ''))
            if price == 799:
                return {
                    'status': 'false',
                    'confidence': 90,
                    'sources': self.knowledge_base['apple']['sources'],
                    'evidence': 'The iPhone 16 actually starts at $829, not $799.'
                }
            elif price == 829:
                return {
                    'status': 'verified',
                    'confidence': 95,
                    'sources': self.knowledge_base['apple']['sources'],
                    'evidence': 'Correct starting price for iPhone 16.'
                }
        
        # User count verification
        if 'grammarly' in context_lower and 'million' in claim_lower:
            if '30 million' in claim_lower:
                return {
                    'status': 'verified',
                    'confidence': 85,
                    'sources': self.knowledge_base['grammarly']['sources'],
                    'evidence': 'Grammarly reported approximately 30 million active users.'
                }
        
        return self._default_verification(claim_text, 'number')
    
    async def _verify_entity_claim(self, claim_text: str, context: str) -> Dict[str, Any]:
        """Verify entity-related claims"""
        claim_lower = claim_text.lower()
        context_lower = context.lower()
        
        # Chip verification
        if 'a18' in claim_lower and 'iphone' in context_lower:
            return {
                'status': 'verified',
                'confidence': 98,
                'sources': self.knowledge_base['apple']['sources'],
                'evidence': 'The iPhone 16 series features the new A18 and A18 Pro chips.'
            }
        
        # Company verification
        known_companies = ['apple', 'google', 'microsoft', 'amazon', 'meta', 'tesla']
        for company in known_companies:
            if company in claim_lower:
                return {
                    'status': 'verified',
                    'confidence': 90,
                    'sources': ['Company Database', 'SEC Filings'],
                    'evidence': f'{company.title()} is a verified entity in our database.'
                }
        
        return self._default_verification(claim_text, 'entity')
    
    async def _verify_fact_claim(self, claim_text: str, context: str) -> Dict[str, Any]:
        """Verify factual statements"""
        claim_lower = claim_text.lower()
        
        # Look for superlative claims that are often subjective
        superlatives = ['most', 'best', 'largest', 'biggest', 'fastest', 'first']
        if any(sup in claim_lower for sup in superlatives):
            return {
                'status': 'unverified',
                'confidence': 50,
                'sources': ['Multiple Sources Required'],
                'evidence': 'Superlative claims require verification from multiple authoritative sources.'
            }
        
        return self._default_verification(claim_text, 'fact')
    
    def _default_verification(self, claim_text: str, claim_type: str = 'unknown') -> Dict[str, Any]:
        """Default verification for unknown claims"""
        return {
            'status': 'unverified',
            'confidence': 60,
            'sources': ['General Knowledge Base'],
            'evidence': f'Could not find specific verification for this {claim_type} claim: "{claim_text}"'
        }
    
    async def batch_verify(self, claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Verify multiple claims in batch"""
        verification_tasks = []
        
        for claim in claims:
            task = self.verify_claim(
                claim['text'], 
                claim['type'], 
                claim.get('context', '')
            )
            verification_tasks.append(task)
        
        results = await asyncio.gather(*verification_tasks)
        
        # Combine claims with verification results
        verified_claims = []
        for claim, verification in zip(claims, results):
            verified_claim = {**claim, **verification}
            verified_claims.append(verified_claim)
        
        return verified_claims