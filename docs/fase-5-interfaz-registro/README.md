# Fase 5 — Interfaz y registro automático

**Objetivo:** interfaz usable por los estudiantes desde los laboratorios de la ESIS y registro confiable de la latencia en ms.

**Archivos:** `scripts/app.py`, `scripts/latencia.py`, método `_registrar` en `asistente.py`.

## Puntos a definir
- Acceso desde la red del laboratorio: `streamlit run scripts/app.py --server.address 0.0.0.0` (comprobar firewall).
- Qué intervalo exacto mide la latencia (L4) y cómo se redacta en la tesis.
- Participantes identificados solo por código (Ley 29733).
- Sincronización del reloj del sistema con el cronómetro de las sesiones.

## Criterios de aceptación
- [ ] Una persona externa usa la interfaz sin ayuda
- [ ] Cada consulta queda en `data/logs/consultas.jsonl` con tiempos en ms y código
- [ ] `python scripts/latencia.py` calcula el promedio

## Resultados
