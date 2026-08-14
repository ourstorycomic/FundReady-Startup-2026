import json
import glob
import os
import difflib

# In-memory store for our 6 sample profiles
PROFILES = []

def load_profiles():
    global PROFILES
    if PROFILES:
        return
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    for filepath in glob.glob(os.path.join(data_dir, "*.json")):
        with open(filepath, "r", encoding="utf-8") as f:
            profile = json.load(f)
            # Make sure profile_id is mapped (some might have it in metadata, fixing based on DAY2_SUMMARY)
            if "profile_id" not in profile and "metadata" in profile:
                profile["profile_id"] = profile["metadata"].get("profile_id", os.path.basename(filepath).replace(".json", ""))
            PROFILES.append(profile)

def extract_keywords(text: str) -> list:
    # A simple keyword extractor based on the README description
    text = text.lower()
    keywords = []
    # Industry
    for ind in ["agritech", "edtech", "healthtech", "logistics", "manufacturing", "saas", "nông nghiệp", "giáo dục", "y tế", "sản xuất"]:
        if ind in text:
            keywords.append(ind)
    # Stage
    for stage in ["seed", "series a", "series b", "enterprise", "sme", "mới thành lập", "startup", "chuyển đổi số"]:
        if stage in text:
            keywords.append(stage)
    # Financial
    for fin in ["arr", "doanh thu", "khách hàng", "dòng tiền"]:
        if fin in text:
            keywords.append(fin)
    return keywords

def find_best_match(description: str, top_n: int = 3) -> list:
    load_profiles()
    desc_lower = description.lower()
    input_keywords = extract_keywords(desc_lower)
    
    scored_profiles = []
    for p in PROFILES:
        # Get profile text to compare
        p_summary = p.get("summary", "")
        if not p_summary and "analysis" in p:
            p_summary = str(p.get("analysis"))
            
        # 1. Text similarity using difflib
        similarity = difflib.SequenceMatcher(None, desc_lower, p_summary.lower()).ratio() * 100
        
        # 2. Keyword boost
        p_keywords = extract_keywords(p_summary.lower())
        overlap = set(input_keywords).intersection(set(p_keywords))
        keyword_boost = len(overlap) * 5  # 5% boost per matching keyword category
        
        # Total similarity score
        final_similarity = round(similarity + keyword_boost, 2)
        
        # Cap at 100%
        final_similarity = min(final_similarity, 100.0)
        
        scored_profiles.append({
            "profile_id": p.get("profile_id", ""),
            "company_name": p.get("company_name", p.get("metadata", {}).get("company_name", "Unknown")),
            "industry": p.get("industry", "Unknown"),
            "stage": p.get("stage", "Unknown"),
            "total_score": p.get("score", {}).get("total_score", p.get("total_score", 0)),
            "grade": p.get("score", {}).get("grade", p.get("grade", "N/A")),
            "similarity_score": final_similarity,
            "summary": p_summary[:200] + "..." if len(p_summary) > 200 else p_summary,
            "_raw": p # Keep raw for full analysis
        })
    
    # Sort by similarity_score descending
    scored_profiles.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored_profiles[:top_n]

def analyze_with_reference(description: str) -> dict:
    top_matches = find_best_match(description, top_n=1)
    if not top_matches:
        return {}
        
    best_match = top_matches[0]
    raw_profile = best_match.pop("_raw")
    
    return {
        "matched_profile": best_match,
        "full_analysis": {
            "score": raw_profile.get("score", {}),
            "analysis": raw_profile.get("analysis", {}),
            "recommendations": raw_profile.get("recommendations", []),
            "risks": raw_profile.get("risks", [])
        },
        "comparison_note": f"Doanh nghiệp của bạn có đặc điểm tương đồng với {best_match['company_name']} ({best_match['similarity_score']}%). Đây là bản phân tích tham chiếu."
    }
