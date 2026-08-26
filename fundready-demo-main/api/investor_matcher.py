import json
import os
import random

def load_funds():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'investment_funds.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading funds: {e}")
        return []

def match_investors(startup_score: int, startup_content: str, desired_amount_str: str, top_n: int = 3):
    funds = load_funds()
    if not funds:
        return []
        
    matched_funds = []
    
    # Rất đơn giản: chấm điểm quỹ nào phù hợp nhất
    for fund in funds:
        match_score = 0
        reasons = []
        
        # 1. Khớp điểm số
        pref_range = fund.get('matching_criteria', {}).get('preferred_score_range', [0, 100])
        if pref_range[0] <= startup_score <= pref_range[1]:
            match_score += 40
            reasons.append("Điểm số doanh nghiệp nằm trong khẩu vị rủi ro của quỹ.")
        elif startup_score > pref_range[1]:
            match_score += 20
            reasons.append("Doanh nghiệp vượt tiêu chuẩn cơ bản của quỹ.")
            
        # 2. Khớp ngành nghề (dùng text search cơ bản trên nội dung startup)
        content_lower = startup_content.lower() if startup_content else ""
        focus_industries = fund.get('focus_industries', [])
        industry_matched = False
        for ind in focus_industries:
            if ind.lower() in content_lower or "agnostic" in ind.lower() or "tech" in content_lower:
                match_score += 30
                reasons.append(f"Ngành nghề phù hợp với danh mục {ind} của quỹ.")
                industry_matched = True
                break
                
        if not industry_matched:
            # Randomize a bit if content is too short
            if len(content_lower) < 50:
                match_score += 15
                reasons.append("Có tiềm năng phù hợp với danh mục đầu tư mở rộng.")
                
        # 3. Randomize remaining score for demo diversity
        match_score += random.randint(0, 30)
        
        matched_funds.append({
            "fund": fund,
            "match_score": min(100, match_score),
            "reasons": reasons
        })
        
    # Sort by score descending
    matched_funds.sort(key=lambda x: x["match_score"], reverse=True)
    
    # Format output
    result = []
    for m in matched_funds[:top_n]:
        fund = m["fund"]
        # Format ticket size to human readable
        min_usd = fund['ticket_size']['min_usd']
        max_usd = fund['ticket_size']['max_usd']
        
        def format_usd(val):
            if val >= 1000000:
                return f"${val/1000000:.1f}M"
            return f"${val/1000:.0f}K"
            
        ticket_str = f"{format_usd(min_usd)} - {format_usd(max_usd)}"
        
        result.append({
            "id": fund["id"],
            "name": fund["name"],
            "type": fund["type"],
            "ticket_size": ticket_str,
            "match_percent": m["match_score"],
            "reason": m["reasons"][0] if m["reasons"] else "Phù hợp với tiêu chí đầu tư chung.",
            "logo_url": fund.get("logo_url", "")
        })
        
    return result
