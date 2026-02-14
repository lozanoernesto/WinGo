#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenerar iconos PNG como placeholders legibles.
Se crean iconos cuadrados con fondo de color y la inicial del nombre centrada.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

icons_dir = Path(__file__).parent / 'icons'
icons_dir.mkdir(exist_ok=True)

# Colores por software
ICON_COLORS = {
    'chrome': '#4285F4', 'firefox': '#FF7139', 'brave': '#FB542B', 'edge': '#0078D4',
    'discord': '#5865F2', 'zoom': '#0B5CFF', 'telegram': '#0088cc', 'vlc': '#FF8800',
    'spotify': '#1DB954', 'obs': '#302E31', 'vscode': '#0078D4', 'git': '#F05032',
    'python': '#3776AB', 'nodejs': '#339933', '7zip': '#FF6B6B', 'winrar': '#FFB81C',
    'notepadpp': '#90E59A', 'anydesk': '#0078D4', 'malwarebytes': '#1A1A1A',
    'libreoffice': '#00A500', 'adobereader': '#EC1C24', 'notion': '#7A7A7A',
    'steam': '#000000', 'epicgames': '#313131'
    , 'matlab': '#A2142F', 'ccleaner': '#F39C12', 'crystaldisk': '#2BB7B1', 'driverbooster': '#00A86B'
}

print("Regenerando iconos legibles...")
for software_id, color in ICON_COLORS.items():
    icon_path = icons_dir / f"{software_id}.png"

    # No sobrescribir iconos existentes por defecto
    import sys
    force = '--force' in sys.argv
    if icon_path.exists() and not force:
        print(f"Saltando (existe): {icon_path.name}")
        continue

    size = 128
    radius = 18
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Dibujar fondo redondeado
    draw.rounded_rectangle((0, 0, size, size), radius=radius, fill=color)

    # Inicial: primera letra del nombre (mayúscula)
    initial = software_id[0].upper()

    # Intentar fuentes comunes; fallback a load_default
    font = None
    for fnt in ("segoeui.ttf", "SegoeUI.ttf", "DejaVuSans-Bold.ttf"):
        try:
            font = ImageFont.truetype(fnt, 64)
            break
        except Exception:
            font = None
    if font is None:
        font = ImageFont.load_default()

    # Calcular posición para centrar la letra
    try:
        w, h = font.getsize(initial)
    except Exception:
        # Fallback
        bbox = draw.textbbox((0,0), initial, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    x = (size - w) / 2
    y = (size - h) / 2 - 6

    # Dibujar sombra y letra blanca
    draw.text((x+1, y+2), initial, font=font, fill=(0, 0, 0, 100))
    draw.text((x, y), initial, font=font, fill='white')

    img.save(icon_path)
    print(f"Icono creado: {icon_path.name}")

print("Iconos regenerados.")
