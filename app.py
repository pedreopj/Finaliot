import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="🌿 Microcultivo Inteligente", layout="wide")

st.markdown("""
    <style>
    .title-container {
        text-align: center;
        padding: 1.5rem 0;
    }
    .section {
        background-color: #f9f9f9;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown("<div class='title-container'><h1>🌿 Panel de Monitoreo para Microcultivo Urbano</h1><p>Cuida tu cultivo con datos en tiempo real y recomendaciones automáticas</p></div>", unsafe_allow_html=True)

# Simulador de datos (esto luego se reemplaza por datos reales desde InfluxDB)
data = pd.DataFrame({
    "Hora": pd.date_range(end=pd.Timestamp.now(), periods=24, freq="H"),
    "Humedad (%)": np.random.randint(30, 80, 24),
    "Temperatura (°C)": np.random.uniform(18, 32, 24),
    "Radiación UV": np.random.uniform(0, 10, 24)
})

# --- Sección: Datos crudos
st.markdown("### 📊 Datos Recogidos")
with st.container():
    st.dataframe(data, use_container_width=True)

# --- Sección: Análisis estadístico
st.markdown("### 📈 Análisis Estadístico")
with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🌡️ Temp. Promedio", f"{data['Temperatura (°C)'].mean():.1f} °C")
        st.metric("📉 Mínima", f"{data['Temperatura (°C)'].min():.1f} °C")
    
    with col2:
        st.metric("💧 Humedad Promedio", f"{data['Humedad (%)'].mean():.1f} %")
        st.metric("📈 Máxima", f"{data['Humedad (%)'].max():.1f} %")

    with col3:
        st.metric("☀️ Radiación UV Promedio", f"{data['Radiación UV'].mean():.1f}")
        st.metric("🔆 Máxima UV", f"{data['Radiación UV'].max():.1f}")

# --- Sección: Recomendaciones
st.markdown("### 🧠 Recomendaciones Automatizadas")
with st.container():
    last = data.iloc[-1]
    recomendaciones = []

    if last["Humedad (%)"] < 40:
        recomendaciones.append("💧 La humedad está baja. Se recomienda regar el cultivo.")
    if last["Radiación UV"] > 7:
        recomendaciones.append("🌞 La radiación UV es alta. Coloca sombra para proteger las plantas.")
    if last["Temperatura (°C)"] > 30:
        recomendaciones.append("🔥 La temperatura está elevada. Asegura una buena ventilación.")

    if recomendaciones:
        for rec in recomendaciones:
            st.success(rec)
    else:
        st.info("✅ Las condiciones actuales son óptimas para tu microcultivo.")

# --- Pie
st.markdown("---")
st.markdown("<p style='text-align:center; color: gray;'>Sistema de monitoreo automatizado para agricultura urbana 🌱</p>", unsafe_allow_html=True)


# --- Pie
st.markdown("---")
st.markdown("<p style='text-align:center; color: gray;'>Sistema de monitoreo automatizado para agricultura urbana 🌱</p>", unsafe_allow_html=True)

