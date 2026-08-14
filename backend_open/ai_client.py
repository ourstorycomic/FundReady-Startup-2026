import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

def analyze_document_content(document_type: str, content: str) -> dict:
    if not client:
        # Fallback if no API key
        return _fallback_response()
        
    system_prompt = """
    Bạn là một Chuyên gia phân tích Quỹ đầu tư (VC Analyst) kỳ cựu.
    
    QUY TẮC XUẤT DỮ LIỆU BẮT BUỘC:
    1. Output CHỈ ĐƯỢC PHÉP là chuẩn định dạng JSON hợp lệ. Không thêm bất kỳ text bình luận nào ở đầu hay cuối.
    2. Các trường "score" và "maximum" BẮT BUỘC phải là SỐ NGUYÊN (Integer), tuyệt đối không dùng chuỗi (string) hay để trống.
    3. Trong mảng "breakdown", trường "reason" BẮT BUỘC viết liền một mạch, KHÔNG dùng ký tự xuống dòng (\\n), KHÔNG dùng dấu nháy kép (") bên trong câu, KHÔNG dùng cú pháp Markdown để tránh lỗi parse bảng HTML.
    4. Các phần tử còn lại (Kịch bản gọi vốn, điểm mạnh/yếu) bắt buộc phải viết thật chi tiết, có chiều sâu, từ 3-5 câu mỗi trường.
    """

    user_prompt = f"""
    Hãy đánh giá doanh nghiệp dựa trên nội dung tài liệu sau đây ({document_type}):
    {content[:8000]}
    
    Hãy chấm điểm theo 4 tiêu chí cốt lõi sau:
    1. Cấu trúc vốn & Quản trị (20 điểm)
    2. Tình hình Tài chính (30 điểm)
    3. Thị trường & Sản phẩm (30 điểm)
    4. Pháp lý (20 điểm)

    Dựa trên đánh giá, hãy xây dựng một "Kịch bản gọi vốn" (Funding Scenario) chuyên sâu. Nếu doanh nghiệp không đề xuất số tiền cụ thể, mặc định là "3,000,000,000 VNĐ".

    Hãy trả về ĐÚNG CẤU TRÚC JSON MẪU DƯỚI ĐÂY (Thay thế các value mẫu bằng dữ liệu phân tích của bạn):
    {{
        "score": 85,
        "max_score": 100,
        "grade": "Tier 2 - Tiềm năng bứt phá",
        "breakdown": [
            {{"name": "Cấu trúc vốn & Quản trị", "score": 15, "maximum": 20, "reason": "Phân tích sâu sắc 3 câu về Cap table và Founders. Viết liền một mạch, tuyệt đối không xuống dòng."}},
            {{"name": "Tình hình Tài chính", "score": 25, "maximum": 30, "reason": "Phân tích chi tiết ARR và biên lợi nhuận. Viết liền một mạch, tuyệt đối không xuống dòng."}},
            {{"name": "Thị trường & Sản phẩm", "score": 25, "maximum": 30, "reason": "Phân tích rào cản cạnh tranh và quy mô thị trường. Viết liền một mạch, tuyệt đối không xuống dòng."}},
            {{"name": "Pháp lý", "score": 20, "maximum": 20, "reason": "Đánh giá tình trạng pháp nhân và hợp đồng. Viết liền một mạch, tuyệt đối không xuống dòng."}}
        ],
        "strengths": ["Điểm mạnh cốt lõi 1 mang tính chiến lược", "Điểm mạnh cốt lõi 2 mang tính chiến lược"],
        "weaknesses": ["Rủi ro 1 cần khắc phục ngay", "Rủi ro 2 cần lưu ý"],
        "recommendations": ["Khuyến nghị hành động 1 thực tế", "Khuyến nghị hành động 2 chi tiết"],
        "funding_scenario": {{
            "current_desire": "Viết 1 đoạn văn dài (4-5 câu) tóm tắt bối cảnh và 3 nhu cầu đầu tư lớn nhất của doanh nghiệp.",
            "recommendation": {{
                "desired_amount": "3 Tỷ VNĐ",
                "recommended_amount": "5 Tỷ VNĐ",
                "difference": "+2 Tỷ VNĐ",
                "rationale": "Viết 1 đoạn văn dài lập luận tài chính sắc bén tại sao đề xuất mức này."
            }},
            "scenarios": [
                {{
                    "name": "Phương án A - Mức vốn hệ thống khuyến nghị",
                    "allocation": [
                        {{"category": "R&D - Sản phẩm", "percentage": "50%", "amount": "2.5 Tỷ", "objective": "Nâng cấp cốt lõi"}},
                        {{"category": "Marketing & Sales", "percentage": "30%", "amount": "1.5 Tỷ", "objective": "Thu hút người dùng"}},
                        {{"category": "Vận hành", "percentage": "20%", "amount": "1 Tỷ", "objective": "Mở rộng hệ thống"}}
                    ],
                    "focus": "Mô tả chiến lược trọng tâm thật chi tiết. Viết ít nhất 3-4 câu.",
                    "expected_result": "Liệt kê các mốc doanh thu, số lượng người dùng kỳ vọng đạt được."
                }}
            ],
            "investment_details": [
                {{
                    "category": "2.5 Tỷ cho R&D",
                    "amount": "2.5 Tỷ",
                    "why_invest": "Phân tích sâu sắc lý do tại sao phải rót vốn vào đây.",
                    "to_solve": ["Vấn đề công nghệ 1", "Vấn đề công nghệ 2"],
                    "expected_result": "Sản phẩm tốt hơn, giữ chân khách hàng lâu hơn."
                }}
            ],
            "comparison_rationale": "Đoạn văn tóm tắt sự khác biệt giữa phương án hiện tại và đề xuất.",
            "comparison_table": [
                {{"category": "Tốc độ tăng trưởng", "scenario_a": "Thận trọng", "scenario_b": "Tăng tốc bứt phá"}},
                {{"category": "R&D", "scenario_a": "Duy trì", "scenario_b": "Nâng cấp toàn diện"}}
            ],
            "final_advice": "Đưa ra lời khuyên chốt hạ mạnh mẽ về mức định giá và nhượng cổ phần."
        }}
    }}
    """
    
    # DEMO MODE HACK: If this is the Nexus Digital demo text, force the perfect hardcoded response
    # BỎ COMMENT HOẶC XÓA ĐOẠN NÀY ĐI
    # if "Nexus Digital" in content and "15tr/tháng" in content:
    #     return _fallback_response()
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        response_text = chat_completion.choices[0].message.content
        return json.loads(response_text)
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return _fallback_response()

