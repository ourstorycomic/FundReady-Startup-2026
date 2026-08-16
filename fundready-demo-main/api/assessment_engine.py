from typing import Dict, Any, List, Optional
from .gemini_client import analyze_with_gemini, DOCUMENT_CRITERIA, get_tier
from .financial_calculator import calculate_financial_score

async def run_full_assessment(
    documents: Dict[str, str],
    financials: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    
    doc_scores = {}
    all_strengths = []
    all_weaknesses = []
    all_recommendations = []
    
    for doc_type, content in documents.items():
        if doc_type in DOCUMENT_CRITERIA:
            try:
                analysis = await analyze_with_gemini(doc_type, content)
                weight = DOCUMENT_CRITERIA[doc_type]["weight"]
                weighted_score = (analysis["score"] / 100) * weight
                
                doc_scores[doc_type] = {
                    "name": DOCUMENT_CRITERIA[doc_type]["name"],
                    "score": analysis["score"],
                    "max": 100,
                    "weight": weight,
                    "weighted_score": weighted_score,
                    "breakdown": analysis.get("breakdown", []),
                    "strengths": analysis.get("strengths", []),
                    "weaknesses": analysis.get("weaknesses", []),
                    "recommendations": analysis.get("recommendations", [])
                }
                
                all_strengths.extend(analysis.get("strengths", []))
                all_weaknesses.extend(analysis.get("weakness", []))
                all_recommendations.extend(analysis.get("recommendations", []))
                
            except Exception as e:
                doc_scores[doc_type] = {
                    "name": DOCUMENT_CRITERIA[doc_type]["name"],
                    "score": 0,
                    "error": str(e)
                }
    
    overall_score = sum(d.get("weighted_score", 0) for d in doc_scores.values())
    overall_score = min(100, round(overall_score))
    
    tier = get_tier(overall_score)
    
    financial_result = None
    if financials:
        try:
            financial_result = calculate_financial_score(
                revenue=financials.get("revenue", 0),
                gross_margin=financials.get("gross_margin", 0),
                roe=financials.get("roe", 0),
                current_ratio=financials.get("current_ratio", 1.0),
                debt_to_equity=financials.get("debt_to_equity", 0),
                cash_flow_margin=financials.get("cash_flow_margin", 0)
            )
        except Exception as e:
            financial_result = {"error": str(e)}
    
    completeness = len([d for d in doc_scores.values() if d.get("score", 0) > 0])
    total_docs = len(DOCUMENT_CRITERIA)
    
    return {
        "overall_score": overall_score,
        "tier": tier,
        "completeness": {
            "present": completeness,
            "total": total_docs,
            "percentage": round((completeness / total_docs) * 100, 1)
        },
        "document_scores": doc_scores,
        "financial_analysis": financial_result,
        "summary": {
            "strengths": all_strengths[:5],
            "weaknesses": all_weaknesses[:5],
            "recommendations": all_recommendations[:5]
        }
    }
