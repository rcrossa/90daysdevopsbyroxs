echo "=== Automatización de tareas con Bash ==="
echo "=== Día 10: Automatización de tareas con Bash ==="

cd "$dirname "$0" )"

# Verifica si docker esta corriendo
if ! docker info > /dev/null 2>&1; then
    echo "Docker no está corriendo. Por favor, inicia Docker y vuelve a intentarlo."
    exit 1
fi

# Verifica si el archivo docker-compose.yml existe
if [ ! -f "Dockercompose.yml" ]; then
    echo "❌ Error: No se encuentra el archivo Dockercompose.yml"
    exit 1
fi

# Crea la carpeta shared si no existe
if [ ! -d "shared" ]; then
    echo "Creando carpeta shared..."
    mkdir -p shared
fi

# Detener y limpiar contenedores existentes
echo "🧹 Limpiando contenedores existentes..."
docker-compose -f Dockercompose.yml down 2>/dev/null


# Iniciar el contenedor
echo "🚀 Iniciando el contenedor hora-container2..."
docker-compose -f Dockercompose.yml up -d


# Verificar si el contenedor está corriendo
if docker-compose -f Dockercompose.yml ps | grep -q "hora-container2"; then
    echo "✅ Contenedor iniciado correctamente"
    echo "📄 El archivo mensaje.txt se está creando en el contenedor"
    echo ""
    echo "Comandos útiles:"
    echo "  - Ver logs: docker-compose -f Dockercompose.yml logs -f hora-container2"
    echo "  - Copiar archivo: docker cp hora-container2:/mensaje.txt ./sharedrive/"
    echo "  - Detener: docker-compose -f Dockercompose.yml down"
    echo ""
    
    # Opcional: Esperar unos segundos y copiar el archivo
    echo "⏳ Esperando 10 segundos para que se genere contenido..."
    sleep 10
    
    echo "📋 Copiando archivo del contenedor al host..."
    docker cp hora-container2:/mensaje.txt ./sharedrive/mensaje.txt
    
    if [ -f "./sharedrive/mensaje.txt" ]; then
        echo "✅ Archivo copiado exitosamente a ./sharedrive/mensaje.txt"
        echo "📊 Últimas 5 líneas del archivo:"
        tail -5 ./sharedrive/mensaje.txt
    fi
else
    echo "❌ Error: El contenedor no se pudo iniciar"
    docker-compose -f Dockercompose.yml logs hora-container2
    exit 1
fi

echo ""
echo "🎉 Automatización completada"