# Hướng dẫn sử dụng FundReady AI

## Cách hoạt động

Hệ thống FundReady AI sử dụng **Gemini API thật** để phân tích doanh nghiệp của bạn dựa trên framework tiêu chuẩn từ 6 hồ sơ mẫu thực tế.

### Quy trình phân tích

1. **Input**: Bạn nhập mô tả doanh nghiệp (ngành nghề, giai đoạn, doanh thu, đội ngũ, sản phẩm, v.v.)

2. **Matching**: Hệ thống tìm hồ sơ mẫu có đặc điểm gần giống nhất làm framework tham chiếu

3. **AI Analysis**: Gemini API phân tích input của bạn dựa trên framework đó:
   - Chấm điểm từng tiêu chí (Capital Structure, Financial Position, Governance, v.v.)
   - Đưa ra nhận xét cụ thể cho từng tiêu chí
   - Đề xuất khuyến nghị hành động thực tế
   - Đánh giá rủi ro và KPIs mục tiêu

4. **Output**: Báo cáo chi tiết với:
   - Điểm tổng (0-100) và xếp hạng (Tier 1-5)
   - Bảng điểm chi tiết 6 nhóm tiêu chí
   - Phân tích chi tiết từng khía cạnh
   - SWOT Analysis (Điểm mạnh, Điểm yếu, Cơ hội, Thách thức)
   - Đánh giá rủi ro
   - Khuyến nghị hành động với mức độ ưu tiên
   - KPIs mục tiêu

## 6 Hồ sơ mẫu tham chiếu

| Profile | Ngành | Giai đoạn | Điểm mẫu |
|---------|-------|-----------|----------|
| GreenCart | AgriTech | Seed | 34/100 |
| EduPath | EdTech | SME | 34/100 |
| LogiTrack | Logistics | Series A | 56/100 |
| Tradeco | Manufacturing | SME | 58/100 |
| AgriSense | AgriTech IoT | Growth | 74/100 |
| MedConnect | HealthTech | Enterprise | 90/100 |

## Ví dụ input

### Ví dụ 1: Startup giai đoạn Seed
```
Startup nông nghiệp công nghệ cao, mới thành lập 6 tháng, đang phát triển MVP cho giải pháp IoT giám sát cây trồng. Đội ngũ 2 founders có kinh nghiệm nông nghiệp nhưng thiếu kỹ năng công nghệ. Doanh thu chưa có, cần gọi vốn seed 2 tỷ để hoàn thiện sản phẩm và mở rộng thị trường.
```

**Kết quả mong đợi**: Điểm thấp (15-30/100), Tier 4-5, khuyến nghị tập trung vào hoàn thiện sản phẩm và đội ngũ.

### Ví dụ 2: SME đang tăng trưởng
```
Công ty SaaS logistics, hoạt động 2 năm, ARR 4.2 tỷ VNĐ, tăng trưởng 180%/năm. Đội ngũ 15 người, có 45 khách hàng doanh nghiệp với retention rate 92%. Đang gọi Series A để mở rộng thị trường Đông Nam Á.
```

**Kết quả mong đợi**: Điểm trung bình (50-65/100), Tier 2-3, khuyến nghị về governance và mở rộng.

### Ví dụ 3: Enterprise sẵn sàng IPO
```
HealthTech enterprise, ARR 85 tỷ VNĐ, profitability 12%. Kiểm toán Big 4, governance chuẩn public company. Sản phẩm triển khai tại 45 bệnh viện. Sẵn sàng cho IPO hoặc strategic acquisition trong 18-24 tháng tới.
```

**Kết quả mong đợi**: Điểm cao (80-95/100), Tier 1, khuyến nghị về chiến lược exit.

## Lưu ý quan trọng

1. **Càng chi tiết càng tốt**: Input càng nhiều thông tin, AI phân tích càng chính xác
2. **Trung thực**: Đừng thêm thông tin không có thật, AI sẽ phát hiện và đánh giá thấp
3. **Cụ thể**: Thay vì "doanh thu tốt", hãy ghi "doanh thu 10 tỷ/năm, tăng trưởng 30%"
4. **Đầy đủ**: Bao gồm cả điểm mạnh và điểm yếu để AI đưa ra khuyến nghị cân bằng

## API Endpoints

### POST /api/analyze-with-reference
Phân tích input text và trả về báo cáo chi tiết.

**Request:**
```json
{
  "description": "Mô tả doanh nghiệp của bạn..."
}
```

**Response:**
```json
{
  "matched_profile": {
    "company_name": "Doanh nghiệp của bạn",
    "industry": "AgriTech",
    "stage": "Seed",
    "total_score": 17,
    "grade": "Tier 4 - Rất rủi ro",
    "similarity_score": 33.48,
    "summary": "..."
  },
  "score_breakdown": [...],
  "detailed_analysis": {...},
  "recommendations": [...],
  "risks": [...],
  "kpis": [...]
}
```

## Công nghệ

- **Backend**: FastAPI (Python)
- **AI**: Google Gemini 3.6 Flash API
- **Frontend**: HTML/CSS/JavaScript (vanilla)
- **Deploy**: Render (backend) + Vercel (frontend)

## Chi phí

- **Gemini API**: Free tier (15 RPM, 1M tokens/ngày)
- **Render**: Free tier (có sleep sau 15 phút)
- **Vercel**: Free tier (100GB bandwidth)

## Liên hệ

Nếu cần hỗ trợ hoặc có câu hỏi, vui lòng liên hệ qua GitHub Issues.
