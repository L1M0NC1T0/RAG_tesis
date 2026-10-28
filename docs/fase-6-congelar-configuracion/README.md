# Fase 6 — Congelar la configuración

**Objetivo:** cumplir el requisito de estabilidad: el modelo, su versión, los embeddings, top-k y los parámetros de generación no cambian durante la evaluación.

## Pasos
1. Copia de `config/config.yaml` final con la etiqueta git `config-evaluacion`.
2. Anotar los digests de los modelos (`ollama list`) y `pip freeze > docs/fase-6-congelar-configuracion/requirements-congelado.txt`.
3. Completar la Tabla 2 de la tesis con los datos de la Fase 0.

## Criterios de aceptación
- [ ] Etiqueta git creada
- [ ] Versiones y digests registrados
- [ ] Nada se modifica después de esto hasta terminar la evaluación

## Configuración congelada
| Parámetro | Valor |
|---|---|
| LLM (etiqueta, digest) | |
| Embeddings (etiqueta, digest) | |
| temperatura / max_tokens / semilla | |
| top_k / umbral | |
| tamaño / solapamiento | |
