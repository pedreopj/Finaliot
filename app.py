import streamlit as st
import streamlit.components.v1 as components
from influxdb_client import InfluxDBClient
import pandas as pd

# Configuración InfluxDB
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
token = "rnRx-Nk8dXeumEsQeDT4hk78QFWNTOVim7UrH5fnYKVSoQQIkhCwKq03-UMKN-S0Nj-DbfmrMD0HUI61qRJaiw=="
org = "0925ccf91ab36478"
bucket = "homeiot"

st.set_page_config(page_title="Microcultivo Dashboard", layout="wide")

st.title("🌱 Monitoreo Ambiental de Microcultivo Urbano")
st.markdown("Visualización en tiempo real desde Grafana y datos crudos desde InfluxDB.")

# Lista con los iframes de los 6 paneles de Grafana
grafana_iframes = [
    "https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=now-6h&to=now&timezone=browser&panelId=6",
    "https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=now-6h&to=now&timezone=browser&panelId=3",
    "https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=now-6h&to=now&timezone=browser&panelId=5",
    "https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=now-6h&to=now&timezone=browser&panelId=1",
    "https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=now-6h&to=now&timezone=browser&panelId=4",
    "https://pelaezescobarpepo.grafana.net/d-solo/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=now-6h&to=now&timezone=browser&panelId=2"
]

# Mostrar los 6 cuadros de Grafana en dos filas de 3 columnas cada una
for i in range(0, 6, 3):
    cols = st.columns(3)
    for idx, col in enumerate(cols):
        url = grafana_iframes[i + idx]
        iframe_code = f'<iframe src="{url}" width="450" height="200" frameborder="0"></iframe>'
        col.markdown(iframe_code, unsafe_allow_html=True)

st.markdown("---")
st.header("Datos Crudos desde InfluxDB")

try:
    client = InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()

    query = f'''
    from(bucket:"{bucket}")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "microcultivo")
      |> filter(fn: (r) => r._field == "humidity" or r._field == "temperature" or r._field == "uv_raw")
      |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
      |> keep(columns: ["_time", "humidity", "temperature", "uv_raw"])
      |> sort(columns: ["_time"])
    '''

    result = query_api.query_data_frame(org=org, query=query)

    if isinstance(result, list):
        df = pd.concat(result)
    else:
        df = result

    df = df.rename(columns={"_time": "time"})
    st.dataframe(df)

except Exception as e:
    st.error(f"❌ Error al consultar InfluxDB: {e}")
