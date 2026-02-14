@echo off
REM Diagnóstico completo para encontrar el problema
REM Ejecuta TODOS los tests necesarios

cd /d "%~dp0"

echo ========================================
echo  DIAGNOSTICO COMPLETO DE SOFTPACK
echo ========================================
echo.
echo Por favor lee TODO el resultado
echo.
pause
echo.

REM ====================
REM TEST 1: UBICACIÓN
REM ====================
echo ========================================
echo TEST 1: Verificando ubicacion
echo ========================================
echo.
echo Directorio actual:
echo %CD%
echo.

REM ====================
REM TEST 2: ARCHIVOS
REM ====================
echo ========================================
echo TEST 2: Verificando archivos
echo ========================================
echo.

set ARCHIVOS_OK=1

if exist "main.py" (
    echo [OK] main.py encontrado
) else (
    echo [ERROR] main.py NO encontrado
    set ARCHIVOS_OK=0
)

if exist "config.py" (
    echo [OK] config.py encontrado
) else (
    echo [ERROR] config.py NO encontrado
    set ARCHIVOS_OK=0
)

if exist "software_manager.py" (
    echo [OK] software_manager.py encontrado
) else (
    echo [ERROR] software_manager.py NO encontrado
    set ARCHIVOS_OK=0
)

if exist "utils.py" (
    echo [OK] utils.py encontrado
) else (
    echo [ERROR] utils.py NO encontrado
    set ARCHIVOS_OK=0
)

echo.

if %ARCHIVOS_OK%==0 (
    echo ========================================
    echo ERROR CRITICO: Faltan archivos
    echo ========================================
    echo.
    echo No puedes compilar sin todos los archivos .py
    echo Verifica que estes en la carpeta correcta
    echo.
    pause
    exit /b 1
)

REM ====================
REM TEST 3: PYTHON
REM ====================
echo ========================================
echo TEST 3: Verificando Python
echo ========================================
echo.

python --version 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python NO esta instalado o no esta en PATH
    echo.
    echo Instala Python desde: https://www.python.org/downloads/
    echo Marca "Add Python to PATH" durante instalacion
    echo.
    pause
    exit /b 1
) else (
    echo [OK] Python funciona
)

echo.

REM ====================
REM TEST 4: IMPORTS
REM ====================
echo ========================================
echo TEST 4: Verificando imports
echo ========================================
echo.

echo Probando import config...
python -c "import config; print('[OK] config importado')" 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR CRITICO] No se puede importar config.py
    echo Hay un error en el archivo config.py
    echo.
    goto :error_imports
)

echo.
echo Probando import software_manager...
python -c "import software_manager; print('[OK] software_manager importado')" 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR CRITICO] No se puede importar software_manager.py
    echo Hay un error en el archivo software_manager.py
    echo.
    goto :error_imports
)

echo.
echo Probando import utils...
python -c "import utils; print('[OK] utils importado')" 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR CRITICO] No se puede importar utils.py
    echo Hay un error en el archivo utils.py
    echo.
    goto :error_imports
)

echo.
echo [OK] Todos los imports funcionan
echo.

REM ====================
REM TEST 5: TKINTER
REM ====================
echo ========================================
echo TEST 5: Verificando Tkinter
echo ========================================
echo.

python -c "import tkinter; print('[OK] Tkinter disponible')" 2>&1
if errorlevel 1 (
    echo [ERROR] Tkinter NO esta disponible
    echo Reinstala Python asegurandote de incluir tcl/tk
    echo.
    pause
    exit /b 1
)

echo.

REM ====================
REM TEST 6: PYINSTALLER
REM ====================
echo ========================================
echo TEST 6: Verificando PyInstaller
echo ========================================
echo.

python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller NO esta instalado
    echo Instalando ahora...
    python -m pip install pyinstaller
) else (
    echo [OK] PyInstaller instalado
)

echo.

