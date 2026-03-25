@echo off
REM SPM Estimation System - Quick Setup Script for Windows

color 0A
title SPM Estimation System - Setup

echo.
echo ========================================
echo    SPM Effort Estimation System
echo    Quick Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org
    pause
    exit /b 1
)

REM Navigate to backend
cd /d "%~dp0backend"

if errorlevel 1 (
    echo ERROR: Could not navigate to backend folder
    pause
    exit /b 1
)

echo.
echo Step 1: Installing dependencies...
echo ========================================
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Starting Flask server...
echo ========================================
echo.
echo Server starting on http://127.0.0.1:5000
echo.
echo Open your browser and go to:
echo   http://127.0.0.1:5000/login
echo.
echo Default credentials:
echo   Username: admin
echo   Password: password
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

python app.py
