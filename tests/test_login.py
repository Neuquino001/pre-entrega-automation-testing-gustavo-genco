"""Tests de Login para Saucedemo"""
import pytest
from utils import crear_driver, cerrar_driver, esperar_url_contiene, esperar_titulo_contiene
from utils.page_objects import PaginaLogin, PaginaInventario


@pytest.fixture(scope="function")
def driver():
    """Fixture que proporciona un driver limpio para cada test."""
    driver = crear_driver(navegador="chrome", headless=False)
    yield driver
    cerrar_driver()


@pytest.fixture(scope="function")
def pagina_login(driver):
    """Fixture que proporciona la página de login cargada."""
    pagina = PaginaLogin(driver)
    pagina.cargar()
    return pagina


@pytest.fixture(scope="function")
def pagina_inventario(driver):
    """Fixture que proporciona la página de inventario."""
    return PaginaInventario(driver)


class TestLogin:
    """Suite de tests para la funcionalidad de login."""
    
    USUARIO_VALIDO = "standard_user"
    CONTRASENA_VALIDA = "secret_sauce"
    
    def test_login_exitoso_redireccion_a_inventario(self, driver, pagina_login, pagina_inventario):
        """
        Test: Login con credenciales válidas redirige a /inventory.html
        Valida: URL contiene /inventory.html y título "Products"
        """
        # Act: Realizar login
        pagina_login.iniciar_sesion(self.USUARIO_VALIDO, self.CONTRASENA_VALIDA)
        
        # Assert: Validar redirección a inventario
        assert esperar_url_contiene(driver, "/inventory.html"), "No redirigió a /inventory.html"
        
        # Assert: Validar que la página de inventario está cargada
        assert pagina_inventario.esta_cargada(), "Página de inventario no cargada"
        
        # Assert: Validar título "Products"
        titulo = pagina_inventario.obtener_titulo()
        assert titulo == "Products", f"Título esperado 'Products', obtenido '{titulo}'"
    
    def test_login_exitoso_valida_titulo_swag_labs(self, driver, pagina_login):
        """
        Test: Login exitoso valida que el título contiene "Swag Labs"
        """
        pagina_login.iniciar_sesion(self.USUARIO_VALIDO, self.CONTRASENA_VALIDA)
        
        # Validar que el título de la página contiene "Swag Labs"
        assert esperar_titulo_contiene(driver, "Swag Labs"), "Título no contiene 'Swag Labs'"
    
    def test_login_pagina_inventario_cargada_correctamente(self, driver, pagina_login, pagina_inventario):
        """
        Test: Después del login, la página de inventario carga correctamente
        """
        pagina_login.iniciar_sesion(self.USUARIO_VALIDO, self.CONTRASENA_VALIDA)
        
        # Esperar carga completa
        assert pagina_inventario.esperar_carga_completa(), "Página no cargó completamente"
        
        # Verificar elementos clave presentes
        assert pagina_inventario.hay_productos_visibles(), "No hay productos visibles"
        assert pagina_inventario.esta_menu_hamburguesa_visible(), "Menú hamburguesa no visible"
        assert pagina_inventario.esta_filtro_visible(), "Filtro de ordenamiento no visible"