import json
import os
from typing import Dict, List, Tuple, Any
from difflib import SequenceMatcher
from .gemini_client import analyze_input_with_framework

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_profiles() -> List[Dict]:
    profiles = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                profiles.append(json.load(f))
    return profiles

def extract_keywords(text: str) -> Dict[str, int]:
    text_lower = text.lower()
    
    industry_keywords = {
        "agritech": ["nông nghiệp", "agri", "farm", "trang trại", "crop", "thủy sản"],
        "edtech": ["giáo dục", "education", "học", "training", "school", "university"],
        "healthtech": ["y tế", "health", "medical", "bệnh viện", "clinic", "pharma"],
        "logistics": ["logistics", "vận tải", "shipping", "warehouse", "delivery"],
        "manufacturing": ["sản xuất", "manufacturing", "factory", "nhà máy", "gia công"],
        "saas": ["saas", "software", "phần mềm", "platform", "subscription"]
    }
    
    stage_keywords = {
        "seed": ["mới thành lập", "mvp", "ý tưởng", "idea", "sớm", "early", "< 1 năm"],
        "series_a": ["series a", "tăng trưởng", "growth", "1-3 năm", "traction"],
        "series_b": ["series b", "mở rộng", "scale", "regional", "3-5 năm"],
        "enterprise": ["ipo", "public", "enterprise", "lớn", "mature", "> 5 năm"],
        "sme": ["sme", "vừa và nhỏ", "hộ kinh doanh", "gia đình", "truyền thống"]
    }
    
    financial_keywords = {
        "revenue_high": ["doanh thu lớn", "arr cao", "> 50 tỷ", "profitable", "có lãi"],
        "revenue_medium": ["doanh thu trung bình", "10-50 tỷ", "đang tăng trưởng"],
        "revenue_low": ["doanh thu nhỏ", "< 10 tỷ", "pre-revenue", "chưa có doanh thu"],
        "burn_rate": ["burn rate", "đốt tiền", "âm dòng tiền", "negative cash flow"],
        "positive_cashflow": ["dòng tiền dương", "positive cash flow", "tự tài trợ"]
    }
    
    scores = {}
    
    for category, keywords in industry_keywords.items():
        scores[f"industry_{category}"] = sum(1 for kw in keywords if kw in text_lower)
    
    for category, keywords in stage_keywords.items():
        scores[f"stage_{category}"] = sum(1 for kw in keywords if kw in text_lower)
    
    for category, keywords in financial_keywords.items():
        scores[f"financial_{category}"] = sum(1 for kw in keywords if kw in text_lower)
    
    return scores

def calculate_similarity(input_text: str, profile: Dict) -> float:
    score = 0.0
    
    input_keywords = extract_keywords(input_text)
    
    metadata = profile.get("metadata", {})
    industry = metadata.get("industry", "").lower()
    stage = metadata.get("stage", "").lower()
    
    for key, value in input_keywords.items():
        if key.startswith("industry_"):
            industry_type = key.replace("industry_", "")
            if industry_type in industry:
                score += value * 10
        
        elif key.startswith("stage_"):
            stage_type = key.replace("stage_", "")
            if stage_type in stage:
                score += value * 8
        
        elif key.startswith("financial_"):
            score += value * 3
    
    summary = profile.get("analysis", {}).get("summary", "").lower()
    text_similarity = SequenceMatcher(None, input_text.lower(), summary).ratio()
    score += text_similarity * 20
    
    total_score = profile.get("score", {}).get("total", 0)
    if "sớm" in input_text.lower() or "seed" in input_text.lower():
        if total_score < 50:
            score += 5
    elif "hoàn chỉnh" in input_text.lower() or "enterprise" in input_text.lower():
        if total_score > 80:
            score += 5
    
    return score

def find_best_match(input_text: str, top_n: int = 3) -> List[Dict[str, Any]]:
    profiles = load_profiles()
    
    matches = []
    for profile in profiles:
        similarity = calculate_similarity(input_text, profile)
        matches.append({
            "profile": profile,
            "similarity_score": similarity
        })
    
    matches.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    results = []
    for match in matches[:top_n]:
        profile = match["profile"]
        metadata = profile.get("metadata", {})
        results.append({
            "profile_id": profile.get("profile_id", "unknown"),
            "company_name": metadata.get("company_name", "Unknown"),
            "industry": metadata.get("industry", "Unknown"),
            "stage": metadata.get("stage", "Unknown"),
            "total_score": profile.get("score", {}).get("total", 0),
            "grade": profile.get("score", {}).get("grade", "Unknown"),
            "similarity_score": round(match["similarity_score"], 2),
            "summary": profile.get("analysis", {}).get("summary", ""),
            "key_metrics": {
                "arr": profile.get("analysis", {}).get("financial_ratios", {}).get("gross_margin"),
                "growth_rate": profile.get("kpis", [{}])[0].get("target") if profile.get("kpis") else None
            }
        })
    
    return results

