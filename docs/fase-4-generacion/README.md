# Fase 4 — Generación fundamentada

**Objetivo:** respuestas claras, completas (requisitos, plazos, oficina, documentos), con citas correctas y sin datos inventados.

**Archivos:** `src/asistente/instrucciones.py`, `src/asistente/asistente.py`, sección `llm` de `config.yaml`.

## Pruebas rápidas
- Con las preguntas de calibración: ¿cada dato de la respuesta está en los fragmentos citados?
- Pregunta cuya respuesta no está en el corpus → debe abstenerse.
- Comparar los LLM candidatos de la Fase 0 (calidad vs. latencia) y elegir uno.

## Pendientes conocidos
- L1: detección robusta de la abstención.
- L2: comportamiento de las fuentes cuando no hay citas.

## Criterios de aceptación
- [ ] Sin datos inventados en las preguntas de calibración
- [ ] Abstención correcta en preguntas fuera del corpus
- [ ] LLM elegido y justificado

## Resultados
| Modelo | Pregunta | ¿Fiel? | ¿Completa? | ¿Citas correctas? | Latencia (s) |
|---|---|---|---|---|---|
