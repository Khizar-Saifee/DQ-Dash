@echo off
echo Starting DQDash...

cd /d %~dp0

echo Activating virtual environment...
call venv\Scripts\activate

echo Running Streamlit App...
streamlit run app.py

pause