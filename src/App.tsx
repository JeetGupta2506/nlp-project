import React, { useState, useRef, useCallback } from 'react';
import { CheckCircle, AlertTriangle, HelpCircle, Clock, Edit3, Search, FileText, Zap } from 'lucide-react';

interface Claim {
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

interface VerificationTooltipProps {
  claim: Claim;
  onConfirm: (id: string) => void;
  onCorrect: (id: string) => void;
}

const VerificationTooltip: React.FC<VerificationTooltipProps> = ({ claim, onConfirm, onCorrect }) => {
  const getStatusIcon = () => {
    switch (claim.status) {
      case 'verified': return <CheckCircle className="w-4 h-4 text-emerald-500" />;
      case 'unverified': return <AlertTriangle className="w-4 h-4 text-amber-500" />;
      case 'false': return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case 'pending': return <Clock className="w-4 h-4 text-blue-500" />;
    }
  };

  const getStatusText = () => {
    switch (claim.status) {
      case 'verified': return 'Verified';
      case 'unverified': return 'Unverified';
      case 'false': return 'Possibly False';
      case 'pending': return 'Checking...';
    }
  };

  const getStatusColor = () => {
    switch (claim.status) {
      case 'verified': return 'text-emerald-600';
      case 'unverified': return 'text-amber-600';
      case 'false': return 'text-red-600';
      case 'pending': return 'text-blue-600';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-xl border border-gray-200 p-4 max-w-sm backdrop-blur-sm">
      <div className="flex items-center gap-2 mb-2">
        {getStatusIcon()}
        <span className={`font-medium ${getStatusColor()}`}>{getStatusText()}</span>
        <span className="text-sm text-gray-500">({claim.confidence}% confident)</span>
      </div>
      
      <p className="text-sm text-gray-600 mb-3">
        <strong>Claim:</strong> "{claim.text}"
      </p>
      
      {claim.evidence && (
        <p className="text-sm text-gray-700 mb-3">
          <strong>Evidence:</strong> {claim.evidence}
        </p>
      )}
      
      {claim.sources && claim.sources.length > 0 && (
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-700 mb-1">Sources:</p>
          <ul className="text-xs text-gray-600 space-y-1">
            {claim.sources.map((source, index) => (
              <li key={index} className="flex items-center gap-1">
                <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
                {source}
              </li>
            ))}
          </ul>
        </div>
      )}
      
      <div className="flex gap-2">
        <button
          onClick={() => onConfirm(claim.id)}
          className="flex-1 px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-md text-sm font-medium hover:bg-emerald-100 transition-colors"
        >
          Confirm
        </button>
        <button
          onClick={() => onCorrect(claim.id)}
          className="flex-1 px-3 py-1.5 bg-gray-50 text-gray-700 rounded-md text-sm font-medium hover:bg-gray-100 transition-colors"
        >
          Correct
        </button>
      </div>
    </div>
  );
};

const App: React.FC = () => {
  const [content, setContent] = useState(`Apple announced the iPhone 16 in September 2024, with over 40 million pre-orders in the first week. The device features a new A18 chip and starts at $799. Tim Cook stated that this was their most successful launch to date.`);
  const [claims, setClaims] = useState<Claim[]>([
    {
      id: '1',
      text: 'iPhone 16 in September 2024',
      start: 19,
      end: 45,
      type: 'date',
      status: 'verified',
      confidence: 95,
      sources: ['Apple Press Release', 'TechCrunch'],
      evidence: 'Apple officially announced the iPhone 16 on September 12, 2024.'
    },
    {
      id: '2',
      text: '40 million pre-orders',
      start: 57,
      end: 76,
      type: 'number',
      status: 'unverified',
      confidence: 60,
      sources: ['Industry Reports'],
      evidence: 'Pre-order numbers have not been officially confirmed by Apple.'
    },
    {
      id: '3',
      text: 'A18 chip',
      start: 122,
      end: 130,
      type: 'entity',
      status: 'verified',
      confidence: 98,
      sources: ['Apple Specifications', 'AnandTech'],
      evidence: 'The iPhone 16 series features the new A18 and A18 Pro chips.'
    },
    {
      id: '4',
      text: 'starts at $799',
      start: 135,
      end: 150,
      type: 'number',
      status: 'false',
      confidence: 85,
      sources: ['Apple Store', 'Multiple retailers'],
      evidence: 'The iPhone 16 actually starts at $829, not $799.'
    }
  ]);
  const [hoveredClaim, setHoveredClaim] = useState<string | null>(null);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const [isProcessing, setIsProcessing] = useState(false);
  
  const editorRef = useRef<HTMLTextAreaElement>(null);

  const extractClaims = useCallback(async (text: string) => {
    setIsProcessing(true);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock claim extraction - in reality, this would use NLP
    const mockClaims: Claim[] = [];
    
    // Extract dates
    const dateRegex = /\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b|\b\d{4}\b/gi;
    let match;
    while ((match = dateRegex.exec(text)) !== null) {
      mockClaims.push({
        id: `date-${mockClaims.length}`,
        text: match[0],
        start: match.index,
        end: match.index + match[0].length,
        type: 'date',
        status: Math.random() > 0.5 ? 'verified' : 'unverified',
        confidence: Math.floor(Math.random() * 30) + 70,
        sources: ['Wikipedia', 'News APIs'],
        evidence: `Date information found in reliable sources.`
      });
    }
    
    // Extract numbers
    const numberRegex = /\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:million|billion|thousand|%|dollars?|\$)?\b/gi;
    const numberText = text;
    let numberMatch;
    while ((numberMatch = numberRegex.exec(numberText)) !== null) {
      if (numberMatch[0].length > 2) { // Only significant numbers
        mockClaims.push({
          id: `number-${mockClaims.length}`,
          text: numberMatch[0],
          start: numberMatch.index,
          end: numberMatch.index + numberMatch[0].length,
          type: 'number',
          status: Math.random() > 0.3 ? 'verified' : 'unverified',
          confidence: Math.floor(Math.random() * 40) + 60,
          sources: ['Company Reports', 'Financial Data'],
          evidence: `Numerical claim verification in progress.`
        });
      }
    }
    
    setClaims(mockClaims);
    setIsProcessing(false);
  }, []);

  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setContent(e.target.value);
  };

