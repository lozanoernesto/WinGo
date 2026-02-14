#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo de SoftPack para macOS
Solo muestra la interfaz, no instala software (que es para Windows)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

print("=" * 60)
print("  DEMO SOFTPACK - Visualización de Interfaz")
print("=" * 60)
print()
print("⚠️  NOTA IMPORTANTE:")
print("   Esta es una versión DEMO para macOS")
print("   Solo muestra la interfaz visual")
print("   Para instalar software, usa SoftPack en Windows")
print()
print("=" * 60)
print()

class SoftPackDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("SoftPack DEMO - Gestor de Software (Solo Vista)")
        self.root.geometry("1000x700")
        
        # Mensaje de advertencia
        warning_frame = tk.Frame(root, bg='#ffc107', padx=10, pady=5)
        warning_frame.pack(fill=tk.X)
        
        tk.Label(warning_frame, 
                text="⚠️ DEMO: Esta es solo una vista previa. SoftPack funciona completamente en Windows.",
                bg='#ffc107', font=('Arial', 10, 'bold')).pack()
        
        # Setup styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#0078d4')
        
        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="🚀 SoftPack - Gestor de Software", 
                 style='Title.TLabel').pack(side=tk.LEFT)
        
        ttk.Label(header_frame, 
                 text="Instala y actualiza software popular de forma rápida y desatendida",
                 font=('Arial', 9)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Software list area
        list_frame = ttk.LabelFrame(main_frame, text="Software Disponible", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Canvas with scrollbar
        canvas = tk.Canvas(list_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Sample software
        categories = {
            '🌐 Navegadores': [
                ('Google Chrome', 'Navegador rápido y seguro'),
                ('Mozilla Firefox', 'Navegador open source'),
                ('Brave Browser', 'Con bloqueador de anuncios'),
            ],
            '💻 Desarrollo': [
                ('Visual Studio Code', 'Editor de código moderno'),
                ('Git', 'Control de versiones'),
                ('Python 3', 'Lenguaje de programación'),
            ],
            '🎵 Multimedia': [
                ('VLC Media Player', 'Reproductor multimedia'),
                ('Spotify', 'Streaming de música'),
                ('OBS Studio', 'Grabación y streaming'),
            ],
            '🔧 Utilidades': [
                ('7-Zip', 'Compresor de archivos'),
                ('Notepad++', 'Editor de texto avanzado'),
            ]
        }
        
        row = 0
        for category, software_list in categories.items():
            ttk.Label(scrollable, text=category, 
                     font=('Arial', 12, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
            row += 1
            
            for name, desc in software_list:
                soft_frame = ttk.Frame(scrollable)
                soft_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), padx=20, pady=2)
                
                var = tk.BooleanVar()
                ttk.Checkbutton(soft_frame, text=name, variable=var).grid(row=0, column=0, sticky=tk.W)
                ttk.Label(soft_frame, text=desc, font=('Arial', 8), 
                         foreground='#666666').grid(row=0, column=1, sticky=tk.W, padx=10)
                ttk.Label(soft_frame, text="⚪ No instalado", 
                         font=('Arial', 8)).grid(row=0, column=2, sticky=tk.E)
                
                row += 1
            
            ttk.Separator(scrollable, orient='horizontal').grid(row=row, column=0, 
                                                               sticky=(tk.W, tk.E), pady=5)
            row += 1
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="✓ Seleccionar Todo", 
                  command=lambda: self.log("Función de ejemplo")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="⬇️ Descargar", 
                  command=lambda: self.show_demo_message("Descargar")).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="🚀 Instalar", 
                  command=lambda: self.show_demo_message("Instalar")).pack(side=tk.RIGHT, padx=5)
        
        # Log
        log_frame = ttk.LabelFrame(main_frame, text="📋 Registro de Actividad", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, 
                                                  font=('Monaco', 9),
                                                  bg='#1e1e1e', fg='#ffffff')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.log("✨ SoftPack DEMO iniciado")
        self.log("⚠️  Esta es una versión de demostración para macOS")
        self.log("📝 Solo muestra la interfaz visual")
        self.log("🪟 Para funcionalidad completa, usa SoftPack en Windows")
        self.log("=" * 60)
        
    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
    def show_demo_message(self, action):
        self.log(f"🔵 Función '{action}' presionada (DEMO - no ejecuta en macOS)")
        messagebox.showinfo("Demo", 
                          f"Esta es una DEMO de SoftPack.\n\n"
                          f"La función '{action}' solo funciona en Windows.\n\n"
                          f"En Windows, esto descargaría e instalaría el software seleccionado.")

def main():
    root = tk.Tk()
    app = SoftPackDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main()

