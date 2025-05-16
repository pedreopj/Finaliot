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
    
    if isinstance(result, list):
        df = pd.concat(result)
    else:
        df = result
    
    if df.empty:
        return pd.DataFrame()
    
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
    
    if isinstance(result, list):
        df = pd.concat(result)
    else:
        df = result
    
    if df.empty:
        return pd.DataFrame()
    
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

# Mostrar datos crudos de InfluxDB (airSensor)
st.markdown("### Datos crudos desde InfluxDB (airSensor, últimos 60 minutos)")

df_air = query_raw_data(60)

if df_air.empty:
    st.write("No hay datos recientes para mostrar de airSensor.")
else:
    pivot_air = df_air.pivot(index="time", columns="field", values="value")
    st.dataframe(pivot_air)

# Mostrar datos crudos de InfluxDB (uv_sensor)
st.markdown("### Datos crudos desde InfluxDB (uv_sensor, últimos 60 minutos)")

df_uv = query_uv_data(60)

if df_uv.empty:
    st.write("No hay datos recientes para mostrar de uv_sensor.")
else:
    pivot_uv = df_uv.pivot(index="time", columns="field", values="value")
    st.dataframe(pivot_uv)

# Recomendaciones automatizadas
st.markdown("### Recomendaciones automatizadas para el cuidado de los microcultivos")

if not df_air.empty and not df_uv.empty:
    latest_humidity = pivot_air['humidity'].iloc[-1]
    latest_uv_raw = pivot_uv['uv_raw'].iloc[-1]
    
    if latest_humidity < 40:
        st.write("- La humedad está baja. **Recomendación:** Regar los cultivos.")
    else:
        st.write("- La humedad está en un nivel adecuado.")
    
    if latest_uv_raw > 200:
        st.write("- La radiación UV es alta. **Recomendación:** Proteger los cultivos con sombra.")
    else:
        st.write("- La radiación UV es baja o moderada.")
else:
    st.write("No hay datos suficientes para generar recomendaciones.")


