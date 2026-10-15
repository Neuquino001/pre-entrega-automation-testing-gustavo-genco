"""Tests de Catálogo/Navegación para Saucedemo"""
import pytest
from utils import crear_driver, cerrar_driver
from utils.page_objects import PaginaLogin, PaginaInventario


@pytest.fixture(scope="function")
def driver():
    """Fixture que proporciona un driver limpio para cada test."""
    driver = crear_driver(navegador="chrome", headless=False)
    yield driver
    cerrar_driver()


@pytest.fixture(scope="function")
def pagina_inventario_logueada(driver):
    """Fixture que loguea y retorna la página de inventario."""
    pagina_login = PaginaLogin(driver)
    pagina_login.cargar()
    pagina_login.iniciar_sesion("standard_user", "secret_sauce")
    
    pagina_inventario = PaginaInventario(driver)
    assert pagina_inventario.esperar_carga_completa(), "Página de inventario no cargó"
    return pagina_inventario


class TestCatalogo:
    """Suite de tests para navegación y verificación del catálogo."""
    
    def test_titulo_pagina_inventario_correcto(self, pagina_inventario_logueada):
        """
        Test: Verificar que el título de la página de inventario sea correcto
        Criterio: Valida título
        """
        titulo = pagina_inventario_logueada.obtener_titulo()
        assert titulo == "Products", f"Título esperado 'Products', obtenido '{titulo}'"
    
    def test_hay_productos_visibles_en_pagina(self, pagina_inventario_logueada):
        """
        Test: Comprobar que existan productos visibles en la página
        Criterio: Valida presencia de productos
        """
        assert pagina_inventario_logueada.hay_productos_visibles(), "No hay productos visibles en la página"
        
        # Verificar al menos un producto
        productos = pagina_inventario_logueada.obtener_productos()
        assert len(productos) >= 1, f"Se esperaba al menos 1 producto, hay {len(productos)}"
    
    def test_elementos_ui_importantes_presentes(self, pagina_inventario_logueada):
        """
        Test: Validar que elementos importantes de la interfaz estén presentes
        Criterio: Menú hamburguesa, filtros, etc.
        """
        # Menú hamburguesa
        assert pagina_inventario_logueada.esta_menu_hamburguesa_visible(), "Menú hamburguesa no visible"
        
        # Filtro de ordenamiento
        assert pagina_inventario_logueada.esta_filtro_visible(), "Filtro de ordenamiento no visible"
        
        # Icono del carrito
        contador = pagina_inventario_logueada.obtener_contador_carrito()
        assert contador == 0, f"Contador del carrito debería ser 0 al inicio, es {contador}"
    
    def test_listar_nombre_y_precio_primer_producto(self, pagina_inventario_logueada):
        """
        Test: Listar nombre y precio del primer producto
        Criterio: Lista nombre/precio del primero
        """
        info_producto = pagina_inventario_logueada.obtener_info_primer_producto()
        
        # Verificar que tiene nombre y precio
        assert "nombre" in info_producto, "Producto sin nombre"
        assert "precio" in info_producto, "Producto sin precio"
        
        nombre = info_producto["nombre"]
        precio = info_producto["precio"]
        
        assert nombre.strip() != "", "Nombre del primer producto está vacío"
        assert precio.strip() != "", "Precio del primer producto está vacío"
        assert precio.startswith("$"), f"Precio no tiene formato esperado: {precio}"
        
        # Log para evidencia
        print(f"\n[EVIDENCIA] Primer producto: {nombre} - {precio}")
    
    def test_obtener_info_todos_los_productos(self, pagina_inventario_logueada):
        """
        Test adicional: Verificar información de todos los productos
        """
        productos = pagina_inventario_logueada.obtener_productos()
        assert len(productos) == 6, f"Se esperaban 6 productos, hay {len(productos)}"
        
        for i in range(len(productos)):
            info = pagina_inventario_logueada.obtener_info_producto(i)
            assert info["nombre"].strip() != "", f"Producto {i} sin nombre"
            assert info["precio"].startswith("$"), f"Producto {i} precio inválido: {info['precio']}"
            print(f"\n[EVIDENCIA] Producto {i+1}: {info['nombre']} - {info['precio']}")