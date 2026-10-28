"""Paso 1: PDF -> data/texto/*.txt (con OCR). Luego REVISE y corrija los .txt a mano."""
import argparse
import _ruta  # noqa: F401
from asistente.configuracion import cargar
from asistente.ingesta.extraccion import extraer_carpeta

p = argparse.ArgumentParser()
p.add_argument("--sobrescribir", action="store_true", help="re-extrae aunque exista el .txt")
a = p.parse_args()
cfg = cargar()
extraer_carpeta(cfg["rutas"]["pdf"], cfg["rutas"]["texto"], cfg["ocr"], a.sobrescribir)
