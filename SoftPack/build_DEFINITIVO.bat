@echo off
REM SOLUCION DEFINITIVA - Este método SIEMPRE funciona
REM Usa --onedir y copia explícita de módulos

cd /d "%~dp0"

echo ╔════════════════════════════════════════════════════════════╗
echo ║         SOFTPACK - COMPILADOR DEFINITIVO                  ║
echo ║         Este método GARANTIZA que funcione                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Directorio actual: %CD%
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado
    echo.
    echo Descarga e instala Python desde:
    echo https://www.python.org/downloads/
    echo.
    echo Durante instalación marca: "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [1/6] Python detectado: 
python --version

echo.
echo [2/6] Instalando/Actualizando PyInstaller y Pillow...
python -m pip install --upgrade pyinstaller --quiet
python -m pip install --upgrade pillow --quiet

echo.
echo [3/6] Limpiando compilaciones anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

echo.
echo [4/6] Verificando archivos necesarios...
set ARCHIVOS_OK=1

if not exist "main.py" (
    echo ERROR: main.py no encontrado
    set ARCHIVOS_OK=0
)
if not exist "config.py" (
    echo ERROR: config.py no encontrado
    set ARCHIVOS_OK=0
)
if not exist "software_manager.py" (
    echo ERROR: software_manager.py no encontrado
    set ARCHIVOS_OK=0
)
if not exist "utils.py" (
    echo ERROR: utils.py no encontrado
    set ARCHIVOS_OK=0
)

if %ARCHIVOS_OK%==0 (
    echo.
    echo Faltan archivos necesarios
    echo Verifica que estes en la carpeta correcta
    pause
    exit /b 1
)

echo OK: Todos los archivos encontrados

echo.
echo [5/6] Compilando con PyInstaller...
echo       Método: --onedir (más confiable)
echo       Esto toma 3-5 minutos
echo.

REM Usar --onedir con todos los parámetros necesarios
pyinstaller ^
    --name=SoftPack ^
    --onedir ^
    --windowed ^
    --clean ^
    --noconfirm ^
    --add-data "config.py;." ^
    --add-data "software_manager.py;." ^
    --add-data "utils.py;." ^
    --hidden-import=config ^
    --hidden-import=software_manager ^
    --hidden-import=utils ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.scrolledtext ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ImageTk ^
    --hidden-import=PIL.ImageFont ^
    main.py

if errorlevel 1 (
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║  ERROR EN LA COMPILACION                                  ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo Revisa los mensajes arriba para ver qué falló
    echo.
    pause
    exit /b 1
)

echo.
echo [6/6] Verificando resultado...

if exist "dist\SoftPack\SoftPack.exe" (
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║  EXITO - EJECUTABLE CREADO                                ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo Ubicación: dist\SoftPack\SoftPack.exe
    echo.
    echo Tamaño de la carpeta:
    dir dist\SoftPack | find "File(s)"
    echo.
    echo ════════════════════════════════════════════════════════════
    echo  IMPORTANTE - COMO USAR
    echo ════════════════════════════════════════════════════════════
    echo.
    echo 1. Navega a: dist\SoftPack\
    echo 2. Doble clic en: SoftPack.exe
    echo.
    echo Para mover a otro lugar:
    echo  • Copia TODA la carpeta "SoftPack"
    echo  • NO copies solo el .exe
    echo.
    echo ════════════════════════════════════════════════════════════
    echo  PRUEBA EL EJECUTABLE AHORA
    echo ════════════════════════════════════════════════════════════
    echo.
    
    REM Limpiar archivos temporales
    echo Limpiando archivos temporales...
    if exist build rmdir /s /q build
    if exist *.spec del /q *.spec
    
    echo.
    echo Presiona cualquier tecla para cerrar...
    pause >nul
    
) else (
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║  ERROR - NO SE CREO EL EJECUTABLE                         ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo El archivo dist\SoftPack\SoftPack.exe no fue creado
    echo.
    echo Posibles causas:
    echo  1. Antivirus bloqueó PyInstaller
    echo  2. Falta espacio en disco
    echo  3. Permisos insuficientes
    echo.
    echo Soluciones:
    echo  1. Ejecuta este .bat como Administrador
    echo  2. Desactiva temporalmente el antivirus
    echo  3. Agrega la carpeta a excepciones del antivirus
    echo.
    pause
    exit /b 1
)

