const API_BASE_URL = 'http://localhost:8000';

export interface Claim {
  id: string;
  text: string;
  start: number;
  end: number;
  type: 'date' | 'number' | 'entity' | 'fact';
  status: 'verified' | 'unverified' | 'false' | 'pending';
  confidence: number;
  sources?: string[];
  evidence?: string;
}

export interface ClaimExtractionResponse {
  claims: Claim[];
  processing_time: number;
  total_claims: number;
  metadata: {
    text_length: number;
    extraction_method: string;
    verification_sources: number;
  };
}

export interface VerificationResponse {
  claim_id: string;
  status: string;
  confidence: number;
  sources: string[];
  evidence: string;
  updated_at: string;
}

class FactCheckAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async extractClaims(text: string): Promise<ClaimExtractionResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/extract-claims`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error extracting claims:', error);
      throw new Error('Failed to extract claims from text');
    }
  }

  async verifyClaim(claimId: string, claimText: string, claimType: string): Promise<VerificationResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/verify-claim/${claimId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          claim_text: claimText,
          claim_type: claimType 
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error verifying claim:', error);
      throw new Error('Failed to verify claim');
    }
  }

  async getAvailableSources(): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/sources`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching sources:', error);
      throw new Error('Failed to fetch available sources');
    }
  }

  async healthCheck(): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error checking health:', error);
      throw new Error('Failed to check API health');
    }
  }
}

export const factCheckAPI = new FactCheckAPI();