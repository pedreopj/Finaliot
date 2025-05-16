import streamlit as st
import pandas as pd
from influxdb_client import InfluxDBClient

# Parámetros InfluxDB (ajusta según tu configuración)
INFLUX_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN = "tu-token-aqui"
ORG = "0925ccf91ab36478"
BUCKET = "homeiot"

def query_air_sensor_data(range_minutes=60):
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)
    query_api = client.query_api()

    query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: -{range_minutes}m)
      |> filter(fn: (r) => r._measurement == "airSensor")
      |> filter(fn: (r) => r._field == "humidity" or r._field == "temperature" or r._field == "heat_index")
    '''

    result = query_api.query_data_frame(query)

    if isinstance(result, list):
        if len(result) == 0:
            return pd.DataFrame()
        df = pd.concat(result)
    elif hasattr(result, "empty"):
        if result.empty:
            return pd.DataFrame()
        df = result
    else:
        return pd.DataFrame()

    df = df.rename(columns={"_time": "time", "_field": "field", "_value": "value"})
    df = df[["time", "field", "value"]]
    return df

def query_uv_sensor_data(range_minutes=60):
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)
    query_api = client.query_api()

    query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: -{range_minutes}m)
      |> filter(fn: (r) => r._measurement == "uv_sensor")
      |> filter(fn: (r) => r._field == "uv_raw" or r._field == "uv_index")
    '''

    result = query_api.query_data_frame(query)

    if isinstance(result, list):
        if len(result) == 0:
            return pd.DataFrame()
        df = pd.concat(result)
    elif hasattr(result, "empty"):
        if result.empty:
            return pd.DataFrame()
        df = result
    else:
        return pd.DataFrame()

    df = df.rename(columns={"_time": "time", "_field": "field", "_value": "value"})
    df = df[["time", "field", "value"]]
    return df

# Streamlit UI
st.title("Dashboard Microcultivo")

# Consultar datos
df_air = query_air_sensor_data()
df_uv = query_uv_sensor_data()

st.subheader("Datos crudos de sensores")
st.write("Datos aire:", df_air)
st.write("Datos UV:", df_uv)

# Extraer valores actuales (últimos registros)
humidity = None
uv_raw = None

if not df_air.empty:
    humid_df = df_air[df_air["field"] == "humidity"]
    if not humid_df.empty:
        humidity = humid_df.iloc[-1]["value"]

if not df_uv.empty:
    uv_df = df_uv[df_uv["field"] == "uv_raw"]
    if not uv_df.empty:
        uv_raw = uv_df.iloc[-1]["value"]

st.subheader("Recomendaciones para el cuidado del microcultivo")

if humidity is not None:
    st.write(f"Humedad actual: {humidity:.2f}%")
    if humidity < 40:
        st.warning("La humedad está baja. Se recomienda **regar** los cultivos.")
    else:
        st.success("La humedad está en un nivel adecuado.")

else:
    st.info("No se encontraron datos de humedad.")

if uv_raw is not None:
    st.write(f"Radiación UV actual (raw): {uv_raw:.2f}")
    if uv_raw > 200:
        st.warning("La radiación UV es alta. Se recomienda **proteger los cultivos con sombra**.")
    else:
        st.success("La radiación UV está en un nivel seguro.")

else:
    st.info("No se encontraron datos de radiación UV.")

