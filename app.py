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
