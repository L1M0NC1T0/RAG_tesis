"""Capa de proveedores: el resto del sistema solo conoce estas interfaces.

Para agregar un modelo/servicio nuevo basta con implementar ProveedorLLM o
ProveedorEmbeddings y registrarlo en `crear_llm` / `crear_embeddings`.
"""
from .base import ProveedorLLM, ProveedorEmbeddings
from .ollama import OllamaLLM, OllamaEmbeddings
from .openai_compatible import OpenAICompatLLM, OpenAICompatEmbeddings

_LLM = {"ollama": OllamaLLM, "openai_compatible": OpenAICompatLLM}
_EMB = {"ollama": OllamaEmbeddings, "openai_compatible": OpenAICompatEmbeddings}


def crear_llm(cfg: dict) -> ProveedorLLM:
    return _LLM[cfg["proveedor"]](cfg)


def crear_embeddings(cfg: dict) -> ProveedorEmbeddings:
    return _EMB[cfg["proveedor"]](cfg)
