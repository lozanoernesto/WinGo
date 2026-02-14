@echo off
REM Wrapper para crear paquete USB de SoftPack
REM Uso simple: doble clic en este .bat, sigue las instrucciones

cd /d "%~dp0"

echo ========================================
echo  SOFTPACK - Empaquetar para USB
echo ========================================

echo Seleccione modo de compilacion:
echo  1) Onefile (un solo archivo .exe) - recomendado
echo  2) Onedir (carpeta con dependencias)
set /p mode_choice=Escriba 1 o 2 [1]: 
if "%mode_choice%"=="2" (
    set MODE=onedir
) else (
    set MODE=onefile
)

echo.
echo ¿Quieres copiar automáticamente al USB detectado? (Recomendado) 
set /p copy_choice=Si/No [S]: 
if /I "%copy_choice%"=="N" (
    set COPY=
) else (
    set COPY=--copy
)

if defined COPY (
    echo Buscando unidades removibles...
    for /f "usebackq tokens=*" %%D in (`powershell -NoProfile -Command "Get-Volume | Where-Object DriveType -eq 'Removable' | Select -ExpandProperty DriveLetter -First 1"`) do set REM=%%D
    if not defined REM (
        echo No se detecto ninguna unidad removible automaticamente.
        echo Inserte la USB y presione Enter, o escriba la letra (ej: F:) y presione Enter.
        set /p user_rem=Tiene la letra (dejar vacio para intentar detectar de nuevo): 
        if not "%user_rem%"=="" (
            set REM=%user_rem%
        ) else (
            for /f "usebackq tokens=*" %%D in (`powershell -NoProfile -Command "Get-Volume | Where-Object DriveType -eq 'Removable' | Select -ExpandProperty DriveLetter -First 1"`) do set REM=%%D
        )
    )
    if defined REM (
        set TARGET=%REM%:
        echo Usando unidad: %TARGET%
    ) else (
        echo No se encontro unidad removible. Saliendo.
        pause
        exit /b 1
    )
)

REM Ejecutar script Python
set ARGS=--mode %MODE%
if defined COPY set ARGS=%ARGS% %COPY%
if defined TARGET set ARGS=%ARGS% --target %TARGET%

echo Ejecutando: python create_usb_package.py %ARGS%
python create_usb_package.py %ARGS%

if errorlevel 1 (
    echo ERROR: Fallo el empaquetado
    pause
    exit /b 1
)

echo.
echo PROCESO COMPLETADO
pause
