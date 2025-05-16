import streamlit as st
import pandas as pd
from influxdb_client import InfluxDBClient
import matplotlib.pyplot as plt

# Configuración InfluxDB
INFLUX_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN = "rnRx-Nk8dXeumEsQeDT4hk78QFWNTOVim7UrH5fnYKVSoQQIkhCwKq03-UMKN-S0Nj-DbfmrMD0HUI61qRJaiw=="
ORG = "0925ccf91ab36478"
BUCKET = "homeiot"

def query_data(measurement, fields, range_minutes=60):
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)
    query_api = client.query_api()
    fields_filter = " or ".join([f'r._field == "{f}"' for f in fields])
    
    query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: -{range_minutes}m)
      |> filter(fn: (r) => r._measurement == "{measurement}")
      |> filter(fn: (r) => {fields_filter})
    '''
    
    result = query_api.query_data_frame(query)
    
    if result is None:
        return pd.DataFrame()
    if isinstance(result, list) and len(result) == 0:
        return pd.DataFrame()
    
    df = pd.concat(result) if isinstance(result, list) else result
    
    if df.empty:
        return pd.DataFrame()
    
    df = df.rename(columns={"_time": "time", "_field": "field", "_value": "value"})
    return df[["time", "field", "value"]]

st.set_page_config(page_title="Microcultivo Dashboard 🌿", layout="wide")

st.title("🌿 Recomendaciones para el cuidado de los Microcultivos")

grafana_url = "https://pelaezescobarpepo.grafana.net/public-dashboards/134b2fe792144aacaba5fed6a61d18ae"
st.info(f'Debido a políticas de seguridad, el panel no puede mostrarse aquí directamente. [Abrir Grafana]({grafana_url})', icon="🔗")

# Consultar datos
df_air = query_data("airSensor", ["heat_index", "humidity", "temperature"])
df_uv = query_data("uv_sensor", ["uv_index", "uv_raw"])

pivot_air = None
pivot_uv = None

if df_air.empty and df_uv.empty:
    st.warning("No hay datos recientes para mostrar.")
else:
    if not df_air.empty:
        pivot_air = df_air.pivot(index="time", columns="field", values="value")
    if not df_uv.empty:
        pivot_uv = df_uv.pivot(index="time", columns="field", values="value")
    
    # Mostrar métricas principales en columnas
    col1, col2, col3 = st.columns(3)

    if pivot_air is not None:
        humedad_ultimo = pivot_air["humidity"].iloc[-1] if "humidity" in pivot_air.columns and not pivot_air["humidity"].empty else None
        temp_ultimo = pivot_air["temperature"].iloc[-1] if "temperature" in pivot_air.columns and not pivot_air["temperature"].empty else None
        heat_index_ultimo = pivot_air["heat_index"].iloc[-1] if "heat_index" in pivot_air.columns and not pivot_air["heat_index"].empty else None
    else:
        humedad_ultimo = temp_ultimo = heat_index_ultimo = None

    if pivot_uv is not None:
        uv_index_ultimo = pivot_uv["uv_index"].iloc[-1] if "uv_index" in pivot_uv.columns and not pivot_uv["uv_index"].empty else None
    else:
        uv_index_ultimo = None

    with col1:
        if humedad_ultimo is not None:
            st.metric(label="💧 Humedad (%)", value=f"{humedad_ultimo:.1f}")
        else:
            st.write("No hay datos de humedad.")

    with col2:
        if temp_ultimo is not None:
            st.metric(label="🌡 Temperatura (°C)", value=f"{temp_ultimo:.1f}")
        else:
            st.write("No hay datos de temperatura.")

    with col3:
        try:
            # Intentar convertir el valor a float y redondear
            uv_value = float(uv_index_ultimo)
            st.metric(label="👏 Índice UV", value=f"{uv_value:.1f}")
        except (TypeError, ValueError):
            st.write("No hay datos UV válidos.")

    # Gráficos de tendencias
    st.markdown("---")
    st.subheader("📈 Tendencias recientes")

    if pivot_air is not None:
        fig, ax = plt.subplots(figsize=(10, 3))
        for field in ["temperature", "humidity", "heat_index"]:
            if field in pivot_air.columns:
                ax.plot(pivot_air.index, pivot_air[field], label=field.capitalize())
        ax.set_ylabel("Valor")
        ax.legend()
        st.pyplot(fig)
    else:
        st.write("No hay datos para graficar del sensor de aire.")

    # Recomendaciones (solo humedad)
    st.markdown("---")
    st.subheader("🌱 Recomendaciones")

    if humedad_ultimo is not None:
        if humedad_ultimo < 40:
            st.error("💧 La humedad está baja. Se recomienda regar los microcultivos.")
        else:
            st.success("🌱 La humedad está adecuada.")
    else:
        st.warning("No hay datos de humedad para evaluar recomendaciones.")
