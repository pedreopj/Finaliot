import streamlit as st
import pandas as pd
from influxdb_client import InfluxDBClient

# Configuración de la app
st.set_page_config(page_title="🌱 Microcultivo - Datos Reales", layout="wide")
st.title("📊 Datos Reales desde InfluxDB - Microcultivo IoT")
st.markdown("Consulta de los últimos datos de sensores desde la base de datos.")

# Conexión a InfluxDB
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
token = "rnRx-Nk8dXeumEsQeDT4hk78QFWNTOVim7UrH5fnYKVSoQQIkhCwKq03-UMKN-S0Nj-DbfmrMD0HUI61qRJaiw=="
org = "0925ccf91ab36478"
bucket = "homeiot"

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# Consulta Flux
query = f'''
from(bucket: "{bucket}")
  |> range(start: -24h)
  |> filter(fn: (r) => r["_measurement"] == "sensor_data")
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> sort(columns: ["_time"])
'''

# Ejecutar la consulta
try:
    result = query_api.query_data_frame(org=org, query=query)
    if isinstance(result, list):
        df = pd.concat(result)
    else:
        df = result

    df = df.rename(columns={"_time": "Tiempo"}).set_index("Tiempo")
    st.success("✅ Datos cargados exitosamente.")
    st.dataframe(df.tail(50))  # Mostrar últimos 50 datos

    # Mostrar algunas estadísticas básicas
    st.subheader("📈 Estadísticas generales")
    st.write(df.describe())

except Exception as e:
    st.error(f"❌ Error al consultar InfluxDB: {e}")


