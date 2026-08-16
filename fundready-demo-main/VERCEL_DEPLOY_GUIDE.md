# Hướng dẫn Deploy Frontend lên Vercel

## Bước 1: Deploy lần đầu

### Qua Vercel CLI

```bash
cd /home/schizo16/fundready-demo

# Login (nếu chưa)
vercel login

# Deploy preview
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Which scope? (chọn account của bạn)
# - Link to existing project? N
# - Project name? fundready-demo
# - Directory? ./
# - Override settings? N

# Deploy production
vercel --prod
```

### Qua Web UI

1. Truy cập: https://vercel.com/new
2. Import Git Repository → chọn **fundready-demo**
3. Framework Preset: **Other**
4. Build Command: (để trống)
5. Output Directory: **./**
6. Click **Deploy**
7. Đợi 1-2 phút

## Bước 2: Kiểm tra

Sau khi deploy xong:
- **Preview URL:** `https://fundready-demo-xxxx.vercel.app`
- **Production URL:** `https://fundready-demo.vercel.app` (sau khi dùng `vercel --prod`)

## Bước 3: Update API_BASE

**QUAN TRỌNG:** Sau khi deploy backend lên Render và có URL, bạn cần update frontend.

1. Mở file `danh-gia.html`
2. Tìm dòng (khoảng dòng 2100):
```javascript
const API_BASE = 'http://localhost:8000';
```

3. Thay bằng URL backend Render:
```javascript
const API_BASE = 'https://fundready-backend-xxxx.onrender.com';
```

4. Commit và push:
```bash
git add danh-gia.html
git commit -m "Update API_BASE to production backend URL"
git push origin main
```

5. Vercel sẽ tự động redeploy

## Bước 4: Test End-to-End

1. Truy cập: `https://fundready-demo.vercel.app/danh-gia.html`
2. Cuộn xuống section "Phân tích nhanh với AI Matcher"
3. Nhập: "Startup nông nghiệp công nghệ cao, mới thành lập..."
4. Click "Phân tích với AI"
5. Xem kết quả

**Lưu ý:** Request đầu tiên có thể mất 30-60s vì Render backend đang wake up từ sleep mode.

## Troubleshooting

### Frontend không gọi được backend
1. Kiểm tra API_BASE đúng URL Render
2. Kiểm tra CORS: Backend đã config `allow_origins=["*"]`
3. Mở DevTools → Console tab để xem lỗi
4. Mở DevTools → Network tab để xem request/response

### Backend trả về lỗi
1. Kiểm tra backend URL có hoạt động không:
```bash
curl https://fundready-backend-xxxx.onrender.com/
```
2. Nếu backend sleep, đợi 30-60s để wake up
3. Kiểm tra Render logs để xem lỗi chi tiết

### Vercel deploy fail
1. Kiểm tra build logs trên Vercel dashboard
2. Đảm bảo không có syntax error trong HTML
3. Kiểm tra `.vercelignore` nếu có

## Custom Domain (Optional)

### Thêm custom domain trên Vercel

1. Vercel Dashboard → Project → Settings → Domains
2. Add domain (ví dụ: `fundready.yourdomain.com`)
3. Update DNS theo hướng dẫn
4. Đợi 5-30 phút để DNS propagate

## Environment Variables (nếu cần)

Nếu frontend cần environment variables:

1. Vercel Dashboard → Project → Settings → Environment Variables
2. Add variable (ví dụ: `API_BASE_URL`)
3. Redeploy

**Lưu ý:** Hiện tại `API_BASE` được hardcode trong `danh-gia.html`, không dùng environment variable.

## Monitoring

### Vercel Analytics
- Vercel Dashboard → Project → Analytics
- Xem page views, performance metrics

### Vercel Logs
- Vercel Dashboard → Project → Deployments
- Click vào deployment để xem build logs

## Rollback

Nếu cần rollback:
```bash
# Xem danh sách deployments
vercel ls

# Rollback về deployment cụ thể
vercel rollback
```

Hoặc qua Web UI:
- Vercel Dashboard → Project → Deployments
- Click "..." → "Promote to Production" cho deployment cũ

## Chi phí

- **Vercel Free Tier:** $0/month
  - 100GB bandwidth
  - Unlimited deployments
  - Automatic HTTPS
  - Custom domains

## Tổng kết

**URLs sau khi deploy:**
- Backend: `https://fundready-backend-xxxx.onrender.com`
- Frontend: `https://fundready-demo.vercel.app`

**Demo URL:**
`https://fundready-demo.vercel.app/danh-gia.html`

**Thời gian deploy:** 5-10 phút
**Chi phí:** $0 (free tier)
