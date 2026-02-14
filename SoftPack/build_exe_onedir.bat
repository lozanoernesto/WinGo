@echo off
REM Compilador usando --onedir (más confiable para módulos)
REM Crea una carpeta con el .exe y sus dependencias

REM Cambiar al directorio donde está este script
cd /d "%~dp0"

echo ========================================
echo  SOFTPACK - Compilador ONEDIR
echo ========================================
echo.
echo Este metodo crea una CARPETA con el ejecutable
echo Es mas confiable y soluciona el error de modulos
echo.
echo Directorio actual: %CD%
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado
    pause
    exit /b 1
)

echo [1/5] Instalando PyInstaller...
python -m pip install --quiet pyinstaller

echo [2/5] Verificando archivos necesarios...
if not exist "main.py" (
    echo ERROR: main.py no encontrado
    pause
    exit /b 1
)
if not exist "config.py" (
    echo ERROR: config.py no encontrado
    pause
    exit /b 1
)
if not exist "software_manager.py" (
    echo ERROR: software_manager.py no encontrado
    pause
    exit /b 1
)
echo OK: Todos los archivos encontrados

echo [3/5] Limpiando archivos antiguos...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist SoftPack.spec del /q SoftPack.spec

echo [4/5] Compilando con --onedir...
echo      (Esto toma 2-3 minutos)
echo.

REM IMPORTANTE: --onedir en lugar de --onefile
REM Esto crea una carpeta con el .exe y sus dependencias
REM Es MÁS CONFIABLE para módulos personalizados

pyinstaller --name=SoftPack ^
    --onedir ^
    --windowed ^
    --clean ^
    --noconfirm ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ImageTk ^
    main.py

if errorlevel 1 (
    echo.
    echo ERROR: Compilacion fallida
    pause
    exit /b 1
)

echo [5/5] Verificando resultado...
echo.

if exist "dist\SoftPack\SoftPack.exe" (
    echo ========================================
    echo  EXITO - EJECUTABLE CREADO
    echo ========================================
    echo.
    echo Ubicacion: dist\SoftPack\SoftPack.exe
    echo.
    echo IMPORTANTE:
    echo  - El ejecutable esta dentro de la carpeta dist\SoftPack\
    echo  - Necesitas TODA la carpeta SoftPack para que funcione
    echo  - NO puedes mover solo el .exe, lleva toda la carpeta
    echo.
    echo Como usar:
    echo  1. Ve a dist\SoftPack\
    echo  2. Haz doble clic en SoftPack.exe
    echo  3. O copia TODA la carpeta SoftPack a donde quieras
    echo.
    
    REM Listar contenido
    echo Contenido de la carpeta:
    dir dist\SoftPack\ | find /V "Volume"
    echo.
    
    REM Limpiar archivos temporales
    echo Limpiando archivos temporales...
    if exist build rmdir /s /q build
    if exist SoftPack.spec del /q SoftPack.spec
    
    echo.
    echo ========================================
    echo  PRUEBA EL EJECUTABLE AHORA
    echo ========================================
    echo.
    echo 1. Navega a: dist\SoftPack\
    echo 2. Doble clic en: SoftPack.exe
    echo 3. Deberia abrir SIN ERRORES
    echo.
    echo Si funciona: EXITO!
    echo Si da error: Copia el error completo
    echo.
) else (
    echo ========================================
    echo  ERROR - NO SE CREO EL EJECUTABLE
    echo ========================================
    echo.
    echo El archivo dist\SoftPack\SoftPack.exe no fue creado
    echo.
    echo Revisa los mensajes de error arriba
    echo.
)

pause

