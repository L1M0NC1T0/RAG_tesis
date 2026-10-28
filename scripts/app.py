"""Interfaz web: streamlit run scripts/app.py"""
import _ruta  # noqa: F401
import streamlit as st
from asistente.configuracion import cargar
from asistente.asistente import Asistente
from asistente.instrucciones import AVISO

st.set_page_config(page_title="Asistente ESIS", page_icon="🎓")
st.title("Asistente virtual ESIS – UNJBG")
st.caption(AVISO)


@st.cache_resource
def asistente():
    return Asistente(cargar())


codigo = st.sidebar.text_input("Código de participante", help="No escriba su nombre")
st.session_state.setdefault("chat", [])
for rol, texto in st.session_state.chat:
    st.chat_message(rol).markdown(texto)

if pregunta := st.chat_input("Escriba su pregunta sobre normativa de la ESIS"):
    st.chat_message("user").markdown(pregunta)
    with st.spinner("Buscando en los documentos oficiales..."):
        r = asistente().preguntar(pregunta, codigo)
    texto = r.respuesta
    if r.fuentes:
        texto += "\n\n**Fuentes:** " + "; ".join(r.fuentes)
    st.chat_message("assistant").markdown(texto)
    st.session_state.chat += [("user", pregunta), ("assistant", texto)]
