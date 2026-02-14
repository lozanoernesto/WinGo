#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración y catálogo de software para WinGo
"""

import os
import sys
from pathlib import Path

# Ruta de iconos
ICONS_DIR = str(Path(__file__).parent / 'icons')

# Función auxiliar para obtener ruta de icono
def get_icon_path(software_id):
    """Obtener ruta del icono para un software"""
    return os.path.join(ICONS_DIR, f'{software_id}.png')

def _get_portable_root():
    """
    Determina la raíz de datos portable.
    Prioridad:
    1) Variable de entorno SOFTPACK_PORTABLE_ROOT (si existe)
    2) Si está empaquetado (.exe), usar carpeta junto al ejecutable
    3) None (modo no portable)
    """
    env_root = os.environ.get('SOFTPACK_PORTABLE_ROOT')
    if env_root:
        return Path(env_root)

    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent / 'SoftPackData'

    return None


def _resolve_data_dirs():
    """
    Resuelve directorios de descarga y temporales.
    Permite override explícito por variables de entorno y soporta modo portable.
    """
    portable_root = _get_portable_root()

    if portable_root:
        default_download = portable_root / 'Downloads'
        default_temp = portable_root / 'Temp'
    else:
        default_download = Path.home() / 'Downloads' / 'SoftPack'
        default_temp = Path.home() / 'AppData' / 'Local' / 'Temp' / 'SoftPack'

    download_dir = Path(os.environ.get('SOFTPACK_DOWNLOAD_DIR', str(default_download)))
    temp_dir = Path(os.environ.get('SOFTPACK_TEMP_DIR', str(default_temp)))
    return str(download_dir), str(temp_dir)


_DOWNLOAD_DIR, _TEMP_DIR = _resolve_data_dirs()

# Configuración general de la aplicación
APP_CONFIG = {
    'app_name': 'SoftPack',
    'version': '1.0.0',
    'download_dir': _DOWNLOAD_DIR,
    'temp_dir': _TEMP_DIR,
    'max_retries': 3,
    'timeout': 300,
}

# Catálogo de software disponible
# Todas las download_url son enlaces OFICIALES del fabricante (dominios oficiales).
# Fuentes: google.com, mozilla.org, brave.com, microsoft.com, discord.com, zoom.us, telegram.org,
# videolan.org, spotify.com, obsproject.com, code.visualstudio.com, python.org, nodejs.org,
# 7-zip.org, win-rar.com, notepad-plus-plus.org, anydesk.com, malwarebytes.com, adobe.com,
# store.steampowered.com, epicgames.com, battle.net, ccleaner.com, git-scm.com, etc.
SOFTWARE_CATALOG = {
    # Navegadores (oficiales: dl.google.com, download.mozilla.org, brave.com, microsoft.com)
    'chrome': {
        'name': 'Google Chrome',
        'description': 'Navegador web rápido y seguro',
        'category': 'Navegadores',
        'download_url': 'https://dl.google.com/chrome/install/latest/chrome_installer.exe',
        'installer_name': 'chrome_installer.exe',
        'install_args': '/silent /install',
        'check_path': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    },
    'firefox': {
        'name': 'Mozilla Firefox',
        'description': 'Navegador open source y personalizable',
        'category': 'Navegadores',
        'download_url': 'https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=es-ES',
        'installer_name': 'firefox_installer.exe',
        'install_args': '/S',
        'check_path': r'C:\Program Files\Mozilla Firefox\firefox.exe',
    },
    'brave': {
        'name': 'Brave Browser',
        'description': 'Navegador con bloqueador de anuncios integrado',
        'category': 'Navegadores',
        'download_url': 'https://laptop-updates.brave.com/latest/winx64',
        'installer_name': 'brave_installer.exe',
        'install_args': '/silent /install',
        'check_path': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
    },
    'edge': {
        'name': 'Microsoft Edge',
        'description': 'Navegador moderno de Microsoft',
        'category': 'Navegadores',
        'download_url': 'https://go.microsoft.com/fwlink/?linkid=2108834&Channel=Stable&language=es',
        'installer_name': 'edge_installer.exe',
        'install_args': '/silent /install',
        'check_path': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    },

    # Comunicación (oficiales: discord.com, zoom.us, telegram.org, microsoft.com)
    'discord': {
        'name': 'Discord',
        'description': 'Plataforma de comunicación para comunidades',
        'category': 'Comunicación',
        # URL directa al CDN de Discord (no pasa por redirección de la API)
        'download_url': 'https://dl.discordapp.net/distro/app/stable/win/x64/1.0.9172/DiscordSetup.exe',
        'fallback_urls': [
            'https://stable.dl2.discordapp.net/distro/app/stable/win/x64/1.0.9172/DiscordSetup.exe',
            'https://discord.com/api/download?platform=win',
        ],
        'manual_download_url': 'https://discord.com/download',
        'installer_name': 'DiscordSetup.exe',
        'install_args': '-s',
        'check_path': r'C:\Users\{username}\AppData\Local\Discord\app-*\Discord.exe',
        'check_paths': [
            r'C:\Users\{username}\AppData\Local\Discord\app-*\Discord.exe',
            r'C:\Users\{username}\AppData\Local\Discord\Update.exe',
        ],
        'verify_after_install': True,
        'install_verify_timeout': 180,
    },
    'zoom': {
        'name': 'Zoom',
        'description': 'Plataforma de videoconferencias',
        'category': 'Comunicación',
        'download_url': 'https://zoom.us/client/latest/ZoomInstaller.exe',
        'installer_name': 'zoom_installer.exe',
        'install_args': '/silent',
        'check_path': r'C:\Program Files\Zoom\bin\Zoom.exe',
    },
    'telegram': {
        'name': 'Telegram Desktop',
        'description': 'Mensajería rápida y segura',
        'category': 'Comunicación',
        'download_url': 'https://telegram.org/dl/desktop/win64',
        'installer_name': 'telegram_installer.exe',
        'install_args': '/VERYSILENT /NORESTART',
        'check_path': r'C:\Program Files\Telegram Desktop\Telegram.exe',
    },
    'teams': {
        'name': 'Microsoft Teams',
        'description': 'Chat, reuniones y colaboración de Microsoft',
        'category': 'Comunicación',
        'download_url': 'https://statics.teams.cdn.office.net/production-windows-x86/lkg/MSTeamsSetup.exe',
        'installer_name': 'teams_installer.exe',
        'install_args': '-s',
        'check_path': r'C:\Users\{username}\AppData\Local\Microsoft\Teams\current\Teams.exe',
    },

    # Multimedia (oficiales: videolan.org, spotify.com, obsproject.com)
    'vlc': {
        'name': 'VLC Media Player',
        'description': 'Reproductor multimedia universal',
        'category': 'Multimedia',
        'download_url': 'https://download.videolan.org/pub/videolan/vlc/3.0.23/win64/vlc-3.0.23-win64.exe',
        'installer_name': 'vlc_installer.exe',
        'install_args': '/L=1034 /S',
        'check_path': r'C:\Program Files\VideoLAN\VLC\vlc.exe',
    },
    'spotify': {
        'name': 'Spotify',
        'description': 'Streaming de música',
        'category': 'Multimedia',
        'download_url': 'https://download.scdn.co/SpotifySetup.exe',
        'installer_name': 'spotify_installer.exe',
        'install_args': '/silent',
        'check_path': r'C:\Users\{username}\AppData\Roaming\Spotify\Spotify.exe',
    },
    'obs': {
        'name': 'OBS Studio',
        'description': 'Software de grabación y streaming',
        'category': 'Multimedia',
        'download_url': 'https://github.com/obsproject/obs-studio/releases/download/31.1.1/OBS-Studio-31.1.1-Windows-x64-Installer.exe',
        'installer_name': 'obs_installer.exe',
        'install_args': '/S',
        'check_path': r'C:\Program Files\obs-studio\bin\64bit\obs64.exe',
    },

    # Desarrollo (oficiales: code.visualstudio.com, git-scm.com, python.org, nodejs.org)
    'vscode': {
        'name': 'Visual Studio Code',
        'description': 'Editor de código moderno',
        'category': 'Desarrollo',
        'download_url': 'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user',
        'installer_name': 'vscode_installer.exe',
        'install_args': '/VERYSILENT /NORESTART /MERGETASKS=!runcode',
        'check_path': r'C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\Code.exe',
    },
    'git': {
        'name': 'Git',
        'description': 'Sistema de control de versiones',
        'category': 'Desarrollo',
        'download_url': 'https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/Git-2.47.1-64-bit.exe',
        'installer_name': 'git_installer.exe',
        'install_args': '/VERYSILENT /NORESTART',
        'check_path': r'C:\Program Files\Git\bin\git.exe',
    },
    'python': {
        'name': 'Python 3',
        'description': 'Lenguaje de programación Python',
        'category': 'Desarrollo',
        'download_url': 'https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe',
        'installer_name': 'python_installer.exe',
        'install_args': '/quiet InstallAllUsers=1 PrependPath=1',
        'check_path': r'C:\Program Files\Python312\python.exe',
    },
    'nodejs': {
        'name': 'Node.js',
        'description': 'Entorno de ejecución JavaScript',
        'category': 'Desarrollo',
        'download_url': 'https://nodejs.org/dist/v22.11.0/node-v22.11.0-x64.msi',
        'installer_name': 'nodejs_installer.msi',
        'install_args': '/quiet /norestart',
        'check_path': r'C:\Program Files\nodejs\node.exe',
    },

    # Utilidades (oficiales: 7-zip.org, win-rar.com, notepad-plus-plus.org, anydesk.com, ccleaner.com)
    '7zip': {
        'name': '7-Zip',
        'description': 'Compresor de archivos potente',
        'category': 'Utilidades',
        'download_url': 'https://www.7-zip.org/a/7z2600-x64.exe',
        'installer_name': '7zip_installer.exe',
        'install_args': '/S',
        'check_path': r'C:\Program Files\7-Zip\7zFM.exe',
    },
    'winrar': {
        'name': 'WinRAR',
        'description': 'Compresor y descompresor RAR',
        'category': 'Utilidades',
        'download_url': 'https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-720.exe',
        'installer_name': 'winrar_installer.exe',
        'install_args': '/S',
        'check_path': r'C:\Program Files\WinRAR\WinRAR.exe',
    },
    'notepadpp': {
        'name': 'Notepad++',
        'description': 'Editor de texto avanzado',
        'category': 'Utilidades',
        'download_url': 'https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.9.1/npp.8.9.1.Installer.x64.exe',
        'installer_name': 'notepadpp_installer.exe',
        'install_args': '/S',
        'check_path': r'C:\Program Files\Notepad++\notepad++.exe',
    },
    'anydesk': {
        'name': 'AnyDesk',
        'description': 'Software de acceso remoto',
        'category': 'Utilidades',
        'download_url': 'https://download.anydesk.com/AnyDesk.exe',
        'installer_name': 'anydesk_installer.exe',
        'install_args': '--silent',
        'check_path': r'C:\Program Files (x86)\AnyDesk\AnyDesk.exe',
    },

    # Seguridad (oficiales: malwarebytes.com, pandasecurity.com, avast.com)
    'malwarebytes': {
        'name': 'Malwarebytes',
        'description': 'Antimalware y protección',
        'category': 'Seguridad',
        'download_url': 'https://data-cdn.mbamupdates.com/web/mb4-setup-consumer/MBSetup.exe',
        'installer_name': 'malwarebytes_installer.exe',
        'install_args': '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART',
        'check_path': r'C:\Program Files\Malwarebytes\Anti-Malware\mbam.exe',
    },
    'panda': {
        'name': 'Panda Security',
        'description': 'Protección antivirus y antimalware (Panda)',
        'category': 'Seguridad',
        'download_url': 'https://download.pandasecurity.com/thankyou/index.php?productID=FREEAV&interstitial=0&track=190530',
        'installer_name': 'panda_installer.exe',
        'install_args': '/silent',
        'check_path': r'C:\Program Files\Panda Security\Panda Dome\PandaDome.exe',
        'fallbacks': ['avast', 'malwarebytes'],
    },
    'avast': {
        'name': 'Avast Antivirus',
        'description': 'Protección antivirus gratuita',
        'category': 'Seguridad',
        'download_url': 'https://www.avast.com/es-mx/download-thank-you.php?product=FAV-PPC&locale=es-mx&direct=1',
        'installer_name': 'avast_installer.exe',
        'install_args': '/silent',
        'check_path': r'C:\Program Files\Avast Software\Avast\AvastUI.exe',
    },

    # Productividad (oficiales: microsoft.com, get.adobe.com/reader, notion.so)
    'microsoftoffice': {
        'name': 'Microsoft Office',
        'description': 'Microsoft 365 / Office (web installer)',
        'category': 'Productividad',
        'download_url': 'https://go.microsoft.com/fwlink/?linkid=2264705&clcid=0x409&culture=en-us&country=us',
        'installer_name': 'office_installer.exe',
        'install_args': '',
        'check_path': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
    },
    'adobereader': {
        'name': 'Adobe Acrobat Reader',
        'description': 'Lector de PDF',
        'category': 'Productividad',
        'download_url': 'https://ardownload2.adobe.com/pub/adobe/acrobat/win/AcrobatDC/2500121111/AcroRdrDCx642500121111_MUI.exe',
        'installer_name': 'adobereader_installer.exe',
        'install_args': '/sAll /rs /msi EULA_ACCEPT=YES',
        'check_path': r'C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe',
    },
    'notion': {
        'name': 'Notion',
        'description': 'Espacio de trabajo todo-en-uno',
        'category': 'Productividad',
        'download_url': 'https://www.notion.so/desktop/windows/download',
        'installer_name': 'notion_installer.exe',
        'install_args': '--silent',
        'check_path': r'C:\Users\{username}\AppData\Local\Programs\Notion\Notion.exe',
    },

    # Gaming (oficiales: store.steampowered.com, epicgames.com, battle.net)
    'steam': {
        'name': 'Steam',
        'description': 'Plataforma de juegos',
        'category': 'Gaming',
        'download_url': 'https://cdn.cloudflare.steamstatic.com/client/installer/SteamSetup.exe',
        'installer_name': 'steam_installer.exe',
        'install_args': '/S',
        'check_path': r'C:\Program Files (x86)\Steam\steam.exe',
    },
    'epicgames': {
        'name': 'Epic Games Launcher',
        'description': 'Plataforma de Epic Games',
        'category': 'Gaming',
        'download_url': 'https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi',
        'installer_name': 'epicgames_installer.msi',
        'install_args': '/quiet /norestart',
        'check_path': r'C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe',
    },
    'battlenet': {
        'name': 'Battle.net',
        'description': 'Blizzard Battle.net launcher',
        'category': 'Gaming',
        'download_url': 'https://www.battle.net/download/getInstaller?os=win&installer=Battle.net-Setup.exe',
        'installer_name': 'battlenet_installer.exe',
        'install_args': '/S',
        'check_path': r'C:\Program Files*\Battle.net*.exe',
    },

    'ccleaner': {
        'name': 'CCleaner',
        'description': 'Limpieza y optimización del sistema',
        'category': 'Utilidades',
        'download_url': 'https://download.ccleaner.com/ccsetup.exe',
        'installer_name': 'ccleaner_installer.exe',
        'install_args': '/S',
        'check_path': r'C:\Program Files\CCleaner\CCleaner.exe',
    },
    'crystaldisk': {
        'name': 'CrystalDiskInfo',
        'description': 'Monitor de estado SMART de discos',
        'category': 'Utilidades',
        'download_url': 'https://downloads.sourceforge.net/project/crystaldiskinfo/9.6.0/CrystalDiskInfo9_6_0.zip',
        'installer_name': 'crystaldisk_installer.zip',
        'install_args': '',
        'check_path': r'C:\Program Files\CrystalDiskInfo\DiskInfo64.exe',
    },
    'driverbooster': {
        'name': 'IObit Driver Booster',
        'description': 'Actualizador de controladores',
        'category': 'Utilidades',
        'download_url': 'https://cdn.iobit.com/dl/db/debug/driver_booster_setup.exe',
        'installer_name': 'driverbooster_installer.exe',
        'install_args': '/silent',
        'check_path': r'C:\Program Files\IObit\Driver Booster\DriverBooster.exe',
    },
}

# Íconos para categorías
CATEGORY_ICONS = {
    'Navegadores': '🌐',
    'Comunicación': '💬',
    'Multimedia': '🎵',
    'Desarrollo': '💻',
    'Utilidades': '🔧',
    'Seguridad': '🔒',
    'Productividad': '📊',
    'Gaming': '🎮',
}

