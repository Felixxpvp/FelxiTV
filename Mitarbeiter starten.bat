@echo off
cd /d "%~dp0"
echo Mitarbeiter wird gestartet...
echo Fenster offen lassen solange du den Bot nutzen moechtest.
echo Schliessen zum Stoppen.
echo.
.venv\Scripts\python.exe scripts\stimme.py
pause
