"""Consulta por terminal: python scripts/consultar.py "¿cuántas veces puedo llevar un curso?" """
import sys
import _ruta  # noqa: F401
from asistente.configuracion import cargar
from asistente.asistente import Asistente

r = Asistente(cargar()).preguntar(" ".join(sys.argv[1:]) or input("Pregunta: "))
print(f"\n{r.respuesta}\n")
for f in r.fuentes:
    print(f"  · {f}")
print(f"\nLatencia: {r.latencia_s:.2f} s")
