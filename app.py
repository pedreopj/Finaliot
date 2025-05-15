import streamlit as st
import streamlit.components.v1 as components

# Configuración de página
st.set_page_config(page_title="🌱 Microcultivo Dashboard", layout="wide")

# Estilos personalizados usando HTML y CSS
st.markdown("""
    <style>
    body {
        background-color: #f4f6f6;
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
    }
    .title-container {
        text-align: center;
        padding: 2rem 0;
    }
    .grafana-frame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Título y subtítulo centrados
st.markdown("<div class='title-container'><h1>🌱 Monitoreo Ambiental de Microcultivo Urbano</h1><p>Visualización en tiempo real de datos ambientales desde Grafana</p></div>", unsafe_allow_html=True)

# Crear dos columnas para futuras expansiones (como más gráficas)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💧 Humedad del Suelo")
    components.html(
        """
        <div class="grafana-frame">
        <iframe src="https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=1747328457815&to=1747350057815&timezone=browser&panelId=6&__feature.dashboardSceneSolo"
            width="100%" height="200" frameborder="0"></iframe>
        </div>
        """,
        height=220
    )

with col2:
    st.subheader("🌡️ Temperatura Ambiental")
    # Puedes cambiar el panelId según otro gráfico que tengas
    components.html(
        """
        <div class="grafana-frame">
        <iframe src="https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=1747328457815&to=1747350057815&timezone=browser&panelId=8&__feature.dashboardSceneSolo"
            width="100%" height="200" frameborder="0"></iframe>
        </div>
        """,
        height=220
    )

# Pie de página o mensaje motivacional
st.markdown("---")
st.markdown("<p style='text-align:center; color: gray;'>Conectando naturaleza y tecnología para un futuro más verde 🌍</p>", unsafe_allow_html=True)


