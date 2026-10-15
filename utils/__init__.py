"""Utilidades core del proyecto"""
from utils.driver_factory import crear_driver, obtener_driver, cerrar_driver
from utils.wait_helpers import (
    esperar_elemento,
    esperar_elementos,
    esperar_clickeable,
    esperar_visible,
    esperar_url_contiene,
    esperar_titulo_contiene,
    esperar_invisibilidad,
    esperar_alerta_presente,
    esperar_y_obtener_texto,
    esperar_y_click,
    esperar_y_enviar_teclas,
)
from utils.screenshot_helper import (
    capturar_pantalla,
    capturar_pantalla_fallo,
    pytest_runtest_makereport,
    adjuntar_captura_al_reporte,
)
from utils.page_objects import PaginaLogin, PaginaInventario, PaginaCarrito

__all__ = [
    "crear_driver",
    "obtener_driver",
    "cerrar_driver",
    "esperar_elemento",
    "esperar_elementos",
    "esperar_clickeable",
    "esperar_visible",
    "esperar_url_contiene",
    "esperar_titulo_contiene",
    "esperar_invisibilidad",
    "esperar_alerta_presente",
    "esperar_y_obtener_texto",
    "esperar_y_click",
    "esperar_y_enviar_teclas",
    "capturar_pantalla",
    "capturar_pantalla_fallo",
    "pytest_runtest_makereport",
    "adjuntar_captura_al_reporte",
    "PaginaLogin",
    "PaginaInventario",
    "PaginaCarrito",
]