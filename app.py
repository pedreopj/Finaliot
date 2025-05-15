import streamlit as st
import pandas as pd
from influxdb_client import InfluxDBClient

# Configuración visual
st.set_page_config(page_title="🌱 Microcultivo - Datos en Vivo", layout="wide")
st.title("🌡️ Panel IoT de Microcultivo")
st.markdown("Visualización de temperatura, calor, humedad y radiación UV capturada desde InfluxDB.")

# Parámetros de conexión
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
token = "rnRx-Nk8dXeumEsQeDT4hk78QFWNTOVim7UrH5fnYKVSoQQIkhCwKq03-UMKN-S0Nj-DbfmrMD0HUI61qRJaiw=="
org = "0925ccf91ab36478"
bucket = "homeiot"

# Conexión a InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# Consulta adaptada
query = f'''
from(bucket: "{bucket}")
  |> range(start: -24h)
  |> filter(fn: (r) =>
    r["_measurement"] == "sensor_data" and
    (r["_field"] == "temperatura" or
     r["_field"] == "calor" or
     r["_field"] == "humedad" or
     r["_field"] == "uv_raw"))
  |> pivot(rowKey:["time"], columnKey: ["_field"], valueColumn: "_value")
  |> sort(columns: ["time"])
'''

# Ejecutar
try:
    result = query_api.query_data_frame(org=org, query=query)

    if isinstance(result, list):
        df = pd.concat(result)
    else:
        df = result

    # Usar "time" como índice y limpiar columnas
    if "time" in df.columns:
        df = df.set_index("time")
        campos = ["temperatura", "calor", "humedad", "uv_raw"]
        campos_disponibles = [col for col in campos if col in df.columns]
        df = df[campos_disponibles]

        st.success("✅ Datos cargados correctamente.")
        st.dataframe(df.tail(50))

        st.subheader("📈 Análisis estadístico")
        st.write(df.describe())

        st.subheader("🤖 Recomendaciones automáticas")
        if "humedad" in df.columns and df["humedad"].iloc[-1] < 40:
            st.warning("💧 La humedad está baja. Se recomienda regar el cultivo.")
        if "uv_raw" in df.columns and df["uv_raw"].iloc[-1] > 700:
            st.warning("☀️ Radiación UV alta. Se recomienda proteger el cultivo con sombra.")
    else:
        st.error("❌ No se encontró la columna `time`. Revisa si el pivot funcionó correctamente.")

except Exception as e:
    st.error(f"❌ Error al consultar InfluxDB: {e}")


