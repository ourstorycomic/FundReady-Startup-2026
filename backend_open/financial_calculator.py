from schemas import FinancialCalculationRequest

def calculate_financial_score(req: FinancialCalculationRequest) -> dict:
    score = 0
    max_score = 100
    strengths = []
    weaknesses = []
    recommendations = []

    # 1. Revenue (0-20 points)
    if req.revenue > 1000000:
        score += 20
        strengths.append("Doanh thu rất tốt, cho thấy quy mô kinh doanh ổn định.")
    elif req.revenue > 100000:
        score += 15
        strengths.append("Doanh thu ở mức khá.")
    elif req.revenue > 0:
        score += 5
        weaknesses.append("Doanh thu còn thấp, cần có kế hoạch mở rộng thị trường.")
        recommendations.append("Tập trung vào các chiến lược growth hacking để tăng trưởng doanh thu.")
    else:
        weaknesses.append("Chưa có doanh thu hoặc doanh thu âm.")
        recommendations.append("Nhanh chóng tìm kiếm mô hình doanh thu khả thi (Monetization).")

    # 2. Gross Margin (0-20 points)
    if req.gross_margin >= 50:
        score += 20
        strengths.append("Biên lợi nhuận gộp rất cao, lợi thế cạnh tranh lớn.")
    elif req.gross_margin >= 20:
        score += 15
        strengths.append("Biên lợi nhuận gộp ở mức khỏe mạnh.")
    elif req.gross_margin > 0:
        score += 5
        weaknesses.append("Biên lợi nhuận gộp thấp.")
        recommendations.append("Tối ưu hóa chi phí giá vốn (COGS) để cải thiện biên lợi nhuận.")
    else:
        weaknesses.append("Lợi nhuận gộp âm, mô hình kinh doanh đang gặp vấn đề cốt lõi.")
        recommendations.append("Đánh giá lại cơ cấu chi phí sản phẩm ngay lập tức.")

    # 3. ROE (0-15 points)
    if req.roe >= 20:
        score += 15
        strengths.append("ROE rất xuất sắc, hiệu quả sử dụng vốn tuyệt vời.")
    elif req.roe >= 10:
        score += 10
        strengths.append("ROE đạt chuẩn ngành.")
    elif req.roe > 0:
        score += 5
        weaknesses.append("Hiệu quả sử dụng vốn (ROE) còn khiêm tốn.")
        recommendations.append("Tìm cách cải thiện lợi nhuận ròng hoặc cơ cấu lại vốn chủ sở hữu.")
    else:
        weaknesses.append("ROE âm, công ty đang lỗ.")
        recommendations.append("Ưu tiên cắt giảm các khoản chi phí không cần thiết để đạt điểm hòa vốn.")

    # 4. Current Ratio (0-15 points)
    if req.current_ratio >= 1.5:
        score += 15
        strengths.append("Thanh khoản cực kỳ an toàn (Current Ratio >= 1.5).")
    elif req.current_ratio >= 1.0:
        score += 10
        strengths.append("Thanh khoản ở mức chấp nhận được.")
    else:
        weaknesses.append("Rủi ro thanh khoản cao (Current Ratio < 1).")
        recommendations.append("Cần tăng tài sản ngắn hạn hoặc giảm nợ ngắn hạn để tránh rủi ro vỡ nợ.")

    # 5. Debt to Equity (0-15 points)
    if req.debt_to_equity < 0.5:
        score += 15
        strengths.append("Tỷ lệ nợ trên vốn chủ sở hữu thấp, cấu trúc vốn an toàn.")
    elif req.debt_to_equity <= 1.5:
        score += 10
        strengths.append("Đòn bẩy tài chính ở mức vừa phải.")
    else:
        weaknesses.append("Đòn bẩy tài chính quá cao, rủi ro nợ vay lớn.")
        recommendations.append("Cân nhắc huy động thêm vốn cổ phần (Equity) thay vì vay nợ thêm.")

    # 6. Cash Flow Margin (0-15 points)
    if req.cash_flow_margin >= 15:
        score += 15
        strengths.append("Dòng tiền tạo ra từ doanh thu rất dồi dào.")
    elif req.cash_flow_margin >= 5:
        score += 10
        strengths.append("Biên dòng tiền dương và ổn định.")
    else:
        weaknesses.append("Biên dòng tiền yếu hoặc âm.")
        recommendations.append("Kiểm soát chặt chẽ các khoản phải thu và hàng tồn kho để cải thiện dòng tiền.")

    # Determine Grade
    if score >= 80:
        grade = "Tier 4 - Enterprise Ready"
    elif score >= 60:
        grade = "Tier 3 - Tăng trưởng mạnh"
    elif score >= 40:
        grade = "Tier 2 - Đủ điều kiện gọi vốn vòng Seed/Series A"
    else:
        grade = "Tier 1 - Chưa đủ điều kiện gọi vốn"

    return {
        "score": score,
        "max_score": max_score,
        "grade": grade,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }
