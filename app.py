import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Microcultivo Dashboard", layout="wide")

st.title("🌱 Monitoreo Ambiental de Microcultivo Urbano")
st.markdown("Este panel muestra una visualización en tiempo real desde Grafana.")

# ⚠️ El iframe de Grafana se embebe aquí
grafana_iframe = """
<iframe src="https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=1747328457815&to=1747350057815&timezone=browser&panelId=6&__feature.dashboardSceneSolo" width="450" height="200" frameborder="0"></iframe>"""

# Insertar el iframe usando components.html
components.html(grafana_iframe, height=220)
