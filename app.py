from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import streamlit as st

# Configura tus credenciales
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
token = "TrnRx-Nk8dXeumEsQeDT4hk78QFWNTOVim7UrH5fnYKVSoQQIkhCwKq03-UMKN-S0Nj-DbfmrMD0HUI61qRJaiw=="
org = "0925ccf91ab36478"
bucket = "homeiot"

# Crea cliente
client = InfluxDBClient(url=url, token=token, org=org)

# Escribe tu consulta Flux (ejemplo: últimos 24h de datos)
query = f'''
from(bucket: "{bucket}")
  |> range(start: -24h)
  |> filter(fn: (r) => r["_measurement"] == "sensor_data")
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> sort(columns: ["_time"])
'''

# Ejecuta la consulta y convierte a DataFrame
query_api = client.query_api()
tables = query_api.query_data_frame(org=org, query=query)

# Unifica los resultados si vienen divididos por tabla
if isinstance(tables, list):
    data = pd.concat(tables)
else:
    data = tables

# Opcional: formatea tiempo como índice
data = data.rename(columns={"_time": "Tiempo"}).set_index("Tiempo")

st.title("🌿 Datos Reales desde InfluxDB")
st.dataframe(data.tail(50))  # Mostrar los últimos 50 datos


