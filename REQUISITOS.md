# Requisitos del Proyecto - Pre-Entrega Automation Testing

## Objetivo
Automatizar flujos básicos de navegación web en [Saucedemo](https://www.saucedemo.com) utilizando Selenium WebDriver y Python, aplicando conocimientos hasta la Clase 8.

## Tecnologías Requeridas
- **Python** como lenguaje principal
- **Pytest** para estructura de testing
- **Selenium WebDriver** para automatización
- **Git y GitHub** para control de versiones

## Estructura del Proyecto
- Mínimo 2 archivos separados (tests y funciones auxiliares)
- Comentarios descriptivos y nomenclatura significativa
- Organización en carpetas: `tests/`, `utils/`, `data/`, `reports/`

## Casos de Prueba Obligatorios

### 1. Automatización de Login
- Navegar a la página de login de saucedemo.com
- Ingresar credenciales válidas:
  - Usuario: `standard_user`
  - Contraseña: `secret_sauce`
- Validar login exitoso verificando redirección a `/inventory.html`
- **Criterios mínimos**: Espera explícita + validación de `/inventory.html` y título "Products/Swag Labs"

### 2. Navegación y Verificación del Catálogo (Clases 6 a 8)
- Verificar que el título de la página de inventario sea correcto
- Comprobar que existan productos visibles (al menos uno)
- Validar elementos importantes de la UI: menú hamburguesa, filtros de ordenamiento
- **Criterios mínimos**: Validar título + presencia de productos + listar nombre/precio del primero

### 3. Interacción con Productos - Carrito (Clase 8)
- Añadir un producto al carrito (clic en botón "Add to cart")
- Verificar que el contador del carrito se incremente correctamente
- Navegar al carrito de compras
- Comprobar que el producto añadido aparezca correctamente en el carrito
- **Criterios mínimos**: Agregar primer producto + verificar ítem en carrito

## Entregables

### Repositorio GitHub Público
- Nombre: `pre-entrega-automation-testing-[nombre-apellido]`
- Commits frecuentes con mensajes descriptivos
- Estructura mínima:
  ```
  tests/
  utils/ (funciones auxiliares)
  data/ (si aplica datos externos)
  reports/ (reportes HTML y capturas)
  ```

### README.md
Debe incluir:
- Propósito del proyecto
- Tecnologías utilizadas
- Instrucciones de instalación de dependencias
- Comando para ejecutar las pruebas (ej: `pytest -v --html=reporte.html`)

### Reporte HTML
Generar con: `pytest tests/ -v --html=reports/reporte.html`

### Evidencias Adicionales
- Capturas de pantalla automáticas en caso de fallos
- Logs de ejecución

## Funcionalidad Esperada
- Tests ejecutándose correctamente en saucedemo.com
- Validaciones claras y específicas por paso
- Código legible y bien organizado
- Tests independientes entre sí (falla de uno no afecta a otros)

## Fecha de Entrega
7 días a partir de la Clase 8