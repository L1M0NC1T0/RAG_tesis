# Fase 3 — Recuperación (búsqueda por significado)

**Objetivo:** que los fragmentos correctos aparezcan entre los primeros resultados, y calibrar `top_k` y `umbral_similitud`.

**Archivos:** `src/asistente/almacen.py`, sección `recuperacion` de `config.yaml`.

## Método
1. Escribir 10 preguntas de **calibración**, **distintas** de las 20 del banco de evaluación (para no sesgar los resultados), cada una con el fragmento correcto esperado.
2. Incluir 3 preguntas fuera de tema (deben quedar bajo el umbral).
3. Ver, para cada pregunta, la posición del fragmento correcto y su similitud.

Hoy no existe un script que muestre solo la recuperación; se propondrá en esta fase (requiere aprobación).

## Criterios de aceptación
- [ ] El fragmento correcto aparece en el top-k en la mayoría de las preguntas de calibración
- [ ] Las preguntas fuera de tema quedan bajo el umbral
- [ ] `top_k` y `umbral_similitud` elegidos y justificados

## Resultados
| Pregunta | Fragmento esperado | Posición obtenida | Similitud | ¿OK? |
|---|---|---|---|---|
