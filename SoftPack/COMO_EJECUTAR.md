# 🚀 Cómo Ejecutar SoftPack

## ⚠️ IMPORTANTE: Compatibilidad

**SoftPack está diseñado exclusivamente para Windows**

- ✅ **Funciona en**: Windows 7, 8, 10, 11
- ❌ **NO funciona en**: macOS, Linux (el software que instala es para Windows)

---

## 🪟 Ejecutar en Windows (FUNCIONALIDAD COMPLETA)

### ✅ Requisitos Previos

1. **Python 3.8 o superior** instalado
   - Descarga desde: https://www.python.org/downloads/
   - ⚠️ **IMPORTANTE**: Marca "Add Python to PATH" durante instalación

2. **Verificar Python**:
   ```bash
   python --version
   ```
   Debe mostrar: `Python 3.x.x`

### 🚀 Método 1: Doble Clic (MÁS FÁCIL)

1. Abre la carpeta `SoftPack`
2. **Haz doble clic en**: `SoftPack.bat`
3. ¡Listo! La aplicación se abre

### 💻 Método 2: Línea de Comandos

```bash
cd SoftPack
python main.py
```

### 🎯 Uso Básico

1. **Marca** los programas que quieres instalar
2. **Haz clic** en "🚀 Descargar e Instalar"
3. **Espera** (todo es automático)
4. **¡Listo!** Software instalado

---

## 🍎 Ejecutar en macOS (SOLO DEMO VISUAL)

### ⚠️ Limitaciones en macOS

- ✅ Puedes ver la interfaz
- ❌ NO puedes instalar software (es software de Windows)
- ❌ Las descargas no funcionarán
- ℹ️ Solo es para visualizar el diseño

### 🎨 Ver Demo en macOS

**Opción A - Doble Clic**:
1. Abre la carpeta `SoftPack`
2. **Haz doble clic en**: `EJECUTAR_AQUI.command`
3. Se abrirá una demo visual

**Opción B - Terminal**:
```bash
cd SoftPack
python3 demo_macos.py
```

---

## 🐧 Linux

SoftPack está diseñado para Windows. En Linux:
- La interfaz puede funcionar (Tkinter)
- Pero NO instalará software (son instaladores .exe y .msi de Windows)
- Similar a macOS: solo demo visual

```bash
cd SoftPack
python3 demo_macos.py  # Funciona también en Linux
```

---

## 📁 Archivos de Ejecución

```
SoftPack/
├── SoftPack.bat              ← Para WINDOWS (doble clic)
├── main.py                   ← Para WINDOWS (python main.py)
├── demo_macos.py            ← Para macOS/Linux (solo vista)
└── EJECUTAR_AQUI.command    ← Para macOS (doble clic demo)
```

---

## 🔧 Solución de Problemas

### Windows: "Python no se reconoce"

**Problema**: Python no está en PATH

**Solución**:
1. Reinstala Python
2. ✅ Marca "Add Python to PATH"
3. O agrega manualmente:
   - Panel de Control → Sistema → Variables de entorno
   - Agrega: `C:\Users\Usuario\AppData\Local\Programs\Python\Python3XX`

### Windows: "Error al abrir"

**Solución**:
1. Click derecho en `SoftPack.bat`
2. "Ejecutar como administrador"
3. Acepta el UAC

### macOS: "No se puede abrir"

**Solución**:
1. Click derecho en `EJECUTAR_AQUI.command`
2. "Abrir"
3. Click en "Abrir" en el diálogo
4. (Primera vez necesita permiso)

### macOS: "Permission denied"

**Solución**:
```bash
chmod +x EJECUTAR_AQUI.command
./EJECUTAR_AQUI.command
```

---

## 📋 Verificar que Todo Funciona

### En Windows

```bash
# 1. Verificar Python
python --version

# 2. Verificar Tkinter
python -c "import tkinter; print('Tkinter OK')"

# 3. Ejecutar SoftPack
python main.py
```

Si todo funciona, verás la ventana de SoftPack.

### En macOS/Linux

```bash
# 1. Verificar Python
python3 --version

# 2. Verificar Tkinter
python3 -c "import tkinter; print('Tkinter OK')"

# 3. Ejecutar Demo
python3 demo_macos.py
```

Verás la interfaz (demo visual).

---

## 🎯 Recomendaciones

### Para Uso Real (Instalar Software)

1. **Usa Windows**: SoftPack solo funciona completamente en Windows
2. **Copia a USB**: Puedes copiar SoftPack a USB para instalar en múltiples PCs
3. **Ejecuta como Admin**: Algunos programas requieren permisos elevados

### Para Desarrollo/Pruebas

1. **Revisa el código**: Todos los archivos están comentados
2. **Lee la documentación**: `README.md`, `GUIA_USUARIO.md`
3. **Personaliza**: Edita `config.py` para agregar tu software

---

## 📞 ¿Necesitas Ayuda?

1. **Lee la documentación**:
   - `README.md` - Información general
   - `GUIA_USUARIO.md` - Manual completo
   - `INSTALL.md` - Guía de instalación

2. **Revisa los ejemplos**:
   - `QUICK_START.md` - Inicio rápido
   - `LEEME.txt` - Referencia rápida

3. **Busca problemas comunes**:
   - Sección de troubleshooting en documentación

---

## 🎉 ¡Listo para Empezar!

### En Windows:
```bash
# Opción más fácil:
Doble clic en: SoftPack.bat

# O en terminal:
python main.py
```

### En macOS (solo demo):
```bash
# Doble clic en:
EJECUTAR_AQUI.command

# O en terminal:
python3 demo_macos.py
```

---

**Recuerda**: SoftPack funciona **100% solo en Windows** 🪟

Para usar todas las funciones, cópialo a una PC con Windows y ejecuta `SoftPack.bat`

¡Disfruta instalando software sin estrés! 🚀

