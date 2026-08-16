# FundReady AI - Nền tảng Đánh giá Sẵn sàng Gọi vốn

> Hệ thống AI đánh giá mức độ sẵn sàng gọi vốn của doanh nghiệp Việt Nam

## 🚀 Live Demo

- **Frontend:** https://fundready-demo.vercel.app/danh-gia.html
- **Backend API:** https://fundready-backend.onrender.com
- **API Docs:** https://fundready-backend.onrender.com/docs

## ✨ Tính năng chính

### 🎯 AI Matcher Engine (Mới!)
- Phân tích mô tả doanh nghiệp và tìm hồ sơ mẫu phù hợp nhất
- Không cần Gemini API, chạy nhanh và miễn phí
- Trả về điểm số, khuyến nghị và phân tích chi tiết

**Test ngay:**
```bash
curl -X POST https://fundready-backend.onrender.com/api/analyze-with-reference \
  -H "Content-Type: application/json" \
  -d '{"description": "Startup nông nghiệp công nghệ cao, mới thành lập, đang phát triển MVP"}'
```

### 📊 6 Hồ sơ Mẫu Thực tế
- **GreenCart** (AgriTech Seed) - 34/100
- **EduPath** (EdTech SME) - 34/100
- **LogiTrack** (Logistics Series A) - 56/100
- **Tradeco** (Manufacturing SME) - 58/100
- **AgriSense** (AgriTech IoT Growth) - 74/100
- **MedConnect** (HealthTech Enterprise) - 90/100

### 📄 Phân tích Tài liệu
- Upload PDF/DOCX/XLSX
- AI phân tích theo 16 loại tài liệu
- Chấm điểm và đưa ra khuyến nghị

### 💰 Financial Calculator
- Tính điểm tài chính từ số liệu thực
- 6 nhóm tiêu chí: Capital Structure, Financial Position, Cash Flow, Governance, Legal, Valuation

## 🛠️ Công nghệ

- **Backend:** FastAPI (Python)
- **Frontend:** HTML/CSS/JavaScript (vanilla)
- **AI:** Google Gemini API + Custom Matcher Engine
- **Deploy:** Render (backend) + Vercel (frontend)

## 📚 Tài liệu

- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Tổng quan dự án
- [DEPLOY.md](DEPLOY.md) - Hướng dẫn deploy
- [SETUP.md](SETUP.md) - Setup local development
- [TEST_MATCHER.md](TEST_MATCHER.md) - Test AI Matcher
- [backend/README.md](backend/README.md) - API documentation

## 🎬 Demo nhanh

1. Truy cập: https://fundready-demo.vercel.app/danh-gia.html
2. Cuộn xuống "Phân tích nhanh với AI Matcher"
3. Nhập mô tả doanh nghiệp
4. Click "Phân tích với AI"
5. Xem kết quả: điểm số, khuyến nghị, phân tích chi tiết

## 📊 API Endpoints

### AI Matcher (Recommended)
```bash
POST /api/analyze-with-reference
{
  "description": "Mô tả doanh nghiệp..."
}
```

### File Upload
```bash
POST /api/upload-document
- file: PDF/DOCX/XLSX
- document_type: pitchdeck, bizplan, etc.
```

### Financial Calculator
```bash
POST /api/financial-calculate
{
  "revenue": 184500,
  "gross_margin": 49.4,
  "roe": 32.8,
  "current_ratio": 2.61,
  "debt_to_equity": 0.55,
  "cash_flow_margin": 15.4
}
```

## 💡 Sử dụng

### Local Development
```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# Frontend
python3 -m http.server 8000
# Mở http://localhost:8000/danh-gia.html
```

### Production
- Backend tự động deploy từ GitHub lên Render
- Frontend tự động deploy từ GitHub lên Vercel

## 📈 Roadmap

- [ ] Thêm 20+ profiles cho matcher
- [ ] Export PDF reports
- [ ] User authentication
- [ ] Database integration
- [ ] Multi-language support

## 📝 License

Private - Internal Use Only

## 👥 Liên hệ

Dự án phát triển cho cuộc thi 30/07/2026

---

**Status:** ✅ Production-ready (demo)  
**Last Updated:** 29/07/2026
