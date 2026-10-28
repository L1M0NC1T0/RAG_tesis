"""Fase 1a: PDF (nativo o escaneado) -> texto revisable a mano.

Cada PDF genera data/texto/<nombre>.txt con marcadores de página. Ese
archivo es el que se revisa y corrige manualmente antes de indexar.
"""
from pathlib import Path
import io

import fitz  # PyMuPDF
import pytesseract
from PIL import Image

MARCA_PAGINA = "=== Página {} ==="


def _ocr(pagina, dpi: int, idioma: str) -> str:
    imagen = Image.open(io.BytesIO(pagina.get_pixmap(dpi=dpi).tobytes("png")))
    return pytesseract.image_to_string(imagen, lang=idioma)


def extraer_pdf(ruta_pdf: Path, cfg_ocr: dict) -> tuple[str, int]:
    """Devuelve (texto, páginas_con_ocr)."""
    partes, con_ocr = [], 0
    with fitz.open(ruta_pdf) as doc:
        for i, pagina in enumerate(doc, start=1):
            texto = pagina.get_text("text")
            if len(texto.strip()) < cfg_ocr["min_caracteres_pagina"]:
                texto = _ocr(pagina, cfg_ocr["dpi"], cfg_ocr["idioma"])
                con_ocr += 1
            partes.append(f"{MARCA_PAGINA.format(i)}\n{texto.strip()}\n")
    return "\n".join(partes), con_ocr


def extraer_carpeta(dir_pdf: str, dir_texto: str, cfg_ocr: dict, sobrescribir=False):
    Path(dir_texto).mkdir(parents=True, exist_ok=True)
    for pdf in sorted(Path(dir_pdf).glob("*.pdf")):
        destino = Path(dir_texto) / f"{pdf.stem}.txt"
        if destino.exists() and not sobrescribir:
            print(f"[omitido] {destino.name} ya existe (posible corrección manual)")
            continue
        texto, con_ocr = extraer_pdf(pdf, cfg_ocr)
        destino.write_text(texto, encoding="utf-8")
        aviso = f" — {con_ocr} pág. con OCR: REVISAR A MANO" if con_ocr else ""
        print(f"[ok] {pdf.name} -> {destino.name}{aviso}")
