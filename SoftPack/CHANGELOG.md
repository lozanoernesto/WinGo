# 📝 Changelog - SoftPack

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2025-11-27

### ✨ Añadido
- Interfaz gráfica moderna con Tkinter
- Sistema de descarga automática de software
- Instalación desatendida de programas
- Catálogo con 30+ programas populares organizados por categorías:
  - Navegadores (Chrome, Firefox, Brave, Edge)
  - Comunicación (Discord, Zoom, Telegram)
  - Multimedia (VLC, Spotify, OBS)
  - Desarrollo (VS Code, Git, Python, Node.js)
  - Utilidades (7-Zip, WinRAR, Notepad++, AnyDesk)
  - Seguridad (Malwarebytes)
  - Productividad (LibreOffice, Adobe Reader, Notion)
  - Gaming (Steam, Epic Games)
- Detección automática de software instalado
- Registro de actividad en tiempo real
- Selección múltiple de programas
- Botones de acción rápida (Seleccionar/Deseleccionar todo)
- Tres modos de operación:
  - Solo descarga
  - Solo instalación
  - Descarga e instalación combinada
- Sistema de threading para operaciones no bloqueantes
- Validación de URLs y manejo de errores
- Documentación completa en español
- Guía del usuario detallada
- Script de inicio rápido (.bat)
- Licencia MIT

### 🔧 Técnico
- Arquitectura modular con separación de responsabilidades
- `main.py`: Interfaz de usuario
- `config.py`: Configuración y catálogo
- `software_manager.py`: Lógica de negocio
- Uso exclusivo de bibliotecas estándar de Python
- Compatible con Python 3.8+
- Soporte para Windows 7+

### 📚 Documentación
- README.md completo con instrucciones
- GUIA_USUARIO.md con tutorial paso a paso
- Comentarios detallados en el código
- requirements.txt con especificaciones
- LICENSE con términos MIT

## [Unreleased]

### 🎯 Planeado para Versiones Futuras

#### v1.1.0 - Mejoras de UX
- [ ] Modo oscuro para la interfaz
- [ ] Perfiles de instalación predefinidos
- [ ] Búsqueda y filtrado de software
- [ ] Favoritos y software recomendado
- [ ] Estadísticas de uso

#### v1.2.0 - Funcionalidad Extendida
- [ ] Sistema de actualizaciones automáticas
- [ ] Verificación de checksums MD5/SHA256
- [ ] Descarga paralela de múltiples programas
- [ ] Cola de instalación con prioridades
- [ ] Soporte para portable apps
- [ ] Exportar/importar listas de software

#### v1.3.0 - Integración
- [ ] Integración con Chocolatey
- [ ] Integración con Winget
- [ ] API REST para control remoto
- [ ] Línea de comandos (CLI)
- [ ] Configuración mediante archivos JSON/YAML

#### v2.0.0 - Características Avanzadas
- [ ] Soporte para macOS y Linux
- [ ] Base de datos SQLite para histórico
- [ ] Sistema de plugins
- [ ] Interfaz web opcional
- [ ] Desinstalación de software
- [ ] Rollback a versiones anteriores
- [ ] Programación de instalaciones
- [ ] Notificaciones del sistema

### 🐛 Problemas Conocidos
- Algunas URLs de descarga pueden cambiar con el tiempo
- La detección de software instalado puede fallar si se instaló en ubicación no estándar
- Instaladores MSI requieren msiexec.exe en PATH
- Algunos antivirus pueden generar falsos positivos
- No hay verificación de integridad de archivos descargados (pendiente para v1.2.0)

### 💡 Ideas de la Comunidad
- Soporte para temas personalizados
- Integración con gestores de paquetes Linux (apt, yum, pacman)
- Sincronización con la nube
- Compartir listas de software entre usuarios
- Sistema de calificaciones y comentarios
- Modo empresa para despliegue masivo

---

## Guía de Versionado

- **Major (X.0.0)**: Cambios incompatibles o rediseño completo
- **Minor (1.X.0)**: Nueva funcionalidad compatible con versiones anteriores
- **Patch (1.0.X)**: Correcciones de errores y mejoras menores

## Notas de Desarrollo

### Cómo Contribuir al Changelog
Al agregar cambios, usar estas categorías:
- **✨ Añadido**: Nueva funcionalidad
- **🔄 Cambiado**: Cambios en funcionalidad existente
- **⚠️ Obsoleto**: Funcionalidad marcada para eliminación
- **🗑️ Eliminado**: Funcionalidad removida
- **🐛 Corregido**: Corrección de errores
- **🔒 Seguridad**: Vulnerabilidades corregidas
- **📚 Documentación**: Cambios en documentación
- **🔧 Técnico**: Cambios internos sin impacto visible

---

[1.0.0]: https://github.com/softpack/softpack/releases/tag/v1.0.0

