# 📦 Guía de Instalación - SoftPack

Esta guía te ayudará a instalar y configurar SoftPack en tu sistema Windows.

## 📋 Requisitos del Sistema

### Mínimos
- **Sistema Operativo**: Windows 7 SP1 (64-bit)
- **Python**: 3.8 o superior
- **RAM**: 2 GB
- **Espacio en Disco**: 100 MB + espacio para descargas (recomendado 10 GB)
- **Conexión a Internet**: Para descargas

### Recomendados
- **Sistema Operativo**: Windows 10/11 (64-bit)
- **Python**: 3.11 o superior
- **RAM**: 4 GB o más
- **Espacio en Disco**: 20 GB libres
- **Conexión a Internet**: Banda ancha (10 Mbps+)

## 🐍 Instalar Python

### Verificar si Python está instalado

Abre PowerShell o CMD y ejecuta:
```bash
python --version
```

Si ves algo como `Python 3.11.x`, ya tienes Python instalado. Si no:

### Instalar Python en Windows

1. **Descarga Python**
   - Ve a https://www.python.org/downloads/
   - Descarga la última versión estable (3.11 o superior)
   - Elige el instalador de Windows (64-bit)

2. **Ejecuta el instalador**
   - ✅ **IMPORTANTE**: Marca "Add Python to PATH"
   - Haz clic en "Install Now"
   - Espera a que termine la instalación

3. **Verifica la instalación**
   ```bash
   python --version
   python -m pip --version
   ```

## 📥 Instalar SoftPack

### Opción 1: Descarga Directa (Recomendado)

1. **Descarga el proyecto**
   - Descarga el archivo ZIP desde GitHub
   - Extrae en una ubicación permanente (ej: `C:\SoftPack`)

2. **Verifica los archivos**
   ```
   SoftPack/
   ├── main.py
   ├── config.py
   ├── software_manager.py
   ├── utils.py
   ├── SoftPack.bat
   └── README.md
   ```

### Opción 2: Git Clone

```bash
# Clonar el repositorio
git clone https://github.com/softpack/softpack.git
cd softpack
```

## 🚀 Primera Ejecución

### Método 1: Usar el Script BAT (Más Fácil)

1. Navega a la carpeta SoftPack
2. Haz doble clic en `SoftPack.bat`
3. Si Windows pregunta, permite la ejecución
4. ¡La aplicación se abrirá!

### Método 2: Línea de Comandos

```bash
cd C:\Ruta\A\SoftPack
python main.py
```

### Método 3: Crear Acceso Directo

1. Click derecho en `SoftPack.bat`
2. "Crear acceso directo"
3. Mueve el acceso directo al Escritorio o Menú Inicio
4. ¡Lanza SoftPack desde donde quieras!

## ⚙️ Configuración Inicial

### Primera Vez

Al ejecutar SoftPack por primera vez:

1. **Interfaz se abre**: Verás la lista de software disponible
2. **Estado inicial**: Todo aparece como "No instalado"
3. **Actualizar estado**: Haz clic en "🔄 Actualizar Estado"
4. **Software detectado**: Los programas ya instalados se marcarán

### Configurar Directorios (Opcional)

Si quieres cambiar dónde se descargan los instaladores:

1. Abre `config.py` en un editor de texto
2. Busca `APP_CONFIG`
3. Modifica `download_dir`:

```python
APP_CONFIG = {
    'download_dir': 'D:\\MisDescargas\\SoftPack',  # Tu ruta personalizada
    ...
}
```

## 🔧 Configuración Avanzada

### Permisos de Administrador

Algunos programas requieren permisos elevados para instalar:

**Ejecutar como administrador:**
1. Click derecho en `SoftPack.bat`
2. "Ejecutar como administrador"
3. Acepta el control de cuentas de usuario (UAC)

### Configurar Firewall/Antivirus

Si tu antivirus bloquea SoftPack:

**Windows Defender:**
1. Abre "Seguridad de Windows"
2. Ve a "Protección contra virus y amenazas"
3. "Administrar configuración"
4. En "Exclusiones", agrega la carpeta SoftPack

