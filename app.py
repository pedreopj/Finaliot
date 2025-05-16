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
    if result.empty:
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
    if result.empty:
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

# Mostrar datos crudos de aire
st.markdown("### Datos crudos desde InfluxDB (últimos 60 minutos) - aire")
df_air = query_raw_data(60)
if df_air.empty:
    st.write("No hay datos recientes para mostrar.")
else:
    pivot_air = df_air.pivot(index="time", columns="field", values="value")
    st.dataframe(pivot_air)

# Mostrar datos crudos UV
st.markdown("### Datos crudos desde InfluxDB (últimos 60 minutos) - radiación UV")
df_uv = query_uv_data(60)
if df_uv.empty:
    st.write("No hay datos recientes de UV para mostrar.")
else:
    pivot_uv = df_uv.pivot(index="time", columns="field", values="value")
    st.dataframe(pivot_uv)

# Recomendaciones automáticas
st.markdown("### Recomendaciones para el cuidado de los microcultivos")

humedad_promedio = pivot_air["humidity"].mean() if not df_air.empty and "humidity" in pivot_air else None
uv_promedio = pivot_uv["uv_raw"].mean() if not df_uv.empty and "uv_raw" in pivot_uv else None

if humedad_promedio is not None:
    if humedad_promedio < 40:
        st.warning(f"Humedad promedio baja ({humedad_promedio:.1f}%). Se recomienda regar los cultivos.")
    else:
        st.success(f"Humedad promedio adecuada ({humedad_promedio:.1f}%).")

else:
    st.info("No hay datos de humedad suficientes para recomendaciones.")

if uv_promedio is not None:
    if uv_promedio > 5:
        st.warning(f"Radiación UV alta ({uv_promedio:.1f}). Se recomienda proteger los cultivos con sombra.")
    else:
        st.success(f"Radiación UV adecuada ({uv_promedio:.1f}).")

else:
    st.info("No hay datos de radiación UV suficientes para recomendaciones.")

