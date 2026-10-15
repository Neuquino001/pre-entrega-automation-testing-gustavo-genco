"""Page Object para la página de Inventario (Productos) de Saucedemo"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from utils.wait_helpers import (
    esperar_visible,
    esperar_clickeable,
    esperar_elemento,
    esperar_elementos,
    esperar_url_contiene,
    esperar_y_click,
)


class PaginaInventario:
    """Page Object para la página de inventario/productos."""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/inventory.html"
        
        # Localizadores
        self.titulo_pagina = (By.CLASS_NAME, "title")
        self.contenedor_productos = (By.CLASS_NAME, "inventory_list")
        self.item_producto = (By.CLASS_NAME, "inventory_item")
        self.nombre_producto = (By.CLASS_NAME, "inventory_item_name")
        self.precio_producto = (By.CLASS_NAME, "inventory_item_price")
        self.descripcion_producto = (By.CLASS_NAME, "inventory_item_desc")
        self.boton_agregar_carrito = (By.CSS_SELECTOR, ".inventory_item button.btn_inventory")
        self.boton_carrito = (By.CLASS_NAME, "shopping_cart_link")
        self.contador_carrito = (By.CLASS_NAME, "shopping_cart_badge")
        self.menu_hamburguesa = (By.ID, "react-burger-menu-btn")
        self.filtro_orden = (By.CLASS_NAME, "product_sort_container")
        self.opciones_filtro = (By.CSS_SELECTOR, ".product_sort_container option")
    
    def esta_cargada(self) -> bool:
        """Verifica si la página de inventario está cargada."""
        try:
            return esperar_visible(self.driver, self.titulo_pagina).is_displayed()
        except:
            return False
    
    def esperar_carga_completa(self, tiempo: int = 10) -> bool:
        """
        Espera a que la página esté completamente cargada.
        
        Args:
            tiempo: Tiempo máximo de espera
        
        Returns:
            True si cargó correctamente
        """
        try:
            esperar_url_contiene(self.driver, "/inventory.html", tiempo)
            return self.esta_cargada()
        except:
            return False
    
    def obtener_titulo(self) -> str:
        """
        Obtiene el título de la página.
        
        Returns:
            Texto del título
        """
        return esperar_visible(self.driver, self.titulo_pagina).text
    
    def obtener_productos(self) -> list:
        """
        Obtiene todos los elementos de producto visibles.
        
        Returns:
            Lista de WebElements de productos
        """
        return esperar_elementos(self.driver, self.item_producto)
    
    def hay_productos_visibles(self) -> bool:
        """Verifica si hay al menos un producto visible."""
        try:
            productos = self.obtener_productos()
            return len(productos) > 0
        except:
            return False
    
    def obtener_primer_producto(self) -> WebElement:
        """
        Obtiene el primer producto de la lista.
        
        Returns:
            WebElement del primer producto
        """
        productos = self.obtener_productos()
        if productos:
            return productos[0]
        raise Exception("No hay productos en la página")
    
    def obtener_info_primer_producto(self) -> dict:
        """
        Obtiene nombre y precio del primer producto.
        
        Returns:
            Diccionario con 'nombre' y 'precio'
        """
        primer_producto = self.obtener_primer_producto()
        nombre = primer_producto.find_element(*self.nombre_producto).text
        precio = primer_producto.find_element(*self.precio_producto).text
        return {"nombre": nombre, "precio": precio}
    
    def obtener_info_producto(self, indice: int) -> dict:
        """
        Obtiene información de un producto por índice.
        
        Args:
            indice: Índice del producto (0-based)
        
        Returns:
            Diccionario con 'nombre', 'precio', 'descripcion'
        """
        productos = self.obtener_productos()
        if 0 <= indice < len(productos):
            producto = productos[indice]
            return {
                "nombre": producto.find_element(*self.nombre_producto).text,
                "precio": producto.find_element(*self.precio_producto).text,
                "descripcion": producto.find_element(*self.descripcion_producto).text
            }
        raise IndexError(f"Índice {indice} fuera de rango. Total productos: {len(productos)}")
    
    def agregar_primero_al_carrito(self) -> None:
        """Agrega el primer producto al carrito."""
        primer_producto = self.obtener_primer_producto()
        boton = primer_producto.find_element(*self.boton_agregar_carrito)
        boton.click()
    
    def agregar_producto_al_carrito(self, indice: int) -> None:
        """
        Agrega un producto al carrito por índice.
        
        Args:
            indice: Índice del producto (0-based)
        """
        productos = self.obtener_productos()
        if 0 <= indice < len(productos):
            boton = productos[indice].find_element(*self.boton_agregar_carrito)
            boton.click()
        else:
            raise IndexError(f"Índice {indice} fuera de rango")
    
    def ir_al_carrito(self) -> None:
        """Navega a la página del carrito."""
        esperar_y_click(self.driver, self.boton_carrito)
    
    def obtener_contador_carrito(self) -> int:
        """
        Obtiene el número de items en el carrito (badge).
        
        Returns:
            Cantidad de items (0 si no hay badge visible)
        """
        try:
            contador = esperar_visible(self.driver, self.contador_carrito)
            return int(contador.text)
        except:
            return 0
    
    def esta_menu_hamburguesa_visible(self) -> bool:
        """Verifica si el menú hamburguesa está visible."""
        try:
            return esperar_visible(self.driver, self.menu_hamburguesa).is_displayed()
        except:
            return False
    
    def esta_filtro_visible(self) -> bool:
        """Verifica si el filtro de ordenamiento está visible."""
        try:
            return esperar_visible(self.driver, self.filtro_orden).is_displayed()
        except:
            return False
    
    def seleccionar_filtro(self, valor: str) -> None:
        """
        Selecciona una opción en el filtro de ordenamiento.
        
        Args:
            valor: Valor de la opción (ej: "az", "za", "lohi", "hilo")
        """
        from selenium.webdriver.support.ui import Select
        filtro = esperar_visible(self.driver, self.filtro_orden)
        Select(filtro).select_by_value(valor)
    
    def obtener_opciones_filtro(self) -> list:
        """
        Obtiene las opciones disponibles del filtro.
        
        Returns:
            Lista de valores de las opciones
        """
        opciones = esperar_elementos(self.driver, self.opciones_filtro)
        return [op.get_attribute("value") for op in opciones]