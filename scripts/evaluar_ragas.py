"""I1-I3 con RAGAS: precisión del contexto, exhaustividad del contexto y fidelidad.

Entrada: eval/banco_consultas.jsonl con {"id", "version", "pregunta", "referencia"}
(referencia = respuesta validada por expertos). Ejecuta N repeticiones (60 ensayos
= 20 consultas x 3) y guarda eval/resultados_ragas.csv.

El LLM juez se configura aparte (sección `juez` opcional en config.yaml; si no
existe usa el mismo LLM). Mantenga el juez FIJO durante toda la evaluación.
"""
import argparse
import json
import _ruta  # noqa: F401
from asistente.configuracion import cargar, RAIZ
from asistente.asistente import Asistente

from ragas import evaluate, EvaluationDataset
from ragas.metrics import LLMContextPrecisionWithReference, LLMContextRecall, Faithfulness
from ragas.llms import LangchainLLMWrapper

p = argparse.ArgumentParser()
p.add_argument("--banco", default=str(RAIZ / "eval" / "banco_consultas.jsonl"))
p.add_argument("--repeticiones", type=int, default=3)
a = p.parse_args()

cfg = cargar()
asis = Asistente(cfg)
juez_cfg = cfg.get("juez", cfg["llm"])
if juez_cfg["proveedor"] == "ollama":
    from langchain_ollama import ChatOllama
    juez = ChatOllama(model=juez_cfg["modelo"], base_url=juez_cfg["url_base"], temperature=0)
else:
    from langchain_openai import ChatOpenAI
    juez = ChatOpenAI(model=juez_cfg["modelo"], base_url=juez_cfg["url_base"],
                      api_key=cfg["llm"]["api_key"], temperature=0)

banco = [json.loads(l) for l in open(a.banco, encoding="utf-8") if l.strip()]
muestras, meta = [], []
for rep in range(1, a.repeticiones + 1):
    for q in banco:
        r = asis.preguntar(q["pregunta"], codigo_participante=f"EVAL-r{rep}")
        muestras.append({
            "user_input": q["pregunta"],
            "retrieved_contexts": [f["texto"] for f in r.fragmentos],
            "response": r.respuesta,
            "reference": q["referencia"],
        })
        meta.append({"id": q["id"], "version": q.get("version", ""), "repeticion": rep,
                     "latencia_s": r.latencia_s})

res = evaluate(
    EvaluationDataset.from_list(muestras),
    metrics=[LLMContextPrecisionWithReference(), LLMContextRecall(), Faithfulness()],
    llm=LangchainLLMWrapper(juez),
)
df = res.to_pandas()
for col in ("id", "version", "repeticion", "latencia_s"):
    df[col] = [m[col] for m in meta]
salida = RAIZ / "eval" / "resultados_ragas.csv"
df.to_csv(salida, index=False)
print(df.groupby("version")[["llm_context_precision_with_reference",
                             "context_recall", "faithfulness", "latencia_s"]].mean())
print(f"Guardado en {salida}")
