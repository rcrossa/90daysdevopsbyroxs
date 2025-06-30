#!/bin/bash
 
# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color


# Función para mostrar redes disponibles
show_networks() {
    echo -e "${BLUE}Redes disponibles:${NC}"
    echo "===================="
    docker network ls --format "table {{.ID}}\t{{.Name}}\t{{.Driver}}\t{{.Scope}}"
    echo
}

# Función para verificar si una red existe
network_exists() {
    local network_name="$1"
    docker network ls --format "{{.Name}}" | grep -q "^${network_name}$"
}

# Función para verificar si la red tiene contenedores conectados
network_has_containers() {
    local network_name="$1"
    local containers=$(docker network inspect "$network_name" --format='{{range .Containers}}{{.Name}} {{end}}' 2>/dev/null)
    [ -n "$containers" ]
}

# Función para mostrar contenedores conectados a una red
show_connected_containers() {
    local network_name="$1"
    echo -e "${YELLOW}Contenedores conectados a la red '$network_name':${NC}"
    docker network inspect "$network_name" --format='{{range .Containers}}{{.Name}} {{end}}' 2>/dev/null | tr ' ' '\n' | grep -v '^$'
}


# Funcion para crear una red
create_network() {
    local network_name="$1"
    if docker network create "$network_name" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Red '$network_name' creada exitosamente.${NC}"
    else
        echo -e "${RED}❌ Error al crear la red '$network_name'.${NC}"
        exit 1
    fi
}

# Función principal
main() {
    echo -e "${BLUE}=== Administrador de redes docker ===${NC}"
    echo
    
    # Mostrar redes disponibles
    show_networks
    
    while true; do
        echo -e "${YELLOW}Seleccione una opción:${NC}"
        echo "1. Crear una nueva red"
        echo "2. Eliminar una red existente"
        echo "3. Salir"
        read -r option
        
        case "$option" in
            1)
                # Solicitar nombre de la nueva red
                echo -e "${YELLOW}Ingrese el nombre de la nueva red:${NC}"
                read -r network_name
                # Verificar si se ingresó un nombre
                if [ -z "$network_name" ]; then
                    echo -e "${RED}❌ Error: Debe ingresar un nombre para la red${NC}"
                    exit 1
                fi
                # Verificar si la red ya existe
                if network_exists "$network_name"; then
                    echo -e "${RED}❌ Error: La red '$network_name' ya existe${NC}"
                    exit 1
                fi
                # Crear la red
                echo -e "${BLUE}Creando la red '$network_name'...${NC}"
                create_network "$network_name"
                echo -e "${BLUE}Redes actuales:${NC}"
                show_networks
                ;;
            2)
                 # Solicitar nombre de la red a eliminar
                    echo -e "${YELLOW}Ingrese el nombre de la red a eliminar:${NC}"
                    read -r network_name
                    
                    # Verificar si se ingresó un nombre
                    if [ -z "$network_name" ]; then
                        echo -e "${RED}❌ Error: Debe ingresar un nombre de red${NC}"
                        exit 1
                    fi
                    
                    # Verificar si la red existe
                    if ! network_exists "$network_name"; then
                        echo -e "${RED}❌ Error: La red '$network_name' no existe${NC}"
                        exit 1
                    fi
                    
                    # Verificar si es una red del sistema (no se puede eliminar)
                    if [[ "$network_name" == "bridge" || "$network_name" == "host" || "$network_name" == "none" ]]; then
                        echo -e "${RED}❌ Error: No se puede eliminar la red del sistema '$network_name'${NC}"
                        exit 1
                    fi
                    
                    # Verificar si hay contenedores conectados
                    if network_has_containers "$network_name"; then
                        echo -e "${YELLOW}⚠️  Advertencia: La red '$network_name' tiene contenedores conectados${NC}"
                        show_connected_containers "$network_name"
                        echo
                        echo -e "${YELLOW}¿Desea desconectar los contenedores y eliminar la red? (y/N):${NC}"
                        read -r confirm
                        
                        if [[ "$confirm" =~ ^[Yy]$ ]]; then
                            # Desconectar contenedores
                            echo -e "${BLUE}Desconectando contenedores...${NC}"
                            docker network inspect "$network_name" --format='{{range .Containers}}{{.Name}} {{end}}' 2>/dev/null | tr ' ' '\n' | grep -v '^$' | while read -r container; do
                                echo "Desconectando $container de $network_name"
                                docker network disconnect "$network_name" "$container" 2>/dev/null || true
                            done
                        else
                            echo -e "${YELLOW}Operación cancelada${NC}"
                            exit 0
                        fi
                    fi
                    
                    # Eliminar la red
                    echo -e "${BLUE}Eliminando la red '$network_name'...${NC}"
                    
                    if docker network rm "$network_name" 2>/dev/null; then
                        echo -e "${GREEN}✅ La red '$network_name' ha sido eliminada exitosamente${NC}"
                        echo
                        echo -e "${BLUE}Redes restantes:${NC}"
                        show_networks
                    else
                        echo -e "${RED}❌ Error al eliminar la red '$network_name'${NC}"
                        exit 1
                    fi


                ;;
            3)
                echo -e "${GREEN}Saliendo...${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Opción no válida, intente de nuevo.${NC}"
                ;;
        esac
    done
}

# Ejecutar función principal
main "$@"


