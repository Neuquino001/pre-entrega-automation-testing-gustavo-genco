"""Helpers de esperas explícitas reutilizables"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from typing import Tuple, Union, Optional

Localizador = Tuple[str, str]


def esperar_elemento(
    driver: WebDriver,
    localizador: Localizador,
    tiempo: int = 10
) -> WebElement:
    """
    Espera a que un elemento esté presente en el DOM.
    
    Args:
        driver: Instancia de WebDriver
        localizador: Tupla (By.TIPO, "valor")
        tiempo: Tiempo máximo de espera en segundos
    
    Returns:
        WebElement encontrado
    
    Raises:
        TimeoutException: Si el elemento no aparece en el tiempo especificado
    """
    wait = WebDriverWait(driver, tiempo)
    return wait.until(EC.presence_of_element_located(localizador))


def esperar_elementos(
    driver: WebDriver,
    localizador: Localizador,
    tiempo: int = 10
) -> list:
    """
    Espera a que al menos un elemento esté presente en el DOM.
    
    Args:
        driver: Instancia de WebDriver
        localizador: Tupla (By.TIPO, "valor")
        tiempo: Tiempo máximo de espera en segundos
    
    Returns:
        Lista de WebElements encontrados
    """
    wait = WebDriverWait(driver, tiempo)
    return wait.until(EC.presence_of_all_elements_located(localizador))


def esperar_clickeable(
    driver: WebDriver,
    localizador: Localizador,
    tiempo: int = 10
) -> WebElement:
    """
    Espera a que un elemento sea clickeable.
    
    Args:
        driver: Instancia de WebDriver
        localizador: Tupla (By.TIPO, "valor")
        tiempo: Tiempo máximo de espera en segundos
    
    Returns:
        WebElement clickeable
    """
    wait = WebDriverWait(driver, tiempo)
    return wait.until(EC.element_to_be_clickable(localizador))


def esperar_visible(
    driver: WebDriver,
    localizador: Localizador,
    tiempo: int = 10
) -> WebElement:
    """
    Espera a que un elemento sea visible.
    
    Args:
        driver: Instancia de WebDriver
        localizador: Tupla (By.TIPO, "valor")
        tiempo: Tiempo máximo de espera en segundos
    
    Returns:
        WebElement visible
    """
    wait = WebDriverWait(driver, tiempo)
    return wait.until(EC.visibility_of_element_located(localizador))


def esperar_url_contiene(
    driver: WebDriver,
    texto_url: str,
    tiempo: int = 10
) -> bool:
    """
    Espera a que la URL actual contenga el texto especificado.
    
    Args:
        driver: Instancia de WebDriver
        texto_url: Texto que debe contener la URL
        tiempo: Tiempo máximo de espera en segundos
    
    Returns:
        True si la URL contiene el texto
    """
    wait = WebDriverWait(driver, tiempo)
    return wait.until(EC.url_contains(texto_url))


def esperar_titulo_contiene(
    driver: WebDriver,
    texto_titulo: str,
    tiempo: int = 10
) -> bool:
    """
    Espera a que el título de la página contenga el texto especificado.
    
    Args:
        driver: Instancia de WebDriver
        texto_titulo: Texto que debe contener el título
        tiempo: Tiempo máximo de espera en segundos
    
    Returns:
        True si el título contiene el texto
    """
    wait = WebDriverWait(driver, tiempo)
    return wait.until(EC.title_contains(texto_titulo))


def esperar_invisibilidad(
    driver: WebDriver,
    localizador: Localizador,
    tiempo: int = 10
) -> bool:
    """
    Espera a que un elemento sea invisible o no esté en el DOM.
    
    Args:
        driver: Instancia de WebDriver
        localizador: Tupla (By.TIPO, "valor")
        tiempo: Tiempo máximo de espera en segundos
    
    Returns:
        True si el elemento es invisible
    """
    wait = WebDriverWait(driver, tiempo)
    return wait.until(EC.invisibility_of_element_located(localizador))


def esperar_alerta_presente(driver: WebDriver, tiempo: int = 10):
    """
    Espera a que una alerta esté presente.
    
    Args:
        driver: Instancia de WebDriver
        tiempo: Tiempo máximo de espera en segundos
    
    Returns:
        Objeto Alert
    """
    wait = WebDriverWait(driver, tiempo)
    return wait.until(EC.alert_is_present())


def esperar_y_obtener_texto(
    driver: WebDriver,
    localizador: Localizador,
    tiempo: int = 10
) -> str:
    """
    Espera a que un elemento sea visible y retorna su texto.
    
    Args:
        driver: Instancia de WebDriver
        localizador: Tupla (By.TIPO, "valor")
        tiempo: Tiempo máximo de espera en segundos
    
    Returns:
        Texto del elemento
    """
    elemento = esperar_visible(driver, localizador, tiempo)
    return elemento.text


def esperar_y_click(
    driver: WebDriver,
    localizador: Localizador,
    tiempo: int = 10
) -> None:
    """
    Espera a que un elemento sea clickeable y hace click.
    
    Args:
        driver: Instancia de WebDriver
        localizador: Tupla (By.TIPO, "valor")
        tiempo: Tiempo máximo de espera en segundos
    """
    elemento = esperar_clickeable(driver, localizador, tiempo)
    elemento.click()


def esperar_y_enviar_teclas(
    driver: WebDriver,
    localizador: Localizador,
    texto: str,
    tiempo: int = 10,
    limpiar_primero: bool = True
) -> None:
    """
    Espera a que un elemento sea visible y envía teclas.
    
    Args:
        driver: Instancia de WebDriver
        localizador: Tupla (By.TIPO, "valor")
        texto: Texto a enviar
        tiempo: Tiempo máximo de espera en segundos
        limpiar_primero: Si True, limpia el campo antes de enviar
    """
    elemento = esperar_visible(driver, localizador, tiempo)
    if limpiar_primero:
        elemento.clear()
    elemento.send_keys(texto)