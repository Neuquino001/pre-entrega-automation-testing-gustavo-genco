"""Fábrica de WebDriver para Selenium"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


_driver = None


def crear_driver(navegador="chrome", headless=False, tamano_ventana=(1920, 1080)):
    """
    Crea y configura una instancia de WebDriver.
    
    Args:
        navegador: "chrome" o "firefox"
        headless: True para modo sin interfaz gráfica
        tamano_ventana: Tupla (ancho, alto) de la ventana
    
    Returns:
        Instancia de WebDriver configurada
    """
    global _driver
    
    if navegador.lower() == "chrome":
        opciones = ChromeOptions()
        if headless:
            opciones.add_argument("--headless=new")
        opciones.add_argument(f"--window-size={tamano_ventana[0]},{tamano_ventana[1]}")
        opciones.add_argument("--no-sandbox")
        opciones.add_argument("--disable-dev-shm-usage")
        opciones.add_argument("--disable-gpu")
        opciones.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        servicio = ChromeService(ChromeDriverManager().install())
        _driver = webdriver.Chrome(service=servicio, options=opciones)
        
    elif navegador.lower() == "firefox":
        opciones = FirefoxOptions()
        if headless:
            opciones.add_argument("--headless")
        opciones.add_argument(f"--width={tamano_ventana[0]}")
        opciones.add_argument(f"--height={tamano_ventana[1]}")
        
        servicio = FirefoxService(GeckoDriverManager().install())
        _driver = webdriver.Firefox(service=servicio, options=opciones)
        
    else:
        raise ValueError(f"Navegador no soportado: {navegador}")
    
    _driver.implicitly_wait(5)
    return _driver


def obtener_driver():
    """Retorna la instancia actual del driver o None si no existe."""
    return _driver


def cerrar_driver():
    """Cierra el driver y limpia la referencia global."""
    global _driver
    if _driver:
        _driver.quit()
        _driver = None