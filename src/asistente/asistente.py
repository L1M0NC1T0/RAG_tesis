"""Fase 2: consulta -> recuperación densa top-k -> instrucción -> LLM -> respuesta.

Toda la lógica (umbral de abstención, instrucción, citas, registro de
latencia) es del sistema; el LLM solo redacta.
"""
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
import json
import re
import time

from . import instrucciones
from .almacen import AlmacenVectorial
from .proveedores import crear_llm, crear_embeddings


@dataclass
class Respuesta:
    consulta: str
    respuesta: str
    fragmentos: list[dict] = field(default_factory=list)
    fuentes: list[str] = field(default_factory=list)
    abstencion: bool = False
    t_envio_ms: int = 0
    t_recepcion_ms: int = 0

    @property
    def latencia_s(self) -> float:
        return (self.t_recepcion_ms - self.t_envio_ms) / 1000


class Asistente:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.llm = crear_llm(cfg["llm"])
        self.emb = crear_embeddings(cfg["embeddings"])
        self.almacen = AlmacenVectorial(cfg["rutas"]["chroma"], cfg["rutas"]["coleccion"], self.emb)

    def preguntar(self, consulta: str, codigo_participante: str = "") -> Respuesta:
        t_envio = time.time_ns() // 1_000_000
        rec = self.cfg["recuperacion"]
        fragmentos = self.almacen.buscar(consulta, rec["top_k"])
        relevantes = [f for f in fragmentos if f["similitud"] >= rec["umbral_similitud"]]

        if not relevantes:
            texto, abstencion = instrucciones.SIN_RESPUESTA, True
        else:
            texto = self.llm.generar(instrucciones.sistema(),
                                     instrucciones.usuario(consulta, relevantes))
            abstencion = instrucciones.SIN_RESPUESTA[:30] in texto

        citados = {int(n) for n in re.findall(r"\[(\d+)\]", texto)}
        fuentes = sorted({
            f"{f['documento']} (pág. {f['pagina']})"
            for i, f in enumerate(relevantes, start=1) if i in citados or not citados
        }) if not abstencion else []

        r = Respuesta(consulta, texto, fragmentos, fuentes, abstencion,
                      t_envio, time.time_ns() // 1_000_000)
        self._registrar(r, codigo_participante)
        return r

    def _registrar(self, r: Respuesta, codigo: str):
        ruta = Path(self.cfg["rutas"]["logs"])
        ruta.parent.mkdir(parents=True, exist_ok=True)
        fila = {
            "fecha_utc": datetime.now(timezone.utc).isoformat(),
            "participante": codigo,  # código, nunca nombre (Ley 29733)
            "llm": self.llm.descripcion(),
            "embeddings": self.emb.descripcion(),
            "top_k": self.cfg["recuperacion"]["top_k"],
            **asdict(r),
            "latencia_s": r.latencia_s,
        }
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(json.dumps(fila, ensure_ascii=False) + "\n")
