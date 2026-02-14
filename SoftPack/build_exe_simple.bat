@echo off
REM Script simple para compilar SoftPack a .exe
REM Automático y sin preguntas

REM Cambiar al directorio donde está este script
cd /d "%~dp0"

echo ========================================
echo  SOFTPACK - Compilador a .exe
echo ========================================
echo.
echo Directorio actual: %CD%
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    pause
    exit /b 1
)

echo [1/4] Instalando PyInstaller...
python -m pip install --quiet pyinstaller

echo [2/4] Limpiando archivos antiguos...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist SoftPack.spec del /q SoftPack.spec

echo [3/4] Compilando SoftPack a .exe...
echo      (Este proceso puede tomar 2-3 minutos)
pyinstaller --name=SoftPack --onefile --windowed --clean --hidden-import=config --hidden-import=software_manager --hidden-import=utils --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageTk main.py

echo [4/4] Limpiando archivos temporales...
if exist build rmdir /s /q build
if exist SoftPack.spec del /q SoftPack.spec

echo.
echo ========================================
echo  COMPILACION COMPLETADA
echo ========================================
echo.
echo El ejecutable esta en: dist\SoftPack.exe
echo.
echo Ahora puedes:
echo  1. Copiar dist\SoftPack.exe a donde quieras
echo  2. Ejecutarlo sin necesidad de Python
echo  3. Compartirlo con otros usuarios
echo.
pause

