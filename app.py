def query_air_sensor_data(range_minutes=60):
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)
    query_api = client.query_api()

    query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: -{range_minutes}m)
      |> filter(fn: (r) => r._measurement == "airSensor")
      |> filter(fn: (r) => r._field == "heat_index" or r._field == "humidity" or r._field == "temperature")
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
      |> filter(fn: (r) => r._field == "uv_index" or r._field == "uv_raw")
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

