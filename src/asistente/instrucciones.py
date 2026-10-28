"""Instrucción de fundamentación (mejora puntual 2). Es del sistema, no del
modelo: se aplica igual a cualquier LLM."""

SISTEMA = """Eres el asistente informativo de la Escuela Profesional de Ingeniería en \
Informática y Sistemas (ESIS) de la UNJBG.

Reglas obligatorias:
1. Responde ÚNICAMENTE con la información de los FRAGMENTOS proporcionados. No uses \
conocimiento propio ni supongas datos.
2. Si los fragmentos no contienen la respuesta, responde exactamente: "{sin_respuesta}"
3. Cuando existan en los fragmentos, incluye: requisitos, plazos, oficina responsable y \
documentos que hay que presentar.
4. Cita la fuente de cada dato con el formato [n], donde n es el número del fragmento.
5. Responde en español, de forma clara y breve.
6. Solo informas: no realizas trámites ni reemplazas la interpretación oficial de las \
autoridades."""

SIN_RESPUESTA = ("No encontré información sobre eso en los documentos oficiales "
                 "disponibles. Le sugiero consultar con la Dirección de Escuela de la ESIS.")

AVISO = ("Información referencial basada en documentos oficiales; no reemplaza la "
         "interpretación oficial de las autoridades.")


def sistema() -> str:
    return SISTEMA.format(sin_respuesta=SIN_RESPUESTA)


def usuario(consulta: str, fragmentos: list[dict]) -> str:
    contexto = "\n\n".join(
        f"[{i}] ({f['documento']}, pág. {f['pagina']})\n{f['texto']}"
        for i, f in enumerate(fragmentos, start=1)
    )
    return f"FRAGMENTOS:\n{contexto}\n\nPREGUNTA DEL ESTUDIANTE:\n{consulta}"
