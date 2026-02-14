# 📖 Guía del Usuario - SoftPack

## Índice
1. [Primeros Pasos](#primeros-pasos)
2. [Interfaz de Usuario](#interfaz-de-usuario)
3. [Cómo Instalar Software](#cómo-instalar-software)
4. [Funciones Avanzadas](#funciones-avanzadas)
5. [Preguntas Frecuentes](#preguntas-frecuentes)
6. [Consejos y Trucos](#consejos-y-trucos)

## Primeros Pasos

### ¿Qué es SoftPack?

SoftPack es una aplicación que te permite instalar múltiples programas populares de Windows de forma automática y desatendida. Es como tener tu propia tienda de aplicaciones personalizada.

### Requisitos

Antes de comenzar, asegúrate de tener:

✅ Windows 7 o superior  
✅ Python 3.8 o superior instalado  
✅ Conexión a Internet activa  
✅ Permisos de administrador en tu PC  
✅ Al menos 5 GB de espacio libre en disco

### Instalación Rápida

1. **Descarga SoftPack** en una carpeta de tu elección
2. **Haz doble clic** en `SoftPack.bat`
3. ¡Listo! La aplicación se abrirá automáticamente

Si prefieres usar la línea de comandos:
```bash
cd SoftPack
python main.py
```

## Interfaz de Usuario

### Componentes Principales

#### 🔝 Encabezado
- **Título**: SoftPack - Gestor de Software
- **Botón "Actualizar Estado"**: Verifica qué software ya está instalado
- **Botón "Acerca de"**: Información de la aplicación

#### 📋 Lista de Software
Organizada por categorías:
- **🌐 Navegadores**: Chrome, Firefox, Brave, Edge
- **💬 Comunicación**: Discord, Zoom, Telegram
- **🎵 Multimedia**: VLC, Spotify, OBS
- **💻 Desarrollo**: VS Code, Git, Python, Node.js
- **🔧 Utilidades**: 7-Zip, WinRAR, Notepad++, AnyDesk
- **🔒 Seguridad**: Malwarebytes
- **📊 Productividad**: LibreOffice, Adobe Reader, Notion
- **🎮 Gaming**: Steam, Epic Games

Cada programa muestra:
- ☑️ Casilla de selección
- 📝 Nombre del programa
- 💬 Descripción breve
- 🔘 Estado (Instalado / No instalado)

#### ⚡ Botones de Acción

| Botón | Función |
|-------|---------|
| **✓ Seleccionar Todo** | Marca todos los programas |
| **✗ Deseleccionar Todo** | Desmarca todos los programas |
| **⬇️ Descargar Seleccionados** | Solo descarga los instaladores |
| **⚙️ Instalar Seleccionados** | Instala software ya descargado |
| **🚀 Descargar e Instalar** | Descarga e instala automáticamente |

#### 📊 Registro de Actividad
Ventana de log que muestra:
- Operaciones en curso
- Descargas completadas
- Instalaciones exitosas
- Errores encontrados

## Cómo Instalar Software

### Método 1: Instalación Rápida (Recomendado)

**Para instalar varios programas a la vez:**

1. ✅ **Marca** los programas que deseas instalar
2. 🖱️ **Haz clic** en "🚀 Descargar e Instalar"
3. ✔️ **Confirma** en el diálogo que aparece
4. ⏳ **Espera** a que termine (puede tomar varios minutos)
5. ✨ **Listo!** Verás un mensaje cuando todo esté instalado

**Ejemplo**: Instalar software esencial para desarrollo
- ✅ Visual Studio Code
- ✅ Git
- ✅ Node.js
- ✅ Chrome
- 🚀 Clic en "Descargar e Instalar"

### Método 2: Descarga e Instalación Manual

**Si prefieres más control:**

1. 📋 **Selecciona** los programas deseados
2. ⬇️ **Haz clic** en "Descargar Seleccionados"
3. ⏳ **Espera** a que terminen las descargas
4. 📂 Los instaladores quedan guardados en `Downloads/SoftPack`
5. ⚙️ **Haz clic** en "Instalar Seleccionados" cuando estés listo
6. ✔️ **Confirma** la instalación

**Ventajas de este método:**
- Puedes usar los instaladores después sin Internet
- Mayor control sobre el proceso
- Útil si quieres instalar en múltiples PCs

### Método 3: Instalación Individual

**Para probar o instalar un solo programa:**

1. 🔍 **Busca** el programa en la lista
2. ✅ **Marca** solo ese programa
3. 🖱️ **Usa cualquiera de los métodos anteriores**

### Estados de Instalación

Durante el proceso verás diferentes mensajes:

| Emoji | Significado |
|-------|-------------|
| ⬇️ | Descargando... |
| ⚙️ | Instalando... |
| ✅ | Instalado correctamente |
| ❌ | Error en el proceso |
| ⚪ | No instalado |
| 🔄 | Actualizando estado |

## Funciones Avanzadas

### Actualizar Estado del Software

Si instalaste software manualmente o con SoftPack:

1. 🔄 **Haz clic** en "Actualizar Estado"
2. La aplicación **detectará** qué software está instalado
3. Los estados se **actualizarán** automáticamente

### Verificar Descargas

Los instaladores se guardan en:
```
C:\Users\TuUsuario\Downloads\SoftPack\
```

Puedes:
- 📂 Navegar a esa carpeta
- 🔍 Ver los archivos descargados
- 💾 Copiarlos a una USB para uso posterior
- 🗑️ Eliminarlos para liberar espacio

### Instalación Desatendida

**¿Qué significa "desatendida"?**

Todos los programas se instalan automáticamente sin que tengas que:
- Hacer clic en "Siguiente"
- Aceptar licencias
- Elegir opciones
- Interactuar con los instaladores

**Configuración por defecto:**
- 📍 Instalación en ubicación estándar
- ✅ Opciones recomendadas activadas
- 🚫 Sin software adicional (toolbars, etc.)
- 📌 Crear accesos directos en escritorio/menú

### Selección por Categoría

**Para instalar todo de una categoría:**

1. 📁 Ubica la categoría deseada (ej: "💻 Desarrollo")
2. ✅ Marca todos los programas de esa sección
3. 🚀 Instala normalmente

**Ejemplo - Kit de Multimedia:**
- VLC Media Player
- Spotify
- OBS Studio

## Preguntas Frecuentes

### ¿Es seguro usar SoftPack?

✅ **SÍ**. SoftPack:
- Descarga solo de fuentes oficiales
- No modifica archivos del sistema
- No contiene malware
- Es código abierto (puedes revisarlo)

### ¿Necesito antivirus desactivado?

❌ **NO**. Mantén tu antivirus activo. Si muestra alertas:
- Son **falsos positivos** comunes con instaladores
- Puedes agregar SoftPack a excepciones
- Los archivos son seguros

### ¿Cuánto tiempo toma instalar todo?

⏱️ Depende de:
- **Cantidad de software**: 1-30 programas
- **Velocidad de Internet**: 2-50 Mbps
- **Tamaño total**: 100 MB - 10 GB

**Estimaciones:**
- 5 programas pequeños: ~10-15 minutos
- 10 programas medianos: ~20-30 minutos
- Todo el catálogo: ~1-2 horas

### ¿Puedo cerrar SoftPack durante la instalación?

⚠️ **NO RECOMENDADO**. Si lo cierras:
- Las descargas se cancelarán
- Las instalaciones en curso pueden quedar incompletas
- Tendrás que reiniciar el proceso

### ¿Qué pasa si falla una instalación?

🔧 **Pasos a seguir:**
1. 📋 Revisa el registro de actividad
2. 🔍 Identifica el programa con error
3. ✅ Verifica que tienes permisos de administrador
4. 🔄 Intenta instalar solo ese programa
5. 📞 Si persiste, reporta el problema

### ¿Puedo usar SoftPack sin Internet?

🌐 **Parcialmente**:
- ❌ No puedes descargar software nuevo
- ✅ Puedes instalar software ya descargado
- 💡 Descarga todo primero, instala después sin Internet

### ¿Se actualiza el software automáticamente?

❌ **No**. SoftPack:
- Instala la versión disponible en la descarga
- No incluye actualizaciones automáticas
- Cada programa tiene su propio sistema de actualización

💡 **Consejo**: Usa "🔄 Actualizar Estado" periódicamente y reinstala para actualizar.

## Consejos y Trucos

### 🚀 Optimizar el Proceso

**Descarga nocturna:**
```
1. Selecciona todo el software
2. Solo descarga (no instales)
3. Deja descargando toda la noche
4. Instala al día siguiente sin esperas
```

**Instalación por etapas:**
```
Día 1: Navegadores + Comunicación
Día 2: Desarrollo
Día 3: Multimedia + Gaming
```

### 💾 Crear Respaldo de Instaladores

1. Descarga todo el software que necesites
2. Copia la carpeta `Downloads/SoftPack` a USB
3. Úsala para instalar en otras PCs sin descargar nuevamente

### 🎯 Perfiles de Uso

**Perfil Gaming:**
- Steam
- Epic Games
- Discord
- OBS Studio
- Navegador preferido

**Perfil Desarrollo:**
- VS Code
- Git
- Python / Node.js
- Chrome
- Notepad++
- 7-Zip

**Perfil Oficina:**
- LibreOffice
- Adobe Reader
- Zoom
- Telegram
- Firefox
- 7-Zip

**Perfil Multimedia:**
- VLC
- Spotify
- OBS Studio
- Discord
- Chrome

### ⚡ Atajos de Teclado

Aunque SoftPack no tiene atajos específicos, puedes:
- **Tab**: Navegar entre elementos
- **Espacio**: Marcar/desmarcar casillas
- **Enter**: Activar botón seleccionado

### 🔧 Mantenimiento

**Limpieza periódica:**
1. Navega a `Downloads/SoftPack`
2. Elimina instaladores antiguos
3. Libera espacio en disco

**Verificación de estado:**
- Ejecuta "🔄 Actualizar Estado" cada semana
- Verifica qué software necesita actualización
- Reinstala si es necesario

### 📊 Monitoreo de Instalaciones

**Observa el log para:**
- ✅ Confirmar instalaciones exitosas
- ❌ Detectar errores tempranamente
- 📈 Ver progreso en tiempo real
- 🐛 Reportar problemas con detalles

### 🎨 Personalización

Para agregar tu propio software, edita `config.py`:

```python
'mi_software': {
    'name': 'Mi Programa',
    'description': 'Descripción del programa',
    'category': 'Categoría',
    'download_url': 'https://...',
    'installer_name': 'installer.exe',
    'install_args': '/S',
    'check_path': r'C:\Path\To\Program.exe',
}
```

## 🆘 Obtener Ayuda

Si necesitas asistencia:

1. 📖 Lee este manual completamente
2. 🔍 Busca en la sección de Issues del repositorio
3. 📝 Crea un Issue nuevo con:
   - Sistema operativo y versión
   - Versión de Python
   - Software que intentabas instalar
   - Mensaje de error completo del log
   - Capturas de pantalla si es posible

---

**¡Disfruta de SoftPack!** 🎉

Esperamos que esta herramienta te ahorre tiempo y haga más fácil la configuración de tu sistema Windows.

