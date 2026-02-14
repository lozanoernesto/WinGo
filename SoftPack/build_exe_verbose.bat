@echo off
REM Compilador de SoftPack con salida detallada
REM Para diagnosticar problemas

REM Cambiar al directorio donde está este script
cd /d "%~dp0"

echo ========================================
echo  SOFTPACK - COMPILADOR DETALLADO
echo ========================================
echo.
echo Directorio actual: %CD%
echo.

REM Verificar Python
python --version
if errorlevel 1 (
    echo ERROR: Python no encontrado
    echo Instala Python desde https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Instalando PyInstaller...
python -m pip install --upgrade pyinstaller

echo.
echo Limpiando archivos antiguos...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist SoftPack.spec del /q SoftPack.spec

echo.
echo ========================================
echo  COMPILANDO CON SALIDA DETALLADA
echo ========================================
echo.
echo Guardando log en: compilacion_log.txt
echo.

REM Compilar con log detallado
pyinstaller --name=SoftPack ^
    --onefile ^
    --windowed ^
    --clean ^
    --log-level=INFO ^
    --hidden-import=config ^
    --hidden-import=software_manager ^
    --hidden-import=utils ^
    main.py > compilacion_log.txt 2>&1

echo.
echo Compilacion completada. Verificando resultado...
echo.

if exist "dist\SoftPack.exe" (
    echo ========================================
    echo  EXITO
    echo ========================================
    echo.
    echo Ejecutable creado: dist\SoftPack.exe
    echo.
    dir dist\SoftPack.exe
    echo.
    echo Limpiando archivos temporales...
    if exist build rmdir /s /q build
    if exist SoftPack.spec del /q SoftPack.spec
    echo.
    echo Para ver detalles de compilacion:
    echo   notepad compilacion_log.txt
    echo.
) else (
    echo ========================================
    echo  ERROR - NO SE CREO EL .EXE
    echo ========================================
    echo.
    echo Revisa el archivo compilacion_log.txt para detalles
    echo.
    echo Abriendo el log...
    notepad compilacion_log.txt
)

echo.
pause

