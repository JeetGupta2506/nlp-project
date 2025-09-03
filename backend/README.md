# FactCheck Pro Backend

A FastAPI-based backend service for intelligent fact-checking and claim verification.

## Features

- **Advanced Claim Extraction**: NLP-powered extraction of dates, numbers, entities, and factual statements
- **Multi-Source Verification**: Verification against Wikipedia, news APIs, company sources, and SEC filings
- **Confidence Scoring**: Intelligent confidence calculation based on source reliability and agreement
- **Real-time Processing**: Fast claim extraction and verification pipeline
- **RESTful API**: Clean, documented API endpoints for frontend integration

## Architecture

### Core Services

1. **NLP Extractor** (`services/nlp_extractor.py`)
   - Pattern-based claim extraction
   - Context analysis
   - Overlap resolution

2. **Claim Verifier** (`services/claim_verifier.py`)
   - Multi-source verification logic
   - Confidence calculation
   - Evidence compilation

3. **Source Manager** (`services/source_manager.py`)
   - Source reliability management
   - API integration framework
   - Result aggregation

## API Endpoints

### POST /extract-claims
Extract and verify claims from text input.

**Request:**
```json
{
  "text": "Apple announced the iPhone 16 in September 2024..."
}
```

**Response:**
```json
{
  "claims": [...],
  "processing_time": 1.23,
  "total_claims": 4,
  "metadata": {...}
}
```

### POST /verify-claim/{claim_id}
Re-verify a specific claim with updated parameters.

### GET /sources
Get available verification sources and their reliability scores.

### GET /health
Health check endpoint for monitoring.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## Production Enhancements

For production deployment, consider adding:

- **spaCy or Transformers**: Advanced NLP models for better claim extraction
- **Vector Database**: For semantic search and retrieval
- **Redis Cache**: For caching verification results
- **Rate Limiting**: To prevent API abuse
- **Authentication**: JWT-based user authentication
- **Monitoring**: Logging and metrics collection
- **Database**: PostgreSQL for persistent storage

## Development

The current implementation uses mock data and simplified patterns. In production:

1. Replace regex patterns with trained NLP models
2. Integrate real APIs (Wikipedia, news sources, etc.)
3. Add vector similarity search for claim matching
4. Implement sophisticated confidence algorithms
5. Add user feedback learning mechanisms