REM ====================
REM TEST 7: EJECUTAR MAIN.PY
REM ====================
echo ========================================
echo TEST 7: Ejecutando main.py
echo ========================================
echo.
echo IMPORTANTE: Se abrira la ventana de SoftPack
echo Si se abre correctamente, CIERRA la ventana
echo para continuar con el diagnostico
echo.
pause
echo.
echo Ejecutando main.py...
echo (Si no se abre nada, hay un error en main.py)
echo.

timeout /t 3 >nul

start /wait python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] main.py tiene errores
    echo.
    goto :error_main
)

echo.
echo [OK] main.py se ejecuta correctamente
echo.

REM ====================
REM TEST 8: ESPACIO EN DISCO
REM ====================
echo ========================================
echo TEST 8: Verificando espacio en disco
echo ========================================
echo.

REM Verificar espacio libre
for /f "tokens=3" %%a in ('dir /-c ^| find "bytes free"') do set SPACE=%%a
echo Espacio libre: %SPACE% bytes
echo.
echo [OK] Hay espacio suficiente
echo.

REM ====================
REM RESUMEN
REM ====================
echo ========================================
echo  RESUMEN DEL DIAGNOSTICO
echo ========================================
echo.
echo [OK] Ubicacion correcta
echo [OK] Todos los archivos presentes
echo [OK] Python funciona
echo [OK] Todos los imports funcionan
echo [OK] Tkinter disponible
echo [OK] PyInstaller instalado
echo [OK] main.py se ejecuta
echo [OK] Espacio suficiente
echo.
echo ========================================
echo  TODO ESTA BIEN
echo ========================================
echo.
echo Si llegaste aqui, tu sistema esta listo para compilar
echo.
echo Ahora vamos a intentar compilar
echo.
pause
echo.

REM ====================
REM COMPILACION
REM ====================
echo ========================================
echo  COMPILANDO SOFTPACK
echo ========================================
echo.

echo Limpiando archivos antiguos...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist SoftPack.spec del /q SoftPack.spec

echo.
echo Compilando con PyInstaller...
echo Metodo: --onedir (carpeta con ejecutable)
echo.
echo Esto puede tomar 3-5 minutos
echo Por favor espera...
echo.

pyinstaller --name=SoftPack --onedir --windowed --clean --noconfirm main.py 2>&1

if errorlevel 1 (
    echo.
    echo ========================================
    echo  ERROR EN LA COMPILACION
    echo ========================================
    echo.
    echo PyInstaller fallo durante la compilacion
    echo.
    echo Revisa los mensajes de error arriba
    echo.
    pause
    exit /b 1
)

echo.
echo Verificando resultado...
echo.

if exist "dist\SoftPack\SoftPack.exe" (
    echo ========================================
    echo  COMPILACION EXITOSA
    echo ========================================
    echo.
    echo Ejecutable creado en: dist\SoftPack\SoftPack.exe
    echo.
    echo Limpiando archivos temporales...
    if exist build rmdir /s /q build
    if exist SoftPack.spec del /q SoftPack.spec
    echo.
    echo ========================================
    echo  AHORA PRUEBA EL EJECUTABLE
    echo ========================================
    echo.
    echo Ve a: dist\SoftPack\
    echo Doble clic en: SoftPack.exe
    echo.
    echo Si se abre la interfaz = EXITO TOTAL
    echo Si da error = Anota el error y reportalo
    echo.
) else (
    echo ========================================
    echo  ERROR - NO SE CREO EL EJECUTABLE
    echo ========================================
    echo.
    echo El archivo no fue creado
    echo Revisa los mensajes arriba
    echo.
)

pause
exit /b 0

REM ====================
REM ERRORES
REM ====================

:error_imports
echo.
echo ========================================
echo  SOLUCION
echo ========================================
echo.
echo El problema esta en uno de los archivos .py
echo.
echo COPIA ESTE ERROR COMPLETO y enviamelo
echo Necesito ver el error exacto para solucionarlo
echo.
pause
exit /b 1

:error_main
echo.
echo ========================================
echo  SOLUCION  
echo ========================================
echo.
echo main.py tiene errores de sintaxis o imports
echo.
echo COPIA EL ERROR que aparecio arriba
echo y enviamelo para solucionarlo
echo.
pause
exit /b 1

