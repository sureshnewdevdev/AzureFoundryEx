@echo off
setlocal
cd /d "%~dp0"
call .venv\Scripts\activate.bat
mcp dev src\mcp_demo\server.py

