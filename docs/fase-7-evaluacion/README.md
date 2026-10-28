# Fase 7 — Evaluación

Se ejecuta **después** de que el sistema esté levantado y funcionando (Fases 0–6 cerradas).

| Indicador | Instrumento | Herramienta |
|---|---|---|
| I1 Precisión del contexto | 60 ensayos (20 consultas A/B × 3) | `scripts/evaluar_ragas.py` |
| I2 Exhaustividad del contexto | Igual | `scripts/evaluar_ragas.py` |
| I3 Fidelidad | Igual | `scripts/evaluar_ragas.py` |
| I4 Tasa no fundamentada | Ficha de 3 expertos contra todo el corpus | Manual (formato por crear) |
| I5 Latencia promedio | Logs del sistema | `scripts/latencia.py` |
| I6 SUS | Cuestionario de 10 ítems a estudiantes | Por crear (cálculo con la fórmula SUS) |

## Pendientes
- L5: probar `evaluar_ragas.py` con la versión de RAGAS instalada y fijar el LLM juez (y sus embeddings, si alguna métrica los usa).
- Banco de 20 consultas con respuestas de referencia validadas por expertos (`eval/banco_consultas.jsonl`).
- Pruebas estadísticas (SciPy / statsmodels) según el diseño de la tesis.

## Resultados
