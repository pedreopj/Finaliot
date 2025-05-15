import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="🌦️ Dashboard IoT del Clima", layout="wide")

st.markdown("""
    <style>
    .grafana-frame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌦️ Dashboard IoT del Clima")
st.markdown("Visualización embebida de datos en tiempo real desde Grafana.")

# URL base para evitar repetir
grafana_base = "https://miguelcmo.grafana.net/d-solo/aehqn58kr54aof/home-iot-weather-conditions"
common_params = "?orgId=1&from=now-6h&to=now&timezone=browser&refresh=10s"

# Lista de paneles con títulos personalizados
paneles = [
    ("🌡️ Temperatura", 1),
    ("💧 Humedad", 2),
    ("🌬️ Velocidad del viento", 3),
    ("☀️ Radiación UV", 4),
    ("🌫️ Presión atmosférica", 5),
    ("🌧️ Probabilidad de lluvia", 6),
]

# Mostrar 2 columnas con 3 filas de paneles
for i in range(0, len(paneles), 2):
    col1, col2 = st.columns(2)

    with col1:
        titulo1, id1 = paneles[i]
        st.subheader(titulo1)
        components.html(
            f"""
            <div class="grafana-frame">
                <iframe src="{grafana_base}{common_params}&panelId={id1}&__feature.dashboardSceneSolo"
                        width="100%" height="220" frameborder="0"></iframe>
            </div>
            """,
            height=240
        )

    if i + 1 < len(paneles):
        with col2:
            titulo2, id2 = paneles[i + 1]
            st.subheader(titulo2)
            components.html(
                f"""
                <div class="grafana-frame">
                    <iframe src="{grafana_base}{common_params}&panelId={id2}&__feature.dashboardSceneSolo"
                            width="100%" height="220" frameborder="0"></iframe>
                </div>
                """,
                height=240
            )

# Nota de seguridad (opcional)
st.markdown("""
<p style='text-align:center; color: gray; font-size: 0.9rem'>
🔐 Si no ves los gráficos correctamente, revisa que tengas acceso al panel de Grafana desde tu navegador.<br>
También puedes <a href='https://miguelcmo.grafana.net/d/aehqn58kr54aof/home-iot-weather-conditions' target='_blank'>abrir el dashboard completo aquí</a>.
</p>
""", unsafe_allow_html=True)

# --- Pie
st.markdown("---")
st.markdown("<p style='text-align:center; color: gray;'>Sistema de monitoreo automatizado para agricultura urbana 🌱</p>", unsafe_allow_html=True)

