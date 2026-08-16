@echo off
echo ===================================================
echo        KHOI DONG HE THONG FUNDREADY AI LOCAL
echo ===================================================
echo.

:: 1. Khoi dong Backend (FastAPI) o cong 8001
echo [1/3] Dang khoi dong Backend API (Port 8001)...
start "FundReady Backend" cmd /c "python -m uvicorn api.index:app --host 127.0.0.1 --port 8001 --reload"

:: Cho 2 giay de Backend khoi dong hoan tat
timeout /t 2 /nobreak > NUL

:: 2. Khoi dong Frontend (HTML/JS) o cong 3000
echo [2/3] Dang khoi dong Frontend UI (Port 3000)...
start "FundReady Frontend" cmd /c "python -m http.server 3000"

:: 3. Mo trinh duyet
echo [3/3] Dang mo trinh duyet...
start http://localhost:3000/danh-gia.html

echo.
echo ===================================================
echo  Hoan tat! He thong dang chay tren:
echo  - Frontend: http://localhost:3000
echo  - Backend:  http://localhost:8001
echo ===================================================
echo.
pause
