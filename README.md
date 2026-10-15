# Pre-Entrega Automation Testing - Saucedemo

## Propósito del Proyecto
Automatización de pruebas funcionales para el sitio web [Saucedemo](https://www.saucedemo.com) utilizando Selenium WebDriver y Python. El proyecto valida los flujos principales: login, navegación del catálogo e interacción con el carrito de compras.

## Tecnologías Utilizadas
- **Python 3.8+**
- **Selenium WebDriver** - Automatización de navegador
- **Pytest** - Framework de testing
- **Webdriver Manager** - Gestión automática de drivers
- **Pytest-HTML** - Generación de reportes HTML
- **Git/GitHub** - Control de versiones

## Estructura del Proyecto
```
pre-entrega-automation-testing-gustavo-genco/
├── tests/              # Casos de prueba
│   ├── test_login.py
│   ├── test_catalog.py
│   └── test_cart.py
├── utils/              # Utilidades y helpers
│   ├── driver_factory.py
│   ├── wait_helpers.py
│   ├── screenshot_helper.py
│   └── page_objects/   # Page Object Model
│       ├── login_page.py
│       ├── inventory_page.py
│       └── cart_page.py
├── data/               # Datos de prueba (credenciales, etc.)
├── reports/            # Reportes HTML y capturas de pantalla
├── requirements.txt    # Dependencias
├── pytest.ini          # Configuración pytest
└── README.md           # Este archivo
```

## Instalación de Dependencias

```bash
# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución de Pruebas

```bash
# Ejecutar todas las pruebas con reporte HTML
pytest -v --html=reports/reporte.html

# Ejecutar pruebas específicas
pytest tests/test_login.py -v --html=reports/reporte.html
pytest tests/test_catalog.py -v
pytest tests/test_cart.py -v

# Ejecutar en modo headless (sin interfaz gráfica)
pytest -v --html=reports/reporte.html --headless
```

## Generar Reporte HTML
```bash
pytest -v --html=reports/reporte.html --self-contained-html
```
El reporte se generará en `reports/reporte.html`

## Evidencias
- **Reportes HTML**: Carpeta `reports/`
- **Capturas de pantalla en fallos**: Se generan automáticamente en `reports/screenshots/` cuando un test falla
- **Logs de ejecución**: Visibles en la consola y en el reporte HTML

## Casos de Prueba Implementados

### 1. Login (test_login.py)
- Navegación a saucedemo.com
- Ingreso de credenciales válidas (standard_user / secret_sauce)
- Validación de redirección a /inventory.html
- Verificación del título "Products"

### 2. Catálogo (test_catalog.py)
- Validación del título de la página "Products"
- Verificación de presencia de productos
- Validación de elementos UI: menú hamburguesa, filtro de ordenamiento
- Listado del nombre y precio del primer producto

### 3. Carrito (test_cart.py)
- Agregar primer producto al carrito
- Verificar incremento del contador del carrito (badge = 1)
- Navegar al carrito de compras
- Verificar que el producto aparece correctamente en el carrito

## Requisitos Previos
- Python 3.8 o superior instalado
- Google Chrome instalado (para ejecución local)
- Conexión a internet (para descargar ChromeDriver automáticamente)

## Autor
Gustavo Genco

## Licencia
Proyecto educativo - Curso de Testing Automatizado