@echo off
REM Compilador usando archivo .spec personalizado
REM Soluciona el problema de ModuleNotFoundError

REM Cambiar al directorio donde está este script
cd /d "%~dp0"

echo ========================================
echo  SOFTPACK - Compilador con .spec
echo ========================================
echo.
echo Este metodo usa un archivo .spec personalizado
echo que asegura incluir todos los modulos necesarios
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado
    pause
    exit /b 1
)

echo Instalando/Actualizando PyInstaller...
python -m pip install --upgrade pyinstaller --quiet

echo.
echo Limpiando compilaciones anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo ========================================
echo  COMPILANDO CON ARCHIVO .SPEC
echo ========================================
echo.
echo Esto asegura que todos los modulos se incluyan
echo (Puede tomar 2-3 minutos)
echo.

REM Compilar usando el archivo .spec
pyinstaller SoftPack.spec --clean

if errorlevel 1 (
    echo.
    echo ========================================
    echo  ERROR EN LA COMPILACION
    echo ========================================
    echo.
    pause
    exit /b 1
)

echo.
if exist "dist\SoftPack.exe" (
    echo ========================================
    echo  EXITO - EJECUTABLE CREADO
    echo ========================================
    echo.
    echo Archivo: dist\SoftPack.exe
    echo.
    dir dist\SoftPack.exe | find "SoftPack.exe"
    echo.
    echo Limpiando archivos temporales...
    if exist build rmdir /s /q build
    echo.
    echo ========================================
    echo  PRUEBA EL EJECUTABLE
    echo ========================================
    echo.
    echo 1. Ve a la carpeta "dist"
    echo 2. Haz doble clic en SoftPack.exe
    echo 3. Deberia abrir sin errores
    echo.
    echo Si ves la interfaz grafica = EXITO
    echo Si ves errores = Reporta el error
    echo.
) else (
    echo ========================================
    echo  ERROR - NO SE CREO EL .EXE
    echo ========================================
    echo.
)

pause

