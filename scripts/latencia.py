"""I5: latencia promedio a partir del registro automático (logs)."""
import json
import statistics
import _ruta  # noqa: F401
from asistente.configuracion import cargar

filas = [json.loads(l) for l in open(cargar()["rutas"]["logs"], encoding="utf-8")]
lat = [f["latencia_s"] for f in filas]
print(f"n={len(lat)}  promedio={statistics.mean(lat):.3f} s  "
      f"mediana={statistics.median(lat):.3f} s  desv={statistics.pstdev(lat):.3f} s")
