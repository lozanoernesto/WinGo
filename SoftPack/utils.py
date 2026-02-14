#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades adicionales para WinGo
"""

import os
import sys
from pathlib import Path
import subprocess
import winreg


def is_admin():
    """
    Verificar si el script se está ejecutando con privilegios de administrador
    
    Returns:
        bool: True si tiene privilegios de administrador
    """
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """
    Reiniciar el script con privilegios de administrador
    """
    if sys.platform != 'win32':
        return False
    
    try:
        import ctypes
        if not is_admin():
            # Reiniciar con privilegios
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                ' '.join(sys.argv), 
                None, 
                1
            )
            return True
    except Exception as e:
        print(f"Error al solicitar privilegios de administrador: {e}")
    
    return False


def get_installed_programs():
    """
    Obtener lista de programas instalados desde el registro de Windows
    
    Returns:
        list: Lista de diccionarios con información de programas
    """
    programs = []
    
    # Rutas del registro donde se almacenan los programas instalados
    registry_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]
    
    for hkey, path in registry_paths:
        try:
            key = winreg.OpenKey(hkey, path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    
                    try:
                        name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        try:
                            version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                        except:
                            version = "Unknown"
                        
                        try:
                            publisher = winreg.QueryValueEx(subkey, "Publisher")[0]
                        except:
                            publisher = "Unknown"
                        
                        try:
                            install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                        except:
                            install_location = ""
                        
                        programs.append({
                            'name': name,
                            'version': version,
                            'publisher': publisher,
                            'location': install_location
                        })
                    except:
                        pass
                    
                    winreg.CloseKey(subkey)
                except:
                    pass
            
            winreg.CloseKey(key)
        except:
            pass
    
    return programs


def check_python_version():
    """
    Verificar que la versión de Python sea compatible
    
    Returns:
        bool: True si la versión es compatible
    """
    import sys
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"Error: Python 3.8 o superior es requerido.")
        print(f"Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    return True


def check_internet_connection():
    """
    Verificar si hay conexión a Internet
    
    Returns:
        bool: True si hay conexión
    """
    import urllib.request
    
    try:
        urllib.request.urlopen('https://www.google.com', timeout=5)
        return True
    except:
        return False


def format_bytes(bytes_size):
    """
    Formatear tamaño en bytes a formato legible
    
    Args:
        bytes_size: Tamaño en bytes
        
    Returns:
        str: Tamaño formateado (ej: "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def get_free_space(path):
    """
    Obtener espacio libre en el disco
    
    Args:
        path: Ruta para verificar
        
    Returns:
        int: Espacio libre en bytes
    """
    if sys.platform == 'win32':
        import ctypes
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(str(path)), 
            None, 
            None, 
            ctypes.pointer(free_bytes)
        )
        return free_bytes.value
    else:
        stat = os.statvfs(path)
        return stat.f_bavail * stat.f_frsize


def create_shortcut(target, shortcut_path, description=""):
    """
    Crear un acceso directo en Windows
    
    Args:
        target: Ruta del archivo objetivo
        shortcut_path: Ruta donde crear el acceso directo
        description: Descripción del acceso directo
    """
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.Description = description
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.save()
        return True
    except:
        print("Error: No se pudo crear el acceso directo")
        print("Instala pywin32: pip install pywin32")
        return False


def validate_url(url):
    """
    Validar si una URL es válida
    
    Args:
        url: URL a validar
        
    Returns:
        bool: True si la URL es válida
    """
    import re
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// o https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # dominio
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # puerto opcional
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(regex, url) is not None


def cleanup_temp_files(directory):
    """
    Limpiar archivos temporales
    
    Args:
        directory: Directorio a limpiar
    """
    import shutil
    try:
        if Path(directory).exists():
            shutil.rmtree(directory)
            Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error al limpiar archivos temporales: {e}")
        return False


if __name__ == "__main__":
    # Pruebas de utilidades
    print("=== Pruebas de Utilidades SoftPack ===\n")
    
    print(f"¿Es administrador?: {is_admin()}")
    print(f"Versión de Python compatible: {check_python_version()}")
    print(f"Conexión a Internet: {check_internet_connection()}")
    print(f"Espacio libre en C: {format_bytes(get_free_space('C:\\'))}")
    
    print("\nProgramas instalados (primeros 5):")
    programs = get_installed_programs()
    for prog in programs[:5]:
        print(f"  - {prog['name']} ({prog['version']})")

