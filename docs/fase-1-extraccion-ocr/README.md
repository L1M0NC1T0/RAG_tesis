# Fase 1 — Extracción de texto y OCR

**Objetivo:** convertir todo el corpus (PDF nativos y escaneados) a texto fiel, revisado a mano.

**Archivos:** `src/asistente/ingesta/extraccion.py`, `scripts/extraer.py`, sección `ocr` de `config.yaml`.

## Pasos
1. Reunir el corpus en `data/pdf/` (nombres sin espacios, por ejemplo `reglamento_grados_titulos_2023.pdf`).
2. Llenar el inventario de abajo.
3. `python scripts/extraer.py`
4. Revisar cada `.txt` contra su PDF; corregir a mano los marcados "REVISAR A MANO".

## Pruebas rápidas
- Un PDF nativo: el `.txt` debe coincidir con el PDF sin aplicar OCR.
- Una resolución escaneada: contar errores en una página (palabras mal leídas / total).
- Ver limitación L6 (páginas mixtas).

## Decisiones a tomar aquí
- ¿`dpi: 300` es suficiente? ¿Se necesita preprocesar imágenes (escala de grises, binarizado)?
- ¿Cómo se tratan tablas, encabezados y pies de página repetidos?

## Criterios de aceptación
- [ ] Todos los documentos del corpus tienen su `.txt`
- [ ] Todos los `.txt` con OCR fueron revisados y corregidos a mano
- [ ] Inventario completo

## Resultados — inventario del corpus
| Archivo | Documento / resolución | Fecha | Páginas | ¿Escaneado? | Revisado por | Fecha de revisión |
|---|---|---|---|---|---|---|
| | | | | | | |
