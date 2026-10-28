"""Fase 1b: texto revisado -> fragmentos con metadatos (documento, página)."""
from pathlib import Path
import re

from langchain_text_splitters import RecursiveCharacterTextSplitter

_PAGINA = re.compile(r"^=== Página (\d+) ===$", re.MULTILINE)


def fragmentar_carpeta(dir_texto: str, cfg_frag: dict) -> list[dict]:
    divisor = RecursiveCharacterTextSplitter(
        chunk_size=cfg_frag["tamano"],
        chunk_overlap=cfg_frag["solapamiento"],
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    fragmentos = []
    for txt in sorted(Path(dir_texto).glob("*.txt")):
        contenido = txt.read_text(encoding="utf-8")
        # split con grupo => ["", "1", texto1, "2", texto2, ...]
        trozos = _PAGINA.split(contenido)
        paginas = zip(trozos[1::2], trozos[2::2]) if len(trozos) > 1 else [("1", contenido)]
        for num, texto in paginas:
            for j, trozo in enumerate(divisor.split_text(texto.strip())):
                fragmentos.append({
                    "id": f"{txt.stem}-p{num}-{j}",
                    "texto": trozo,
                    "documento": txt.stem,
                    "pagina": int(num),
                })
    return fragmentos
