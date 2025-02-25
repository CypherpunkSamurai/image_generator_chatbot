@ECHO OFF

REM Run FastAPI App
REM Author: @CypherpunkSamurai
REM Activate Virtual Environment if .venc exists
IF EXIST .venv\Scripts\activate.bat (
    CALL .venv\Scripts\activate.bat
)

python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000