#!/bin/bash
# Script para intentar compilar SoftPack en macOS
# NOTA: Esto creará un ejecutable de macOS, NO un .exe de Windows

echo "════════════════════════════════════════════════════════════"
echo "  SoftPack - Compilador para macOS"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "⚠️  ADVERTENCIA IMPORTANTE:"
echo "   • Este script funciona en macOS"
echo "   • Creará un ejecutable de macOS, NO un .exe de Windows"
echo "   • Para crear un .exe de Windows, necesitas ejecutar en Windows"
echo ""
echo "El ejecutable de macOS:"
echo "  ✓ Funcionará en macOS"
echo "  ✗ NO funcionará en Windows"
echo "  ✗ NO instalará software de Windows"
echo ""
read -p "¿Deseas continuar de todas formas? (s/n): " respuesta

if [ "$respuesta" != "s" ]; then
    echo "❌ Cancelado"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  Instalando PyInstaller..."
echo "════════════════════════════════════════════════════════════"

python3 -m pip install --quiet pyinstaller

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  Compilando SoftPack (Demo para macOS)..."
echo "════════════════════════════════════════════════════════════"
echo ""
echo "⏳ Este proceso puede tomar 2-3 minutos..."
echo ""

# Limpiar builds anteriores
rm -rf build dist SoftPack.spec 2>/dev/null

# Compilar demo de macOS (no el programa principal)
pyinstaller --name=SoftPack_Demo_macOS \
    --onefile \
    --windowed \
    --clean \
    demo_macos.py

echo ""
if [ -f "dist/SoftPack_Demo_macOS" ]; then
    echo "════════════════════════════════════════════════════════════"
    echo "  ✅ COMPILACIÓN EXITOSA"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "📦 Ejecutable creado:"
    echo "   dist/SoftPack_Demo_macOS"
    echo ""
    echo "🎯 Uso:"
    echo "   cd dist"
    echo "   ./SoftPack_Demo_macOS"
    echo ""
    echo "⚠️  Recuerda:"
    echo "   • Esto es solo una DEMO visual"
    echo "   • NO instala software de Windows"
    echo "   • Para funcionalidad completa, usa Windows"
    echo ""
    
    # Dar permisos de ejecución
    chmod +x dist/SoftPack_Demo_macOS
    
    # Limpiar archivos temporales
    echo "🧹 Limpiando archivos temporales..."
    rm -rf build SoftPack_Demo_macOS.spec
    
    echo ""
    echo "✨ ¡Completado!"
    echo ""
else
    echo "════════════════════════════════════════════════════════════"
    echo "  ❌ ERROR EN LA COMPILACIÓN"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "Revisa los mensajes de error arriba"
    exit 1
fi

