@echo off
REM cd ไป folder ที่ .bat อยู่
cd /d "%~dp0"

REM ตั้ง PYTHONPATH เป็น path ของ .bat (ให้ Python หา src เจอ)
set PYTHONPATH=%CD%\src

REM activate venv (อยู่ใน folder เดียวกับ .bat)
call venv\Scripts\activate

echo [1/4] Running Ruff Formatter...
REM ใช้ ruff แทน black และ isort (จัดการทั้ง format และจัดระเบียบ import)
ruff format src/

echo [2/4] Running Ruff Linter (Fixing auto-fixable issues)...
REM ใช้ ruff แทน flake8 (และสั่ง --fix เพื่อแก้ปัญหาเบื้องต้นให้เลย)
ruff check src/ --fix

echo [3/4] Running Mypy Type Checker...
mypy src/

echo [4/4] Starting FastAPI Server...
REM run python
python src\app\main.py

pause
