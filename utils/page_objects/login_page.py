"""Page Object para la página de Login de Saucedemo"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from utils.wait_helpers import (
    esperar_visible,
    esperar_clickeable,
    esperar_y_enviar_teclas,
    esperar_y_click,
)


class PaginaLogin:
    """Page Object para la página de login."""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.url = "https://www.saucedemo.com"
        
        # Localizadores
        self.campo_usuario = (By.ID, "user-name")
        self.campo_contrasena = (By.ID, "password")
        self.boton_login = (By.ID, "login-button")
        self.mensaje_error = (By.CSS_SELECTOR, "[data-test='error']")
        self.logo = (By.CLASS_NAME, "login_logo")
    
    def cargar(self) -> None:
        """Navega a la página de login."""
        self.driver.get(self.url)
    
    def esta_cargada(self) -> bool:
        """Verifica si la página de login está cargada."""
        try:
            return esperar_visible(self.driver, self.boton_login).is_displayed()
        except:
            return False
    
    def iniciar_sesion(self, usuario: str, contrasena: str) -> None:
        """
        Realiza el login con credenciales dadas.
        
        Args:
            usuario: Nombre de usuario
            contrasena: Contraseña
        """
        esperar_y_enviar_teclas(self.driver, self.campo_usuario, usuario)
        esperar_y_enviar_teclas(self.driver, self.campo_contrasena, contrasena)
        esperar_y_click(self.driver, self.boton_login)
    
    def obtener_mensaje_error(self) -> str:
        """
        Obtiene el mensaje de error si hay uno visible.
        
        Returns:
            Texto del mensaje de error o cadena vacía
        """
        try:
            return esperar_visible(self.driver, self.mensaje_error).text
        except:
            return ""
    
    def hay_error_visible(self) -> bool:
        """Verifica si hay un mensaje de error visible."""
        try:
            return esperar_visible(self.driver, self.mensaje_error).is_displayed()
        except:
            return False