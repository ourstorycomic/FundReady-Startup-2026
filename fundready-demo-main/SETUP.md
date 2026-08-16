# FundReady AI - Hướng dẫn Setup & Deploy

## Cấu trúc dự án

```
fundready-demo/
├── index.html              # Landing page
├── danh-gia.html           # Assessment tool (existing)
├── test-upload.html        # Test UI cho AI upload
├── ai-integration.js       # Frontend API client
└── backend/
    ├── main.py             # FastAPI server
    ├── gemini_client.py    # Gemini AI integration
    ├── financial_calculator.py
    ├── assessment_engine.py
    ├── file_parser.py      # PDF/DOCX/XLSX parser
    ├── requirements.txt
    ├── .env                # Thêm GEMINI_API_KEY
    └── .venv/              # Python virtual environment
```

## Local Development

### 1. Backend

```bash
cd backend

# Activate virtual environment
source .venv/bin/activate

# Thêm Gemini API key
echo "GEMINI_API_KEY=your_actual_key_here" > .env

# Chạy server
python main.py
```

Backend chạy tại: http://localhost:8000

### 2. Frontend

Mở `test-upload.html` trong browser, hoặc serve với:

```bash
# Terminal khác
python3 -m http.server 8080
```

Truy cập: http://localhost:8080/test-upload.html

### 3. Test API

```bash
# Test financial calculator
curl -X POST http://localhost:8000/api/financial-calculate \
  -H "Content-Type: application/json" \
  -d '{"revenue":184500,"gross_margin":49.4,"roe":32.8,"current_ratio":2.61,"debt_to_equity":0.55,"cash_flow_margin":15.4}'

# Test file upload
curl -X POST http://localhost:8000/api/upload-document \
  -F "file=@/path/to/file.pdf" \
  -F "document_type=pitchdeck"
```

## Deploy

### Option 1: Railway (Recommended)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Init project
cd backend
railway init

# Set environment variable
railway variables set GEMINI_API_KEY=your_key_here

# Deploy
railway up
```

### Option 2: Render

1. Push code lên GitHub
2. Vào render.com, tạo New Web Service
3. Connect GitHub repo
4. Root directory: `backend`
5. Build command: `pip install -r requirements.txt`
6. Start command: `python main.py`
7. Environment: thêm `GEMINI_API_KEY`
8. Deploy

### Update Frontend

Sau khi deploy backend, cập nhật `API_BASE` trong `ai-integration.js`:

```javascript
const API_BASE = 'https://your-backend-url.up.railway.app';
```

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/upload-document` | Upload file PDF/DOCX/XLSX → phân tích |
| POST | `/api/financial-calculate` | Tính điểm tài chính từ số liệu |
| POST | `/api/full-assessment` | Đánh giá toàn bộ hồ sơ |
| GET | `/` | Health check |

## 16 Loại tài liệu

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

## Troubleshooting

### Lỗi "API key not valid"
- Kiểm tra `.env` có `GEMINI_API_KEY` chưa
- Verify key tại: https://aistudio.google.com/apikey

### Lỗi "Connection refused"
- Đảm bảo backend đang chạy: `python main.py`
- Check port 8000 không bị占用: `lsof -i :8000`

### File quá lớn
- Tối đa 10MB cho mỗi file
- PDF scan (hình ảnh) cần OCR - chưa hỗ trợ

## Next Steps

- [ ] Thêm OCR cho PDF scan (pytesseract)
- [ ] Tích hợp vào `danh-gia.html` chính
- [ ] Thêm database lưu kết quả (SQLite/PostgreSQL)
- [ ] Authentication cho multi-user
- [ ] Export kết quả ra PDF
