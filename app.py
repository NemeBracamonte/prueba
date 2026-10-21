import joblib
import pandas as pd
import streamlit as st

MODEL_PATH = "modelo_especie_rl.joblib"

# Nombres de columnas: deben coincidir con los usados al entrenar (morph_features).
# Si el modelo guardó los nombres (feature_names_in_), se usan esos automáticamente.
DEFAULT_FEATURES = [
    "culmen_length_mm",
    "culmen_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
]

# (etiqueta, unidad, mínimo plausible, máximo plausible) -> solo para ADVERTENCIAS
CAMPOS = [
    ("Longitud del pico", "mm", 30.0, 62.0),
    ("Profundidad del pico", "mm", 12.0, 23.0),
    ("Longitud de la aleta", "mm", 165.0, 240.0),
    ("Masa corporal", "g", 2500.0, 6500.0),
]


@st.cache_resource
def cargar_modelo():
    return joblib.load(MODEL_PATH)


def parsear(texto: str):
    """Devuelve (valor, error). Acepta coma o punto decimal."""
    texto = texto.strip()
    if texto == "":
        return None, "obligatorio"
    try:
        valor = float(texto.replace(",", "."))
    except ValueError:
        return None, "no numérico"
    if valor != valor or valor in (float("inf"), float("-inf")):
        return None, "no numérico"
    if valor <= 0:
        return None, "debe ser mayor que 0"
    return valor, None


st.set_page_config(page_title="Clasificador de pingüinos", page_icon="🐧")
st.title("🐧 Clasificador de especies de pingüinos")
st.caption("App de testing — modelo de regresión logística")

try:
    modelo = cargar_modelo()
except FileNotFoundError:
    st.error(f"No se encontró `{MODEL_PATH}`. Ponelo en la misma carpeta que app.py.")
    st.stop()

features = list(getattr(modelo, "feature_names_in_", DEFAULT_FEATURES))

with st.form("form_prediccion"):
    entradas = []
    for etiqueta, unidad, _, _ in CAMPOS:
        entradas.append(st.text_input(f"{etiqueta} ({unidad})", key=etiqueta))
    enviado = st.form_submit_button("Predecir especie")

if enviado:
    valores, errores, avisos = [], [], []

    for (etiqueta, unidad, vmin, vmax), texto in zip(CAMPOS, entradas):
        valor, error = parsear(texto)
        if error == "obligatorio":
            errores.append(f"**{etiqueta}**: campo obligatorio sin completar.")
        elif error:
            errores.append(f"**{etiqueta}**: valor inválido ({error}).")
        else:
            if not (vmin <= valor <= vmax):
                avisos.append(
                    f"**{etiqueta}** = {valor:g} {unidad} está fuera del rango "
                    f"habitual ({vmin:g}–{vmax:g} {unidad}). Revisá el dato."
                )
        valores.append(valor)

    if errores:
        st.error("No se puede predecir. Corregí lo siguiente:")
        for e in errores:
            st.markdown(f"- {e}")
    else:
        for a in avisos:
            st.warning(a)

        X = pd.DataFrame([valores], columns=features)
        especie = modelo.predict(X)[0]
        proba = pd.Series(modelo.predict_proba(X)[0], index=modelo.classes_)

        st.success(f"Especie predicha: **{especie}**  ({proba.max():.1%} de probabilidad)")
        st.subheader("Probabilidad por especie")
        st.bar_chart(proba)
        st.dataframe(proba.round(3).rename("probabilidad").to_frame())
