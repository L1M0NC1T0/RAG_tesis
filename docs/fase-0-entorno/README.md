# Fase 0 — Entorno

**Objetivo:** dejar el equipo listo y registrar versiones para la Tabla 2.

Equipo: ASUS TUF F15 FX507ZC4, i5-12500H, 24 GiB RAM, RTX 3050 Mobile 4 GB, CachyOS (kernel 7.3.0-3-cachyos).

## Pasos
```bash
sudo pacman -S python tesseract tesseract-data-spa ollama-cuda
```
```bash
sudo systemctl enable --now ollama
```
```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

## Modelos candidatos (a comparar, no decidido)
| Uso | Candidato | Tamaño aprox. | Nota |
|---|---|---|---|
| LLM | `qwen2.5:3b-instruct` | ~2 GB | Cabe entero en 4 GB de VRAM |
| LLM | `llama3.2:3b` | ~2 GB | Alternativa |
| LLM | `qwen2.5:7b-instruct` | ~4.7 GB | No cabe entero: parte en CPU, más lento |
| Embeddings | `bge-m3` | ~1.2 GB | Multilingüe |

## Pruebas rápidas
```bash
nvidia-smi
```
```bash
tesseract --version && tesseract --list-langs | grep spa
```
```bash
ollama pull qwen2.5:3b-instruct && ollama run qwen2.5:3b-instruct "Hola, responde en español"
```
```bash
ollama ps
```
`ollama ps` debe mostrar `100% GPU` en la columna PROCESSOR (si dice CPU, la GPU no se está usando).

## Criterios de aceptación
- [ ] La GPU es usada por Ollama
- [ ] Tesseract tiene el idioma `spa`
- [ ] Todas las dependencias de `requirements.txt` instaladas
- [ ] Versiones anotadas abajo

## Resultados
| Componente | Versión | Comando |
|---|---|---|
| Python | | `python --version` |
| LangChain text splitters | | `pip show langchain-text-splitters` |
| ChromaDB | | `pip show chromadb` |
| Tesseract | | `tesseract --version` |
| Ollama | | `ollama --version` |
| LLM (etiqueta + digest) | | `ollama list` |
| Embeddings (etiqueta + digest) | | `ollama list` |
| RAGAS / SciPy / statsmodels | | `pip show ragas scipy statsmodels` |
