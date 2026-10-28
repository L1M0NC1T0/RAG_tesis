"""Paso 2: textos revisados -> fragmentos -> embeddings -> ChromaDB.
Actualizar el conocimiento = cambiar los .txt y volver a ejecutar esto (sin reentrenar)."""
import _ruta  # noqa: F401
from asistente.configuracion import cargar
from asistente.ingesta.fragmentacion import fragmentar_carpeta
from asistente.almacen import AlmacenVectorial
from asistente.proveedores import crear_embeddings

cfg = cargar()
frags = fragmentar_carpeta(cfg["rutas"]["texto"], cfg["fragmentacion"])
emb = crear_embeddings(cfg["embeddings"])
n = AlmacenVectorial(cfg["rutas"]["chroma"], cfg["rutas"]["coleccion"], emb).reconstruir(frags)
print(f"Indexados {n} fragmentos con {emb.descripcion()}")
