# FundReady AI Backend

FastAPI backend cho hệ thống đánh giá hồ sơ gọi vốn FundReady AI.

## Setup

```bash
cd backend
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Copy .env và thêm Gemini API key
cp .env.example .env
# Edit .env: GEMINI_API_KEY=your_key_here
```

## Chạy local

```bash
python main.py
```

API chạy tại: http://localhost:8000

## API Endpoints

### `POST /api/match-profile` (Recommended - Fast & Free)

Tìm profile phù hợp nhất từ 6 bộ dữ liệu mẫu. **Không cần Gemini API, chạy local, nhanh.**

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
      "similarity_score": 33.48,
      "summary": "..."
    }
  ]
}
```

### `POST /api/analyze-with-reference` (Recommended - Fast & Free)

Phân tích chi tiết dựa trên profile phù hợp nhất.

**Input:**
```json
{
  "description": "Startup nông nghiệp công nghệ cao, mới thành lập..."
}
```

**Output:** Full analysis với recommendations, risks, KPIs từ profile match.

### `POST /api/upload-document`

Upload file PDF/DOCX/XLSX → phân tích với Gemini AI.

**Input:**
```json
{
  "file": "file.pdf",
  "document_type": "pitchdeck"
}
```

**Output:**
```json
{
  "filename": "file.pdf",
  "document_type": "pitchdeck",
  "content_length": 5000,
  "analysis": {
    "score": 85,
    "strengths": [...],
    "weaknesses": [...],
    "recommendations": [...]
  }
}
```

### `POST /api/financial-calculate`

Tính điểm tài chính từ số liệu.

**Input:**
```json
{
  "revenue": 184500,
  "gross_margin": 49.4,
  "roe": 32.8,
  "current_ratio": 2.61,
  "debt_to_equity": 0.55,
  "cash_flow_margin": 15.4
}
```

### `POST /api/full-assessment`

Đánh giá toàn bộ hồ sơ (16 loại tài liệu + tài chính).

**Input:**
```json
{
  "documents": {
    "pitchdeck": "Nội dung pitch deck...",
    "bizplan": "Nội dung kế hoạch kinh doanh..."
  },
  "financials": {
    "revenue": 184500,
    "gross_margin": 49.4
  }
}
```

## 6 Bộ dữ liệu mẫu (Matcher Engine)

| Profile | Industry | Stage | Score | Mô tả |
|---------|----------|-------|-------|-------|
| **GreenCart** | AgriTech | Seed | 34 | Startup nông nghiệp giai đoạn rất sớm |
| **EduPath** | EdTech | SME | 34 | Hộ kinh doanh giáo dục |
| **LogiTrack** | Logistics SaaS | Series A | 56 | SaaS logistics, ARR 4.2 tỷ |
| **Tradeco** | Manufacturing | SME Transform | 58 | Sản xuất thương mại 10 năm |
| **AgriSense** | AgriTech IoT | Growth | 74 | AgriTech IoT, ARR 18 tỷ |
| **MedConnect** | HealthTech | Enterprise | 90 | HealthTech enterprise, ARR 85 tỷ |

Xem chi tiết: [MATCHER_README.md](MATCHER_README.md)

## 16 loại tài liệu

| Key | Tên | Trọng số |
|-----|-----|----------|
| hsgt | Hồ sơ giới thiệu | 6% |
| pitchdeck | Pitch Deck | 9% |
| execsum | Executive Summary | 6% |
| bizplan | Kế hoạch kinh doanh | 9% |
| legalfin | Pháp lý & Tài chính | 9% |
| legal | Hồ sơ pháp lý | 6% |
| financial | Báo cáo tài chính | 9% |
| forecast | Dự báo tài chính | 6% |
| captable | Cap Table | 6% |
| shagreement | Hợp đồng cổ đông | 5% |
| shlist | Danh sách cổ đông | 3% |
| prodcust | Sản phẩm và khách hàng | 7% |
| ip | Hồ sơ sở hữu trí tuệ | 4% |
| proddata | Dữ liệu sản phẩm | 4% |
| custdata | Dữ liệu khách hàng | 5% |
| useoffunds | Kế hoạch sử dụng vốn | 6% |

## Deploy

### Railway
```bash
railway login
railway init
railway up
```

### Render
1. Push code lên GitHub
2. Connect Render với repo
3. Set environment variable: `GEMINI_API_KEY`
4. Deploy

## Cấu trúc

```
backend/
├── main.py                 # FastAPI app + routes
├── gemini_client.py        # Gemini API integration + 16 bộ tiêu chí
├── financial_calculator.py # Rule-based financial scoring
├── assessment_engine.py    # Orchestrator cho full assessment
├── requirements.txt
└── .env
```
