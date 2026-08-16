# Hướng dẫn Deploy Fly.io

## Bước 1: Cài đặt Fly.io CLI

```bash
# macOS
brew install flyctl

# Linux/Windows
curl -L https://fly.io/install.sh | sh

# Hoặc dùng npm
npm install -g @flydotio/dockerfile
```

## Bước 2: Đăng ký và đăng nhập

```bash
# Đăng ký tài khoản (nếu chưa có)
fly auth signup

# Đăng nhập
fly auth login
```

## Bước 3: Deploy ứng dụng

```bash
cd backend

# Khởi tạo app trên Fly.io (chọn region gần nhất)
fly launch

# Khi được hỏi:
# - App name: fundready-backend (hoặc tên bạn thích)
# - Region: sin (Singapore - gần Việt Nam nhất)
# - PostgreSQL: No
# - Upstash Redis: No
# - Deploy now: Yes

# Set environment variables
fly secrets set GROQ_API_KEY=your_groq_api_key_here
fly secrets set GEMINI_API_KEY=your_gemini_api_key_here

# Deploy lại nếu cần
fly deploy
```

## Bước 4: Kiểm tra deployment

```bash
# Xem logs
fly logs

# Xem status
fly status

# Mở app trong browser
fly open
```

## Bước 5: Cập nhật frontend

Sau khi deploy xong, cập nhật `API_BASE` trong `danh-gia.html`:

```javascript
const API_BASE = 'https://fundready-backend.fly.dev';
```

Commit và push:
```bash
git add danh-gia.html
git commit -m "Update API_BASE to Fly.io URL"
git push
```

Deploy Vercel:
```bash
vercel --prod
```

## Tính năng Fly.io

- **Free tier**: 3 shared-cpu-1x VMs, 160GB outbound bandwidth
- **Auto-scaling**: Tự động scale lên khi có traffic
- **Global deployment**: Deploy gần user nhất
- **No cold starts**: Máy luôn sẵn sàng
- **Docker support**: Deploy bất kỳ app nào

## So sánh với Render

| Tính năng | Render Free | Fly.io Free |
|-----------|-------------|-------------|
| TPM Limit | 12,000 | Không giới hạn |
| Cold Start | 30-60s | Không có |
| Region | US | Global (Singapore) |
| Bandwidth | 100GB | 160GB |
| Auto-scaling | Không | Có |

## Troubleshooting

### Lỗi "App not found"
```bash
fly apps list
fly status
```

### Lỗi "Build failed"
```bash
fly deploy --local-only
```

### Xem logs chi tiết
```bash
fly logs --region sin
fly ssh console
```

### Restart app
```bash
fly restart
```

## Chi phí

- **Free tier**: Đủ cho demo 1-2 người
- **Paid**: $5-10/tháng cho production
- **Scaling**: Tự động theo traffic

## Liên hệ

Nếu gặp vấn đề, kiểm tra:
1. Fly.io dashboard: https://fly.io/dashboard
2. Docs: https://fly.io/docs/
3. Community: https://community.fly.io/
