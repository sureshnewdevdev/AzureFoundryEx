@echo off
setlocal
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python examples\02_in_memory_client.py

