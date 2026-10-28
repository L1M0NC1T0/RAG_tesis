"""Cualquier servicio con API compatible con OpenAI (Groq, OpenRouter,
Gemini, LM Studio, vLLM, llama.cpp server...)."""
import requests

from .base import ProveedorLLM, ProveedorEmbeddings


def _cabeceras(cfg):
    return {"Authorization": f"Bearer {cfg.get('api_key', '')}"}


class OpenAICompatLLM(ProveedorLLM):
    def generar(self, sistema: str, usuario: str) -> str:
        cuerpo = {
            "model": self.modelo,
            "temperature": self.cfg["temperatura"],
            "max_tokens": self.cfg["max_tokens"],
            "messages": [
                {"role": "system", "content": sistema},
                {"role": "user", "content": usuario},
            ],
        }
        if self.cfg.get("semilla") is not None:
            cuerpo["seed"] = self.cfg["semilla"]
        r = requests.post(
            f"{self.cfg['url_base']}/chat/completions",
            json=cuerpo,
            headers=_cabeceras(self.cfg),
            timeout=self.cfg.get("timeout_s", 180),
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()


class OpenAICompatEmbeddings(ProveedorEmbeddings):
    def _vectorizar(self, textos):
        r = requests.post(
            f"{self.cfg['url_base']}/embeddings",
            json={"model": self.modelo, "input": textos},
            headers=_cabeceras(self.cfg),
            timeout=300,
        )
        r.raise_for_status()
        return [d["embedding"] for d in sorted(r.json()["data"], key=lambda d: d["index"])]
