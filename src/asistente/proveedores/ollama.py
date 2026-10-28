import requests

from .base import ProveedorLLM, ProveedorEmbeddings


class OllamaLLM(ProveedorLLM):
    def generar(self, sistema: str, usuario: str) -> str:
        r = requests.post(
            f"{self.cfg['url_base']}/api/chat",
            json={
                "model": self.modelo,
                "stream": False,
                "messages": [
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": usuario},
                ],
                "options": {
                    "temperature": self.cfg["temperatura"],
                    "num_predict": self.cfg["max_tokens"],
                    "seed": self.cfg.get("semilla"),
                },
            },
            timeout=self.cfg.get("timeout_s", 180),
        )
        r.raise_for_status()
        return r.json()["message"]["content"].strip()


class OllamaEmbeddings(ProveedorEmbeddings):
    def _vectorizar(self, textos):
        r = requests.post(
            f"{self.cfg['url_base']}/api/embed",
            json={"model": self.modelo, "input": textos},
            timeout=300,
        )
        r.raise_for_status()
        return r.json()["embeddings"]
