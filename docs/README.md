# Plan de desarrollo por fases

Regla de trabajo: **nada se escribe ni se cambia sin aprobación**, y una fase
solo se cierra cuando sus criterios se cumplen **en la laptop del autor** con
modelos y documentos reales. Ningún resultado de la tesis sale de pruebas
simuladas.

Estado del código: existe una versión base (commit inicial) que se revisa y
ajusta fase por fase. Hasta ahora solo se comprobó, fuera del repositorio y con
embeddings simulados, que la fragmentación y ChromaDB guardan y buscan. Nada
más ha sido probado.

| Fase | Carpeta | Estado |
|---|---|---|
| 0. Entorno | [fase-0-entorno](fase-0-entorno/README.md) | Pendiente |
| 1. Extracción y OCR | [fase-1-extraccion-ocr](fase-1-extraccion-ocr/README.md) | Pendiente |
| 2. Fragmentación e indexación | [fase-2-fragmentacion-indexacion](fase-2-fragmentacion-indexacion/README.md) | Pendiente |
| 3. Recuperación | [fase-3-recuperacion](fase-3-recuperacion/README.md) | Pendiente |
| 4. Generación | [fase-4-generacion](fase-4-generacion/README.md) | Pendiente |
| 5. Interfaz y registro | [fase-5-interfaz-registro](fase-5-interfaz-registro/README.md) | Pendiente |
| 6. Congelar configuración | [fase-6-congelar-configuracion](fase-6-congelar-configuracion/README.md) | Pendiente |
| 7. Evaluación | [fase-7-evaluacion](fase-7-evaluacion/README.md) | Pendiente |

Además: [revision-codigo-base.md](revision-codigo-base.md), una guía para revisar el
código entregado archivo por archivo, con pruebas rápidas y limitaciones conocidas.

Cada fase tiene: objetivo, archivos involucrados, pruebas rápidas, criterios de
aceptación y una sección **Resultados** para anotar lo obtenido (fecha, versiones,
observaciones).
