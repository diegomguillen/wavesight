@echo off
title WaveSight Server (R&S RTC1002)
cd /d "%~dp0"
echo ===================================================
echo   Iniciando WaveSight con Proxy para RTC1002
echo   Accede desde tu navegador a: http://localhost:8080
echo ===================================================
python server.py 8080
pause
