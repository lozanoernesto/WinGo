#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para compilar SoftPack a ejecutable .exe
Usa PyInstaller para crear un ejecutable independiente
"""

import os
import sys
import subprocess
from pathlib import Path

print("=" * 70)
print("  SOFTPACK - Compilador de Ejecutable")
print("=" * 70)
print()

# Verificar que estamos en Windows
if sys.platform != 'win32':
    print("⚠️  ADVERTENCIA: Este script debe ejecutarse en Windows")
    print("   PyInstaller creará un .exe que solo funciona en Windows")
    print()
    response = input("¿Deseas continuar de todas formas? (s/n): ")
    if response.lower() != 's':
        sys.exit(0)

# Verificar PyInstaller
print("🔍 Verificando PyInstaller...")
try:
    import PyInstaller
    print("✅ PyInstaller está instalado")
except ImportError:
    print("❌ PyInstaller no está instalado")
    print()
    print("Instalando PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("✅ PyInstaller instalado correctamente")

print()
print("=" * 70)
print("  Configuración de Compilación")
print("=" * 70)
print()

# Configuración
APP_NAME = "SoftPack"
MAIN_SCRIPT = "main.py"
ICON_FILE = "icon.ico" if Path("icon.ico").exists() else None

# Opciones de PyInstaller
options = [
    MAIN_SCRIPT,
    f"--name={APP_NAME}",
    "--onefile",                    # Un solo archivo ejecutable
    "--windowed",                   # Sin ventana de consola
    "--clean",                      # Limpiar caché antes de compilar
    "--paths=.",
    f"--add-data=config.py{os.pathsep}.",
    f"--add-data=software_manager.py{os.pathsep}.",
    f"--add-data=utils.py{os.pathsep}.",
    "--hidden-import=config",
    "--hidden-import=software_manager",
    "--hidden-import=utils",
    "--hidden-import=PIL",
    "--hidden-import=PIL.Image",
    "--hidden-import=PIL.ImageTk",
    "--hidden-import=PIL.ImageFont",
    "--hidden-import=glob",
    "--hidden-import=ssl",
    "--hidden-import=webbrowser",
    "--hidden-import=contextlib",
    "--hidden-import=urllib",
    "--hidden-import=urllib.request",
    "--hidden-import=urllib.error",
    "--hidden-import=shutil",
    "--hidden-import=pathlib",
    "--hidden-import=subprocess",
    "--hidden-import=time",
    "--hidden-import=threading",
    "--collect-submodules=PIL",
]

# Incluir recursos visuales si están disponibles (modo portable).
if Path("icons").exists():
    options.append(f"--add-data=icons{os.pathsep}icons")

# Agregar ícono si existe
if ICON_FILE:
    options.append(f"--icon={ICON_FILE}")
    print(f"📦 Ícono: {ICON_FILE}")
else:
    print("ℹ️  Sin ícono personalizado")

print(f"📦 Nombre: {APP_NAME}.exe")
print(f"📦 Script principal: {MAIN_SCRIPT}")
print(f"📦 Modo: Un solo archivo (onefile)")
print(f"📦 Tipo: Aplicación con interfaz gráfica (windowed)")
print()

# Confirmar
print("=" * 70)
response = input("¿Iniciar compilación? (s/n): ")
if response.lower() != 's':
    print("❌ Compilación cancelada")
    sys.exit(0)

print()
print("=" * 70)
print("  Compilando...")
print("=" * 70)
print()
print("⏳ Este proceso puede tomar varios minutos...")
print("   PyInstaller está analizando dependencias y creando el ejecutable")
print()

# Ejecutar PyInstaller
try:
    result = subprocess.run(
        ["pyinstaller"] + options,
        check=True,
        capture_output=True,
        text=True
    )
    
    print("=" * 70)
    print("  ✅ COMPILACIÓN EXITOSA")
    print("=" * 70)
    print()
    print(f"📦 El ejecutable se creó en: dist\\{APP_NAME}.exe")
    print()
    print("📂 Estructura de archivos creados:")
    print(f"   • dist\\{APP_NAME}.exe    ← EJECUTABLE PRINCIPAL")
    print(f"   • build\\                  ← Archivos temporales (puedes borrar)")
    print(f"   • {APP_NAME}.spec          ← Configuración de compilación")
    print()
    print("=" * 70)
    print("  Cómo usar el ejecutable:")
    print("=" * 70)
    print()
    print(f"1. Navega a la carpeta 'dist'")
    print(f"2. Copia {APP_NAME}.exe donde quieras")
    print(f"3. Haz doble clic en {APP_NAME}.exe para ejecutar")
    print(f"4. ¡No necesitas Python instalado para ejecutarlo!")
    print()
    print("ℹ️  El ejecutable es portable:")
    print("   • Puedes copiarlo a USB")
    print("   • Funciona en cualquier PC con Windows")
    print("   • No requiere instalación")
    print()
    
except subprocess.CalledProcessError as e:
    print("=" * 70)
    print("  ❌ ERROR EN LA COMPILACIÓN")
    print("=" * 70)
    print()
    print("Error:", str(e))
    if e.stderr:
        print()
        print("Detalles del error:")
        print(e.stderr)
    print()
    print("💡 Posibles soluciones:")
    print("   1. Verifica que todos los archivos .py estén presentes")
    print("   2. Ejecuta como administrador")
    print("   3. Desactiva temporalmente el antivirus")
    print("   4. Intenta con: pyinstaller --onedir main.py")
    print()
    sys.exit(1)

print("=" * 70)
print()

# Preguntar si desea limpiar archivos temporales
response = input("¿Deseas limpiar archivos temporales (build/)? (s/n): ")
if response.lower() == 's':
    import shutil
    if Path("build").exists():
        shutil.rmtree("build")
        print("✅ Archivos temporales eliminados")
    if Path(f"{APP_NAME}.spec").exists():
        Path(f"{APP_NAME}.spec").unlink()
        print("✅ Archivo .spec eliminado")

print()
print("✨ ¡Proceso completado!")
print()
print(f"👉 Tu ejecutable está en: dist\\{APP_NAME}.exe")
print()