def analyze_full_assessment(documents_content: str, financials: dict = None) -> dict:
    if not client:
        return _fallback_response()
        
    fin_text = json.dumps(financials, ensure_ascii=False) if financials else "Không có dữ liệu tài chính."
    
    prompt = f"""
    Bạn là một chuyên gia đánh giá đầu tư. Dưới đây là thông tin tổng hợp của một doanh nghiệp:
    
    Tài liệu đính kèm (đã trích xuất):
    {documents_content[:6000]}
    
    Dữ liệu tài chính:
    {fin_text}
    
    Dựa trên tất cả thông tin này, hãy đánh giá tổng thể doanh nghiệp và trả về JSON:
    {{
        "score": <điểm số tổng quát 0-100>,
        "max_score": 100,
        "grade": "<Xếp loại>",
        "strengths": ["<điểm mạnh>"],
        "weaknesses": ["<điểm yếu>"],
        "recommendations": ["<khuyến nghị hành động>"]
    }}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a top-tier VC analyst. Output JSON only."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192", # Dùng model lớn hơn cho đánh giá toàn diện
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"Error calling Groq API (Full Assessment): {e}")
        return _fallback_response()

def _fallback_response():
    return {
        "score": 50,
        "max_score": 100,
        "grade": "Tier 1 - Đang trong quá trình đánh giá",
        "breakdown": [
            {"name": "Cấu trúc vốn & Quản trị", "score": 10, "maximum": 20, "reason": "Dữ liệu mẫu từ Fallback. Hãy kiểm tra lại API Key hoặc tắt chế độ Demo."},
            {"name": "Tình hình Tài chính", "score": 15, "maximum": 30, "reason": "Dữ liệu mẫu từ Fallback. Hãy kiểm tra lại kết nối mạng."},
            {"name": "Thị trường & Sản phẩm", "score": 15, "maximum": 30, "reason": "Dữ liệu mẫu từ Fallback. AI chưa được gọi thành công."},
            {"name": "Pháp lý", "score": 10, "maximum": 20, "reason": "Dữ liệu mẫu từ Fallback. Vui lòng thử lại."}
        ],
        "strengths": ["Đã cung cấp tài liệu đầy đủ"],
        "weaknesses": ["Chưa thể phân tích chuyên sâu do đang ở chế độ Fallback/Demo"],
        "recommendations": ["Vui lòng cấu hình API Key (GROQ_API_KEY) trong file .env", "Tắt đoạn code DEMO MODE HACK để AI hoạt động."],
        "funding_scenario": {
            "current_desire": "Theo thông tin cung cấp, Nexus Digital hiện mong muốn huy động 3 tỷ đồng để phục vụ quá trình phát triển và mở rộng hoạt động kinh doanh. Tuy nhiên hệ thống nhận thấy doanh nghiệp đang đứng trước 3 nhu cầu đầu tư lớn: Nâng cấp AI, Marketing, và Hạ tầng.",
            "recommendation": {
                "desired_amount": "3 tỷ VNĐ",
                "recommended_amount": "5 tỷ VNĐ",
                "difference": "+2 tỷ VNĐ",
                "rationale": "Với 3 tỷ đồng, Nexus Digital có thể ưu tiên giải quyết một số vấn đề cấp thiết nhất..."
            },
            "scenarios": [
                {
                    "name": "Phương án A – Nếu doanh nghiệp giữ mức gọi vốn 3 tỷ đồng",
                    "allocation": [
                        {"category": "R&D – AI & Công nghệ", "percentage": "50%", "amount": "1,5 tỷ", "objective": "Củng cố sản phẩm"}
                    ],
                    "focus": "Mô phỏng chiến lược",
                    "expected_result": "Mô phỏng kết quả"
                }
            ],
            "investment_details": [
                {
                    "category": "2,5 tỷ đồng cho R&D",
                    "amount": "2,5 tỷ",
                    "why_invest": "Phân tích mẫu",
                    "to_solve": ["Nâng cấp AI"],
                    "expected_result": "Sản phẩm tốt hơn"
                }
            ],
            "comparison_rationale": "Hệ thống không phủ nhận nhu cầu 3 tỷ...",
            "comparison_table": [
                {"category": "R&D", "scenario_a": "Củng cố", "scenario_b": "Phát triển mạnh"}
            ],
            "final_advice": "Nếu Nexus Digital ưu tiên kiểm soát tỷ lệ pha loãng..."
        }
    }
