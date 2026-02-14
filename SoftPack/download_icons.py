#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Descargar iconos para las aplicaciones
"""
import urllib.request
import os
from pathlib import Path

icons_dir = Path(__file__).parent / 'icons'
icons_dir.mkdir(exist_ok=True)

# Mapeo de software a URLs de iconos
ICON_URLS = {
    'chrome': 'https://www.gstatic.com/images/branding/product/1x/chrome_48dp.png',
    'firefox': 'https://www.mozilla.org/media/img/logos/firefox/logo-only.9adacd5987be.png',
    'brave': 'https://raw.githubusercontent.com/brave/brave-core/master/ui/webui/resources/images/brave_logo.png',
    'edge': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Microsoft%20Edge/3D/microsoft_edge_3d.png',
    'discord': 'https://discord.com/api/guilds/81384788765712384/widget.png?style=banner2',
    'zoom': 'https://www.gstatic.com/images/branding/product/1x/zoom_48dp.png',
    'telegram': 'https://www.gstatic.com/images/branding/product/1x/telegram_48dp.png',
    'vlc': 'https://www.videolan.org/images/VLC_icon.png',
    'spotify': 'https://www.gstatic.com/images/branding/product/1x/spotify_48dp.png',
    'obs': 'https://obsproject.com/assets/images/logos/obs-logo.png',
    'vscode': 'https://www.gstatic.com/images/branding/product/1x/visual_studio_code_48dp.png',
    'git': 'https://git-scm.com/images/logos/downloads/Git-Icon-1788C.png',
    'python': 'https://www.python.org/static/community_logos/python-logo.png',
    'nodejs': 'https://nodejs.org/static/images/logo.svg',
    '7zip': 'https://www.7-zip.org/7z.png',
    'winrar': 'https://www.rarlab.com/rar/winrar-x64.exe',
    'notepadpp': 'https://notepad-plus-plus.org/images/logo.svg',
    'anydesk': 'https://www.gstatic.com/images/branding/product/1x/anydesk_48dp.png',
    'malwarebytes': 'https://www.gstatic.com/images/branding/product/1x/malwarebytes_48dp.png',
    'libreoffice': 'https://www.libreoffice.org/assets/img/global/libreoffice-logo.svg',
    'adobereader': 'https://www.gstatic.com/images/branding/product/1x/adobe_acrobat_reader_48dp.png',
    'notion': 'https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png',
    'steam': 'https://www.gstatic.com/images/branding/product/1x/steam_48dp.png',
    'epicgames': 'https://www.gstatic.com/images/branding/product/1x/epic_games_launcher_48dp.png',
}

print("Descargando iconos...")
for software_id, url in ICON_URLS.items():
    icon_path = icons_dir / f'{software_id}.png'
    if not icon_path.exists():
        try:
            print(f"Descargando {software_id}...", end=' ')
            urllib.request.urlretrieve(url, icon_path)
            print("OK")
        except Exception as e:
            print(f"Error: {e}")
            # Crear icono por defecto (pequeño placeholder)
            # Por ahora solo log del error
    else:
        print(f"{software_id} ya existe")

print("Descarga completada")
