# 🤝 Guía de Contribución - SoftPack

¡Gracias por tu interés en contribuir a SoftPack! Este documento te guiará a través del proceso de contribución.

## 📋 Tabla de Contenidos

1. [Código de Conducta](#código-de-conducta)
2. [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
3. [Guía de Desarrollo](#guía-de-desarrollo)
4. [Agregar Nuevo Software](#agregar-nuevo-software)
5. [Estilo de Código](#estilo-de-código)
6. [Proceso de Pull Request](#proceso-de-pull-request)

## Código de Conducta

Este proyecto y todos sus participantes se rigen por un código de conducta. Al participar, se espera que mantengas este código. Por favor reporta comportamiento inaceptable.

**Principios básicos:**
- Sé respetuoso y considerado
- Acepta críticas constructivas
- Enfócate en lo que es mejor para la comunidad
- Muestra empatía hacia otros miembros

## ¿Cómo Puedo Contribuir?

### 🐛 Reportar Errores

Antes de reportar un error:
1. Verifica que uses la última versión
2. Busca en los issues existentes
3. Intenta reproducir el error

Al reportar incluye:
- **Sistema operativo** y versión
- **Versión de Python**
- **Pasos para reproducir** el error
- **Comportamiento esperado** vs **comportamiento actual**
- **Capturas de pantalla** si es relevante
- **Log completo** del error

### 💡 Sugerir Mejoras

Las sugerencias son bienvenidas. Para proponer una mejora:
1. Verifica que no exista ya en issues
2. Crea un issue detallando:
   - **Problema actual**: ¿Qué limitación existe?
   - **Solución propuesta**: ¿Cómo lo mejorarías?
   - **Alternativas**: ¿Consideraste otras opciones?
   - **Contexto adicional**: Screenshots, mockups, etc.

### 📝 Mejorar Documentación

La documentación siempre puede mejorar:
- Corregir errores tipográficos
- Clarificar instrucciones confusas
- Agregar ejemplos
- Traducir a otros idiomas
- Mejorar formato y estructura

### 💻 Contribuir Código

Antes de comenzar:
1. Comenta en el issue relevante
2. Haz fork del repositorio
3. Crea una rama desde `main`
4. Realiza tus cambios
5. Haz push a tu fork
6. Abre un Pull Request

## Guía de Desarrollo

### Configuración del Entorno

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/softpack.git
cd softpack

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# No hay dependencias externas, ¡listo para desarrollar!
```

### Estructura del Proyecto

```
SoftPack/
├── main.py                 # Aplicación principal (GUI)
├── config.py              # Configuración y catálogo
├── software_manager.py    # Lógica de descarga/instalación
├── requirements.txt       # Dependencias (solo stdlib)
├── README.md             # Documentación principal
├── GUIA_USUARIO.md       # Guía del usuario
└── CONTRIBUTING.md       # Este archivo
```

### Ejecutar en Modo Desarrollo

```bash
python main.py
```

## Agregar Nuevo Software

### Paso 1: Investigar el Software

Antes de agregar software, verifica:
- ✅ Es software legítimo y seguro
- ✅ Tiene una descarga directa disponible
- ✅ Soporta instalación silenciosa/desatendida
- ✅ Es software popular o útil

### Paso 2: Encontrar URLs y Parámetros

Necesitas:
1. **URL de descarga directa**: No debe requerir clicks adicionales
2. **Argumentos de instalación silenciosa**: Busca en la documentación oficial
3. **Ruta de instalación**: Dónde se instala por defecto

**Argumentos comunes:**
- NSIS: `/S`
- Inno Setup: `/VERYSILENT /NORESTART`
- InstallShield: `/s /v/qn`
- MSI: `/quiet /norestart`

### Paso 3: Agregar al Catálogo

Edita `config.py` y agrega tu entrada:

```python
'id_unico': {
    'name': 'Nombre del Software',
    'description': 'Descripción breve y clara',
    'category': 'Categoría Apropiada',
    'download_url': 'https://url-descarga-directa.com/installer.exe',
    'installer_name': 'nombre_instalador.exe',
    'install_args': '/argumentos /silenciosos',
    'check_path': r'C:\Program Files\Software\ejecutable.exe',
},
```

**Categorías disponibles:**
- Navegadores
- Comunicación
- Multimedia
- Desarrollo
- Utilidades
- Seguridad
- Productividad
- Gaming

### Paso 4: Probar

1. Ejecuta SoftPack
2. Verifica que el software aparece en la lista
3. Prueba descargar
4. Prueba instalar
5. Verifica que se detecta correctamente después de instalar

### Paso 5: Documentar

En tu Pull Request incluye:
- ¿Por qué agregaste este software?
- ¿Cómo verificaste que funciona?
- ¿La URL es estable o puede cambiar?
- ¿Hay consideraciones especiales?

## Estilo de Código

### Python

Seguimos [PEP 8](https://pep8.org/) con algunas adaptaciones:

```python
# Buenos nombres descriptivos
def download_and_install(software_id):
    """Descarga e instala el software especificado."""
    pass

# Comentarios útiles
# Verificar que el software existe antes de proceder
if software_id not in SOFTWARE_CATALOG:
    return False

# Strings con comillas simples para código, dobles para mensajes
config_path = 'config.py'
message = "Software instalado correctamente"

# Formato claro y legible
result = some_function(
    param1=value1,
    param2=value2,
    param3=value3
)
```

### Documentación

```python
def my_function(param1, param2):
    """
    Descripción breve de la función.
    
    Args:
        param1: Descripción del primer parámetro
        param2: Descripción del segundo parámetro
        
    Returns:
        Descripción del valor de retorno
        
    Raises:
        ExceptionType: Cuándo se lanza la excepción
    """
    pass
```

### Commits

Mensajes de commit claros y descriptivos:

```bash
# Bueno
git commit -m "Agregar soporte para VLC Media Player"
git commit -m "Corregir error en detección de software instalado"
git commit -m "Actualizar documentación de instalación"

# Malo
git commit -m "cambios"
git commit -m "fix"
git commit -m "WIP"
```

**Prefijos útiles:**
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de error
- `docs:` - Cambios en documentación
- `style:` - Formato, espacios, etc.
- `refactor:` - Refactorización de código
- `test:` - Agregar o modificar tests
- `chore:` - Mantenimiento

## Proceso de Pull Request

### Antes de Enviar

- [ ] El código funciona correctamente
- [ ] Seguiste el estilo de código del proyecto
- [ ] Actualizaste la documentación si es necesario
- [ ] Agregaste comentarios en código complejo
- [ ] Probaste en Windows (si es cambio funcional)
- [ ] Revisaste que no hay errores de tipeo

### Plantilla de Pull Request

```markdown
## Descripción
[Descripción clara de qué hace este PR]

## Tipo de cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Cambio que rompe compatibilidad
- [ ] Documentación

## ¿Cómo se probó?
[Describe cómo probaste los cambios]

## Checklist
- [ ] Mi código sigue el estilo del proyecto
- [ ] He realizado una auto-revisión
- [ ] He comentado código complejo
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan nuevos warnings
- [ ] He probado que funciona correctamente
```

### Proceso de Revisión

1. **Envío**: Creas el PR
2. **Revisión inicial**: Mantenedor revisa en 1-3 días
3. **Feedback**: Pueden solicitar cambios
4. **Iteración**: Realizas ajustes si es necesario
5. **Aprobación**: PR es aprobado
6. **Merge**: Se integra a `main`

### Después del Merge

- Tu contribución se agregará al CHANGELOG
- Serás mencionado en los créditos
- El software se incluirá en la próxima release

## Tipos de Contribuciones Necesarias

### 🔴 Alta Prioridad
- Actualizar URLs obsoletas
- Corregir bugs críticos
- Mejorar detección de software instalado
- Agregar software muy popular

### 🟡 Media Prioridad
- Agregar nuevo software útil
- Mejorar interfaz de usuario
- Optimizar velocidad de descarga
- Ampliar documentación

### 🟢 Baja Prioridad
- Refactorización de código
- Agregar tests
- Mejoras cosméticas
- Traducciones

## Recursos Útiles

### Aprendizaje
- [Python Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Silent Install Builders](https://silentinstallhq.com/)
- [Chocolatey Packages](https://community.chocolatey.org/packages) (para referencias)

### Herramientas
- [7-Zip](https://www.7-zip.org/) - Extraer instaladores para ver estructura
- [Universal Silent Switch Finder](https://hopelesslygeek.com/ussf/) - Encontrar argumentos silenciosos

### Comunidad
- GitHub Issues - Discusiones y reportes
- GitHub Discussions - Preguntas generales
- Pull Requests - Revisión de código

## Preguntas Frecuentes

**¿Cuánto tiempo toma revisar un PR?**  
Generalmente 1-3 días. Si es urgente, menciona en el PR.

**¿Puedo trabajar en múltiples issues?**  
Sí, pero mejor terminar uno antes de empezar otro.

**¿Qué pasa si mi PR no es aceptado?**  
Explicaremos el motivo. Puedes hacer ajustes o discutir alternativas.

**¿Necesito experiencia previa?**  
No. Contribuciones simples como documentación son perfectas para empezar.

**¿Puedo agregar software de mi compañía?**  
Sí, si es útil para usuarios generales y cumple los criterios.

## Reconocimientos

Todos los contribuidores son reconocidos en:
- Archivo CONTRIBUTORS.md
- Releases notes
- README principal

¡Gracias por contribuir a SoftPack! 🎉

---

**Preguntas adicionales?** Abre un issue con la etiqueta `question`.

