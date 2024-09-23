echo off
cls
cd ..
:: enter to venv
call .venv\Scripts\activate.bat

:: start program
echo project starting...
.venv\Scripts\python src/app.py