  const handleAnalyze = () => {
    extractClaims(content);
  };

  const handleClaimHover = (claimId: string, event: React.MouseEvent) => {
    setHoveredClaim(claimId);
    const rect = event.currentTarget.getBoundingClientRect();
    setTooltipPosition({
      x: rect.left + rect.width / 2,
      y: rect.top - 10
    });
  };

  const handleClaimLeave = () => {
    setHoveredClaim(null);
  };

  const confirmClaim = (claimId: string) => {
    setClaims(prev => prev.map(claim => 
      claim.id === claimId ? { ...claim, status: 'verified' as const, confidence: 100 } : claim
    ));
    setHoveredClaim(null);
  };

  const correctClaim = (claimId: string) => {
    setClaims(prev => prev.filter(claim => claim.id !== claimId));
    setHoveredClaim(null);
  };

  const getClaimHighlight = (claim: Claim) => {
    switch (claim.status) {
      case 'verified': return 'bg-emerald-100 border-b-2 border-emerald-400';
      case 'unverified': return 'bg-amber-100 border-b-2 border-amber-400';
      case 'false': return 'bg-red-100 border-b-2 border-red-400';
      case 'pending': return 'bg-blue-100 border-b-2 border-blue-400';
    }
  };

  const renderHighlightedContent = () => {
    if (claims.length === 0) return content;
    
    let highlightedContent = content;
    const sortedClaims = [...claims].sort((a, b) => b.start - a.start);
    
    sortedClaims.forEach(claim => {
      const before = highlightedContent.slice(0, claim.start);
      const claimText = highlightedContent.slice(claim.start, claim.end);
      const after = highlightedContent.slice(claim.end);
      
      highlightedContent = before + 
        `<span class="${getClaimHighlight(claim)} cursor-pointer px-1 rounded-sm transition-all duration-200 hover:shadow-md" data-claim-id="${claim.id}">${claimText}</span>` + 
        after;
    });
    
    return highlightedContent;
  };

  const getVerificationStats = () => {
    const total = claims.length;
    const verified = claims.filter(c => c.status === 'verified').length;
    const unverified = claims.filter(c => c.status === 'unverified').length;
    const false_ = claims.filter(c => c.status === 'false').length;
    
    return { total, verified, unverified, false: false_ };
  };

  const stats = getVerificationStats();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200/50 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <Search className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">FactCheck Pro</h1>
                <p className="text-sm text-gray-600">Intelligent claim verification</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              {stats.total > 0 && (
                <div className="flex items-center gap-4 text-sm">
                  <div className="flex items-center gap-1">
                    <CheckCircle className="w-4 h-4 text-emerald-500" />
                    <span className="font-medium text-emerald-700">{stats.verified}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                    <span className="font-medium text-amber-700">{stats.unverified}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <AlertTriangle className="w-4 h-4 text-red-500" />
                    <span className="font-medium text-red-700">{stats.false}</span>
                  </div>
                </div>
              )}
              
