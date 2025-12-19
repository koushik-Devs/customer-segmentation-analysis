@echo off
echo ========================================
echo Customer Segmentation Streamlit App
echo ========================================
echo.

REM Check if models exist
if not exist "models\" (
    echo [WARNING] Models directory not found!
    echo.
    echo Training models first...
    python run_all_systems.py
    if errorlevel 1 (
        echo.
        echo [ERROR] Model training failed!
        pause
        exit /b 1
    )
)

REM Verify setup
echo Verifying setup...
python test_streamlit_setup.py
if errorlevel 1 (
    echo.
    echo [ERROR] Setup verification failed!
    echo Please fix the issues above and try again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Launching Streamlit App...
echo ========================================
echo.
echo The app will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run streamlit_app.py

pause
