# -*- coding: utf-8 -*-
from groq import Groq
import os
import json
from typing import Dict, Any, List
import hashlib
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables first
load_dotenv(override=True)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Cache directory
if os.environ.get('VERCEL'):
    CACHE_DIR = Path('/tmp/cache')
else:
    CACHE_DIR = Path(__file__).parent / "cache"

try:
    CACHE_DIR.mkdir(exist_ok=True)
except OSError:
    pass

DOCUMENT_CRITERIA = {
    "hsgt": {
        "name": "Hồ sơ giới thiệu",
        "weight": 6,
        "criteria": [
            {"name": "Tổng quan doanh nghiệp và mô hình kinh doanh", "max": 10},
            {"name": "Vấn đề thị trường và giải pháp", "max": 20},
            {"name": "Thị trường và khách hàng mục tiêu", "max": 15},
            {"name": "Chỉ số tăng trưởng và lợi thế cạnh tranh", "max": 35},
            {"name": "Mô hình doanh thu và nhu cầu gọi vốn", "max": 20}
        ]
    },
    "pitchdeck": {
        "name": "Pitch Deck",
        "weight": 9,
        "criteria": [
            {"name": "Vấn đề và Giải pháp", "max": 15},
            {"name": "Thị trường mục tiêu và Cơ hội", "max": 15},
            {"name": "Sản phẩm và Lợi thế cạnh tranh", "max": 15},
            {"name": "Chỉ số tăng trưởng và Tài chính", "max": 20},
            {"name": "Năng lực đội ngũ sáng lập", "max": 15},
            {"name": "Dự báo tài chính và Mô hình lợi nhuận", "max": 10},
            {"name": "Nhu cầu gọi vốn, Phân bổ vốn và Lộ trình", "max": 10}
        ]
    },
    "financial": {
        "name": "Báo cáo tài chính",
        "weight": 9,
        "criteria": [
            {"name": "Tính minh bạch và tuân thủ chuẩn mực kế toán", "max": 15},
            {"name": "Cơ cấu tài sản và mức độ an toàn tài chính", "max": 15},
            {"name": "Cấu trúc nguồn vốn và đòn bẩy tài chính", "max": 20},
            {"name": "Hiệu quả kinh doanh và khả năng sinh lời", "max": 20},
            {"name": "Quản trị dòng tiền và khả năng thanh khoản", "max": 15},
            {"name": "Chính sách phân phối lợi nhuận", "max": 15}
        ]
    },
    "captable": {
        "name": "Cap Table",
        "weight": 6,
        "criteria": [
            {"name": "Cấu trúc sở hữu Founders", "max": 30},
            {"name": "Quỹ cổ phần nhân viên (ESOP)", "max": 20},
            {"name": "Lịch trình chuyển giao cổ phần (Vesting)", "max": 20},
            {"name": "Lịch sử gọi vốn & Pha loãng", "max": 15},
            {"name": "Tính minh bạch & Công cụ đầu tư nợ", "max": 15}
        ]
    },
    "legal": {
        "name": "Hồ sơ pháp lý",
        "weight": 6,
        "criteria": [
            {"name": "Cấu trúc pháp lý thành lập", "max": 15},
            {"name": "Cơ cấu quản trị doanh nghiệp và cổ đông", "max": 15},
            {"name": "Quản trị lao động và tuân thủ pháp lý nhân sự", "max": 20},
            {"name": "Khung bảo vệ dữ liệu và pháp lý an ninh mạng", "max": 20},
            {"name": "Quản trị rủi ro pháp lý đối tác", "max": 15},
            {"name": "Chính sách rà soát và kiểm soát tuân thủ", "max": 15}
        ]
    }
}

def get_cache_key(content: str) -> str:
    """Generate cache key from content"""
    return hashlib.md5(content.encode()).hexdigest()

def get_cached_result(cache_key: str) -> Dict[str, Any]:
    """Get cached result if exists"""
    cache_file = CACHE_DIR / f"{cache_key}.json"
    if cache_file.exists():
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def cache_result(cache_key: str, result: Dict[str, Any]) -> None:
    """Cache analysis result"""
    cache_file = CACHE_DIR / f"{cache_key}.json"
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

