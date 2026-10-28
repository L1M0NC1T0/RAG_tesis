# Fase 2 — Fragmentación e indexación

**Objetivo:** fragmentos de tamaño moderado que conserven unidades de sentido (artículos) y queden indexados con los embeddings reales.

**Archivos:** `src/asistente/ingesta/fragmentacion.py`, `src/asistente/almacen.py`, `scripts/indexar.py`.

## Pruebas rápidas
- `python scripts/indexar.py` → anotar número de fragmentos y tiempo.
- Revisar 20 fragmentos al azar: ¿cortan un artículo a la mitad? ¿documento y página son correctos?
- Prueba de seguridad: cambiar `embeddings.modelo` sin reindexar → debe dar error.

## Decisiones a tomar aquí
- Tamaño y solapamiento (valores iniciales 800/120 caracteres, ver L3).
- ¿Fragmentar por artículo ("Artículo N°") en lugar de por caracteres? Se decide viendo los textos reales.

## Criterios de aceptación
- [ ] Índice creado con el modelo de embeddings elegido
- [ ] Muestra de fragmentos revisada sin cortes graves

## Resultados
| Fecha | Modelo embeddings | Tamaño / solapamiento | N.º fragmentos | Tiempo | Observaciones |
|---|---|---|---|---|---|
