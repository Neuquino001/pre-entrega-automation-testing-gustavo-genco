"""Page Object para la página de Carrito de Saucedemo"""
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


class PaginaCarrito:
    """Page Object para la página del carrito de compras."""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/cart.html"
        
        # Localizadores
        self.titulo_pagina = (By.CLASS_NAME, "title")
        self.lista_items = (By.CLASS_NAME, "cart_list")
        self.item_carrito = (By.CLASS_NAME, "cart_item")
        self.nombre_producto = (By.CLASS_NAME, "inventory_item_name")
        self.precio_producto = (By.CLASS_NAME, "inventory_item_price")
        self.cantidad_producto = (By.CLASS_NAME, "cart_quantity")
        self.descripcion_producto = (By.CLASS_NAME, "inventory_item_desc")
        self.boton_quitar = (By.CSS_SELECTOR, ".cart_item button.cart_button")
        self.boton_continuar_comprando = (By.ID, "continue-shopping")
        self.boton_checkout = (By.ID, "checkout")
        self.boton_carrito = (By.CLASS_NAME, "shopping_cart_link")
        self.contador_carrito = (By.CLASS_NAME, "shopping_cart_badge")
    
    def esta_cargada(self) -> bool:
        """Verifica si la página del carrito está cargada."""
        try:
            return esperar_visible(self.driver, self.titulo_pagina).is_displayed()
        except:
            return False
    
    def esperar_carga_completa(self, tiempo: int = 10) -> bool:
        """
        Espera a que la página del carrito esté completamente cargada.
        
        Args:
            tiempo: Tiempo máximo de espera
        
        Returns:
            True si cargó correctamente
        """
        try:
            esperar_url_contiene(self.driver, "/cart.html", tiempo)
            return self.esta_cargada()
        except:
            return False
    
    def obtener_titulo(self) -> str:
        """Obtiene el título de la página."""
        return esperar_visible(self.driver, self.titulo_pagina).text
    
    def obtener_items(self) -> list:
        """
        Obtiene todos los items del carrito.
        
        Returns:
            Lista de WebElements de items en el carrito
        """
        return esperar_elementos(self.driver, self.item_carrito)
    
    def hay_items_en_carrito(self) -> bool:
        """Verifica si hay al menos un item en el carrito."""
        try:
            items = self.obtener_items()
            return len(items) > 0
        except:
            return False
    
    def obtener_cantidad_items(self) -> int:
        """
        Obtiene la cantidad de items distintos en el carrito.
        
        Returns:
            Número de items
        """
        return len(self.obtener_items())
    
    def obtener_info_items(self) -> list:
        """
        Obtiene información detallada de todos los items en el carrito.
        
        Returns:
            Lista de diccionarios con 'nombre', 'precio', 'cantidad', 'descripcion'
        """
        items = self.obtener_items()
        info_items = []
        for item in items:
            info_items.append({
                "nombre": item.find_element(*self.nombre_producto).text,
                "precio": item.find_element(*self.precio_producto).text,
                "cantidad": int(item.find_element(*self.cantidad_producto).text),
                "descripcion": item.find_element(*self.descripcion_producto).text
            })
        return info_items
    
    def esta_producto_en_carrito(self, nombre_producto: str) -> bool:
        """
        Verifica si un producto específico está en el carrito.
        
        Args:
            nombre_producto: Nombre exacto del producto a buscar
        
        Returns:
            True si el producto está en el carrito
        """
        items = self.obtener_items()
        for item in items:
            if item.find_element(*self.nombre_producto).text == nombre_producto:
                return True
        return False
    
    def obtener_info_producto(self, nombre_producto: str) -> dict:
        """
        Obtiene información de un producto específico en el carrito.
        
        Args:
            nombre_producto: Nombre exacto del producto
        
        Returns:
            Diccionario con info del producto
        
        Raises:
            ValueError: Si el producto no está en el carrito
        """
        items = self.obtener_items()
        for item in items:
            if item.find_element(*self.nombre_producto).text == nombre_producto:
                return {
                    "nombre": item.find_element(*self.nombre_producto).text,
                    "precio": item.find_element(*self.precio_producto).text,
                    "cantidad": int(item.find_element(*self.cantidad_producto).text),
                    "descripcion": item.find_element(*self.descripcion_producto).text
                }
        raise ValueError(f"Producto '{nombre_producto}' no encontrado en el carrito")
    
    def quitar_producto(self, nombre_producto: str) -> None:
        """
        Quita un producto del carrito.
        
        Args:
            nombre_producto: Nombre del producto a quitar
        """
        items = self.obtener_items()
        for item in items:
            if item.find_element(*self.nombre_producto).text == nombre_producto:
                boton_quitar = item.find_element(*self.boton_quitar)
                boton_quitar.click()
                return
        raise ValueError(f"Producto '{nombre_producto}' no encontrado en el carrito")
    
    def continuar_comprando(self) -> None:
        """Hace click en 'Continue Shopping' y vuelve al inventario."""
        boton = self.driver.find_element(*self.boton_continuar_comprando)
        self.driver.execute_script("arguments[0].click();", boton)
        import time
        time.sleep(1)
    
    def ir_a_checkout(self) -> None:
        """Hace click en 'Checkout' para ir al proceso de pago."""
        esperar_y_click(self.driver, self.boton_checkout)
    
    def obtener_contador_carrito(self) -> int:
        """
        Obtiene el contador del carrito (badge en el icono).
        
        Returns:
            Cantidad total de items (suma de cantidades)
        """
        try:
            contador = esperar_visible(self.driver, self.contador_carrito)
            return int(contador.text)
        except:
            return 0
    
    def calcular_total_items(self) -> int:
        """
        Calcula el total de items sumando las cantidades.
        
        Returns:
            Suma de cantidades de todos los items
        """
        items_info = self.obtener_info_items()
        return sum(item["cantidad"] for item in items_info)