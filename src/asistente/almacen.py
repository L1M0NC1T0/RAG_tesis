"""Base de datos vectorial (ChromaDB, similitud del coseno).

Guarda en los metadatos de la colección qué modelo de embeddings la creó:
si se cambia ese modelo sin reindexar, el sistema se niega a consultar
(evita resultados silenciosamente malos). Cambiar el LLM no requiere reindexar.
"""
import chromadb

from .proveedores import ProveedorEmbeddings


class AlmacenVectorial:
    def __init__(self, ruta: str, nombre: str, emb: ProveedorEmbeddings):
        self.cliente = chromadb.PersistentClient(path=ruta)
        self.nombre = nombre
        self.emb = emb

    def reconstruir(self, fragmentos: list[dict], lote: int = 32):
        try:
            self.cliente.delete_collection(self.nombre)
        except Exception:
            pass
        col = self.cliente.create_collection(
            self.nombre,
            metadata={"hnsw:space": "cosine", "modelo_embeddings": self.emb.descripcion()},
        )
        for i in range(0, len(fragmentos), lote):
            parte = fragmentos[i:i + lote]
            col.add(
                ids=[f["id"] for f in parte],
                documents=[f["texto"] for f in parte],
                embeddings=self.emb.documentos([f["texto"] for f in parte]),
                metadatas=[{"documento": f["documento"], "pagina": f["pagina"]} for f in parte],
            )
        return col.count()

    def buscar(self, consulta: str, k: int) -> list[dict]:
        col = self.cliente.get_collection(self.nombre)
        indexado = col.metadata.get("modelo_embeddings")
        if indexado != self.emb.descripcion():
            raise RuntimeError(
                f"El índice se creó con '{indexado}' pero la configuración usa "
                f"'{self.emb.descripcion()}'. Ejecute scripts/indexar.py de nuevo."
            )
        r = col.query(query_embeddings=[self.emb.consulta(consulta)], n_results=k)
        return [
            {"texto": d, **m, "similitud": round(1 - dist, 4)}
            for d, m, dist in zip(r["documents"][0], r["metadatas"][0], r["distances"][0])
        ]
