from google import genai
from google.genai import types
import os
import json
from typing import Dict, Any, List
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path, override=True)

# Lazy load client
_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        _client = genai.Client(api_key=api_key)
    return _client

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
    "execsum": {
        "name": "Executive Summary",
        "weight": 6,
        "criteria": [
            {"name": "Tổng quan doanh nghiệp", "max": 10},
            {"name": "Vấn đề thị trường và Giải pháp", "max": 15},
            {"name": "Thị trường mục tiêu và Khách hàng", "max": 10},
            {"name": "Chỉ số tăng trưởng và Hào kinh tế", "max": 25},
            {"name": "Mô hình doanh thu và Dự báo tài chính", "max": 15},
            {"name": "Đội ngũ lãnh đạo và Lộ trình", "max": 10},
            {"name": "Nhu cầu gọi vốn và Phân bổ vốn", "max": 15}
        ]
    },
    "bizplan": {
        "name": "Kế hoạch kinh doanh",
        "weight": 9,
        "criteria": [
            {"name": "Tóm tắt điều hành & Tầm nhìn", "max": 10},
            {"name": "Phân tích thị trường & Khách hàng", "max": 15},
            {"name": "Sản phẩm, Dịch vụ & Giải pháp", "max": 15},
            {"name": "Mô hình kinh doanh & Chiến lược doanh thu", "max": 15},
            {"name": "Chỉ số tăng trưởng & Hiệu quả tài chính", "max": 20},
            {"name": "Chiến lược Go-To-Market & Vận hành", "max": 15},
            {"name": "Kế hoạch tài chính & Nhu cầu gọi vốn", "max": 10}
        ]
    },
    "legalfin": {
        "name": "Pháp lý & Tài chính",
        "weight": 9,
        "criteria": [
            {"name": "Tổng quan doanh nghiệp và mô hình hoạt động", "max": 10},
            {"name": "Khung pháp lý và tuân thủ dữ liệu", "max": 15},
            {"name": "Báo cáo và chỉ số tài chính cốt lõi", "max": 25},
            {"name": "Cấu trúc chi phí vận hành", "max": 20},
            {"name": "Tái cấu trúc vốn và quản trị cổ đông", "max": 15},
            {"name": "Quản trị quỹ dự phòng và khả năng chống chịu", "max": 15}
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
    "forecast": {
        "name": "Dự báo tài chính",
        "weight": 6,
        "criteria": [
            {"name": "Tính logic và thực tế của giả định", "max": 15},
            {"name": "Tính khả thi của bảng dự báo KQKD", "max": 25},
            {"name": "Cân đối bảng cân đối kế toán dự báo", "max": 20},
            {"name": "Đánh giá năng lực sinh lời", "max": 20},
            {"name": "Quản trị rủi ro thanh khoản", "max": 10},
            {"name": "Chính sách tích lũy nguồn vốn", "max": 10}
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
    "shagreement": {
        "name": "Hợp đồng cổ đông",
        "weight": 5,
        "criteria": [
            {"name": "Cơ cấu cổ phần & Bảng vốn hóa", "max": 20},
            {"name": "Quyền quản trị & Quyết định doanh nghiệp", "max": 25},
            {"name": "Quy định chuyển nhượng cổ phần", "max": 20},
            {"name": "Chiến lược thoái vốn & Quyền ưu tiên", "max": 15},
            {"name": "Pháp lý, Bảo mật & Xử lý tranh chấp", "max": 20}
        ]
    },
    "shlist": {
        "name": "Danh sách cổ đông",
        "weight": 3,
        "criteria": [
            {"name": "Tính chính xác định danh pháp lý", "max": 25},
            {"name": "Minh bạch cấu trúc vốn", "max": 30},
            {"name": "Tình trạng thực nộp vốn", "max": 20},
            {"name": "Hiệu lực pháp lý & Chữ ký", "max": 15},
            {"name": "Tính hợp lý cho kêu gọi đầu tư", "max": 10}
        ]
    },
    "prodcust": {
        "name": "Sản phẩm và khách hàng",
        "weight": 7,
        "criteria": [
            {"name": "Giải pháp sản phẩm & Giá trị cốt lõi", "max": 30},
            {"name": "Chân dung khách hàng mục tiêu", "max": 25},
            {"name": "Mô hình kinh doanh & Luồng doanh thu", "max": 20},
            {"name": "Báo cáo Traction & Số liệu thực tế", "max": 15},
            {"name": "Rào cản cạnh tranh & Scalability", "max": 10}
        ]
    },
    "ip": {
        "name": "Hồ sơ sở hữu trí tuệ",
        "weight": 4,
        "criteria": [
            {"name": "Tính quyền sở hữu & Chuyển giao hợp pháp", "max": 30},
            {"name": "Danh mục tài sản IP & Văn bằng bảo hộ", "max": 25},
            {"name": "Bảo vệ bí mật kinh doanh", "max": 20},
            {"name": "Rủi ro xâm phạm IP bên thứ ba", "max": 15},
            {"name": "Khả năng thương mại hóa & Định giá IP", "max": 10}
        ]
    },
    "proddata": {
        "name": "Dữ liệu sản phẩm",
        "weight": 4,
        "criteria": [
            {"name": "Chuẩn hóa thông tin sản phẩm", "max": 25},
            {"name": "Chiến lược định giá & Cơ cấu chi phí", "max": 30},
            {"name": "Điểm cân bằng tài chính khách hàng", "max": 20},
            {"name": "Bằng chứng thực tế thị trường", "max": 15},
            {"name": "Tính minh bạch & Điều khoản thương mại", "max": 10}
        ]
    },
    "custdata": {
        "name": "Dữ liệu khách hàng",
        "weight": 5,
        "criteria": [
            {"name": "Đầy đủ & Đo lường chỉ số tăng trưởng", "max": 25},
            {"name": "Tỷ lệ giữ chân & Rời bỏ", "max": 25},
            {"name": "Hiệu quả thu hút khách hàng (CAC)", "max": 20},
            {"name": "Mức độ hài lòng & Social Proof", "max": 15},
            {"name": "Bảo mật & Tuân thủ pháp lý dữ liệu", "max": 15}
        ]
    },
    "useoffunds": {
        "name": "Kế hoạch sử dụng vốn",
        "weight": 6,
        "criteria": [
            {"name": "Phân bổ ngân sách & Mục tiêu rõ ràng", "max": 30},
            {"name": "Thời gian sử dụng vốn & Runway", "max": 25},
            {"name": "Kỳ vọng kết quả & Cột mốc tăng trưởng", "max": 20},
            {"name": "Tính cân bằng & Cơ cấu chi phí", "max": 15},
            {"name": "Dự phòng rủi ro & Kịch bản tài chính", "max": 10}
        ]
    }
}

TIERS = [
    {"min": 0, "max": 39, "name": "Chưa đủ điều kiện gọi vốn", "color": "#dc2626"},
    {"min": 40, "max": 59, "name": "Có tiềm năng nhưng rủi ro cao", "color": "#ea580c"},
    {"min": 60, "max": 74, "name": "Sẵn sàng có điều kiện", "color": "#ca8a04"},
    {"min": 75, "max": 89, "name": "Sẵn sàng gọi vốn", "color": "#16a34a"},
    {"min": 90, "max": 100, "name": "Sẵn sàng thẩm định chuyên sâu", "color": "#15803d"}
]

from typing import Dict, Any, List, Optional

def get_tier(score: int) -> Dict[str, Any]:
    for tier in TIERS:
        if tier["min"] <= score <= tier["max"]:
            return tier
    return TIERS[0]

async def analyze_with_gemini(document_type: str, content: str, desired_amount: Optional[str] = None) -> Dict[str, Any]:
    if document_type not in DOCUMENT_CRITERIA:
        raise ValueError(f"Unknown document type: {document_type}")
    
    doc_info = DOCUMENT_CRITERIA[document_type]
    criteria_text = "\n".join([
        f"- {c['name']} (tối đa {c['max']} điểm)" 
        for c in doc_info["criteria"]
    ])
    
    prompt = f"""Bạn là **Tổng Giám đốc Đầu tư (Managing Partner)** tại một quỹ Venture Capital hàng đầu thế giới. Bạn nổi tiếng với những bản phân tích (Due Diligence) cực kỳ khắt khe, dài dòng, và chi tiết đến từng ngóc ngách.

Hãy phân tích tài liệu "{doc_info['name']}" sau và chấm điểm theo bộ tiêu chí:

{criteria_text}

NỘI DUNG TÀI LIỆU:
{content}

YÊU CẦU BẮT BUỘC:
1. Trả lời CHỈ bằng JSON hợp lệ, KHÔNG có text nào khác ngoài JSON.
2. KHÔNG sử dụng markdown, KHÔNG có ```json.
3. Đảm bảo JSON valid tuyệt đối, không có trailing commas.
4. PHÂN TÍCH CHUYÊN MÔN SÂU: Mọi nhận xét phải mang tính chuyên gia tài chính cấp cao (VC/PE). VIẾT THẬT DÀI, CHI TIẾT VÀ SẮC BÉN.
5. Mỗi "reason" trong breakdown phải phân tích cặn kẽ lý do được điểm đó (Tối thiểu 300 chữ, đưa ra bằng chứng thực tế).
6. Bắt buộc MỖI mảng (strengths, weaknesses, recommendations) phải có đúng 5 ý, MỖI Ý DÀI TỐI THIỂU 150 CHỮ.
7. Trong "funding_scenario", các chiến lược phải cực kỳ chi tiết, mỗi phần tối thiểu 250 chữ.
8. BẮT BUỘC cung cấp 2 phương án (scenarios) khác nhau (Phương án A - Đầu tư mạnh mẽ và Phương án B - Tinh gọn/Dự phòng).
9. Mọi câu chữ phải trích dẫn data từ tài liệu và so sánh với Benchmark ngành.

FORMAT JSON:
{{
  "score": <tổng điểm 0-100>,
  "breakdown": [
    {{"name": "<tên tiêu chí>", "score": <điểm đạt được>, "max": <điểm tối đa>, "reason": "<PHÂN TÍCH SẮC BÉN DÀI TỐI THIỂU 300 CHỮ>"}}
  ],
  "strengths": [
    "<điểm mạnh 1: Lợi thế cốt lõi, RẤT CHI TIẾT tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<điểm mạnh 2: Rào cản gia nhập/Công nghệ, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<điểm mạnh 3: Thị trường/Business Model, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<điểm mạnh 4: Đội ngũ/Tài chính, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<điểm mạnh 5: Insight đặc biệt, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>"
  ],
  "weaknesses": [
    "<điểm yếu 1: Rủi ro thị trường/đối thủ, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<điểm yếu 2: Rủi ro thực thi (Execution), cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<điểm yếu 3: Kẽ hở trong mô hình kinh doanh, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<điểm yếu 4: Vấn đề dòng tiền/Burn Rate, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<điểm yếu 5: Rủi ro phụ thuộc (Dependencies), cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>"
  ],
  "recommendations": [
    "<khuyến nghị 1: Chiến lược tăng trưởng ngắn hạn, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<khuyến nghị 2: Tối ưu hóa sản phẩm/vận hành, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<khuyến nghị 3: Quản trị dòng tiền, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<khuyến nghị 4: Chiến lược Pivot/Dự phòng, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>",
    "<khuyến nghị 5: Lời khuyên gọi vốn tiếp theo, cực kỳ chi tiết tối thiểu 150 chữ, trích dẫn số liệu cụ thể>"
  ],
  "risk_if_missing": "<rủi ro nếu thiếu tài liệu này>",
  "risk_if_weak": "<rủi ro nếu tài liệu yếu>",
  "funding_scenario": {{
    "desired_amount": "<Số tiền doanh nghiệp mong muốn, lấy từ {desired_amount} hoặc suy luận>",
    "recommended_amount": "<Số tiền hệ thống khuyến nghị để đạt hiệu quả cao nhất (Vd: 5 tỷ, 10 tỷ)>",
    "rationale": {{
      "why_recommended": "<PHÂN TÍCH ĐỊNH GIÁ & VỐN (Ít nhất 400 chữ, mổ xẻ mọi góc độ): Tại sao mức tiền này là chuẩn nhất? Nó giúp startup sống được bao lâu (runway)?>",
      "investment_needs": [
        "<Nhu cầu cốt lõi 1>",
        "<Nhu cầu cốt lõi 2>",
        "<Nhu cầu cốt lõi 3>",
        "<Nhu cầu cốt lõi 4>",
        "<Nhu cầu cốt lõi 5>"
      ]
    }},
    "scenarios": [
      {{
        "name": "<Phương án A - Tăng trưởng Đột phá (Hyper-growth)>",
        "focus_explanation": "<PHÂN TÍCH TẦM NHÌN (Ít nhất 250 chữ, phân tích chuyên sâu): Kịch bản này dành cho việc chiếm lĩnh thị trường ra sao?>",
        "allocation": [
          {{ 
            "category": "<Hạng mục 1>", 
            "percentage": "<%>", 
            "amount": "<Số tiền>", 
            "why_invest": "<LÝ DO CHI TIẾT (Ít nhất 300 chữ, mổ xẻ mọi góc độ)>",
            "action_items": ["<Hành động 1 rất chi tiết>", "<Hành động 2 rất chi tiết>", "<Hành động 3>"]
          }}
        ],
        "expected_results": [
          "<Kỳ vọng 1>", "<Kỳ vọng 2>", "<Kỳ vọng 3>", "<Kỳ vọng 4>"
        ]
      }},
      {{
        "name": "<Phương án B - Tinh gọn & Sống sót (Bootstrapping & Survival)>",
        "focus_explanation": "<PHÂN TÍCH TẦM NHÌN (Ít nhất 250 chữ, phân tích chuyên sâu): Kịch bản phòng thủ, cắt giảm chi phí?>",
        "allocation": [
          {{ 
            "category": "<Hạng mục 1>", 
            "percentage": "<%>", 
            "amount": "<Số tiền>", 
            "why_invest": "<LÝ DO CHI TIẾT (Ít nhất 300 chữ, mổ xẻ mọi góc độ)>",
            "action_items": ["<Hành động 1 rất chi tiết>", "<Hành động 2 rất chi tiết>"]
          }}
        ],
        "expected_results": [
          "<Kỳ vọng 1>", "<Kỳ vọng 2>", "<Kỳ vọng 3>"
        ]
      }}
    ],
    "burn_rate_runway": "<ĐÁNH GIÁ TÀI CHÍNH (Ít nhất 250 chữ, phân tích chuyên sâu): Tốc độ đốt tiền dự kiến? Bao nhiêu tháng thì hết vốn?>",
    "milestones": [
      {{ "phase": "<Tháng 1-3>", "goal": "<Mục tiêu rất chi tiết 1>" }},
      {{ "phase": "<Tháng 4-6>", "goal": "<Mục tiêu rất chi tiết 2>" }},
      {{ "phase": "<Tháng 7-12>", "goal": "<Mục tiêu rất chi tiết 3>" }},
      {{ "phase": "<Tháng 12-18>", "goal": "<Mục tiêu rất chi tiết 4>" }}
    ],
    "suggested_deal": {{
      "instrument": "<Công cụ: SAFE, Cổ phần ưu đãi...>",
      "pre_money": "<Định giá Pre-money>",
      "post_money": "<Định giá Post-money>",
      "dilution": "<% pha loãng>",
      "note": "<GHI CHÚ ĐÀM PHÁN (Ít nhất 200 chữ): Lời khuyên đàm phán Term Sheet>"
    }},
    "final_recommendation": "<TỔNG KẾT VÀ QUYẾT ĐỊNH (Ít nhất 300 chữ, mổ xẻ mọi góc độ): Tóm lại quỹ có nên đầu tư không?>"
  }}
}}

Chấm điểm vô cùng khắt khe, khách quan và chuyên sâu dựa trên bằng chứng thực tế trong tài liệu. Đồng thời xây dựng kịch bản gọi vốn, cấu trúc deal (Deal Structure) và lộ trình (Runway/Milestones) chi tiết ở mức độ chuyên gia ngân hàng đầu tư.
LƯU Ý QUAN TRỌNG: TRẢ VỀ JSON HỢP LỆ. TUYỆT ĐỐI KHÔNG SỬ DỤNG DẤU NGOẶC KÉP (") BÊN TRONG NỘI DUNG CÁC TRƯỜNG VĂN BẢN (NẾU CẦN TRÍCH DẪN, HÃY DÙNG DẤU NGOẶC ĐƠN (')). KHÔNG SỬ DỤNG KÝ TỰ XUỐNG DÒNG (\n) CHƯA ĐƯỢC ESCAPE."""



    try:
        response = get_client().models.generate_content(
            model='gemini-1.5-pro',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=8192,
                response_mime_type="application/json"
            )
        )
        result_text = response.text.strip()
        
        # Xử lý trường hợp model trả về markdown code blocks
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
            
        import re
        json_match = re.search(r'\{[\s\S]*\}', result_text)
        if json_match:
            result_text = json_match.group(0)
            
        result_text = re.sub(r',(\s*[}\]])', r'\1', result_text)
            
        result = json.loads(result_text)
        
        # Ensure required fields exist
        result.setdefault('score', 0)
        result.setdefault('breakdown', [])
        result.setdefault('strengths', [])
        result.setdefault('weaknesses', [])
        result.setdefault('recommendations', [])
        
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        error_str = str(e).lower()
        if '429' in error_str or 'quota' in error_str or 'exhausted' in error_str:
            reason = "Hệ thống đang quá tải hoặc API Key đã hết hạn mức (Quota Exceeded). Vui lòng đợi 1 phút và thử lại."
        else:
            reason = "Lỗi khi kết nối với AI (Timeout hoặc lỗi định dạng). Vui lòng thử lại."
            
        # Return basic fallback result
        breakdown = []
        for criterion in doc_info["criteria"]:
            breakdown.append({
                "name": criterion["name"],
                "score": 0,
                "max": criterion["max"],
                "reason": reason
            })
            
        return {
            "score": 0,
            "grade": "N/A",
            "breakdown": breakdown,
            "strengths": [reason],
            "weaknesses": [reason],
            "recommendations": ["Hãy kiểm tra lại API Key hoặc đợi một lúc rồi thử lại."],
            "funding_scenario": None
        }


async def analyze_input_with_framework(input_text: str, framework_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Phân tích input text của user dựa trên framework từ profile mẫu.
    Dùng Gemini API để đánh giá thật, không copy dữ liệu mẫu.
    """
    
    # Extract framework từ profile mẫu
    score_breakdown = framework_profile.get("score", {}).get("breakdown", [])
    analysis_sections = framework_profile.get("analysis", {})
    
    # Tạo prompt chi tiết với framework
    framework_text = ""
    for item in score_breakdown:
        framework_text += f"\n- {item['name']} (tối đa {item['maximum']} điểm)"
    
    prompt = f"""Bạn là chuyên gia thẩm định hồ sơ gọi vốn doanh nghiệp tại Việt Nam với 15 năm kinh nghiệm.

NHIỆM VỤ: Phân tích mô tả doanh nghiệp dưới đây và chấm điểm theo khung tiêu chí có sẵn.

MÔ TẢ DOANH NGHIỆP:
{input_text}

KHUNG TIÊU CHÍ ĐÁNH GIÁ (tham chiếu từ hồ sơ mẫu):
{framework_text}

YÊU CẦU BẮT BUỘC:
1. Trả lời CHỈ bằng JSON hợp lệ, KHÔNG có text nào khác
2. KHÔNG sử dụng markdown, KHÔNG có ```json
3. Bắt đầu bằng {{ và kết thúc bằng }}
4. Đảm bảo JSON valid, không có trailing commas
5. Đọc kỹ mô tả doanh nghiệp
6. Chấm điểm TỪNG tiêu chí dựa trên thông tin CÓ TRONG mô tả (không suy diễn thêm)
7. Nếu thiếu thông tin, chấm điểm thấp và ghi rõ "Thiếu thông tin"
8. Đưa ra nhận xét cụ thể cho từng tiêu chí
9. Đề xuất khuyến nghị hành động thực tế

FORMAT JSON:
{{
  "total_score": <tổng điểm 0-100>,
  "grade": "<Tier description>",
  "score_breakdown": [
    {{
      "name": "<tên tiêu chí>",
      "score": <điểm đạt được>,
      "maximum": <điểm tối đa>,
      "reason": "<nhận xét chi tiết 2-3 câu>"
    }}
  ],
  "detailed_analysis": {{
    "financial_position": "<phân tích vị thế tài chính 2-3 câu>",
    "governance": "<phân tích quản trị 2-3 câu>",
    "cash_flow": "<phân tích dòng tiền 2-3 câu>",
    "capital_structure": "<phân tích cấu trúc vốn 2-3 câu>",
    "legal_compliance": "<phân tích tuân thủ pháp lý 2-3 câu>",
    "valuation": "<phân tích định giá 2-3 câu>"
  }},
  "strengths": ["<điểm mạnh 1>", "<điểm mạnh 2>", "<điểm mạnh 3>"],
  "weaknesses": ["<điểm yếu 1>", "<điểm yếu 2>", "<điểm yếu 3>"],
  "recommendations": [
    {{
      "priority": "Critical|High|Medium|Low",
      "category": "<Legal|Governance|Financial|Growth|Product>",
      "recommendation": "<khuyến nghị cụ thể>",
      "financial_impact": "<tác động tài chính>",
      "implementation": "<cách triển khai>"
    }}
  ],
  "risks": [
    {{
      "category": "<loại rủi ro>",
      "severity": "Critical|High|Medium|Low",
      "financial_impact": "<tác động tài chính>",
      "mitigation": "<biện pháp giảm thiểu>"
    }}
  ],
  "kpis": [
    {{
      "name": "<tên KPI>",
      "current": "<giá trị hiện tại hoặc N/A>",
      "target": "<mục tiêu>",
      "unit": "<đơn vị>",
      "deadline": "<thời hạn>"
    }}
  ],
  "summary": "<tóm tắt tổng quan 3-4 câu về doanh nghiệp>"
}}

Chấm điểm KHÁCH QUAN, dựa trên BẰNG CHỨNG trong mô tả. Không suy diễn hoặc thêm thông tin không có."""

    try:
        response = get_client().models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=8192,
            )
        )
        
        result_text = response.text.strip()
        
        # Remove markdown code blocks
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        # Try to find JSON object
        import re
        json_match = re.search(r'\{[\s\S]*\}', result_text)
        if json_match:
            result_text = json_match.group(0)
        
        # Fix common JSON errors
        # Remove trailing commas before } or ]
        result_text = re.sub(r',(\s*[}\]])', r'\1', result_text)
        
        # Try to parse JSON
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Problematic JSON (first 500 chars): {result_text[:500]}")
            
            # Fallback: Parse text response and create structured result
            text_response = response.text.strip()
            
            # Extract score if mentioned
            score_match = re.search(r'(\d+)\s*/\s*100', text_response)
            total_score = int(score_match.group(1)) if score_match else 50
            
            # Extract bullet points
            lines = text_response.split('\n')
            bullet_points = [line.strip().lstrip('*-• ') for line in lines if line.strip().startswith(('*', '-', '•'))]
            
            # Categorize bullet points
            strengths = []
            weaknesses = []
            recommendations = []
            
            for point in bullet_points[:10]:
                point_lower = point.lower()
                if any(word in point_lower for word in ['điểm mạnh', 'ưu điểm', 'tốt', 'tích cực', 'strong', 'strength']):
                    strengths.append(point)
                elif any(word in point_lower for word in ['điểm yếu', 'nhược điểm', 'cần cải thiện', 'weakness', 'improve']):
                    weaknesses.append(point)
                else:
                    recommendations.append(point)
            
            # Create score breakdown from framework
            score_breakdown_result = []
            for item in score_breakdown:
                score_breakdown_result.append({
                    "name": item['name'],
                    "score": int(item['maximum'] * 0.5),
                    "maximum": item['maximum'],
                    "reason": "Cần phân tích chi tiết hơn"
                })
            
            # Create recommendations
            reco_result = []
            for reco_text in recommendations[:3]:
                reco_result.append({
                    "priority": "High",
                    "category": "General",
                    "recommendation": reco_text,
                    "financial_impact": "Cần đánh giá thêm",
                    "implementation": "Cần lập kế hoạch chi tiết"
                })
            
            # Create risks
            risks_result = []
            for weak_text in weaknesses[:3]:
                risks_result.append({
                    "category": "General Risk",
                    "severity": "Medium",
                    "financial_impact": "Cần đánh giá thêm",
                    "mitigation": weak_text
                })
            
            result = {
                "total_score": total_score,
                "grade": "Tier 2 - Cần cải thiện",
                "score_breakdown": score_breakdown_result,
                "detailed_analysis": {
                    "financial_position": "Cần phân tích chi tiết hơn",
                    "governance": "Cần phân tích chi tiết hơn",
                    "cash_flow": "Cần phân tích chi tiết hơn",
                    "capital_structure": "Cần phân tích chi tiết hơn"
                }
            }
            return result
        
    except Exception as e:
        print(f"ERROR in analyze_with_gemini: {e}")
        return {
            "score": 0,
            "grade": "N/A",
            "breakdown": [],
            "strengths": ["Không thể phân tích chi tiết do lỗi kết nối AI"],
            "weaknesses": ["Lỗi khi gọi AI"],
            "recommendations": ["Vui lòng thử lại sau"],
            "risk_if_missing": "",
            "risk_if_weak": ""
        }
