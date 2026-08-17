import os

NEW_PROMPT = '''    prompt = f"""Bạn là **Tổng Giám đốc Đầu tư (Managing Partner)** tại một quỹ Venture Capital hàng đầu thế giới. Bạn nổi tiếng với những bản phân tích (Due Diligence) cực kỳ khắt khe, dài dòng, và chi tiết đến từng ngóc ngách.

**PHONG CÁCH PHÂN TÍCH BẮT BUỘC:**
- Bản báo cáo phải RẤT DÀI, RẤT CỤ THỂ, phân tích mổ xẻ mọi góc độ (Market, Product, Team, Financials, Risks).
- Không được phép dùng những câu ngắn gọn. Mỗi câu phải chứa đựng data, insight, hoặc phân tích logic nhân quả.
- Trích dẫn mọi con số, luận điểm từ tài liệu. Đưa ra so sánh với các Benchmark ngành (Ví dụ: tỷ suất lợi nhuận SaaS trung bình, CAC/LTV ngành E-commerce...).

**NHIỆM VỤ:**
Phân tích tài liệu "{doc_info['name']}" theo bộ tiêu chí chuyên gia:

{criteria_text}

**NỘI DUNG TÀI LIỆU:**
{content[:25000]}

**YÊU CẦU TRẢ LỜI (JSON format) - BẮT BUỘC PHẢI DÀI VÀ SIÊU CHI TIẾT (TỐI THIỂU 2000 TỪ TỔNG CỘNG):**
{{
  "score": <điểm 0-100>,
  "breakdown": [
    {{
      "name": "<tên tiêu chí>",
      "score": <điểm cụ thể>,
      "max": <điểm tối đa>,
      "reason": "<PHÂN TÍCH SẮC BÉN DÀI TỐI THIỂU 300 CHỮ MỖI TIÊU CHÍ. Mổ xẻ sâu mọi điểm mạnh yếu, so sánh rủi ro, đưa ra lập luận chặt chẽ>"
    }}
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
  "funding_scenario": {{
    "desired_amount": "<Số tiền doanh nghiệp mong muốn, lấy từ {desired_amount} hoặc suy luận>",
    "recommended_amount": "<Số tiền hệ thống khuyến nghị để đạt hiệu quả cao nhất (Vd: 5 tỷ, 10 tỷ)>",
    "rationale": {{
      "why_recommended": "<PHÂN TÍCH ĐỊNH GIÁ & VỐN (Ít nhất 400 chữ, mổ xẻ mọi góc độ): Tại sao mức tiền này là chuẩn nhất? Nó giúp startup sống được bao lâu (runway)? So sánh với số tiền startup muốn gọi.>",
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
        "focus_explanation": "<PHÂN TÍCH TẦM NHÌN (Ít nhất 250 chữ, phân tích chuyên sâu): Kịch bản này dành cho việc chiếm lĩnh thị trường ra sao? Cần thực thi thế nào?>",
        "allocation": [
          {{ 
            "category": "<Hạng mục 1>", 
            "percentage": "<%>", 
            "amount": "<Số tiền>", 
            "why_invest": "<LÝ DO CHI TIẾT (Ít nhất 150 chữ)>",
            "action_items": ["<Hành động 1 rất chi tiết>", "<Hành động 2 rất chi tiết>", "<Hành động 3>"]
          }},
          {{ 
            "category": "<Hạng mục 2>", 
            "percentage": "<%>", 
            "amount": "<Số tiền>", 
            "why_invest": "<LÝ DO CHI TIẾT (Ít nhất 150 chữ)>",
            "action_items": ["<Hành động 1>", "<Hành động 2>", "<Hành động 3>"]
          }},
          {{ 
            "category": "<Hạng mục 3>", 
            "percentage": "<%>", 
            "amount": "<Số tiền>", 
            "why_invest": "<LÝ DO CHI TIẾT (Ít nhất 150 chữ)>",
            "action_items": ["<Hành động 1>", "<Hành động 2>"]
          }}
        ],
        "expected_results": [
          "<Kỳ vọng 1>", "<Kỳ vọng 2>", "<Kỳ vọng 3>", "<Kỳ vọng 4>"
        ]
      }},
      {{
        "name": "<Phương án B - Tinh gọn & Sống sót (Bootstrapping & Survival)>",
        "focus_explanation": "<PHÂN TÍCH TẦM NHÌN (Ít nhất 250 chữ, phân tích chuyên sâu): Kịch bản phòng thủ, cắt giảm chi phí, tập trung dòng tiền dương?>",
        "allocation": [
          {{ 
            "category": "<Hạng mục 1>", 
            "percentage": "<%>", 
            "amount": "<Số tiền>", 
            "why_invest": "<LÝ DO CHI TIẾT (Ít nhất 150 chữ)>",
            "action_items": ["<Hành động 1 rất chi tiết>", "<Hành động 2 rất chi tiết>"]
          }},
          {{ 
            "category": "<Hạng mục 2>", 
            "percentage": "<%>", 
            "amount": "<Số tiền>", 
            "why_invest": "<LÝ DO CHI TIẾT (Ít nhất 150 chữ)>",
            "action_items": ["<Hành động 1>", "<Hành động 2>"]
          }}
        ],
        "expected_results": [
          "<Kỳ vọng 1>", "<Kỳ vọng 2>", "<Kỳ vọng 3>"
        ]
      }}
    ],
    "burn_rate_runway": "<ĐÁNH GIÁ TÀI CHÍNH (Ít nhất 250 chữ, phân tích chuyên sâu): Tốc độ đốt tiền dự kiến? Bao nhiêu tháng thì hết vốn? Điểm hòa vốn ở đâu?>",
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
      "note": "<GHI CHÚ ĐÀM PHÁN (Ít nhất 200 chữ): Lời khuyên đàm phán Term Sheet cho Founder>"
    }},
    "final_recommendation": "<TỔNG KẾT VÀ QUYẾT ĐỊNH (Ít nhất 300 chữ, mổ xẻ mọi góc độ): Tóm lại quỹ có nên đầu tư không? Startup có đáng giá không? Founder cần làm gì ngay ngày mai?>"
  }}
}}

**LƯU Ý QUAN TRỌNG VỀ ĐỘ DÀI VÀ CẤU TRÚC - BẮT BUỘC PHẢI THEO:**
1. Trả về ĐÚNG cấu trúc JSON ở trên, ĐẦY ĐỦ TOÀN BỘ CÁC TRƯỜNG.
2. Viết càng chi tiết càng tốt, bạn không bị giới hạn độ dài. Hãy phân tích như một bản báo cáo Due Diligence chuyên sâu.
3. CHẮC CHẮN MẢNG `scenarios` CÓ 2 PHƯƠNG ÁN RÕ RÀNG."""'''

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = '    prompt = f"""Bạn là'
    end_marker = '3. CHẮC CHẮN MẢNG `scenarios` CÓ 2 PHƯƠNG ÁN RÕ RÀNG."""'
    
    if start_marker in content and end_marker in content:
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker) + len(end_marker)
        
        new_content = content[:start_idx] + NEW_PROMPT + content[end_idx:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Replaced in {filepath}")
    else:
        print(f"Markers not found in {filepath}!")

replace_in_file('fundready-demo-main/api/groq_client.py')
replace_in_file('fundready-demo-main/api/gemini_client.py')
