# Hướng dẫn Test AI Matcher

## 1. Chạy Backend

```bash
cd /home/schizo16/fundready-demo/backend
source .venv/bin/activate
python main.py
```

Backend chạy tại: http://localhost:8000

## 2. Test API với curl

### Test 1: AgriTech Seed → GreenCart
```bash
curl -X POST http://localhost:8000/api/analyze-with-reference \
  -H "Content-Type: application/json" \
  -d '{"description": "Startup nông nghiệp công nghệ cao, mới thành lập 6 tháng, đang phát triển MVP cho giải pháp IoT giám sát cây trồng."}'
```

**Expected:** Matched với GreenCart (Score: 34, Similarity: ~29)

### Test 2: SaaS Logistics → LogiTrack
```bash
curl -X POST http://localhost:8000/api/analyze-with-reference \
  -H "Content-Type: application/json" \
  -d '{"description": "Công ty SaaS về quản lý vận tải, ARR 18 tỷ tăng trưởng 220%/năm. Đã có 180 khách hàng doanh nghiệp, retention rate 95%. Đang gọi Series B."}'
```

**Expected:** Matched với LogiTrack (Score: 56, Similarity: ~22)

### Test 3: HealthTech Enterprise → MedConnect
```bash
curl -X POST http://localhost:8000/api/analyze-with-reference \
  -H "Content-Type: application/json" \
  -d '{"description": "HealthTech enterprise với ARR 85 tỷ, profitability 12%. Kiểm toán Big 4, governance chuẩn public company. Sản phẩm triển khai tại 45 bệnh viện. Sẵn sàng IPO."}'
```

**Expected:** Matched với MedConnect (Score: 90, Similarity: ~62)

### Test 4: SME Manufacturing → Tradeco
```bash
curl -X POST http://localhost:8000/api/analyze-with-reference \
  -H "Content-Type: application/json" \
  -d '{"description": "Doanh nghiệp sản xuất thương mại 10 năm, doanh thu 45 tỷ/năm, 120 nhân viên. Cần chuyển đổi số để tăng năng suất. Cần gọi vốn đầu tư ERP."}'
```

**Expected:** Matched với Tradeco (Score: 58, Similarity: ~20)

## 3. Test Frontend

### Cách 1: Mở file trực tiếp
```bash
# Mở danh-gia.html trong browser
open /home/schizo16/fundready-demo/danh-gia.html
```

### Cách 2: Serve với Python
```bash
cd /home/schizo16/fundready-demo
python3 -m http.server 8080
```

Truy cập: http://localhost:8080/danh-gia.html

### Test trên browser:

1. Cuộn xuống section "Phân tích nhanh với AI Matcher"
2. Nhập mô tả doanh nghiệp vào textarea
3. Click "Phân tích với AI"
4. Xem kết quả:
   - Tên company matched
   - Industry, Stage
   - Similarity score
   - Total score & grade
   - Summary
   - Top 5 recommendations

## 4. Kết quả Test

| Input | Matched Profile | Score | Similarity |
|-------|----------------|-------|------------|
| AgriTech Seed | GreenCart | 34 | 28.68 |
| SaaS Logistics | LogiTrack | 56 | 21.97 |
| HealthTech Enterprise | MedConnect | 90 | 61.97 |
| SME Manufacturing | Tradeco | 58 | 19.55 |

**Tất cả đều match đúng!**

## 5. Lưu ý

- Backend phải chạy trước khi test frontend
- API base URL trong frontend: `http://localhost:8000`
- Nếu deploy backend lên Railway/Render, cần update `API_BASE` trong `danh-gia.html`
- Matcher engine chạy local, không cần Gemini API key
