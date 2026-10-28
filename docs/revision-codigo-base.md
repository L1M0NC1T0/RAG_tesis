# Revisión del código base

Recorrido recomendado (en orden del flujo de datos). Cada prueba requiere el
entorno de la Fase 0 (`source .venv/bin/activate` en la raíz del repositorio).

## 1. `config/config.yaml`
Único lugar donde se eligen modelos y parámetros. Revise que entienda cada clave.
Prueba: `python -c "import sys; sys.path.insert(0,'src'); from asistente.configuracion import cargar; import pprint; pprint.pprint(cargar())"`
Esperado: las rutas aparecen como rutas absolutas dentro del repositorio.

## 2. `src/asistente/proveedores/`
- `base.py`: interfaces. Un LLM solo implementa `generar(sistema, usuario)`; unos embeddings solo `_vectorizar(textos)`.
- `ollama.py`: llamadas HTTP a `/api/chat` y `/api/embed`.
- `openai_compatible.py`: lo mismo para APIs (no se usará: trabajamos en local).

Prueba (con Ollama encendido y modelos descargados):
```bash
python -c "import sys; sys.path.insert(0,'src'); from asistente.configuracion import cargar; from asistente.proveedores import crear_llm, crear_embeddings; c=cargar(); print(crear_llm(c['llm']).generar('Responde en una frase.','¿Qué es la UNJBG?')); print(len(crear_embeddings(c['embeddings']).consulta('hola')))"
```
Esperado: una frase en español y la dimensión del vector (1024 para bge-m3).

## 3. `src/asistente/ingesta/extraccion.py`
Por cada página: si tiene menos de `min_caracteres_pagina` caracteres nativos, aplica OCR con Tesseract. Escribe `data/texto/<pdf>.txt` con marcas `=== Página N ===`. **No sobrescribe** un `.txt` existente (para no perder correcciones manuales) salvo con `--sobrescribir`.
Prueba: un PDF nativo y uno escaneado en `data/pdf/` y luego `python scripts/extraer.py`.

## 4. `src/asistente/ingesta/fragmentacion.py`
Divide cada página por separado (un fragmento nunca mezcla dos páginas) con `RecursiveCharacterTextSplitter` (800 caracteres, 120 de solapamiento).
Prueba: `python -c "import sys; sys.path.insert(0,'src'); from asistente.configuracion import cargar; from asistente.ingesta.fragmentacion import fragmentar_carpeta; c=cargar(); f=fragmentar_carpeta(c['rutas']['texto'],c['fragmentacion']); print(len(f)); print(f[0])"`

## 5. `src/asistente/almacen.py`
ChromaDB con distancia coseno; `similitud = 1 - distancia`. Guarda qué modelo de embeddings creó el índice y se niega a buscar si la configuración cambió.
Prueba: `python scripts/indexar.py`, luego cambie `embeddings.modelo` a otro nombre y ejecute `consultar.py`; debe dar error pidiendo reindexar. Restaure el valor.

## 6. `src/asistente/instrucciones.py` y `asistente.py`
Flujo: buscar top-k → filtrar por `umbral_similitud` → si no queda nada, responder "no encontré" **sin llamar al LLM** → si hay, llamar al LLM con la instrucción → extraer citas `[n]` → registrar en `data/logs/consultas.jsonl`.
Prueba: `python scripts/consultar.py "¿cuántas veces puedo llevar un curso desaprobado?"` y `python scripts/consultar.py "¿quién ganó el mundial?"` (la segunda debe abstenerse).

## 7. `scripts/`
`extraer.py`, `indexar.py`, `consultar.py`, `app.py` (Streamlit), `latencia.py`, `evaluar_ragas.py`.

## Limitaciones conocidas (a resolver en su fase)
| # | Dónde | Problema | Fase |
|---|---|---|---|
| L1 | `asistente.py` | La abstención del LLM se detecta comparando los primeros 30 caracteres del mensaje fijo; si el modelo lo parafrasea, no se detecta | 4 |
| L2 | `asistente.py` | Si el LLM no pone citas `[n]`, se listan como fuentes **todos** los fragmentos relevantes | 4 |
| L3 | `config.yaml` | `umbral_similitud: 0.35`, `top_k: 4`, `tamano: 800` son valores iniciales sin calibrar | 2–3 |
| L4 | `asistente.py` | La latencia registrada incluye la búsqueda y la generación, pero no el tiempo de la interfaz web; debe definirse en la tesis qué se mide | 5 |
| L5 | `evaluar_ragas.py` | No probado; la API de RAGAS cambia entre versiones y falta fijar el LLM juez y sus embeddings | 7 |
| L6 | `extraccion.py` | Páginas mixtas (texto nativo + sello o firma escaneados) no pasan por OCR si superan el umbral de caracteres | 1 |
| L7 | `app.py` | La interfaz no muestra historial al modelo (cada pregunta es independiente); es intencional en naive RAG, pero debe declararse | 5 |
| L8 | Logs | El registro guarda el texto completo de los fragmentos; el archivo puede crecer, aunque sirve como evidencia | 5 |
