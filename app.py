import streamlit as st
import pandas as pd
from influxdb_client import InfluxDBClient

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

st.title("Dashboard Microcultivo")

grafana_url = "https://pelaezescobarpepo.grafana.net/public-dashboards/134b2fe792144aacaba5fed6a61d18ae"
st.markdown(
    f"""### Panel Público Grafana  
    Debido a políticas de seguridad, el panel no puede mostrarse aquí directamente.  
    [Haz clic aquí para abrir el panel en una nueva pestaña.]({grafana_url})
    """,
    unsafe_allow_html=True,
)

df_air = query_data("airSensor", ["heat_index", "humidity", "temperature"])
df_uv = query_data("uv_sensor", ["uv_index", "uv_raw"])

if df_air.empty and df_uv.empty:
    st.write("No hay datos recientes para mostrar.")
else:
    if not df_air.empty:
        pivot_air = df_air.pivot(index="time", columns="field", values="value")
        st.markdown("#### Datos aire (temperatura, humedad, heat index)")
        st.dataframe(pivot_air)
    else:
        st.write("No hay datos recientes del sensor de aire.")

    if not df_uv.empty:
        pivot_uv = df_uv.pivot(index="time", columns="field", values="value")
        st.markdown("#### Datos UV (uv_index, uv_raw)")
        st.dataframe(pivot_uv)
    else:
        st.write("No hay datos recientes del sensor UV.")

    st.markdown("### Recomendaciones para el cuidado de los microcultivos")

    humedad_ultimo = pivot_air["humidity"].iloc[-1] if "humidity" in pivot_air.columns and not pivot_air["humidity"].empty else None
    uv_index_ultimo = pivot_uv["uv_index"].iloc[-1] if "uv_index" in pivot_uv.columns and not pivot_uv["uv_index"].empty else None

    if humedad_ultimo is not None and humedad_ultimo < 40:
        st.write("💧 La humedad está baja. Se recomienda regar los microcultivos.")
    elif humedad_ultimo is not None:
        st.write("🌱 La humedad está adecuada.")
    else:
        st.write("No hay datos de humedad para evaluar recomendaciones.")

    if uv_index_ultimo is not None and uv_index_ultimo > 6:
        st.write("🛡️ La radiación UV es alta. Se recomienda proteger los cultivos con sombra.")
    elif uv_index_ultimo is not None:
        st.write("☀️ La radiación UV está en niveles seguros.")
    else:
        st.write("No hay datos de radiación UV para evaluar recomendaciones.")

        st.write("☀️ La radiación UV está en niveles seguros.")