**Otros antivirus:**
- Consulta la documentación de tu antivirus
- Agrega SoftPack a la lista blanca/excepciones

### Variables de Entorno (Opcional)

Para ejecutar SoftPack desde cualquier lugar:

1. Abre "Variables de entorno"
2. Edita "Path" en variables de usuario
3. Agrega la ruta a SoftPack: `C:\Ruta\A\SoftPack`
4. Ahora puedes ejecutar: `python main.py` desde cualquier lugar

## 🧪 Verificar Instalación

Ejecuta estos comandos para verificar todo:

```bash
# Verificar Python
python --version

# Verificar que SoftPack inicia
python main.py

# Verificar módulos necesarios
python -c "import tkinter; print('Tkinter OK')"
python -c "import urllib.request; print('urllib OK')"
```

Si todo muestra OK, ¡estás listo!

## 📱 Crear Acceso Rápido

### En el Escritorio

```bash
# Copia este código en un archivo .vbs
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\SoftPack.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "C:\Ruta\A\SoftPack\SoftPack.bat"
oLink.WorkingDirectory = "C:\Ruta\A\SoftPack"
oLink.Description = "SoftPack - Gestor de Software"
oLink.Save
```

Guarda como `crear_acceso.vbs` y ejecútalo.

### En el Menú Inicio

1. Click derecho en `SoftPack.bat`
2. "Anclar al menú inicio"

### En la Barra de Tareas

1. Abre SoftPack
2. Click derecho en el icono de la barra
3. "Anclar a la barra de tareas"

## 🐛 Solución de Problemas de Instalación

### "Python no se reconoce como comando"

**Problema**: Python no está en PATH

**Solución**:
1. Reinstala Python
2. Marca "Add Python to PATH"
3. O agrega manualmente: `C:\Users\Usuario\AppData\Local\Programs\Python\Python3XX`

### "tkinter no está disponible"

**Problema**: Tkinter no instalado (raro en Windows)

**Solución**:
```bash
# Reinstala Python asegurándote de incluir tcl/tk
# O instala manualmente:
pip install tk
```

### "No se puede ejecutar SoftPack.bat"

**Problema**: Restricciones de ejecución

**Solución**:
1. Click derecho → Propiedades
2. "Desbloquear" si aparece la opción
3. Aplicar y OK
4. Intenta de nuevo

### "Error de permisos al instalar"

**Problema**: Sin privilegios de administrador

**Solución**:
- Ejecuta SoftPack.bat como administrador
- Click derecho → "Ejecutar como administrador"

### "No hay conexión a Internet"

**Problema**: Firewall o proxy bloqueando

**Solución**:
1. Verifica tu conexión: `ping google.com`
2. Configura proxy si es necesario
3. Desactiva temporalmente firewall para probar
4. Consulta con tu administrador de red

## 🔄 Actualizar SoftPack

Cuando haya una nueva versión:

### Método 1: Descarga Manual
1. Descarga la nueva versión
2. Respalda tu `config.py` si lo modificaste
3. Reemplaza los archivos
4. Restaura tu configuración personalizada

### Método 2: Git Pull
```bash
cd SoftPack
git pull origin main
```

## 🗑️ Desinstalar SoftPack

SoftPack no requiere desinstalación formal:

1. Cierra SoftPack si está abierto
2. Elimina la carpeta SoftPack
3. Elimina accesos directos si los creaste
4. Los programas instalados con SoftPack permanecen (desinstala desde Windows)

## 📞 Obtener Ayuda

Si tienes problemas:

1. **Revisa esta guía** completa
2. **Lee el README.md** para más información
3. **Consulta GUIA_USUARIO.md** para uso
4. **Busca en Issues** de GitHub
5. **Crea un Issue** nuevo con detalles

## ✅ Siguiente Paso

Una vez instalado, consulta:
- 📖 [README.md](README.md) - Información general
- 📚 [GUIA_USUARIO.md](GUIA_USUARIO.md) - Cómo usar SoftPack
- ⚡ [QUICK_START.md](QUICK_START.md) - Inicio rápido

---

¡Felicidades! SoftPack está instalado y listo para usar. 🎉

