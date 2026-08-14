# Matcher Engine - Phân tích & Match Profile

Module phân tích mô tả doanh nghiệp và tìm profile phù hợp nhất từ 6 bộ dữ liệu mẫu.

## Cách hoạt động

1. **Extract Keywords**: Phân tích input text để tìm keywords về:
   - Industry (agritech, edtech, healthtech, logistics, manufacturing, saas)
   - Stage (seed, series_a, series_b, enterprise, sme)
   - Financial (revenue_high, revenue_medium, revenue_low, burn_rate, positive_cashflow)

2. **Calculate Similarity**: Tính điểm tương đồng với từng profile dựa trên:
   - Keyword matching (industry, stage, financial)
   - Text similarity với summary (SequenceMatcher)
   - Score alignment (sớm vs hoàn chỉnh)

3. **Return Top Matches**: Trả về top N profiles phù hợp nhất

## 6 Bộ dữ liệu mẫu

| Profile | Industry | Stage | Score | Mô tả |
|---------|----------|-------|-------|-------|
| **GreenCart** | AgriTech | Seed | 34 | Startup nông nghiệp giai đoạn rất sớm, MVP, 200 khách hàng |
| **EduPath** | EdTech | SME | 34 | Hộ kinh doanh giáo dục, 5 năm, 150 học viên |
| **LogiTrack** | Logistics SaaS | Series A | 56 | SaaS logistics, ARR 4.2 tỷ, 45 khách hàng |
| **Tradeco** | Manufacturing | SME Transform | 58 | Sản xuất thương mại 10 năm, 45 tỷ/năm, 120 nhân viên |
| **AgriSense** | AgriTech IoT | Growth | 74 | AgriTech IoT, ARR 18 tỷ, 180 trang trại |
| **MedConnect** | HealthTech | Enterprise | 90 | HealthTech enterprise, ARR 85 tỷ, 45 bệnh viện, sẵn sàng IPO |

## API Endpoints

### `POST /api/match-profile`

Tìm top N profiles phù hợp nhất với mô tả.

**Input:**
```json
{
  "description": "Startup nông nghiệp công nghệ cao, mới thành lập, đang phát triển MVP...",
  "top_n": 3
}
```

**Output:**
```json
{
  "matches": [
    {
      "profile_id": "greencart_seed",
      "company_name": "GreenCart",
      "industry": "AgriTech",
      "stage": "Seed",
      "total_score": 34,
      "grade": "Tier 1 - Chưa đủ điều kiện gọi vốn",
      "similarity_score": 33.48,
      "summary": "GreenCart là startup AgriTech giai đoạn rất sớm..."
    }
  ]
}
```

### `POST /api/analyze-with-reference`

Phân tích và trả về full analysis từ profile phù hợp nhất.

**Input:**
```json
{
  "description": "Startup nông nghiệp công nghệ cao, mới thành lập..."
}
```

**Output:**
```json
{
  "matched_profile": {
    "company_name": "GreenCart",
    "similarity_score": 33.48,
    "total_score": 34
  },
  "full_analysis": {
    "score": {...},
    "analysis": {...},
    "recommendations": [...],
    "risks": [...]
  },
  "comparison_note": "Doanh nghiệp của bạn có điểm tương đồng với GreenCart..."
}
```

## Test Results

```
=== Test 1: AgriTech Seed ===
  GreenCart - similarity: 33.48 - Seed - Score: 34 ✓
  AgriSense - similarity: 12.09 - Growth Stage - Score: 74
  EduPath - similarity: 6.47 - SME - Score: 34

=== Test 2: SaaS Logistics Growth ===
  LogiTrack - similarity: 21.97 - Series A - Score: 56 ✓
  AgriSense - similarity: 6.97 - Growth Stage - Score: 74
  MedConnect - similarity: 1.5 - Enterprise Ready - Score: 90

=== Test 3: HealthTech Enterprise ===
  MedConnect - similarity: 61.97 - Enterprise Ready - Score: 90 ✓
  AgriSense - similarity: 2.43 - Growth Stage - Score: 74
  Tradeco - similarity: 2.17 - SME chuyển đổi số - Score: 58

=== Test 4: SME Manufacturing ===
  Tradeco - similarity: 19.55 - SME chuyển đổi số - Score: 58 ✓
  EduPath - similarity: 3.25 - SME - Score: 34
  MedConnect - similarity: 1.5 - Enterprise Ready - Score: 90
```

## Sử dụng

```python
from matcher_engine import find_best_match, analyze_with_reference

# Tìm top 3 profiles phù hợp
matches = find_best_match("Startup nông nghiệp mới thành lập...", top_n=3)

# Phân tích chi tiết với reference
result = analyze_with_reference("Startup nông nghiệp mới thành lập...")
print(result["matched_profile"]["company_name"])  # GreenCart
print(result["recommendations"])  # Danh sách khuyến nghị
```

## Ưu điểm

- **Không cần API call**: Matcher chạy local, không tốn Gemini API credits
- **Nhanh**: < 100ms cho mỗi query
- **Deterministic**: Cùng input → cùng output
- **Explainable**: Có similarity score để hiểu tại sao match

## Hạn chế

- **Chỉ 6 profiles**: Cần thêm profiles để cover nhiều industry/stage hơn
- **Keyword-based**: Có thể miss nếu input dùng từ khác
- **No ML**: Không có machine learning, chỉ dựa trên rule-based matching

## Mở rộng

Để cải thiện accuracy:
1. Thêm nhiều profiles (20-30 profiles cho các industry/stage khác nhau)
2. Dùng embeddings (sentence-transformers) thay vì keyword matching
3. Fine-tune model trên dataset thực tế
