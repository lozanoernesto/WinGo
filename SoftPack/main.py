#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WinGo - Gestor de Instalación de Software (Rediseñado)
Interfaz moderna con tarjetas/tiles para cada programa
"""

import sys
import os

# --- PyInstaller runtime path fix ---
# Cuando se ejecuta como .exe empaquetado, los módulos locales (config.py,
# software_manager.py, utils.py) se extraen a un directorio temporal.
# Asegurar que ese directorio esté al inicio de sys.path para que los
# imports funcionen correctamente.
if getattr(sys, 'frozen', False):
    _bundle_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    if _bundle_dir not in sys.path:
        sys.path.insert(0, _bundle_dir)
# --- Fin fix ---

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from software_manager import SoftwareManager
from config import SOFTWARE_CATALOG, APP_CONFIG
from pathlib import Path
from PIL import Image, ImageTk

# Generar un logo placeholder si no existe (usa Pillow)
def ensure_wingo_logo():
    try:
        icons_dir = Path(__file__).parent / 'icons'
        icons_dir.mkdir(exist_ok=True)
        # Prefer a user-provided logo if present. Look for common names/extensions.
        candidates = ['wingo_custom.png', 'wingo_custom.jpg', 'wingo_custom.jpeg',
                      'wingo_logo.png', 'wingo_logo.jpg', 'wingo_logo.jpeg']
        for name in candidates:
            p = icons_dir / name
            if p.exists():
                return str(p)
        # Also accept any file that starts with 'wingo' (useful if user saved different extension)
        for p in icons_dir.glob('wingo*'):
            if p.is_file():
                return str(p)

        # Default placeholder path
        logo_path = icons_dir / 'wingo_logo.png'
        if logo_path.exists():
            return str(logo_path)

        # Crear imagen simple con texto y un rectángulo que simula un monitor
        from PIL import ImageDraw, ImageFont
        w, h = 512, 160
        img = Image.new('RGBA', (w, h), (40, 40, 40, 255))
        draw = ImageDraw.Draw(img)

        # Dibujar rectángulo del monitor
        monitor_box = (20, 20, 140, 100)
        draw.rounded_rectangle(monitor_box, radius=8, fill=(255,255,255,255))
        # Soporte del monitor
        draw.rectangle((70, 100, 90, 108), fill=(255,255,255,255))

        # Texto WinGo
        try:
            font = ImageFont.truetype('segoeui.ttf', 72)
        except Exception:
            try:
                font = ImageFont.truetype('DejaVuSans-Bold.ttf', 72)
            except Exception:
                font = ImageFont.load_default()

        text = 'WinGo'
        text_color = (198, 149, 113, 255)
        tw, th = draw.textsize(text, font=font)
        draw.text((170, (h - th) / 2 - 8), text, font=font, fill=text_color)

        img.save(logo_path)
        return str(logo_path)
    except Exception:
        return None

class SoftwareCard(tk.Frame):
    """Tarjeta visual para cada software"""
    def __init__(self, parent, soft_id, soft_data, on_select, status_callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.soft_id = soft_id
        self.soft_data = soft_data
        self.on_select = on_select
        self.status_callback = status_callback
        self.photo_image = None  # Mantener referencia a la imagen
        
        # Configurar estilos de la tarjeta y tamaño fijo (cuadrado)
        CARD_SIZE = 260
        self.config(bg='white', relief=tk.RAISED, bd=1, highlightthickness=1,
                    highlightbackground='#e0e0e0', highlightcolor='#0078d4',
                    width=CARD_SIZE, height=CARD_SIZE)
        # Evitar que los widgets hijos cambien el tamaño del frame
        try:
            self.pack_propagate(False)
        except Exception:
            pass
        try:
            self.grid_propagate(False)
        except Exception:
            pass
        
        # Crear contenido de la tarjeta
        self.create_card_content()
        
        # Binds para hover effect
        self.bind('<Enter>', self.on_hover_enter)
        self.bind('<Leave>', self.on_hover_leave)
        
    def create_card_content(self):
        """Crear el contenido de la tarjeta"""
        # Icono en la parte superior
        icon_frame = tk.Frame(self, bg='white', height=110)
        icon_frame.pack(fill=tk.X, padx=5, pady=5)
        icon_frame.pack_propagate(False)
        
        # Cargar y mostrar icono
        icon_path = os.path.join(Path(__file__).parent / 'icons', f'{self.soft_id}.png')
        if os.path.exists(icon_path):
            try:
                img = Image.open(icon_path)
                img.thumbnail((90, 90), Image.Resampling.LANCZOS)
                self.photo_image = ImageTk.PhotoImage(img)
                icon_label = tk.Label(icon_frame, image=self.photo_image, bg='white')
                icon_label.pack(pady=5)
            except Exception as e:
                print(f"Error cargando icono para {self.soft_id}: {e}")
        
        # Header con checkbox y nombre
        header_frame = tk.Frame(self, bg='white')
        header_frame.pack(fill=tk.X, padx=10, pady=(6, 4))
        
        # Checkbox
        self.var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(header_frame, text=self.soft_data['name'], 
                                       variable=self.var, font=('Segoe UI', 11, 'bold'),
                                       bg='white', fg='#1a1a1a',
                                       command=self.on_select)
        self.checkbox.pack(side=tk.LEFT)
        
        # Descripción
        desc_frame = tk.Frame(self, bg='white')
        desc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        desc_label = tk.Label(desc_frame, text=self.soft_data.get('description', ''),
                     font=('Segoe UI', 9), bg='white', fg='#666666',
                     wraplength=220, justify=tk.LEFT)
        desc_label.pack(anchor=tk.W)
        
        # Status bar
        status_frame = tk.Frame(self, bg='#f5f5f5', height=35)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text='⚪ No instalado',
                                     font=('Segoe UI', 8), bg='#f5f5f5', fg='#555555')
        self.status_label.pack(side=tk.LEFT, padx=10, pady=8)
        
    def on_hover_enter(self, event):
        """Efecto hover al entrar"""
        self.config(bg='#f8f8f8', highlightbackground='#0078d4', highlightcolor='#0078d4')
        self.checkbox.config(bg='#f8f8f8')
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg='#f8f8f8')
            elif isinstance(widget, tk.Label):
                widget.config(bg='#f8f8f8')
    
    def on_hover_leave(self, event):
        """Efecto hover al salir"""
        self.config(bg='white', highlightbackground='#e0e0e0')
        self.checkbox.config(bg='white')
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.winfo_children()[-1]:
                widget.config(bg='white')
            elif isinstance(widget, tk.Label) and widget != self.status_label:
                widget.config(bg='white')
    
    def update_status(self, is_installed):
        """Actualizar el estado de instalación"""
        if is_installed:
            self.status_label.config(text='✅ Instalado', fg='#28a745')
        else:
            self.status_label.config(text='⚪ No instalado', fg='#555555')
    
    def get_selected(self):
        """Obtener si está seleccionado"""
        return self.var.get()


class WinGoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WinGo - Instalador de Software")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Colores
        self.bg_color = "#f5f5f5"
        self.primary_color = "#0078d4"
        
        # Configurar tema
        self.root.configure(bg=self.bg_color)
        
        # Inicializar manager
        self.manager = SoftwareManager()
        self.cards = {}  # Mapear soft_id -> SoftwareCard
        
        # Crear interfaz
        self.create_widgets()
        
        # Cargar estado
        self.refresh_software_status()
        
        # Limpiar temporales al cerrar (modo ultra portable)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_widgets(self):
        """Crear widgets principales"""
        # Header
        self.create_header()
        
        # Contenido con scroll
        self.create_software_grid()
        
        # Botones de acción
        self.create_action_buttons()
        
        # Log
        self.create_log_section()
    
    def create_header(self):
        """Crear encabezado"""
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=140)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        # Left area: logo + title
        left_frame = tk.Frame(header_frame, bg=self.primary_color)
        left_frame.pack(side=tk.LEFT, anchor=tk.W, padx=20, pady=(12, 8))

        # Intentar asegurar logo y cargarlo
        logo_path = ensure_wingo_logo()
        if logo_path and os.path.exists(logo_path):
            try:
                logo_img = Image.open(logo_path)
                # Ajustar alto a ~80px
                logo_img.thumbnail((220, 80), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                logo_lbl = tk.Label(left_frame, image=self.logo_photo, bg=self.primary_color)
                logo_lbl.pack(side=tk.LEFT, padx=(0, 12))
            except Exception:
                pass

        # Título y descripción junto al logo
        title_container = tk.Frame(left_frame, bg=self.primary_color)
        title_container.pack(side=tk.LEFT)

        title_label = tk.Label(title_container, text="WinGo",
                               font=('Segoe UI', 26, 'bold'), bg=self.primary_color, fg='#d9b38c')
        title_label.pack(anchor=tk.W)

        subtitle_label = tk.Label(title_container,
                                 text="Instala y actualiza software popular de forma rápida",
                                 font=('Segoe UI', 10), bg=self.primary_color, fg='#e0e0e0')
        subtitle_label.pack(anchor=tk.W)

        # Barra de búsqueda rediseñada (estilizada para el header), colocada a la right
        search_frame = tk.Frame(header_frame, bg=self.primary_color)
        search_frame.pack(side=tk.RIGHT, fill=tk.X, expand=False, padx=20, pady=(18, 8))

        search_label = tk.Label(search_frame, text="🔍", font=('Segoe UI', 14),
                                bg=self.primary_color, fg='white')
        search_label.pack(side=tk.LEFT, padx=(0, 8))

        self.search_var = tk.StringVar()
        entry_container = tk.Frame(search_frame, bg='white')
        entry_container.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Entry estilizado (más grande) y guardado como atributo
        self.search_entry = tk.Entry(entry_container, textvariable=self.search_var,
                                     font=('Segoe UI', 12), relief=tk.FLAT,
                                     bd=0, highlightthickness=0, bg='white', fg='#000000')
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=8, pady=6)
        # Placeholder inicial
        self.search_var.set('Buscar programas...')
        self.search_entry.config(fg='#999999')

        # Botones de acción: Buscar y Limpiar
        btn_style = {'bg': 'white', 'fg': '#333333', 'bd': 0, 'relief': tk.FLAT}
        search_btn = tk.Button(entry_container, text='Buscar', command=self.perform_search, **btn_style)
        search_btn.pack(side=tk.RIGHT, padx=(0, 6), pady=6)
        clear_btn = tk.Button(entry_container, text='✖', command=self.clear_search, **btn_style)
        clear_btn.pack(side=tk.RIGHT, padx=(0, 6), pady=6)

        # Asegurar que la entrada reciba foco al hacer clic y muestre cursor
        self.search_entry.config(takefocus=True, cursor='xterm')
        self.search_entry.bind('<Button-1>', lambda e: self.search_entry.focus_set())
        # Permitir que hacer clic en el contenedor blanco también enfoque la entrada
        entry_container.bind('<Button-1>', lambda e: self.search_entry.focus_set())

        def on_focus_in(event):
            if self.search_entry.get() == 'Buscar programas...':
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg='#000000')

        def on_focus_out(event):
            if self.search_entry.get().strip() == '':
                self.search_var.set('Buscar programas...')
                self.search_entry.config(fg='#999999')

        self.search_entry.bind('<FocusIn>', on_focus_in)
        self.search_entry.bind('<FocusOut>', on_focus_out)
        # Enter hace la búsqueda explícita
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        # Botones en header
        btn_frame = tk.Frame(header_frame, bg=self.primary_color)
        btn_frame.pack(side=tk.RIGHT, padx=20, pady=(0, 15))
        
        ttk.Button(btn_frame, text="🔄 Actualizar", command=self.refresh_software_status).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="ℹ️ Acerca de", command=self.show_about).pack(side=tk.LEFT, padx=3)
    
    def create_software_grid(self):
        """Crear grid de tarjetas de software"""
        # Frame con scroll
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Agrupar por categoría
        categories = {}
        for soft_id, soft_data in SOFTWARE_CATALOG.items():
            category = soft_data.get('category', 'Otros')
            if category not in categories:
                categories[category] = []
            categories[category].append((soft_id, soft_data))

        # Area de resultados de búsqueda (inicialmente vacía y no visible)
        self.search_result_cards = []  # tarjetas temporales creadas para mostrar resultados
        self.category_sections = []  # guardar referencias a títulos y marcos por categoría

        # Crear un contenedor de resultados (se mostrará cuando haya búsqueda)
        self.results_title = tk.Label(scrollable_frame, text="Resultados de búsqueda",
                                      font=('Segoe UI', 13, 'bold'), bg=self.bg_color, fg='#1a1a1a')
        self.results_grid = tk.Frame(scrollable_frame, bg=self.bg_color)

        # Crear secciones por categoría y guardar referencias para poder ocultarlas
        for category in sorted(categories.keys()):
            # Título de categoría
            cat_title = tk.Label(scrollable_frame, text=f"📁 {category}",
                                font=('Segoe UI', 13, 'bold'), bg=self.bg_color, fg='#1a1a1a')
            cat_title.pack(anchor=tk.W, padx=0, pady=(20, 10))
            
            # Lista de marcos que contendrán las tarjetas (una o más filas)
            frames = []
            grid_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
            grid_frame.pack(fill=tk.X, padx=0, pady=(0, 10))
            frames.append(grid_frame)
            
            col = 0
            for soft_id, soft_data in sorted(categories[category], key=lambda x: x[1]['name']):
                card = SoftwareCard(grid_frame, soft_id, soft_data, 
                                   lambda sid=soft_id: None,  # Callback vacío
                                   lambda: None,  # status_callback vacío
                                   bg=self.bg_color)
                card.grid(row=0, column=col, sticky=(tk.N,), padx=8, pady=5)
                # Asegurar columna con tamaño mínimo para alinear tarjetas
                try:
                    grid_frame.grid_columnconfigure(col, minsize=280)
                except Exception:
                    pass

                self.cards[soft_id] = card
                col += 1
                
                # Limitar columnas a 4 por fila: crear un nuevo grid_frame en la misma categoría
                if col >= 4:
                    col = 0
                    grid_frame.grid_rowconfigure(0, weight=1)
                    next_grid = tk.Frame(scrollable_frame, bg=self.bg_color)
                    next_grid.pack(fill=tk.X, padx=0, pady=(0, 10))
                    frames.append(next_grid)
                    grid_frame = next_grid
            
            # Configurar peso de columnas para el último grid_frame creado
            for c in range(col):
                grid_frame.grid_columnconfigure(c, weight=1)

            # Guardar la sección (título + todos los marcos que contienen tarjetas)
            self.category_sections.append({'title': cat_title, 'frames': frames})
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self.canvas = canvas
    
    def create_action_buttons(self):
        """Crear botones de acción"""
        btn_frame = tk.Frame(self.root, bg='white', relief=tk.RIDGE, bd=1)
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # Botones de selección
        tk.Button(btn_frame, text="✓ Seleccionar Todo", command=self.select_all,
                 bg='#f0f0f0', fg='#1a1a1a', font=('Segoe UI', 9),
                 relief=tk.FLAT, padx=10, pady=8).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(btn_frame, text="✗ Deseleccionar Todo", command=self.deselect_all,
                 bg='#f0f0f0', fg='#1a1a1a', font=('Segoe UI', 9),
                 relief=tk.FLAT, padx=10, pady=8).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Spacer
        spacer = tk.Label(btn_frame, bg='white')
        spacer.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botones de acción principales
        tk.Button(btn_frame, text="⬇️ Descargar", command=self.download_selected,
                 bg='#0078d4', fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(btn_frame, text="⚙️ Instalar", command=self.install_selected,
                 bg='#28a745', fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(btn_frame, text="🚀 Descargar e Instalar", command=self.download_and_install,
                 bg='#ff6b35', fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_log_section(self):
        """Crear sección de log"""
        log_frame = tk.Frame(self.root, bg='white', relief=tk.SUNKEN, bd=1)
        log_frame.pack(fill=tk.BOTH, expand=False, padx=15, pady=(0, 15), ipady=5)
        
        log_label = tk.Label(log_frame, text="📋 Registro de Actividad",
                            font=('Segoe UI', 10, 'bold'), bg='white', fg='#1a1a1a')
        log_label.pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6,
                                                 font=('Consolas', 8),
                                                 bg='#1e1e1e', fg='#00ff00',
                                                 insertbackground='white')
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log("✨ WinGo iniciado correctamente")
        self.log(f"📂 Directorio: {self.manager.download_dir}")
    
    def log(self, message):
        """Agregar mensaje al log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def filter_cards(self):
        """Compatibilidad: delega en perform_search para mostrar resultados arriba."""
        self.perform_search()

    def clear_search(self):
        """Limpiar la caja de búsqueda y mostrar todas las tarjetas"""
        # Vaciar la búsqueda y restaurar placeholder visual
        self.search_var.set('Buscar programas...')
        self.search_entry.config(fg='#999999')
        # Eliminar tarjetas temporales de resultados
        for c in list(self.search_result_cards):
            try:
                c.destroy()
            except Exception:
                pass
        self.search_result_cards = []

        # Ocultar contenedor de resultados
        try:
            self.results_title.pack_forget()
            self.results_grid.pack_forget()
        except Exception:
            pass

        # Volver a mostrar las secciones por categoría en el orden original
        for section in self.category_sections:
            try:
                section['title'].pack(anchor=tk.W, padx=0, pady=(20, 10))
                for f in section['frames']:
                    f.pack(fill=tk.X, padx=0, pady=(0, 10))
            except Exception:
                pass

        # Asegurar que las tarjetas originales estén visibles
        for card in self.cards.values():
            try:
                card.grid()
            except Exception:
                pass

    def perform_search(self):
        """Realiza la búsqueda mostrando primero coincidencias exactas (name == query),
        y si no hay resultados, intenta substring match en los nombres.
        """
        raw = (self.search_var.get() or '').strip()
        query = raw.lower()

        # Si está vacío o es el placeholder, mostrar todo
        if query == '' or query == 'buscar programas...':
            self.clear_search()
            return

        # Buscar coincidencias exactas por nombre
        # Recolectar coincidencias: exactas primero
        matches = []
        for soft_id, info in SOFTWARE_CATALOG.items():
            name = info.get('name', '').lower()
            if name == query:
                matches.append(soft_id)

        # Si no hay exactas, buscar por substring
        if not matches:
            for soft_id, info in SOFTWARE_CATALOG.items():
                name = info.get('name', '').lower()
                if query in name:
                    matches.append(soft_id)

        # Ocultar todas las secciones por categoría
        for section in self.category_sections:
            try:
                section['title'].pack_forget()
                for f in section['frames']:
                    f.pack_forget()
            except Exception:
                pass

        # Limpiar resultados previos
        for c in list(self.search_result_cards):
            try:
                c.destroy()
            except Exception:
                pass
        self.search_result_cards = []

        # Mostrar contenedor de resultados
        self.results_title.config(text=f"Resultados para: '{raw}'")
        self.results_title.pack(anchor=tk.W, padx=0, pady=(20, 10))
        self.results_grid.pack(fill=tk.X, padx=0, pady=(0, 10))

        # Si no hay matches, mostrar mensaje
        if not matches:
            lbl = tk.Label(self.results_grid, text="No se encontraron resultados.",
                           font=('Segoe UI', 10), bg=self.bg_color, fg='#666666')
            lbl.pack(anchor=tk.W, padx=8, pady=6)
            self.search_result_cards.append(lbl)
            return

        # Crear tarjetas temporales para los resultados y colocarlas en una grilla
        max_cols = 4
        col = 0
        row = 0
        for sid in matches:
            info = SOFTWARE_CATALOG.get(sid, {})
            card = SoftwareCard(self.results_grid, sid, info,
                                lambda sid=sid: None, lambda: None, bg=self.bg_color)
            card.grid(row=row, column=col, sticky=(tk.N,), padx=8, pady=5)
            try:
                self.results_grid.grid_columnconfigure(col, minsize=280)
            except Exception:
                pass
            self.search_result_cards.append(card)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def get_selected_items(self):
        """Obtener software seleccionado"""
        return [soft_id for soft_id, card in self.cards.items() if card.get_selected()]
    
    def select_all(self):
        """Seleccionar todo"""
        for card in self.cards.values():
            card.var.set(True)
        self.log("✓ Todo seleccionado")
    
    def deselect_all(self):
        """Deseleccionar todo"""
        for card in self.cards.values():
            card.var.set(False)
        self.log("✗ Todo deseleccionado")
    
    def refresh_software_status(self):
        """Actualizar estado de instalación"""
        self.log("🔄 Actualizando estado...")
        for soft_id, card in self.cards.items():
            is_installed = self.manager.check_installed(soft_id)
            card.update_status(is_installed)
        self.log("✓ Estado actualizado")
    
    def download_selected(self):
        """Descargar software seleccionado"""
        selected = self.get_selected_items()
        if not selected:
            messagebox.showwarning("Advertencia", "No hay software seleccionado")
            return
        
        self.log(f"⬇️ Descargando {len(selected)} programa(s)...")
        
        def task():
            for soft_id in selected:
                self.log(f"⬇️ Descargando {SOFTWARE_CATALOG[soft_id]['name']}...")
                if self.manager.download(soft_id):
                    self.log(f"✅ {SOFTWARE_CATALOG[soft_id]['name']} descargado")
                else:
                    self.log(f"❌ Error al descargar")
            self.log("✓ Descarga completada")
        
        threading.Thread(target=task, daemon=True).start()
    
    def install_selected(self):
        """Instalar software seleccionado"""
        selected = self.get_selected_items()
        if not selected:
            messagebox.showwarning("Advertencia", "No hay software seleccionado")
            return
        
        if not messagebox.askyesno("Confirmar", f"¿Instalar {len(selected)} programa(s)?"):
            return
        
        self.log(f"⚙️ Instalando {len(selected)} programa(s)...")
        
        def task():
            for soft_id in selected:
                name = SOFTWARE_CATALOG[soft_id]['name']
                self.log(f"⚙️ Instalando {name}...")
                if self.manager.install(soft_id):
                    self.log(f"✅ {name} instalado")
                    self.cards[soft_id].update_status(True)
                else:
                    self.log(f"❌ Error al instalar")
            self.log("✓ Instalación completada")
            messagebox.showinfo("Completado", "¡Instalación finalizada!")
        
        threading.Thread(target=task, daemon=True).start()
    
    def download_and_install(self):
        """Descargar e instalar"""
        selected = self.get_selected_items()
        if not selected:
            messagebox.showwarning("Advertencia", "No hay software seleccionado")
            return
        
        if not messagebox.askyesno("Confirmar", f"¿Descargar e instalar {len(selected)} programa(s)?"):
            return
        
        self.log(f"🚀 Iniciando descargas e instalaciones...")
        
        def task():
            for soft_id in selected:
                name = SOFTWARE_CATALOG[soft_id]['name']
                self.log(f"⬇️ Descargando {name}...")
                if self.manager.download(soft_id):
                    self.log(f"⚙️ Instalando {name}...")
                    if self.manager.install(soft_id):
                        self.log(f"✅ {name} completado")
                        self.cards[soft_id].update_status(True)
                    else:
                        self.log(f"❌ Error al instalar")
                else:
                    self.log(f"❌ Error al descargar")
            self.log("✓ Proceso completado")
            messagebox.showinfo("Completado", "¡Todo finalizado!")
        
        threading.Thread(target=task, daemon=True).start()
    
    def show_about(self):
        """Mostrar acerca de"""
        about_text = """WinGo - Instalador de Software v1.0

Aplicación moderna para instalar software popular
de forma rápida y sencilla.

Características:
• Interfaz moderna con tarjetas visuales
• Búsqueda rápida de programas
• Instalación desatendida
• Soporte para múltiples categorías

Desarrollado para facilitar la gestión de software."""
        messagebox.showinfo("Acerca de WinGo", about_text)

    def on_close(self):
        """Cerrar la aplicación limpiando temporales."""
        try:
            self.manager.cleanup_temp()
        except Exception:
            pass
        self.root.destroy()


def main():
    """Función principal"""
    root = tk.Tk()
    app = WinGoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
