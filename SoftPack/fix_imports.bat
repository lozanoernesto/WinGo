@echo off
REM Script de diagnóstico de imports
REM Verifica si Python puede importar los módulos

cd /d "%~dp0"

echo ========================================
echo  DIAGNOSTICO DE IMPORTS
echo ========================================
echo.
echo Directorio actual: %CD%
echo.

echo Probando imports de Python...
echo.

REM Prueba 1: Verificar que Python encuentra los módulos
echo [TEST 1] Importando config...
python -c "import config; print('OK: config importado')" 2>&1
if errorlevel 1 (
    echo ERROR: No se puede importar config
) else (
    echo EXITO: config se puede importar
)

echo.
echo [TEST 2] Importando software_manager...
python -c "import software_manager; print('OK: software_manager importado')" 2>&1
if errorlevel 1 (
    echo ERROR: No se puede importar software_manager
) else (
    echo EXITO: software_manager se puede importar
)

echo.
echo [TEST 3] Importando utils...
python -c "import utils; print('OK: utils importado')" 2>&1
if errorlevel 1 (
    echo ERROR: No se puede importar utils
) else (
    echo EXITO: utils se puede importar
)

echo.
echo [TEST 4] Ejecutando main.py directamente...
python main.py
if errorlevel 1 (
    echo.
    echo ERROR: main.py tiene errores
    echo Esto explica por que PyInstaller falla
) else (
    echo.
    echo EXITO: main.py se ejecuta correctamente
)

echo.
echo ========================================
echo  FIN DEL DIAGNOSTICO
echo ========================================
echo.
pause

