import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Microcultivo Dashboard", layout="wide")

st.title("🌿 Monitoreo Ambiental de Microcultivo Urbano")

st.markdown("""
Este panel presenta en tiempo real las condiciones de temperatura, humedad y radiación UV capturadas desde el sistema IoT.
""")

# Sustituye esta URL por el link público de tu dashboard de Grafana (public snapshot o embed)

components.iframe("https://pelaezescobarpepo.grafana.net/dashboard/snapshot/wqETKzwr91ZKmSpulKCbBBjaCCVHWyZH" , height=800, scrolling=True)
