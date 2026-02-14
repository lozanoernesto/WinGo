@echo off
REM Lanzador de ejemplo para ejecutar SoftPack desde la raíz de la USB
REM Copia este archivo a la raíz de la USB junto a SoftPack.exe o la carpeta SoftPack\

cd /d %~dp0

if exist "SoftPack.exe" (
    start "" "%~dp0SoftPack.exe"
    goto :EOF
)

if exist "SoftPack\SoftPack.exe" (
    start "" "%~dp0SoftPack\SoftPack.exe"
    goto :EOF
)

echo No se encontro SoftPack.exe ni la carpeta SoftPack\
pause
