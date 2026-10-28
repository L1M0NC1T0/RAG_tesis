"""Carga de la configuración única del sistema (config/config.yaml)."""
from pathlib import Path
import os

import yaml
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[2]


def cargar(ruta: str | Path = RAIZ / "config" / "config.yaml") -> dict:
    load_dotenv(RAIZ / ".env")
    with open(ruta, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    for clave, valor in cfg["rutas"].items():
        if clave != "coleccion":
            cfg["rutas"][clave] = str(RAIZ / valor)
    cfg["llm"]["api_key"] = os.getenv("LLM_API_KEY", "")
    cfg["embeddings"]["api_key"] = os.getenv("EMBEDDINGS_API_KEY", cfg["llm"]["api_key"])
    return cfg
