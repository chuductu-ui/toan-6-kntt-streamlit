@echo off
chcp 65001 >nul
title Vuon Toan Lop 6 - Hoc Cung Con
echo ======================================================================
echo           DANG KHOI DONG NEN TANG VUON TOAN LOP 6 (KNTT)
echo ======================================================================
echo.
cd /d "%~dp0"

echo 1. Kiem tra va cap nhat thu vien can thiet...
python -m pip install streamlit pillow pytest pandas -q

echo 2. May chu dang chay tai cac dia chi sau:
echo.
echo    💻 Tren may tinh nay:              http://localhost:8501
echo    📱 Tren Smartphone / iPad / iPhone: http://192.168.1.3:8501
echo.
echo (Luu y: Dien thoai phai bat Wi-Fi chung mang voi may tinh)
echo (Neu dien thoai khong vao duoc, hay chay file MO_KET_NOI_DIEN_THOAI.bat)
echo ======================================================================
echo.

python -m streamlit run app.py --server.port 8501

pause
