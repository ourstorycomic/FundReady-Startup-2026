from typing import Dict, Any, List

def band_score(value: float, bands: List[tuple]) -> float:
    sorted_bands = sorted(bands, key=lambda x: x[0], reverse=True)
    for threshold, score in sorted_bands:
        if value >= threshold:
            return score
    return 0

def calculate_financial_score(
    revenue: float,
    gross_margin: float,
    roe: float,
    current_ratio: float,
    debt_to_equity: float,
    cash_flow_margin: float
) -> Dict[str, Any]:
    
    growth_bands = [
        (100000, 20), (50000, 16), (20000, 12), (10000, 8), (5000, 4), (0, 0)
    ]
    margin_bands = [
        (70, 20), (50, 16), (30, 12), (20, 8), (10, 4), (0, 0)
    ]
    roe_bands = [
        (25, 20), (20, 16), (15, 12), (10, 8), (5, 4), (0, 0)
    ]
    current_bands = [
        (2.0, 15), (1.5, 12), (1.2, 9), (1.0, 6), (0.8, 3), (0, 0)
    ]
    debt_bands = [
        (0, 15), (0.5, 12), (1.0, 9), (1.5, 6), (2.0, 3), (999, 0)
    ]
    cf_bands = [
        (20, 15), (15, 12), (10, 9), (5, 6), (0, 3), (-999, 0)
    ]
    
    capital_score = band_score(revenue, growth_bands)
    position_score = band_score(gross_margin, margin_bands) + band_score(roe, roe_bands)
    cashflow_score = band_score(cash_flow_margin, cf_bands)
    governance_score = 15
    legal_score = 15
    valuation_score = 15
    
    total = min(100, capital_score + position_score + cashflow_score + governance_score + legal_score + valuation_score)
    
    ratios = {
        "gross_margin": f"{gross_margin}%",
        "roe": f"{roe}%",
        "current_ratio": f"{current_ratio}x",
        "debt_to_equity": f"{debt_to_equity}x",
        "cash_flow_margin": f"{cash_flow_margin}%"
    }
    
    risks = []
    if gross_margin < 30:
        risks.append({"severity": "High", "message": "Biên lợi nhuận gộp thấp (<30%)"})
    if roe < 10:
        risks.append({"severity": "High", "message": "ROE thấp (<10%)"})
    if current_ratio < 1.2:
        risks.append({"severity": "Critical", "message": "Thanh khoản yếu (Current ratio < 1.2)"})
    if debt_to_equity > 1.5:
        risks.append({"severity": "High", "message": "Đòn bẩy tài chính cao (D/E > 1.5)"})
    if cash_flow_margin < 5:
        risks.append({"severity": "Medium", "message": "Dòng tiền yếu (<5%)"})
    
    recommendations = []
    if gross_margin < 50:
        recommendations.append("Cải thiện biên lợi nhuận gộp lên ≥50%")
    if roe < 20:
        recommendations.append("Tăng ROE lên ≥20% qua tối ưu chi phí")
    if current_ratio < 2.0:
        recommendations.append("Tăng thanh khoản lên ≥2.0x")
    if debt_to_equity > 1.0:
        recommendations.append("Giảm nợ, đưa D/E về ≤1.0x")
    
    return {
        "total_score": total,
        "max_score": 100,
        "breakdown": {
            "capital_structure": {"score": capital_score, "max": 20},
            "financial_position": {"score": position_score, "max": 40},
            "cash_flow": {"score": cashflow_score, "max": 15},
            "governance": {"score": governance_score, "max": 15},
            "legal_compliance": {"score": legal_score, "max": 15},
            "valuation": {"score": valuation_score, "max": 15}
        },
        "ratios": ratios,
        "risks": risks,
        "recommendations": recommendations
    }
