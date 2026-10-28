"""Interfaces mínimas. Al modelo solo se le pide redactar y vectorizar;
recuperación, umbrales, instrucciones, citas y registro viven en el sistema."""
from abc import ABC, abstractmethod


class ProveedorLLM(ABC):
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.modelo = cfg["modelo"]

    @abstractmethod
    def generar(self, sistema: str, usuario: str) -> str:
        """Devuelve el texto completo de la respuesta."""

    def descripcion(self) -> str:
        return f"{self.cfg['proveedor']}:{self.modelo}"


class ProveedorEmbeddings(ABC):
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.modelo = cfg["modelo"]

    @abstractmethod
    def _vectorizar(self, textos: list[str]) -> list[list[float]]: ...

    def documentos(self, textos: list[str]) -> list[list[float]]:
        p = self.cfg.get("prefijo_documento", "")
        return self._vectorizar([p + t for t in textos])

    def consulta(self, texto: str) -> list[float]:
        p = self.cfg.get("prefijo_consulta", "")
        return self._vectorizar([p + texto])[0]

    def descripcion(self) -> str:
        return f"{self.cfg['proveedor']}:{self.modelo}"
