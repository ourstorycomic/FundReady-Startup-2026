import asyncio
from api.groq_client import get_cache_path, DOCUMENT_CRITERIA

desired_amount = "3 ty"
document_type = "pitchdeck"
criteria_json = DOCUMENT_CRITERIA.get(document_type, DOCUMENT_CRITERIA["pitchdeck"])

prompt = f"""
Bạn là một chuyên gia đánh giá đầu tư (Venture Capitalist) chuyên nghiệp.
Hãy phân tích tài liệu sau đây dựa trên các tiêu chí nghiêm ngặt.

**Yêu Cầu Phân Tích (BẮT BUỘC):**
1. Đọc và hiểu sâu sắc toàn bộ nội dung tài liệu.
2. Đánh giá khách quan, sắc bén, CHỈ rõ điểm yếu, điểm mạnh, rủi ro tiềm ẩn. KHÔNG nói chung chung.
3. Chấm điểm từng tiêu chí theo thang điểm cho trước một cách khắt khe. Điểm thấp (dưới trung bình) nếu thiếu số liệu hoặc lập luận mờ nhạt.
4. NẾU TÀI LIỆU KHÔNG THUỘC LOẠI {document_type} HOẶC LÀ RÁC/MẬP MỜ: Cho điểm 0 và giải thích ngắn gọn lý do.
5. Xây dựng "funding_scenario" CỰC KỲ CHI TIẾT.

Định dạng JSON đầu ra phải tuân thủ nghiêm ngặt cấu trúc sau.
BẮT BUỘC TRẢ VỀ CHỈ MỘT CHUỖI JSON HỢP LỆ, KHÔNG BAO GỒM BẤT KỲ VĂN BẢN NÀO KHÁC BÊN NGOÀI JSON.

{{
  "score": <Điểm tổng 0-100 (INT)>,
  "grade": "<Hạng chữ (Vd: A, B+, C)>",
  "breakdown": [
    {{ "name": "<Tiêu chí>", "score": <Điểm>, "max": <Điểm tối đa>, "reason": "<Lý do chấm điểm dài, chi tiết>" }}
  ],
  "strengths": [
    "<điểm mạnh 1: NÊU RÕ VÀ SÂU, tối thiểu 50 chữ>"
  ],
  "weaknesses": [
    "<điểm yếu 1: NÊU RÕ VÀ SÂU, tối thiểu 50 chữ>"
  ],
  "recommendations": [
    "<khuyến nghị 1: HÀNH ĐỘNG CỤ THỂ, tối thiểu 50 chữ>"
  ],
  "funding_scenario": {{
    "desired_amount": "<Số tiền doanh nghiệp mong muốn, lấy từ {desired_amount} hoặc suy luận>",
    "recommended_amount": "<Số tiền hệ thống khuyến nghị để đạt hiệu quả cao nhất (Vd: 5 tỷ, 10 tỷ)>",
    "rationale": {{
      "why_recommended": "<PHÂN TÍCH SẮC BÉN VÀ DÀI (Ít nhất 150 chữ)>",
      "investment_needs": [
        "<Nhu cầu cốt lõi 1>"
      ]
    }},
    "scenarios": [
      {{
        "name": "<Tên Kịch Bản>",
        "focus_explanation": "<PHÂN TÍCH SÂU>",
        "allocation": [
          {{ 
            "category": "<Tên Hạng mục>", 
            "percentage": "<%>", 
            "amount": "<Số tiền cụ thể>", 
            "why_invest": "<PHÂN TÍCH SÂU>",
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
    "burn_rate_runway": "<Đánh giá chi tiết (Ít nhất 100 chữ)>",
    "milestones": [
      {{ "phase": "<Giai đoạn 1>", "goal": "<Mục tiêu>" }}
    ],
    "suggested_deal": {{
      "instrument": "<Công cụ: SAFE, Cổ phần ưu đãi...>",
      "pre_money": "<Định giá Pre-money ước tính>",
      "post_money": "<Định giá Post-money>",
      "dilution": "<% pha loãng ước tính>",
      "note": "<Lưu ý thêm về định giá (nếu có)>"
    }},
    "final_recommendation": "<KHUYẾN NGHỊ CUỐI CÙNG (Ít nhất 100 chữ)>"
  }}
}}
"""
with open('prompt_dump.txt', 'w', encoding='utf-8') as f:
    f.write(prompt)
