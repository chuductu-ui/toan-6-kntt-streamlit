@echo off
chcp 65001 >nul
title Mo ket noi Smartphone / iPad / iPhone vao Vuon Toan 6

:: Tu dong yeu cau quyen Administrator (UAC Prompt)
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Đang yêu cầu quyền Administrator để mở cổng tường lửa...
    powershell -Command "Start-Process cmd -ArgumentList '/c `\"%~f0`\"' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"
echo ======================================================================
echo    CẤU HÌNH KẾT NỐI TỪ ĐIỆN THOẠI / IPAD / IPHONE VÀO VƯỜN TOÁN 6
echo ======================================================================
echo.
echo Đang thêm quy tắc tường lửa (Windows Firewall Rule cho cổng 8501)...
netsh advfirewall firewall delete rule name="Streamlit Toan 6 (Port 8501)" >nul 2>&1
netsh advfirewall firewall add rule name="Streamlit Toan 6 (Port 8501)" dir=in action=allow protocol=TCP localport=8501 >nul

echo.
echo [V] ĐÃ MỞ CỔNG TƯỜNG LỬA THÀNH CÔNG!
echo.
echo ======================================================================
echo HƯỚNG DẪN TRUY CẬP TRÊN ĐIỆN THOẠI / IPAD:
echo.
echo 1. Đảm bảo Điện thoại / iPad kết nối CÙNG MẠNG WI-FI với máy tính này.
echo.
echo 2. Mở trình duyệt Safari hoặc Chrome trên điện thoại, gõ địa chỉ:
echo.
echo       http://192.168.1.3:8501
echo.
echo (Mẹo: Trên iPhone/iPad, khi bấm 'Tải file ảnh lên', máy sẽ cho phép
echo  bạn chọn trực tiếp 'Chụp ảnh' từ camera sau cực kỳ rõ nét!)
echo ======================================================================
echo.
pause
