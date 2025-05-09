import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Microcultivo Dashboard", layout="wide")

st.title("🌿 Monitoreo Ambiental de Microcultivo Urbano")

st.markdown("""
Este panel presenta en tiempo real las condiciones de temperatura, humedad y radiación UV capturadas desde el sistema IoT.
""")

# Sustituye esta URL por el link público de tu dashboard de Grafana (public snapshot o embed)
grafana_url = "https://pelaezescobarpepo.grafana.net/d/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=2025-05-08T19:06:31.288Z&to=2025-05-09T01:06:31.288Z&timezone=browser&viewPanel=panel-6"

components.iframe(grafana_url, height=800, scrolling=True)