              <button
                onClick={handleAnalyze}
                disabled={isProcessing}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg font-medium transition-colors duration-200"
              >
                {isProcessing ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4" />
                    Analyze Claims
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Editor */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200/50 overflow-hidden">
              <div className="border-b border-gray-100 px-6 py-4">
                <div className="flex items-center gap-2">
                  <Edit3 className="w-5 h-5 text-gray-400" />
                  <h2 className="font-semibold text-gray-900">Content Editor</h2>
                </div>
              </div>
              
              <div className="p-6">
                <div className="space-y-4">
                  <textarea
                    ref={editorRef}
                    value={content}
                    onChange={handleContentChange}
                    placeholder="Paste your content here to verify claims..."
                    className="w-full h-64 p-4 border border-gray-200 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-300 transition-colors duration-200"
                  />
                  
                  {claims.length > 0 && (
                    <div className="border-t pt-4">
                      <h3 className="font-medium text-gray-900 mb-3">Verified Content Preview</h3>
                      <div 
                        className="p-4 bg-gray-50 rounded-xl border leading-relaxed"
                        dangerouslySetInnerHTML={{ __html: renderHighlightedContent() }}
                        onMouseOver={(e) => {
                          const target = e.target as HTMLElement;
                          const claimId = target.getAttribute('data-claim-id');
                          if (claimId) {
                            handleClaimHover(claimId, e as any);
                          }
                        }}
                        onMouseLeave={handleClaimLeave}
                      />
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Legend */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200/50 p-6">
              <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Verification Legend
              </h3>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-4 h-2 bg-emerald-100 border-b-2 border-emerald-400 rounded-sm"></div>
                  <span className="text-sm text-gray-700">Verified claims</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-4 h-2 bg-amber-100 border-b-2 border-amber-400 rounded-sm"></div>
                  <span className="text-sm text-gray-700">Unverified claims</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-4 h-2 bg-red-100 border-b-2 border-red-400 rounded-sm"></div>
                  <span className="text-sm text-gray-700">Possibly false</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-4 h-2 bg-blue-100 border-b-2 border-blue-400 rounded-sm"></div>
                  <span className="text-sm text-gray-700">Checking...</span>
                </div>
              </div>
            </div>

            {/* Claims List */}
            {claims.length > 0 && (
              <div className="bg-white rounded-2xl shadow-sm border border-gray-200/50 p-6">
                <h3 className="font-semibold text-gray-900 mb-4">Detected Claims</h3>
                <div className="space-y-3">
                  {claims.map(claim => (
                    <div
                      key={claim.id}
                      className="p-3 border border-gray-100 rounded-lg hover:border-gray-200 transition-colors duration-200 cursor-pointer"
                      onMouseEnter={(e) => handleClaimHover(claim.id, e)}
                      onMouseLeave={handleClaimLeave}
                    >
                      <div className="flex items-start gap-2">
                        {claim.status === 'verified' && <CheckCircle className="w-4 h-4 text-emerald-500 mt-0.5" />}
                        {claim.status === 'unverified' && <AlertTriangle className="w-4 h-4 text-amber-500 mt-0.5" />}
                        {claim.status === 'false' && <AlertTriangle className="w-4 h-4 text-red-500 mt-0.5" />}
                        {claim.status === 'pending' && <Clock className="w-4 h-4 text-blue-500 mt-0.5" />}
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            "{claim.text}"
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            {claim.confidence}% confidence • {claim.type}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Quick Tips */}
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl border border-blue-100 p-6">
              <h3 className="font-semibold text-blue-900 mb-3">💡 Quick Tips</h3>
              <ul className="text-sm text-blue-800 space-y-2">
                <li>• Hover over highlighted claims to see verification details</li>
                <li>• Green highlights indicate verified facts</li>
                <li>• Yellow highlights need further verification</li>
                <li>• Red highlights may contain inaccuracies</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Tooltip */}
      {hoveredClaim && (
        <div
          className="fixed z-50 pointer-events-auto"
          style={{
            left: tooltipPosition.x - 150,
            top: tooltipPosition.y - 10,
            transform: 'translateY(-100%)'
          }}
        >
          <VerificationTooltip
            claim={claims.find(c => c.id === hoveredClaim)!}
            onConfirm={confirmClaim}
            onCorrect={correctClaim}
          />
        </div>
      )}
    </div>
  );
};

export default App;