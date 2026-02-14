# SoftPack - Paquete USB 📦🔌

Este documento explica cómo preparar SoftPack para ejecutarlo desde una memoria USB.

## Opciones

- Opción rápida: Copiar `dist\SoftPack.exe` directamente a la USB (modo onefile)
- Opción automatizada: Ejecutar `build_for_usb.bat` desde la carpeta `SoftPack` (recomendado)

## Uso recomendado (automático)

1. Inserta tu memoria USB en el PC.
2. Abre la carpeta `SoftPack` y haz doble clic en `build_for_usb.bat`.
3. Selecciona el modo de compilación (recomendado: `onefile`).
4. Cuando te pregunte, permite copiar automáticamente a la USB.
5. En la USB se crearán:
   - `SoftPack.exe` (si elegiste `onefile`) o
   - la carpeta `SoftPack\` con `SoftPack.exe` dentro (si elegiste `onedir`)
   - `run_softpack.bat` → lanzador con rutas relativas
   - `README_USB.txt` → instrucciones simples

## Cómo ejecutar desde la USB

- Doble clic en `run_softpack.bat` (o en `SoftPack.exe`) para iniciar la aplicación.
- En modo ultra portable, las descargas y temporales se guardan en `SoftPackData\` dentro de la misma USB.
- Al cerrar la app, `SoftPackData\Temp` se limpia automáticamente.
- Si el antivirus bloquea la ejecución, agrega una excepción temporal.

## Limitaciones y advertencias ⚠️

- Windows 7/8/10/11: la ejecución desde USB es soportada, pero Windows ya no permite la ejecución automática (`autorun.inf`) por seguridad.
- Algunos antivirus marcan archivos generados por PyInstaller como sospechosos (falsos positivos). Si esto ocurre:
  - Permite SoftPack en el antivirus
  - O ejecuta `SoftPack.exe` como administrador
- No asumas que la letra de la unidad será siempre la misma en otras PCs.
- Si la app necesita escribir archivos, la USB debe tener permisos de escritura.

## Buenas prácticas ✅

- Prueba el paquete en otra PC antes de distribuirlo.
- Usa `onefile` para mayor simplicidad.
- Mantén una copia de seguridad del ejecutable en tu disco duro.

## Soporte
Si tienes problemas, revisa la salida del compilador o abre un issue en el repositorio.

