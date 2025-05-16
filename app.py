import streamlit as st
import pandas as pd
from influxdb_client import InfluxDBClient

# Configuración InfluxDB
INFLUX_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN = "rnRx-Nk8dXeumEsQeDT4hk78QFWNTOVim7UrH5fnYKVSoQQIkhCwKq03-UMKN-S0Nj-DbfmrMD0HUI61qRJaiw=="
ORG = "0925ccf91ab36478"
BUCKET = "homeiot"

def query_raw_data(range_minutes=60):
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)
    query_api = client.query_api()
    
    query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: -{range_minutes}m)
      |> filter(fn: (r) => r._measurement == "airSensor")
      |> filter(fn: (r) => r._field == "heat_index" or r._field == "humidity" or r._field == "temperature")
    '''
    
    result = query_api.query_data_frame(query)
    if not result or (isinstance(result, list) and len(result) == 0):
        return pd.DataFrame()
    else:
        if isinstance(result, list):
            df = pd.concat(result)
        else:
            df = result
        
        df = df.rename(columns={"_time": "time", "_field": "field", "_value": "value"})
        df = df[["time", "field", "value"]]
        return df

def query_uv_data(range_minutes=60):
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)
    query_api = client.query_api()
    
    query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: -{range_minutes}m)
      |> filter(fn: (r) => r._measurement == "uv_sensor")
      |> filter(fn: (r) => r._field == "uv_index" or r._field == "uv_raw")
    '''
    
    result = query_api.query_data_frame(query)
    if not result or (isinstance(result, list) and len(result) == 0):
        return pd.DataFrame()
    else:
        if isinstance(result, list):
            df = pd.concat(result)
        else:
            df = result
        
        df = df.rename(columns={"_time": "time", "_field": "field", "_value": "value"})
        df = df[["time", "field", "value"]]
        return df

# Streamlit app
st.title("Dashboard Microcultivo")

# Mostrar solo el panel público de Grafana
grafana_url = "https://pelaezescobarpepo.grafana.net/public-dashboards/134b2fe792144aacaba5fed6a61d18ae"

st.markdown(
    f"""
    ### Panel Público Grafana  
    Debido a políticas de seguridad, el panel no puede mostrarse aquí directamente.  
    [Haz clic aquí para abrir el panel en una nueva pestaña.]({grafana_url})
    """,
    unsafe_allow_html=True,
)

# Mostrar datos crudos de InfluxDB
st.markdown("### Datos crudos desde InfluxDB (últimos 60 minutos)")

df_air = query_raw_data(60)
df_uv = query_uv_data(60)

if df_air.empty:
    st.write("No hay datos recientes de temperatura, humedad o calor para mostrar.")
else:
    pivot_air = df_air.pivot(index="time", columns="field", values="value")
    st.dataframe(pivot_air)

if df_uv.empty:
    st.write("No hay datos recientes de radiación UV para mostrar.")
else:
    pivot_uv = df_uv.pivot(index="time", columns="field", values="value")
    st.dataframe(pivot_uv)

# Recomendaciones automáticas

# Últimos valores (tomamos el último valor disponible en cada dataframe)
humedad_ultimo = None
uv_index_ultimo = None

if not df_air.empty:
    df_air_sorted = df_air.sort_values("time")
    humedad_ultimo = df_air_sorted[df_air_sorted["field"] == "humidity"]["value"].iloc[-1] if not df_air_sorted[df_air_sorted["field"] == "humidity"].empty else None

if not df_uv.empty:
    df_uv_sorted = df_uv.sort_values("time")
    uv_index_ultimo = df_uv_sorted[df_uv_sorted["field"] == "uv_index"]["value"].iloc[-1] if not df_uv_sorted[df_uv_sorted["field"] == "uv_index"].empty else None

st.markdown("### Recomendaciones para el cuidado del microcultivo")

if humedad_ultimo is not None and not pd.isna(humedad_ultimo):
    if humedad_ultimo < 40:  # Umbral ejemplo, ajusta según necesidad
        st.write("💧 La humedad está baja. Se recomienda regar los microcultivos.")
    else:
        st.write("🌱 La humedad está adecuada.")
else:
    st.write("No hay datos de humedad para evaluar recomendaciones.")

if uv_index_ultimo is not None and not pd.isna(uv_index_ultimo):
    if uv_index_ultimo > 6:  # Umbral ejemplo de UV alto
        st.write("🛡️ La radiación UV es alta. Se recomienda proteger los cultivos con sombra.")
    else:
        st.write("☀️ La radiación UV está en niveles seguros.")
else:
    st.write("No hay datos de radiación UV para evaluar recomendaciones.")
    else:
        st.write("No hay datos de radiación UV para evaluar recomendaciones.")

