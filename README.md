# Asistente virtual RAG – ESIS UNJBG

RAG básico (naive RAG) con dos mejoras puntuales: **OCR** para resoluciones
escaneadas e **instrucción de responder solo con lo recuperado**.

## Arquitectura independiente del modelo

```
src/asistente/
  proveedores/        <- ÚNICO lugar que conoce a los modelos (Ollama / API compatible OpenAI)
  ingesta/            <- PDF -> texto (+OCR Tesseract) -> fragmentos con documento y página
  almacen.py          <- ChromaDB, similitud del coseno, top-k
  instrucciones.py    <- regla de fundamentación, mensaje de abstención, formato de citas
  asistente.py        <- flujo de consulta + registro de latencia en ms (logs JSONL)
config/config.yaml    <- modelo, versión, top-k y parámetros (FIJOS durante la evaluación)
```

El sistema, no el modelo, se encarga de: recuperación, **umbral de abstención**
(si ningún fragmento supera la similitud mínima, responde "no encontré" *sin llamar al LLM*),
instrucción anti-alucinación, citas `[n]` → fuentes (documento + página), registro
de latencia y códigos de participante. El LLM solo redacta.

**Cambiar de LLM** = editar `llm:` en `config.yaml`. No hay que reindexar.
**Cambiar de embeddings** = editar `embeddings:` y ejecutar `indexar.py`; si se
olvida, el sistema se niega a consultar (guarda qué modelo creó el índice).

> Ojo: para la tesis, un cambio de modelo **sí** cambia los resultados medidos;
> la arquitectura evita que el sistema se rompa, pero debe anotarse y la
> configuración debe quedar fija durante toda la evaluación.

## ¿Modelo local o API gratuita? (para su equipo: RTX 3050 4 GB, 24 GB RAM)

| Criterio | Local (Ollama) | API gratuita (Groq, Gemini, OpenRouter) |
|---|---|---|
| Modelo que cabe | 3–4B cuantizado (qwen2.5:3b, llama3.2:3b, phi-4-mini) en GPU; 7–8B se desborda a CPU (~4–8 tok/s) | 8B–70B, mejor redacción en español |
| Latencia (I5) | ~3–10 s con 3B; >20 s con 8B | ~1–3 s, pero variable (cola, límites) |
| Reproducibilidad / versión fija | **Total** (digest del modelo) | El proveedor puede cambiar o retirar el modelo, y hay límites por minuto/día |
| Datos | No salen del equipo | Las consultas salen a terceros |
| Coherencia con la Tabla 2 | Sí (Ollama, local) | Habría que modificar la tesis |

**Recomendación:** modelo **local** para el asistente evaluado (requisito de
configuración fija, Tabla 2, Ley 29733), con `qwen2.5:3b-instruct` o
`qwen2.5:7b-instruct` si la latencia es aceptable. Embeddings **siempre locales**
(`bge-m3`, ~1,2 GB). Use la API gratuita solo como alternativa de desarrollo o
como **LLM juez de RAGAS** (un juez más grande que el asistente da métricas más
confiables). Gracias a la capa de proveedores, probar ambos es cambiar 3 líneas.

## Uso

```bash
sudo pacman -S tesseract tesseract-data-spa ollama-cuda
```
```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```
```bash
ollama pull qwen2.5:3b-instruct && ollama pull bge-m3
```
1. Copie los PDF en `data/pdf/`.
2. `python scripts/extraer.py` → genera `data/texto/*.txt`. **Revise y corrija a mano** los marcados con OCR.
3. `python scripts/indexar.py`
4. `streamlit run scripts/app.py` (o `python scripts/consultar.py "pregunta"`)

Evaluación (cuando el sistema esté funcionando): copie
`eval/banco_consultas.ejemplo.jsonl` a `eval/banco_consultas.jsonl` con las 20 consultas y
referencias validadas, luego `python scripts/evaluar_ragas.py` (I1–I3, 60 ensayos) y
`python scripts/latencia.py` (I5). Anote versiones con `pip freeze` y `ollama show <modelo>`.
