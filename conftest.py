"""Configuración global de pytest - Registra hooks y fixtures compartidos"""
import os
import pytest
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver

# Importar utilidades
from utils.driver_factory import crear_driver, cerrar_driver
from utils.screenshot_helper import capturar_pantalla_fallo

# Directorio de capturas
RUTA_CAPTURAS = os.path.join(os.path.dirname(__file__), "reports", "screenshots")


def _asegurar_directorio_capturas():
    """Crea el directorio de capturas si no existe."""
    os.makedirs(RUTA_CAPTURAS, exist_ok=True)


@pytest.fixture(scope="function")
def driver():
    """Fixture global que proporciona un driver limpio para cada test."""
    driver = crear_driver(navegador="chrome", headless=False)
    yield driver
    cerrar_driver()


def pytest_runtest_makereport(item, call):
    """
    Hook de pytest para capturar pantalla automáticamente en fallos.
    
    Se ejecuta después de cada fase (setup, call, teardown).
    Si la fase 'call' falla, captura la pantalla.
    """
    if call.when == "call" and call.excinfo is not None:
        # Obtener driver del fixture si existe
        driver = None
        if hasattr(item, "funcargs") and "driver" in item.funcargs:
            driver = item.funcargs["driver"]
        elif hasattr(item, "_request") and hasattr(item._request, "getfixturevalue"):
            try:
                driver = item._request.getfixturevalue("driver")
            except Exception:
                pass
        
        if driver:
            nombre_test = item.name
            _asegurar_directorio_capturas()
            ruta = capturar_pantalla_fallo(driver, nombre_test)
            print(f"\n[Captura de fallo guardada: {ruta}]")