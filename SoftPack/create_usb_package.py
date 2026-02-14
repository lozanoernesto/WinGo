#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para compilar SoftPack y crear un paquete listo para copiar a una USB.
Uso:
  python create_usb_package.py [--mode onefile|onedir] [--target F:\\] [--copy]

Características:
 - Construye con PyInstaller (instala si es necesario)
 - Soporta --onefile (por defecto) o --onedir
 - Detecta unidades removibles si no se especifica --target
 - Copia los archivos al destino y crea un `run_softpack.bat` con rutas relativas

Nota: Ejecutar en Windows.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def ensure_pyinstaller_and_pillow():
    ok = True
    try:
        import PyInstaller  # noqa: F401
    except Exception:
        print("PyInstaller no está instalado. Intentando instalar...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        try:
            import PyInstaller  # noqa: F401
        except Exception:
            ok = False

    try:
        import PIL  # noqa: F401
    except Exception:
        print("Pillow (PIL) no está instalado. Intentando instalar...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        try:
            import PIL  # noqa: F401
        except Exception:
            ok = False

    return ok


def get_removable_drives():
    # Devuelve lista de letras de unidades con tipo removible (Windows)
    drives = []
    if sys.platform != 'win32':
        return drives
    try:
        import ctypes
        drive_bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for d in range(26):
            if drive_bitmask & (1 << d):
                drive = f"{chr(65 + d)}:\\"
                DRIVE_REMOVABLE = 2
                dt = ctypes.windll.kernel32.GetDriveTypeW(ctypes.c_wchar_p(drive))
                if dt == DRIVE_REMOVABLE:
                    drives.append(drive)
    except Exception:
        pass
    return drives


def build(mode='onefile', name='SoftPack', icon=None, additional_data=None):
    if not ensure_pyinstaller_and_pillow():
        raise RuntimeError('PyInstaller o Pillow no disponible')

    args = ["pyinstaller", f"--name={name}", "--clean", "--noconfirm"]
    if mode == 'onefile':
        args.append("--onefile")
        args.append("--windowed")
    elif mode == 'onedir':
        args.append("--onedir")
        args.append("--windowed")
    else:
        raise ValueError('Modo desconocido')

    if icon:
        args.append(f"--icon={icon}")

    # Añadir datos adicionales (formato: origen;dest)
    if additional_data:
        for item in additional_data:
            args.append(f"--add-data={item}")

    # Añadir hidden-imports para PIL (Pillow)
    hidden = ["--hidden-import=PIL", "--hidden-import=PIL.Image", "--hidden-import=PIL.ImageTk", "--hidden-import=PIL.ImageFont"]
    args.extend(hidden)

    args.append("main.py")

    print("Compilando con PyInstaller: ", " ".join(args))
    subprocess.check_call(args)
    print("Compilación completada.")


def copy_to_target(mode, name, target_path: Path):
    target_path = Path(target_path)
    if not target_path.exists():
        raise FileNotFoundError(f'Destino no encontrado: {target_path}')

    dist_dir = Path('dist')
    if mode == 'onefile':
        exe_src = dist_dir / f"{name}.exe"
        if not exe_src.exists():
            raise FileNotFoundError(f'No se encontró el ejecutable: {exe_src}')
        dest_exe = target_path / f"{name}.exe"
        shutil.copy2(exe_src, dest_exe)
        print(f'Copiado {exe_src} -> {dest_exe}')
    else:  # onedir
        src_dir = dist_dir / name
        if not src_dir.exists():
            raise FileNotFoundError(f'No se encontró la carpeta: {src_dir}')
        dest_dir = target_path / name
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        shutil.copytree(src_dir, dest_dir)
        print(f'Copiada carpeta {src_dir} -> {dest_dir}')

    # Crear lanzador en la raíz del destino
    launcher = target_path / 'run_softpack.bat'
    if mode == 'onefile':
        launcher.write_text(
            "@echo off\n"
            "setlocal\n\n"
            "REM Ejecutar SoftPack en modo ultra portable desde USB\n"
            "cd /d %~dp0\n"
            "set \"SOFTPACK_PORTABLE_ROOT=%~dp0SoftPackData\"\n"
            "if not exist \"%SOFTPACK_PORTABLE_ROOT%\" mkdir \"%SOFTPACK_PORTABLE_ROOT%\"\n"
            "if not exist \"%SOFTPACK_PORTABLE_ROOT%\\Downloads\" mkdir \"%SOFTPACK_PORTABLE_ROOT%\\Downloads\"\n"
            "if not exist \"%SOFTPACK_PORTABLE_ROOT%\\Temp\" mkdir \"%SOFTPACK_PORTABLE_ROOT%\\Temp\"\n"
            "start \"\" \"%~dp0SoftPack.exe\"\n"
            "endlocal\n"
        )
    else:
        launcher.write_text(
            "@echo off\n"
            "setlocal\n\n"
            "REM Ejecutar SoftPack en modo ultra portable desde USB (modo carpeta)\n"
            "cd /d %~dp0\n"
            "set \"SOFTPACK_PORTABLE_ROOT=%~dp0SoftPackData\"\n"
            "if not exist \"%SOFTPACK_PORTABLE_ROOT%\" mkdir \"%SOFTPACK_PORTABLE_ROOT%\"\n"
            "if not exist \"%SOFTPACK_PORTABLE_ROOT%\\Downloads\" mkdir \"%SOFTPACK_PORTABLE_ROOT%\\Downloads\"\n"
            "if not exist \"%SOFTPACK_PORTABLE_ROOT%\\Temp\" mkdir \"%SOFTPACK_PORTABLE_ROOT%\\Temp\"\n"
            "start \"\" \"%~dp0SoftPack\\SoftPack.exe\"\n"
            "endlocal\n"
        )
    print(f'Creado lanzador: {launcher}')

    # Crear archivo de instrucciones en la raíz
    readme = target_path / 'README_USB.txt'
    readme.write_text(
        "SoftPack - Ejecución desde USB\n\n" 
        "Para ejecutar: doble clic en run_softpack.bat o en el .exe correspondiente.\n" 
        "Si el antivirus bloquea la ejecución, permita SoftPack en tu antivirus.\n" 
        "Nota: Autorun no está habilitado en Windows moderno por razones de seguridad.\n"
    )
    print(f'Archivo de instrucciones creado: {readme}')


def main(argv=None):
    p = argparse.ArgumentParser(description='Crear paquete USB de SoftPack')
    p.add_argument('--mode', choices=('onefile', 'onedir'), default='onefile', help='Modo de compilación')
    p.add_argument('--target', help='Letra de unidad o ruta destino (ej: F:\\ o "C:\\ruta")')
    p.add_argument('--copy', action='store_true', help='Copiar automáticamente al destino detectado o especificado')
    p.add_argument('--name', default='SoftPack', help='Nombre de la aplicación (por defecto SoftPack)')
    p.add_argument('--icon', help='Icono a usar (.ico)')
    args = p.parse_args(argv)

    if sys.platform != 'win32':
        print('Advertencia: este script está pensado para ejecutarse en Windows')

    mode = args.mode
    name = args.name

    # Detectar unidad removible si no se especifica target y --copy
    target = None
    if args.copy and not args.target:
        drives = get_removable_drives()
        if not drives:
            print('No se detectaron unidades removibles. Inserte la USB o especifique --target')
            sys.exit(1)
        # Si hay varias, tomar la primera
        target = Path(drives[0])
        print(f'Usando unidad removible detectada: {target}')
    elif args.target:
        target = Path(args.target)
        if len(str(target)) == 2 and str(target).endswith(':'):
            target = Path(str(target) + '\\')

    # Preparar opciones de add-data locales.
    # Incluimos recursos no-Python necesarios para que el .exe sea portátil.
    add_data = [
        f"config.py{os.pathsep}.",
        f"software_manager.py{os.pathsep}.",
        f"utils.py{os.pathsep}.",
    ]
    icons_dir = Path("icons")
    if icons_dir.exists() and icons_dir.is_dir():
        add_data.append(f"icons{os.pathsep}icons")

    # Compilar
    build(mode=mode, name=name, icon=args.icon, additional_data=add_data)

    # Copiar si se pidió
    if args.copy:
        if not target:
            print('--copy especificado pero no se encontró destino')
            sys.exit(1)
        copy_to_target(mode, name, target)
        print('✅ Paquete USB preparado correctamente.')
    else:
        print('✅ Compilación completada. Copia manualmente el ejecutable o la carpeta desde la carpeta dist\')


if __name__ == '__main__':
    main()
