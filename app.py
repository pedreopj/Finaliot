import streamlit as st
import pandas as pd
from influxdb_client import InfluxDBClient

# Configuración
st.set_page_config(page_title="🌱 Microcultivo - Datos Reales", layout="wide")
st.title("📊 Datos Reales desde InfluxDB - Microcultivo IoT")
st.markdown("Visualización de temperatura, calor, humedad y radiación UV en los últimos datos registrados.")

# Parámetros de conexión
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
token = "rnRx-Nk8dXeumEsQeDT4hk78QFWNTOVim7UrH5fnYKVSoQQIkhCwKq03-UMKN-S0Nj-DbfmrMD0HUI61qRJaiw=="
org = "0925ccf91ab36478"
bucket = "homeiot"

# Conexión a InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# Consulta Flux adaptada
query = f'''
from(bucket: "{bucket}")
  |> range(start: -24h)
  |> filter(fn: (r) =>
    r["_measurement"] == "sensor_data" and
    (r["_field"] == "temperatura" or
     r["_field"] == "calor" or
     r["_field"] == "humedad" or
     r["_field"] == "uv_raw"))
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> sort(columns: ["_time"])
'''

# Ejecutar y procesar
try:
    result = query_api.query_data_frame(org=org, query=query)

    # Asegurar que es DataFrame válido
    if isinstance(result, list):
        df = pd.concat(result)
    else:
        df = result

    if "_time" not in df.columns:
        st.error("❌ No se encontró la columna `_time`. Revisa la estructura de la medición.")
    else:
        df = df.rename(columns={"_time": "Tiempo"}).set_index("Tiempo")
        campos = ["temperatura", "calor", "humedad", "uv_raw"]
        df = df[[c for c in campos if c in df.columns]]  # Solo columnas existentes

        st.success("✅ Datos cargados exitosamente.")
        st.dataframe(df.tail(50))

        st.subheader("📈 Estadísticas básicas")
        st.write(df.describe())

except Exception as e:
    st.error(f"❌ Error al consultar InfluxDB: {e}")


except Exception as e:
    st.error(f"❌ Error al consultar InfluxDB: {e}")


