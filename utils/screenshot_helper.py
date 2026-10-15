"""Helper para capturas de pantalla automáticas en fallos"""
import os
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver


RUTA_CAPTURAS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")


def _asegurar_directorio_capturas():
    """Crea el directorio de capturas si no existe."""
    os.makedirs(RUTA_CAPTURAS, exist_ok=True)


def capturar_pantalla(driver: WebDriver, nombre_archivo: str) -> str:
    """
    Captura una pantalla y la guarda en reports/screenshots/.
    
    Args:
        driver: Instancia de WebDriver
        nombre_archivo: Nombre base del archivo (sin extensión)
    
    Returns:
        Ruta completa del archivo guardado
    """
    _asegurar_directorio_capturas()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_completo = f"{nombre_archivo}_{timestamp}.png"
    ruta_completa = os.path.join(RUTA_CAPTURAS, nombre_completo)
    
    driver.save_screenshot(ruta_completa)
    return ruta_completa


def capturar_pantalla_fallo(driver: WebDriver, nombre_test: str) -> str:
    """
    Captura pantalla específicamente para fallos de test.
    
    Args:
        driver: Instancia de WebDriver
        nombre_test: Nombre del test que falló
    
    Returns:
        Ruta completa del archivo guardado
    """
    return capturar_pantalla(driver, f"FALLO_{nombre_test}")


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
            except:
                pass
        
        if driver:
            nombre_test = item.name
            ruta = capturar_pantalla_fallo(driver, nombre_test)
            print(f"\n[Captura de fallo guardada: {ruta}]")


def adjuntar_captura_al_reporte(driver: WebDriver, nombre_test: str, reporte_html=None) -> str:
    """
    Captura pantalla y opcionalmente la adjunta al reporte HTML.
    
    Args:
        driver: Instancia de WebDriver
        nombre_test: Nombre del test
        reporte_html: Objeto de reporte HTML (opcional)
    
    Returns:
        Ruta de la captura
    """
    ruta = capturar_pantalla_fallo(driver, nombre_test)
    
    if reporte_html and hasattr(reporte_html, "extra"):
        import base64
        with open(ruta, "rb") as f:
            imagen_b64 = base64.b64encode(f.read()).decode()
        reporte_html.extra.append(
            f'<div><img src="data:image/png;base64,{imagen_b64}" style="max-width: 600px;"></div>'
        )
    
    return ruta