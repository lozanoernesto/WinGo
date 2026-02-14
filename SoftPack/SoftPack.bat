@echo off
REM SoftPack Launcher
REM Script para iniciar SoftPack fácilmente en Windows

echo ========================================
echo  SoftPack - Gestor de Software
echo ========================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo.
    echo Por favor instala Python 3.8 o superior desde:
    echo https://www.python.org/downloads/
    echo.
    echo Asegúrate de marcar "Add Python to PATH" durante la instalación
    pause
    exit /b 1
)

echo Python detectado correctamente
echo.
echo Iniciando SoftPack...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Ejecutar la aplicación
python main.py

REM Si hay error, mostrar mensaje
if errorlevel 1 (
    echo.
    echo ERROR: No se pudo iniciar SoftPack
    echo Verifica que todos los archivos están presentes
    pause
)