def calculate_base_score(content: str, document_type: str) -> Dict[str, Any]:
    """
    Rule-based scoring (không tốn API).
    Phân tích cơ bản dựa trên keywords và độ dài.
    """
    content_lower = content.lower()
    content_length = len(content)
    
    # Base score theo độ dài và độ phức tạp
    base_score = min(30, content_length // 100)
    
    # Keyword detection
    keywords = {
        "doanh thu": ["doanh thu", "revenue", "arr", "mrr"],
        "tăng trưởng": ["tăng trưởng", "growth", "yoy", "mom"],
        "khách hàng": ["khách hàng", "customer", "user", "client"],
        "tài chính": ["tài chính", "financial", "báo cáo", "bctc"],
        "pháp lý": ["pháp lý", "legal", "giấy phép", "đkkd"],
        "đội ngũ": ["đội ngũ", "team", "founder", "nhân sự"]
    }
    
    detected_keywords = {}
    for category, words in keywords.items():
        count = sum(1 for word in words if word in content_lower)
        detected_keywords[category] = count
        if count > 0:
            base_score += 5
    
    # Create breakdown
    doc_info = DOCUMENT_CRITERIA.get(document_type, DOCUMENT_CRITERIA["pitchdeck"])
    breakdown = []
    for criterion in doc_info["criteria"]:
        score = int(criterion["max"] * (base_score / 100))
        breakdown.append({
            "name": criterion["name"],
            "score": score,
            "max": criterion["max"],
            "reason": "Đang phân tích chi tiết..."
        })
    
    return {
        "score": min(base_score, 100),
        "breakdown": breakdown,
        "detected_keywords": detected_keywords
    }

async def analyze_with_groq(document_type: str, content: str, desired_amount: str = "Tùy chọn") -> Dict[str, Any]:
    """Hybrid: Rule-based + Groq AI (chỉ khi cần)"""
    
    # Check cache first
    cache_key = get_cache_key(content)
    cached = get_cached_result(cache_key)
    if cached:
        print(f"Cache hit for {document_type}")
        return cached
    
    # Step 1: Rule-based scoring (free)
    base_result = calculate_base_score(content, document_type)
    
    # Step 2: Chỉ gọi AI nếu cần qualitative analysis
    if base_result["score"] < 20 or len(content) < 50:
        # Không đủ thông tin, trả về base result
        result = {
            "score": base_result["score"],
            "breakdown": base_result["breakdown"],
            "strengths": ["Thông tin hạn chế"],
            "weaknesses": ["Cần bổ sung thêm chi tiết"],
            "recommendations": ["Cung cấp thêm thông tin chi tiết"],
            "risk_if_missing": "Thiếu tài liệu quan trọng",
            "risk_if_weak": "Tài liệu không đủ chi tiết"
        }
        cache_result(cache_key, result)
        return result
    
    # Step 3: Gọi Groq API cho qualitative analysis
    doc_info = DOCUMENT_CRITERIA.get(document_type, DOCUMENT_CRITERIA["pitchdeck"])
    criteria_text = "\n".join([
        f"- {c['name']} (tối đa {c['max']} điểm)" 
        for c in doc_info["criteria"]
    ])
    
    prompt = f"""Bạn là **Chuyên gia Thẩm định Đầu tư Cấp cao** với 15+ năm kinh nghiệm tại các quỹ VC hàng đầu Việt Nam và Đông Nam Á. Bạn đã tham gia thẩm định hơn 500 startup và tư vấn cho các quỹ như Do Ventures, Golden Gate Ventures, Jungle Ventures.

**PHONG CÁCH PHÂN TÍCH BẮT BUỘC:**
- Dùng ngôn ngữ CHUYÊN NGHIỆP, SẮC BÉN của dân đầu tư
- Đưa ra nhận định DỨT KHOÁT, KHÔNG CHUNG CHUNG, VIẾT RẤT DÀI VÀ CỰC KỲ CHI TIẾT
- Mỗi điểm phải có BẰNG CHỨNG CỤ THỂ từ tài liệu
- Dùng số liệu THỰC TẾ, so sánh benchmark ngành
- Phân tích sâu theo framework: Strengths -> Risks -> Opportunities -> Recommendations

**NHIỆM VỤ:**
Phân tích tài liệu "{doc_info['name']}" theo bộ tiêu chí chuyên gia:

{criteria_text}

**NỘI DUNG TÀI LIỆU:**
{content[:4000]}

**YÊU CẦU TRẢ LỜI (JSON format) - BẮT BUỘC PHẢI RẤT DÀI, CHI TIẾT VÀ BỔ SUNG TẤT CẢ THÔNG TIN QUAN TRỌNG:**
{{
  "score": <điểm 0-100>,
  "breakdown": [
    {{
      "name": "<tên tiêu chí>",
      "score": <điểm cụ thể>,
      "max": <điểm tối đa>,
      "reason": "<PHÂN TÍCH SẮC BÉN CỰC KỲ CHI TIẾT TỐI THIỂU 250 CHỮ. Trích dẫn số liệu cụ thể. So sánh benchmark. Dùng thuật ngữ chuyên môn>"
    }}
  ],
  "strengths": [
    "<điểm mạnh 1: CỤ THỂ, phân tích cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể, có số liệu chứng minh từ tài liệu>",
    "<điểm mạnh 2: INSIGHT SÂU mà người thường không thấy, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<điểm mạnh 3: LỢI THẾ CẠNH TRANH, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>"
  ],
  "weaknesses": [
    "<điểm yếu 1: CHỈ RA RỦI RO CỤ THỂ, có số liệu, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<điểm yếu 2: PHÂN TÍCH TÁC ĐỘNG tài chính và chiến lược, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<điểm yếu 3: SO SÁNH BENCHMARK, chỉ ra gap, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>"
  ],
  "recommendations": [
    "<khuyến nghị 1: ACTION ITEM CỤ THỂ, có timeline rõ ràng, phân tích cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<khuyến nghị 2: CHIẾN LƯỢC DÀI HẠN, có mục tiêu định lượng, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<khuyến nghị 3: TỐI ƯU HÓA, có KPI cụ thể, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>"
  ],
  "funding_scenario": {{
    "desired_amount": "<Số tiền doanh nghiệp mong muốn, lấy từ {desired_amount} hoặc suy luận>",
    "recommended_amount": "<Số tiền hệ thống khuyến nghị để đạt hiệu quả cao nhất (Vd: 5 tỷ, 10 tỷ)>",
    "rationale": {{
      "why_recommended": "<PHÂN TÍCH SẮC BÉN VÀ DÀI (Ít nhất 300 chữ, mổ xẻ mọi góc độ): Tại sao hệ thống đề xuất mức này? Phân tích sự chênh lệch so với mức mong muốn. Rủi ro nếu chỉ gọi mức mong muốn là gì?>",
      "investment_needs": [
        "<Nhu cầu cốt lõi 1 (Vd: Nâng cấp công nghệ và AI)>",
        "<Nhu cầu cốt lõi 2>",
        "<Nhu cầu cốt lõi 3>"
      ]
    }},
    "scenarios": [
      {{
        "name": "<Tên Kịch Bản (Vd: Phương án A - Tập trung tối ưu sản phẩm)>",
        "focus_explanation": "<PHÂN TÍCH SÂU (Ít nhất 250 chữ, phân tích chuyên sâu): Trọng tâm của phương án này là gì? Thích hợp trong trường hợp nào?>",
        "allocation": [
          {{ 
            "category": "<Tên Hạng mục (Vd: R&D, Marketing)>", 
            "percentage": "<%>", 
            "amount": "<Số tiền cụ thể>", 
            "why_invest": "<PHÂN TÍCH SÂU (Ít nhất 150 chữ): Tại sao hạng mục này cần ngân sách như vậy?>",
            "action_items": [
              "<Việc cần làm 1 (Vd: Xây dựng thuật toán Matching)>",
              "<Việc cần làm 2>"
            ]
          }}
        ],
        "expected_results": [
          "<Kết quả kỳ vọng chi tiết 1>",
          "<Kết quả kỳ vọng chi tiết 2>",
          "<Kết quả kỳ vọng chi tiết 3>"
        ]
      }},
      {{
        "name": "<Tên Kịch Bản (Vd: Phương án B - Tinh gọn & Dự phòng rủi ro)>",
        "focus_explanation": "<PHÂN TÍCH SÂU (Ít nhất 250 chữ, phân tích chuyên sâu): Trọng tâm của phương án B là gì?>",
        "allocation": [
          {{ 
            "category": "<Tên Hạng mục>", 
            "percentage": "<%>", 
            "amount": "<Số tiền cụ thể>", 
            "why_invest": "<PHÂN TÍCH SÂU (Ít nhất 150 chữ)>",
            "action_items": [
              "<Việc cần làm 1>"
            ]
          }}
        ],
        "expected_results": [
          "<Kết quả kỳ vọng chi tiết 1>"
        ]
      }}
    ],
    "burn_rate_runway": "<Đánh giá chi tiết (Ít nhất 250 chữ, phân tích chuyên sâu) về tốc độ đốt tiền (Burn Rate) và thời gian sống sót (Runway). Lập luận sắc bén.>",
    "milestones": [
      {{ "phase": "<Giai đoạn 1>", "goal": "<Mục tiêu kinh doanh và công nghệ cần đạt>" }},
      {{ "phase": "<Giai đoạn 2>", "goal": "<Mục tiêu kinh doanh và công nghệ cần đạt>" }}
    ],
    "suggested_deal": {{
      "instrument": "<Công cụ: SAFE, Cổ phần ưu đãi...>",
      "pre_money": "<Định giá Pre-money ước tính>",
      "post_money": "<Định giá Post-money>",
      "dilution": "<% pha loãng ước tính>",
      "note": "<Lưu ý thêm về định giá (nếu có)>"
    }},
    "final_recommendation": "<KHUYẾN NGHỊ CUỐI CÙNG (Ít nhất 250 chữ, phân tích chuyên sâu): Tổng kết lại nhà sáng lập nên chọn phương án nào và tại sao?>"
  }}
}}

**LƯU Ý QUAN TRỌNG - PHẢI TUÂN THỦ:**
1. Điểm số phải phản ánh ĐÚNG chất lượng (60-70 = trung bình, 80+ = tốt, 90+ = xuất sắc)
2. KHÔNG khen ngợi chung chung, PHẢI có bằng chứng cụ thể từ tài liệu
3. Dùng thuật ngữ chuyên môn: TAM/SAM/SOM, CAC/LTV, burn rate, runway, unit economics, moat, CAGR, EBITDA, v.v.
4. Mỗi recommendation PHẢI có action item cụ thể, timeline, và KPI định lượng
5. MỖI LUẬN ĐIỂM Ở `reason`, `strengths`, `weaknesses` PHẢI DÀI ÍT NHẤT 50-80 CHỮ. KHÔNG ĐƯỢC LÀM SƠ SÀI. VIẾT THẬT DÀI VÀ CHUYÊN SÂU NHƯ MỘT BÁO CÁO TÀI CHÍNH!
6. BẮT BUỘC cung cấp ít nhất 2 phương án (scenarios) khác nhau (Ví dụ: Phương án A - Đầu tư mạnh mẽ và Phương án B - Tinh gọn/Dự phòng).
7. KIỂM TRA KỸ ĐỊNH DẠNG JSON. Đảm bảo JSON hoàn toàn hợp lệ."""

    try:
        # Retry logic với exponential backoff
        max_retries = 3
        for attempt in range(max_retries):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": """Bạn là chuyên gia thẩm định đầu tư cấp cao với 15+ năm kinh nghiệm. 

YÊU CẦU BẮT BUỘC:
1. Phân tích SẮC BÉN, CHUYÊN NGHIỆP, dùng thuật ngữ chính xác
2. KHÔNG khen ngợi suông, PHẢI có bằng chứng cụ thể từ tài liệu
3. TRÍCH DẪN SỐ LIỆU thực tế từ tài liệu để chứng minh mỗi điểm
4. Mỗi recommendation PHẢI có action item cụ thể, timeline, và KPI định lượng
5. Độ dài tối thiểu: reason 4-5 câu, strengths/weaknesses 4-5 câu (tối thiểu 50-80 chữ), recommendations 4-5 câu. Phân tích CỰC KỲ DÀI VÀ CHI TIẾT.
6. So sánh với benchmark ngành khi có thể
7. Đưa ra nhận định DỨT KHOÁT về investment readiness
8. BẮT BUỘC trả về 2 phương án (scenarios) gọi vốn khác nhau trong mảng scenarios.

VÍ DỤ VỀ PHÂN TÍCH SẮC BÉN:
- TỐT: "Doanh thu tăng trưởng 253% CAGR (từ 10 tỷ lên 35 tỷ) vượt xa benchmark ngành SaaS 30%. Unit economics xuất sắc với LTV/CAC 13.8x so với benchmark 3x. Tuy nhiên, burn rate 500 triệu/tháng cao hơn mức an toàn 300 triệu, runway chỉ còn 6 tháng."
- TỆ: "Doanh nghiệp có doanh thu tốt và tăng trưởng nhanh."

VÍ DỤ VỀ RECOMMENDATION CỤ THỂ:
- TỐT: "Trong 90 ngày tới, giảm burn rate 20% từ 500 triệu xuống 400 triệu/tháng bằng cách: (1) Tối ưu CAC từ 500K xuống 400K qua focus vào organic channels, (2) Cắt giảm 2 nhân sự marketing không hiệu quả, (3) Renegotiate hợp đồng SaaS tools để tiết kiệm 50 triệu/tháng."
- TỆ: "Cần cải thiện burn rate."

Luôn trả lời bằng JSON hợp lệ với đầy đủ các field yêu cầu."""
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.6,
                    max_tokens=8000,
                    response_format={"type": "json_object"}
                )
                break
            except Exception as e:
                if "413" in str(e) and attempt < max_retries - 1:
                    # Nếu lỗi 413, retry sau 2^attempt giây
                    import time
                    time.sleep(2 ** attempt)
                    continue
                raise
        
        ai_result = json.loads(chat_completion.choices[0].message.content)
        
        # Merge base score với AI result
        result = {
            "score": ai_result.get("score", base_result["score"]),
            "breakdown": ai_result.get("breakdown", base_result["breakdown"]),
            "strengths": ai_result.get("strengths", []),
            "weaknesses": ai_result.get("weaknesses", []),
            "recommendations": ai_result.get("recommendations", []),
            "funding_scenario": ai_result.get("funding_scenario", None),
            "expert_insight": ai_result.get("expert_insight", ""),
            "investment_thesis": ai_result.get("investment_thesis", ""),
            "risk_if_missing": ai_result.get("risk_if_missing", "Không xác định"),
            "risk_if_weak": ai_result.get("risk_if_weak", "Không xác định")
        }
        
        # Cache result
        cache_result(cache_key, result)
        
        return result
        
    except Exception as e:
        print(f"Groq API error: {e}")
        # Fallback to base result
        result = {
            "score": base_result["score"],
            "breakdown": base_result["breakdown"],
            "strengths": ["Không thể phân tích chi tiết"],
            "weaknesses": ["Lỗi API"],
            "recommendations": ["Thử lại sau"],
            "risk_if_missing": "Không xác định",
            "risk_if_weak": "Không xác định"
        }
        return result


async def analyze_combined_documents(documents: List[Dict], document_type: str) -> Dict[str, Any]:
    """
    Hybrid: Rule-based + Groq AI cho multiple documents.
    Gom tất cả tài liệu thành 1 prompt, gọi Groq 1 lần.
    """
    
    # Check cache
    combined_content = ""
    for doc in documents:
        combined_content += doc["content"]
    
    cache_key = get_cache_key(combined_content)
    cached = get_cached_result(cache_key)
    if cached:
        print("Cache hit for combined documents")
        return cached
    
    # Step 1: Rule-based scoring
    base_result = calculate_base_score(combined_content, document_type)
    
    # Step 2: Build combined content cho AI (giới hạn để tránh vượt token limit)
    combined_text = ""
    for i, doc in enumerate(documents, 1):
        # Giới hạn mỗi file 500 ký tự, tổng tối đa 2500 ký tự
        content_preview = doc['content'][:500]
        combined_text += f"\n\n=== TÀI LIỆU {i}: {doc['filename']} ===\n{content_preview}"
        if len(combined_text) > 2500:
            break
    
    doc_info = DOCUMENT_CRITERIA.get(document_type, DOCUMENT_CRITERIA["pitchdeck"])
    criteria_text = "\n".join([
        f"- {c['name']} (tối đa {c['max']} điểm)" 
        for c in doc_info["criteria"]
    ])
    
    prompt = f"""Bạn là **Chuyên gia Thẩm định Đầu tư Cấp cao** với 15+ năm kinh nghiệm tại các quỹ VC hàng đầu Việt Nam và Đông Nam Á. Bạn đã tham gia thẩm định hơn 500 startup và tư vấn cho các quỹ như Do Ventures, Golden Gate Ventures, Jungle Ventures.

**PHONG CÁCH PHÂN TÍCH:**
- Dùng ngôn ngữ chuyên nghiệp, sắc bén của dân đầu tư
- Đưa ra nhận định DỨT KHOÁT, không chung chung
- Chỉ ra insight sâu mà người thường không thấy
- Dùng số liệu cụ thể, so sánh benchmark ngành
- Phân tích theo framework: Strengths -> Risks -> Opportunities -> Recommendations

**NHIỆM VỤ:**
Phân tích {len(documents)} tài liệu từ một doanh nghiệp theo bộ tiêu chí chuyên gia:

{criteria_text}

**CÁC TÀI LIỆU:**
{combined_text}

**YÊU CẦU TRẢ LỜI (JSON format):**
{{
  "total_score": <điểm 0-100, phải phản ánh đúng chất lượng tổng hợp>,
  "grade": "<Tier 1-5 với mô tả chuyên môn>",
  "score_breakdown": [
    {{
      "name": "<tên tiêu chí>",
      "score": <điểm cụ thể>,
      "maximum": <điểm tối đa>,
      "reason": "<phân tích sắc bén 3-4 câu, dùng thuật ngữ chuyên môn>"
    }}
  ],
  "detailed_analysis": {{
    "financial_position": "<phân tích 3-4 câu, có số liệu cụ thể>",
    "governance": "<phân tích 3-4 câu, chỉ ra rủi ro>",
    "cash_flow": "<phân tích 3-4 câu, so sánh benchmark>",
    "capital_structure": "<phân tích 3-4 câu, đánh giá tính bền vững>",
    "legal_compliance": "<phân tích 3-4 câu, chỉ ra điểm yếu pháp lý>",
    "valuation": "<phân tích 3-4 câu, so sánh với thị trường>"
  }},
  "strengths": [
    "<điểm mạnh 1: cụ thể, có số liệu chứng minh>",
    "<điểm mạnh 2: insight sâu>",
    "<điểm mạnh 3: lợi thế cạnh tranh>",
    "<điểm mạnh 4: tiềm năng tăng trưởng>",
    "<điểm mạnh 5: yếu tố độc đáo>"
  ],
  "weaknesses": [
    "<điểm yếu 1: chỉ ra rủi ro cụ thể>",
    "<điểm yếu 2: phân tích tác động>",
    "<điểm yếu 3: so sánh benchmark>",
    "<điểm yếu 4: gap so với kỳ vọng>",
    "<điểm yếu 5: rủi ro tiềm ẩn>"
  ],
  "recommendations": [
    {{
      "priority": "Critical|High|Medium|Low",
      "category": "<Legal|Governance|Financial|Growth|Product>",
      "recommendation": "<khuyến nghị CỤ THỂ, có action item rõ ràng>",
      "financial_impact": "<tác động tài chính định lượng nếu có thể>",
      "implementation": "<cách triển khai chi tiết, có timeline>"
    }}
  ],
  "risks": [
    {{
      "category": "<loại rủi ro>",
      "severity": "Critical|High|Medium|Low",
      "financial_impact": "<tác động tài chính cụ thể>",
      "mitigation": "<biện pháp giảm thiểu chi tiết>"
    }}
  ],
  "kpis": [
    {{
      "name": "<tên KPI>",
      "current": "<giá trị hiện tại hoặc N/A>",
      "target": "<mục tiêu cụ thể>",
      "unit": "<đơn vị>",
      "deadline": "<timeline>"
    }}
  ],
  "summary": "<tóm tắt chuyên gia 4-5 câu về investment readiness>",
  "expert_insight": "<nhận định chuyên gia về tiềm năng đầu tư>",
  "investment_thesis": "<tại sao nên/không nên đầu tư, với lý do cụ thể>"
}}

**LƯU Ý QUAN TRỌNG:**
- Điểm số phải phản ánh ĐÚNG chất lượng (60-70 = trung bình, 80+ = tốt, 90+ = xuất sắc)
- Không khen ngợi chung chung, phải có bằng chứng cụ thể
- Dùng thuật ngữ: TAM/SAM/SOM, CAC/LTV, burn rate, runway, unit economics, moat, v.v.
- So sánh với benchmark ngành khi có thể
- Đưa ra nhận định DỨT KHOÁT về investment readiness
- Mỗi recommendation phải KHÁC BIỆT, không lặp lại"""

    try:
        # Retry logic với exponential backoff
        max_retries = 3
        for attempt in range(max_retries):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "Bạn là chuyên gia thẩm định đầu tư cấp cao. Phân tích sắc bén, chuyên nghiệp, dùng thuật ngữ chính xác. Không khen ngợi suông, phải có bằng chứng cụ thể. Mỗi recommendation phải độc đáo và khác biệt."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.6,  # Cân bằng giữa sáng tạo và chính xác
                    max_tokens=8000,
                    response_format={"type": "json_object"}
                )
                break
            except Exception as e:
                if "413" in str(e) and attempt < max_retries - 1:
                    # Nếu lỗi 413, retry sau 2^attempt giây
                    import time
                    time.sleep(2 ** attempt)
                    continue
                raise
        
        ai_result = json.loads(chat_completion.choices[0].message.content)
        
        # Merge results
        result = {
            "total_score": ai_result.get("total_score", base_result["score"]),
            "grade": ai_result.get("grade", "Tier 2 - Cần cải thiện"),
            "score_breakdown": ai_result.get("score_breakdown", base_result["breakdown"]),
            "detailed_analysis": ai_result.get("detailed_analysis", {}),
            "strengths": ai_result.get("strengths", []),
            "weaknesses": ai_result.get("weaknesses", []),
            "recommendations": ai_result.get("recommendations", []),
            "risks": ai_result.get("risks", []),
            "kpis": ai_result.get("kpis", []),
            "summary": ai_result.get("summary", "Không có thông tin"),
            "expert_insight": ai_result.get("expert_insight", ""),
            "investment_thesis": ai_result.get("investment_thesis", ""),
            "aggregate_score": ai_result.get("total_score", base_result["score"]),
            "aggregate_analysis": {
                "score": ai_result.get("total_score", base_result["score"]),
                "breakdown": ai_result.get("score_breakdown", []),
                "strengths": ai_result.get("strengths", [])[:5],
                "weaknesses": ai_result.get("weaknesses", [])[:5],
                "recommendations": [r.get("recommendation", "") for r in ai_result.get("recommendations", [])[:5]]
            }
        }
        
        # Cache result
        cache_result(cache_key, result)
        
        return result
        
    except Exception as e:
        print(f"Groq API error: {e}")
        # Fallback: trả về kết quả cơ bản dựa trên rule-based scoring
        return {
            "total_score": base_result["score"],
            "grade": "Tier 3 - Cần cải thiện nhiều",
            "score_breakdown": base_result["breakdown"],
            "detailed_analysis": {},
            "strengths": ["Không thể phân tích chi tiết do giới hạn API"],
            "weaknesses": ["Cần cung cấp tài liệu ngắn gọn hơn"],
            "recommendations": [
                {
                    "priority": "High",
                    "category": "General",
                    "recommendation": "Giảm số lượng tài liệu hoặc độ dài nội dung để phù hợp với giới hạn API",
                    "financial_impact": "N/A",
                    "implementation": "N/A"
                }
            ],
            "risks": [],
            "kpis": [],
            "summary": f"Lỗi khi gọi AI: {str(e)[:200]}",
            "aggregate_score": base_result["score"],
            "aggregate_analysis": {
                "score": base_result["score"],
                "breakdown": base_result["breakdown"],
                "strengths": [],
                "weaknesses": [],
                "recommendations": []
            }
        }
