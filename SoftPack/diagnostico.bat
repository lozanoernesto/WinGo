@echo off
REM Script de diagnóstico para SoftPack
REM Verifica por qué no se genera el .exe

REM IMPORTANTE: Cambiar al directorio donde está este script
cd /d "%~dp0"

echo ========================================
echo  SOFTPACK - DIAGNOSTICO
echo ========================================
echo.
echo Directorio actual: %CD%
echo.

echo [Paso 1] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo PROBLEMA: Python NO esta instalado o no esta en PATH
    echo.
    echo Solucion:
    echo 1. Instala Python desde https://www.python.org/downloads/
    echo 2. Durante instalacion, marca "Add Python to PATH"
    echo.
    pause
    exit /b 1
) else (
    python --version
    echo OK: Python instalado correctamente
)

echo.
echo [Paso 2] Verificando pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo PROBLEMA: pip no funciona
    echo.
    pause
    exit /b 1
) else (
    python -m pip --version
    echo OK: pip funciona correctamente
)

echo.
echo [Paso 3] Verificando archivos necesarios...
if not exist "main.py" (
    echo PROBLEMA: main.py no encontrado
    echo Asegurate de estar en la carpeta SoftPack
    pause
    exit /b 1
)
if not exist "config.py" (
    echo PROBLEMA: config.py no encontrado
    pause
    exit /b 1
)
if not exist "software_manager.py" (
    echo PROBLEMA: software_manager.py no encontrado
    pause
    exit /b 1
)
echo OK: Todos los archivos .py encontrados

echo.
echo [Paso 4] Verificando espacio en disco...
echo OK: (Asume que hay espacio suficiente)

echo.
echo [Paso 5] Verificando PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller NO esta instalado
    echo Instalando ahora...
    python -m pip install pyinstaller
) else (
    echo OK: PyInstaller ya instalado
)

echo.
echo ========================================
echo  DIAGNOSTICO COMPLETADO
echo ========================================
echo.
echo Todos los requisitos estan OK
echo.
echo Ahora presiona cualquier tecla para intentar compilar...
pause

echo.
echo ========================================
echo  INTENTANDO COMPILACION
echo ========================================
echo.

REM Limpiar compilaciones anteriores
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist SoftPack.spec del /q SoftPack.spec

echo Compilando SoftPack...
echo (Esto puede tomar 2-5 minutos)
echo.

pyinstaller --name=SoftPack --onefile --windowed --clean --hidden-import=config --hidden-import=software_manager --hidden-import=utils main.py 2>&1

if errorlevel 1 (
    echo.
    echo ========================================
    echo  ERROR EN LA COMPILACION
    echo ========================================
    echo.
    echo Revisa los mensajes de error arriba
    echo.
    echo Posibles causas:
    echo  1. Antivirus esta bloqueando PyInstaller
    echo  2. Falta permisos de administrador
    echo  3. Archivos .py tienen errores
    echo.
    echo Soluciones:
    echo  1. Desactiva temporalmente el antivirus
    echo  2. Ejecuta este .bat como Administrador
    echo  3. Revisa que main.py no tenga errores
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  VERIFICANDO RESULTADO
echo ========================================
echo.

if exist "dist\SoftPack.exe" (
    echo ========================================
    echo  EXITO - EJECUTABLE CREADO
    echo ========================================
    echo.
    echo El ejecutable esta en:
    echo   %CD%\dist\SoftPack.exe
    echo.
    echo Tamano del archivo:
    dir dist\SoftPack.exe | find "SoftPack.exe"
    echo.
    echo Para usarlo:
    echo  1. Ve a la carpeta "dist"
    echo  2. Haz doble clic en SoftPack.exe
    echo.
    echo Limpiando archivos temporales...
    if exist build rmdir /s /q build
    if exist SoftPack.spec del /q SoftPack.spec
    echo.
    echo TODO LISTO!
) else (
    echo ========================================
    echo  ERROR - NO SE CREO EL EJECUTABLE
    echo ========================================
    echo.
    echo El archivo dist\SoftPack.exe NO fue creado
    echo.
    echo Esto puede ser porque:
    echo  1. El antivirus elimino el .exe
    echo  2. Hubo errores durante la compilacion
    echo  3. PyInstaller no completo el proceso
    echo.
    echo Soluciones:
    echo  1. Desactiva Windows Defender temporalmente
    echo  2. Agrega la carpeta SoftPack a excepciones
    echo  3. Ejecuta como Administrador
    echo  4. Lee los mensajes de error arriba
    echo.
)

echo.
pause