async def analyze_with_reference(input_text: str) -> Dict[str, Any]:
    """
    Phân tích input text của user bằng Gemini API dựa trên framework từ profile mẫu.
    Không copy dữ liệu mẫu, mà dùng AI phân tích thật.
    """
    matches = find_best_match(input_text, top_n=1)
    
    if not matches:
        return {
            "error": "Không tìm thấy profile phù hợp",
            "suggestion": "Vui lòng cung cấp thêm thông tin về doanh nghiệp"
        }
    
    best_match = matches[0]
    profile_id = best_match.get("profile_id")
    
    if not profile_id or profile_id == "unknown":
        return {
            "error": "Không tìm thấy profile phù hợp",
            "suggestion": "Vui lòng cung cấp thêm thông tin về doanh nghiệp"
        }
    
    profile_path = os.path.join(DATA_DIR, f"{profile_id}.json")
    
    if not os.path.exists(profile_path):
        return {
            "error": f"Profile {profile_id} không tồn tại",
            "suggestion": "Vui lòng thử lại với mô tả khác"
        }
    
    with open(profile_path, "r", encoding="utf-8") as f:
        framework_profile = json.load(f)
    
    # Gọi Gemini API để phân tích input dựa trên framework mẫu
    try:
        ai_result = await analyze_input_with_framework(input_text, framework_profile)
        
        # Cập nhật matched_profile với kết quả từ AI
        matched_profile = {
            "profile_id": profile_id,
            "company_name": best_match.get("company_name", "Doanh nghiệp của bạn"),
            "industry": best_match.get("industry", "N/A"),
            "stage": best_match.get("stage", "N/A"),
            "total_score": ai_result.get("total_score", 50),
            "grade": ai_result.get("grade", "Tier 2 - Cần cải thiện"),
            "similarity_score": best_match.get("similarity_score", 0),
            "summary": ai_result.get("summary", "Không có thông tin")
        }
        
        return {
            "matched_profile": matched_profile,
            "full_analysis": {
                "score": {
                    "total": ai_result.get("total_score", 50),
                    "grade": ai_result.get("grade", "Tier 2 - Cần cải thiện"),
                    "breakdown": ai_result.get("score_breakdown", [])
                },
                "analysis": ai_result.get("detailed_analysis", {}),
                "recommendations": ai_result.get("recommendations", []),
                "risks": ai_result.get("risks", []),
                "kpis": ai_result.get("kpis", [])
            },
            "comparison_note": f"AI đã phân tích doanh nghiệp của bạn dựa trên framework tham chiếu từ {best_match.get('company_name', 'N/A')} ({best_match.get('similarity_score', 0)}% tương đồng).",
            "score_breakdown": ai_result.get("score_breakdown", []),
            "detailed_analysis": ai_result.get("detailed_analysis", {}),
            "recommendations": ai_result.get("recommendations", []),
            "risks": ai_result.get("risks", []),
            "kpis": ai_result.get("kpis", []),
            "references": framework_profile.get("references", [])
        }
        
    except Exception as e:
        print(f"ERROR calling Gemini API: {e}")
        # Fallback: trả về dữ liệu mẫu nếu Gemini API lỗi
        return {
            "matched_profile": best_match,
            "full_analysis": framework_profile,
            "comparison_note": f"Lỗi AI: {str(e)}. Đang hiển thị dữ liệu tham chiếu từ {best_match.get('company_name', 'N/A')}.",
            "score_breakdown": framework_profile.get("score", {}).get("breakdown", []),
            "detailed_analysis": framework_profile.get("analysis", {}),
            "recommendations": framework_profile.get("recommendations", []),
            "risks": framework_profile.get("risks", []),
            "kpis": framework_profile.get("kpis", []),
            "references": framework_profile.get("references", [])
        }
