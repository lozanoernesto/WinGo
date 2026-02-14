# 🚀 SoftPack - Gestor de Software Todo-en-Uno

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

**SoftPack** es una aplicación moderna y sencilla que facilita la instalación, actualización y gestión de los programas más populares y útiles para Windows. Con instalaciones desatendidas y versiones oficiales limpias, ahorrarás tiempo configurando tu sistema.

## ✨ Características Principales

- 🎯 **Interfaz Intuitiva**: Diseño moderno y fácil de usar
- ⚡ **Instalación Desatendida**: Sin necesidad de interacción durante el proceso
- 🔒 **Versiones Oficiales**: Descargas directas desde fuentes oficiales
- 🧹 **Instalaciones Limpias**: Sin software adicional no deseado
- 📦 **Múltiples Categorías**: Navegadores, desarrollo, multimedia, productividad y más
- 🔄 **Gestión Centralizada**: Instala múltiples programas con un solo clic
- 📊 **Seguimiento en Tiempo Real**: Log detallado de todas las operaciones

## 📋 Software Incluido

### 🌐 Navegadores
- Google Chrome
- Mozilla Firefox
- Brave Browser
- Microsoft Edge

### 💬 Comunicación
- Discord
- Zoom
- Telegram Desktop

### 🎵 Multimedia
- VLC Media Player
- Spotify
- OBS Studio

### 💻 Desarrollo
- Visual Studio Code
- Git
- Python 3
- Node.js

### 🔧 Utilidades
- 7-Zip
- WinRAR
- Notepad++
- AnyDesk

### 🔒 Seguridad
- Malwarebytes

### 📊 Productividad
- LibreOffice
- Adobe Acrobat Reader
- Notion

### 🎮 Gaming
- Steam
- Epic Games Launcher

## 🚀 Inicio Rápido

### ⚡ Opción 1: Usar Ejecutable (SIN Python) ⭐ RECOMENDADO

**¿Quieres usar SoftPack como un .exe sin instalar Python?**

1. **Compila a ejecutable** (una sola vez):
   ```bash
   Doble clic en: build_exe_simple.bat
   ```

2. **Usa el ejecutable**:
   ```bash
   El .exe estará en: dist\SoftPack.exe
   Doble clic para ejecutar - ¡Sin Python necesario!
   ```

📖 **Guía completa**: Lee `CREAR_EJECUTABLE.md` para instrucciones detalladas

### 🐍 Opción 2: Ejecutar con Python

**Requisitos**:
- Windows 7+ (64-bit recomendado)
- Python 3.8 o superior
- Conexión a Internet

**Ejecución**:
1. Doble clic en `SoftPack.bat`
2. O ejecuta: `python main.py`

### Uso Básico

1. **Selecciona el software** que deseas instalar marcando las casillas
2. **Elige una acción**:
   - ⬇️ **Descargar**: Solo descarga los instaladores
   - ⚙️ **Instalar**: Instala el software previamente descargado
   - 🚀 **Descargar e Instalar**: Descarga e instala automáticamente
3. **Espera** a que el proceso complete
4. **Verifica** el estado de instalación con el botón "Actualizar Estado"

## 📁 Estructura del Proyecto

```
SoftPack/
│
├── main.py                 # Aplicación principal con interfaz GUI
├── config.py              # Catálogo de software y configuración
├── software_manager.py    # Lógica de descarga e instalación
├── requirements.txt       # Dependencias (solo Python estándar)
├── README.md             # Este archivo
├── SoftPack.bat          # Script de inicio rápido para Windows
└── LICENSE               # Licencia del proyecto
```

## 🔧 Configuración Avanzada

### Modificar el Catálogo de Software

Puedes agregar o modificar software editando el archivo `config.py`. Cada entrada debe seguir este formato:

```python
'software_id': {
    'name': 'Nombre del Software',
    'description': 'Descripción breve',
    'category': 'Categoría',
    'download_url': 'URL de descarga directa',
    'installer_name': 'nombre_instalador.exe',
    'install_args': '/argumentos /silenciosos',
    'check_path': r'C:\Ruta\Al\Ejecutable\programa.exe',
}
```

### Cambiar Directorio de Descargas

Modifica `APP_CONFIG` en `config.py`:

```python
APP_CONFIG = {
    'download_dir': 'C:\\TuRuta\\Personalizada',
    ...
}
```

## 🛠️ Argumentos de Instalación Silenciosa

La mayoría del software usa estos argumentos para instalación desatendida:

- **NSIS**: `/S`
- **Inno Setup**: `/VERYSILENT /NORESTART`
- **MSI**: `/quiet /norestart`
- **InstallShield**: `/s /v/qn`

## 📝 Registro de Actividad

Todas las operaciones se registran en la ventana de log de la aplicación:
- ⬇️ Descargas iniciadas
- ✅ Instalaciones exitosas
- ❌ Errores encontrados
- 🔄 Actualizaciones de estado

## ⚠️ Consideraciones Importantes

1. **Permisos de Administrador**: Muchas instalaciones requieren privilegios elevados
2. **Antivirus**: Algunos antivirus pueden marcar los instaladores como sospechosos (falsos positivos)
3. **Espacio en Disco**: Asegúrate de tener suficiente espacio para las descargas
4. **Conexión a Internet**: Se requiere conexión estable para descargas grandes
5. **URLs Actualizadas**: Las URLs de descarga pueden cambiar; actualiza `config.py` si es necesario

## 🔄 Actualización de Software

Para actualizar software ya instalado:

1. Selecciona el software en la lista
2. Descarga la versión más reciente
3. La mayoría de instaladores detectarán la versión anterior y actualizarán automáticamente

## 🐛 Solución de Problemas

### El software no se instala
- Verifica que tienes permisos de administrador
- Comprueba que el instalador se descargó correctamente
- Revisa el log para ver mensajes de error específicos

### Error de descarga
- Verifica tu conexión a Internet
- Comprueba que la URL de descarga sigue siendo válida
- Algunos servidores pueden requerir VPN en ciertas regiones

### Software no detectado como instalado
- Las rutas de instalación pueden variar según la configuración
- Verifica manualmente si el software está en Programas y Características
- Actualiza el `check_path` en `config.py` si es necesario

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para agregar software nuevo:

1. Fork el proyecto
2. Agrega la entrada en `config.py`
3. Prueba que la descarga e instalación funcionan
4. Envía un Pull Request

### Ideas para Mejoras

- [ ] Sistema de actualizaciones automáticas
- [ ] Descarga paralela de múltiples programas
- [ ] Soporte para portable apps
- [ ] Verificación de checksums
- [ ] Perfiles de instalación (Gaming, Desarrollo, Oficina)
- [ ] Integración con Chocolatey/Winget
- [ ] Modo oscuro para la interfaz

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- A todos los desarrolladores del software incluido en el catálogo
- A la comunidad de Python y Tkinter
- A los usuarios que prueban y reportan problemas

## 📞 Soporte

Si encuentras problemas o tienes sugerencias:
- Abre un Issue en el repositorio
- Revisa la sección de Solución de Problemas
- Consulta la documentación del software específico

---

**Nota**: Este software es una herramienta de gestión. Todos los programas instalados pertenecen a sus respectivos propietarios y están sujetos a sus propias licencias y términos de uso.

---

Desarrollado con ❤️ para facilitar la configuración de sistemas Windows

**SoftPack** - Tu gestor de software todo-en-uno

