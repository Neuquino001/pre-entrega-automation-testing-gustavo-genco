"""Tests de Carrito para Saucedemo"""
import pytest
from utils import crear_driver, cerrar_driver
from utils.page_objects import PaginaLogin, PaginaInventario, PaginaCarrito


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


@pytest.fixture(scope="function")
def pagina_carrito(driver):
    """Fixture que proporciona la página de carrito."""
    return PaginaCarrito(driver)


class TestCarrito:
    """Suite de tests para interacción con el carrito."""
    
    def test_agregar_primer_producto_incrementa_contador(self, pagina_inventario_logueada):
        """
        Test: Añadir un producto al carrito y verificar que el contador se incremente
        Criterio: Agrega primer producto + Verifica ítem en carrito
        """
        # Obtener info del primer producto antes de agregar
        info_producto = pagina_inventario_logueada.obtener_info_primer_producto()
        nombre_producto = info_producto["nombre"]
        
        # Contador inicial debe ser 0
        contador_inicial = pagina_inventario_logueada.obtener_contador_carrito()
        assert contador_inicial == 0, f"Contador inicial debería ser 0, es {contador_inicial}"
        
        # Act: Agregar primer producto al carrito
        pagina_inventario_logueada.agregar_primero_al_carrito()
        
        # Assert: Verificar que el contador se incrementó a 1
        contador_despues = pagina_inventario_logueada.obtener_contador_carrito()
        assert contador_despues == 1, f"Contador debería ser 1 después de agregar, es {contador_despues}"
        
        print(f"\n[EVIDENCIA] Producto agregado: {nombre_producto} - Contador: {contador_despues}")
    
    def test_navegar_al_carrito_y_verificar_producto(self, driver, pagina_inventario_logueada, pagina_carrito):
        """
        Test: Navegar al carrito y comprobar que el producto añadido aparezca correctamente
        Criterio: Verifica ítem en carrito
        """
        # Obtener info del primer producto
        info_producto = pagina_inventario_logueada.obtener_info_primer_producto()
        nombre_producto = info_producto["nombre"]
        precio_esperado = info_producto["precio"]
        
        # Agregar al carrito
        pagina_inventario_logueada.agregar_primero_al_carrito()
        
        # Navegar al carrito
        pagina_inventario_logueada.ir_al_carrito()
        
        # Verificar que la página de carrito cargó
        assert pagina_carrito.esperar_carga_completa(), "Página de carrito no cargó"
        assert pagina_carrito.obtener_titulo() == "Your Cart", "Título de carrito incorrecto"
        
        # Assert: Verificar que el producto está en el carrito
        assert pagina_carrito.esta_producto_en_carrito(nombre_producto), \
            f"Producto '{nombre_producto}' no encontrado en el carrito"
        
        # Assert: Verificar detalles del producto en el carrito
        info_en_carrito = pagina_carrito.obtener_info_producto(nombre_producto)
        assert info_en_carrito["nombre"] == nombre_producto, "Nombre no coincide"
        assert info_en_carrito["precio"] == precio_esperado, f"Precio no coincide: esperado {precio_esperado}, obtenido {info_en_carrito['precio']}"
        assert info_en_carrito["cantidad"] == 1, f"Cantidad debería ser 1, es {info_en_carrito['cantidad']}"
        
        # Assert: Verificar contador del carrito (badge)
        contador_badge = pagina_carrito.obtener_contador_carrito()
        assert contador_badge == 1, f"Badge del carrito debería ser 1, es {contador_badge}"
        
        print(f"\n[EVIDENCIA] Producto en carrito: {info_en_carrito['nombre']} - {info_en_carrito['precio']} x{info_en_carrito['cantidad']}")
    
    def test_flujo_completo_agregar_verificar_carrito(self, driver, pagina_inventario_logueada, pagina_carrito):
        """
        Test: Flujo completo - Agregar, ir al carrito, verificar, volver, verificar contador
        """
        # 1. Obtener info del primer producto
        info_producto = pagina_inventario_logueada.obtener_info_primer_producto()
        nombre_producto = info_producto["nombre"]
        
        # 2. Agregar al carrito desde inventario
        pagina_inventario_logueada.agregar_primero_al_carrito()
        assert pagina_inventario_logueada.obtener_contador_carrito() == 1
        
        # 3. Ir al carrito
        pagina_inventario_logueada.ir_al_carrito()
        assert pagina_carrito.esperar_carga_completa()
        
        # 4. Verificar producto en carrito
        assert pagina_carrito.esta_producto_en_carrito(nombre_producto)
        info_carrito = pagina_carrito.obtener_info_producto(nombre_producto)
        assert info_carrito["cantidad"] == 1
        
        # 5. Volver a inventario (Continue Shopping)
        pagina_carrito.continuar_comprando()
        assert pagina_inventario_logueada.esperar_carga_completa()
        
        # 6. Verificar que el contador persiste
        assert pagina_inventario_logueada.obtener_contador_carrito() == 1
        
        print(f"\n[EVIDENCIA] Flujo completo verificado para: {nombre_producto}")
    
    def test_agregar_multiples_productos_contador_acumula(self, pagina_inventario_logueada, pagina_carrito):
        """
        Test adicional: Agregar múltiples productos y verificar contador
        """
        # Agregar primer producto
        pagina_inventario_logueada.agregar_producto_al_carrito(0)
        assert pagina_inventario_logueada.obtener_contador_carrito() == 1
        
        # Agregar segundo producto
        pagina_inventario_logueada.agregar_producto_al_carrito(1)
        assert pagina_inventario_logueada.obtener_contador_carrito() == 2
        
        # Ir al carrito y verificar ambos
        pagina_inventario_logueada.ir_al_carrito()
        assert pagina_carrito.esperar_carga_completa()
        
        items = pagina_carrito.obtener_info_items()
        assert len(items) == 2, f"Deberían haber 2 items distintos, hay {len(items)}"
        assert pagina_carrito.calcular_total_items() == 2, "Total de items debería ser 2"
        
        print(f"\n[EVIDENCIA] Múltiples productos agregados. Total items: {pagina_carrito.calcular_total_items()}")