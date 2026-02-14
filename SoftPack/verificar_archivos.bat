@echo off
REM Script para verificar que los archivos están presentes
REM y que estamos en el directorio correcto

REM Cambiar al directorio donde está este script
cd /d "%~dp0"

echo ========================================
echo  VERIFICACION DE ARCHIVOS
echo ========================================
echo.
echo Directorio actual:
echo %CD%
echo.
echo ========================================
echo  Archivos necesarios:
echo ========================================
echo.

if exist "main.py" (
    echo [OK] main.py encontrado
) else (
    echo [ERROR] main.py NO encontrado
)

if exist "config.py" (
    echo [OK] config.py encontrado
) else (
    echo [ERROR] config.py NO encontrado
)

if exist "software_manager.py" (
    echo [OK] software_manager.py encontrado
) else (
    echo [ERROR] software_manager.py NO encontrado
)

if exist "utils.py" (
    echo [OK] utils.py encontrado
) else (
    echo [ERROR] utils.py NO encontrado
)

echo.
echo ========================================
echo  Todos los archivos en esta carpeta:
echo ========================================
echo.
dir /b *.py
echo.
echo ========================================
echo  Scripts .bat disponibles:
echo ========================================
echo.
dir /b *.bat
echo.

if exist "main.py" (
    echo ========================================
    echo  TODO CORRECTO
    echo ========================================
    echo.
    echo Todos los archivos necesarios están presentes
    echo Ahora puedes ejecutar:
    echo.
    echo   diagnostico.bat        - Para diagnostico completo
    echo   build_exe_simple.bat   - Para compilar
    echo.
) else (
    echo ========================================
    echo  ERROR - ARCHIVOS FALTANTES
    echo ========================================
    echo.
    echo No se encontraron los archivos .py necesarios
    echo.
    echo Posibles causas:
    echo  1. Estas en el directorio equivocado
    echo  2. Los archivos no se copiaron correctamente
    echo  3. Los archivos tienen nombres diferentes
    echo.
    echo Verifica que estes en la carpeta SoftPack
    echo que contiene todos los archivos .py
    echo.
)

pause

