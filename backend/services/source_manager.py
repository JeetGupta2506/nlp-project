from typing import List, Dict, Any, Optional
import asyncio
import json

class SourceManager:
    """
    Manages verification sources and their reliability scores.
    In production, this would integrate with APIs like Wikipedia, news sources, etc.
    """
    
    def __init__(self):
        self.sources = self._initialize_sources()
        self.cache = {}
    
    def _initialize_sources(self) -> Dict[str, Dict[str, Any]]:
        return {
            "wikipedia": {
                "reliability": 0.85,
                "type": "encyclopedia",
                "api_endpoint": "https://en.wikipedia.org/api/rest_v1/",
                "rate_limit": 100  # requests per minute
            },
            "apple_press": {
                "reliability": 0.95,
                "type": "official",
                "api_endpoint": "https://www.apple.com/newsroom/",
                "rate_limit": 60
            },
            "techcrunch": {
                "reliability": 0.80,
                "type": "news",
                "api_endpoint": "https://techcrunch.com/wp-json/",
                "rate_limit": 50
            },
            "reuters": {
                "reliability": 0.90,
                "type": "news",
                "api_endpoint": "https://www.reuters.com/",
                "rate_limit": 30
            },
            "company_filings": {
                "reliability": 0.95,
                "type": "official",
                "api_endpoint": "https://www.sec.gov/",
                "rate_limit": 20
            }
        }
    
    async def search_sources(self, query: str, claim_type: str) -> List[Dict[str, Any]]:
        """Search across multiple sources for claim verification"""
        
        # Simulate API calls to different sources
        search_tasks = []
        
        # Determine which sources to query based on claim type
        relevant_sources = self._get_relevant_sources(claim_type)
        
        for source_name in relevant_sources:
            task = self._search_single_source(source_name, query)
            search_tasks.append(task)
        
        results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        # Filter out exceptions and combine results
        valid_results = []
        for i, result in enumerate(results):
            if not isinstance(result, Exception) and result:
                source_name = relevant_sources[i]
                result['source'] = source_name
                result['reliability'] = self.sources[source_name]['reliability']
                valid_results.append(result)
        
        return valid_results
    
    def _get_relevant_sources(self, claim_type: str) -> List[str]:
        """Determine which sources are most relevant for a claim type"""
        source_mapping = {
            'date': ['wikipedia', 'apple_press', 'techcrunch', 'reuters'],
            'number': ['company_filings', 'reuters', 'techcrunch'],
            'entity': ['wikipedia', 'apple_press', 'company_filings'],
            'fact': ['wikipedia', 'reuters', 'techcrunch', 'apple_press']
        }
        
        return source_mapping.get(claim_type, ['wikipedia', 'reuters'])
    
    async def _search_single_source(self, source_name: str, query: str) -> Optional[Dict[str, Any]]:
        """Search a single source (mocked for demo)"""
        
        # Simulate API call delay
        await asyncio.sleep(0.2)
        
        # Mock responses based on source and query
        query_lower = query.lower()
        
        if source_name == "wikipedia":
            return await self._mock_wikipedia_search(query_lower)
        elif source_name == "apple_press":
            return await self._mock_apple_search(query_lower)
        elif source_name == "techcrunch":
            return await self._mock_techcrunch_search(query_lower)
        elif source_name == "reuters":
            return await self._mock_reuters_search(query_lower)
        elif source_name == "company_filings":
            return await self._mock_sec_search(query_lower)
        
        return None
    
    async def _mock_wikipedia_search(self, query: str) -> Optional[Dict[str, Any]]:
        """Mock Wikipedia API response"""
        if 'iphone 16' in query:
            return {
                'title': 'iPhone 16',
                'extract': 'The iPhone 16 is a smartphone designed and marketed by Apple Inc.',
                'url': 'https://en.wikipedia.org/wiki/IPhone_16',
                'confidence': 0.9
            }
        elif 'apple' in query:
            return {
                'title': 'Apple Inc.',
                'extract': 'Apple Inc. is an American multinational technology company.',
                'url': 'https://en.wikipedia.org/wiki/Apple_Inc.',
                'confidence': 0.95
            }
        return None
    
    async def _mock_apple_search(self, query: str) -> Optional[Dict[str, Any]]:
        """Mock Apple Press Release search"""
        if 'iphone 16' in query or 'september 2024' in query:
            return {
                'title': 'Apple Introduces iPhone 16',
                'extract': 'Apple today announced iPhone 16 and iPhone 16 Plus...',
                'url': 'https://www.apple.com/newsroom/2024/09/apple-introduces-iphone-16/',
                'confidence': 0.98,
                'date': '2024-09-12'
            }
        return None
    
    async def _mock_techcrunch_search(self, query: str) -> Optional[Dict[str, Any]]:
        """Mock TechCrunch search"""
        if 'iphone 16' in query:
            return {
                'title': 'iPhone 16 hands-on: Apple\'s latest flagship',
                'extract': 'Apple\'s iPhone 16 brings several new features...',
                'url': 'https://techcrunch.com/2024/09/12/iphone-16-hands-on/',
                'confidence': 0.85
            }
        return None
    
    async def _mock_reuters_search(self, query: str) -> Optional[Dict[str, Any]]:
        """Mock Reuters search"""
        if 'apple' in query and ('sales' in query or 'revenue' in query):
            return {
                'title': 'Apple reports quarterly earnings',
                'extract': 'Apple Inc reported quarterly revenue...',
                'url': 'https://www.reuters.com/business/apple-earnings/',
                'confidence': 0.92
            }
        return None
    
    async def _mock_sec_search(self, query: str) -> Optional[Dict[str, Any]]:
        """Mock SEC filings search"""
        if 'apple' in query:
            return {
                'title': 'Apple Inc. 10-K Annual Report',
                'extract': 'Annual report filed with the Securities and Exchange Commission...',
                'url': 'https://www.sec.gov/edgar/browse/?CIK=320193',
                'confidence': 0.98
            }
        return None
    
    def calculate_overall_confidence(self, source_results: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence based on source reliability and agreement"""
        if not source_results:
            return 0.5
        
        # Weight by source reliability
        total_weight = 0
        weighted_confidence = 0
        
        for result in source_results:
            reliability = result.get('reliability', 0.5)
            confidence = result.get('confidence', 0.5)
            
            weighted_confidence += reliability * confidence
            total_weight += reliability
        
        if total_weight == 0:
            return 0.5
        
        return min(weighted_confidence / total_weight, 0.98)
    
    def determine_status(self, confidence: float, source_count: int) -> str:
        """Determine verification status based on confidence and source count"""
        if confidence >= 0.85 and source_count >= 2:
            return 'verified'
        elif confidence >= 0.70:
            return 'unverified'
        elif confidence < 0.40:
            return 'false'
        else:
            return 'unverified'