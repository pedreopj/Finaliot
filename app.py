import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Microcultivo Dashboard", layout="wide")

st.title("🌱 Monitoreo Ambiental de Microcultivo Urbano")
st.markdown("Este panel muestra una visualización en tiempo real desde Grafana.")

# URLs de los 6 iframes de Grafana (puedes cambiar las URLs por las que necesites)
iframes = [
    """<iframe src="https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=1747328457815&to=1747350057815&timezone=browser&panelId=6&__feature.dashboardSceneSolo" width="450" height="200" frameborder="0"></iframe>""",
    """<iframe src="https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=1747328457815&to=1747350057815&timezone=browser&panelId=7&__feature.dashboardSceneSolo" width="450" height="200" frameborder="0"></iframe>""",
    """<iframe src="https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=1747328457815&to=1747350057815&timezone=browser&panelId=8&__feature.dashboardSceneSolo" width="450" height="200" frameborder="0"></iframe>""",
    """<iframe src="https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=1747328457815&to=1747350057815&timezone=browser&panelId=9&__feature.dashboardSceneSolo" width="450" height="200" frameborder="0"></iframe>""",
    """<iframe src="https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=1747328457815&to=1747350057815&timezone=browser&panelId=10&__feature.dashboardSceneSolo" width="450" height="200" frameborder="0"></iframe>""",
    """<iframe src="https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=1747328457815&to=1747350057815&timezone=browser&panelId=11&__feature.dashboardSceneSolo" width="450" height="200" frameborder="0"></iframe>"""
]

# Mostrar los iframes en una grilla 2 columnas x 3 filas
cols = st.columns(2)

for i in range(6):
    with cols[i % 2]:
        components.html(iframes[i], height=220)

