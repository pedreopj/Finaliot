import streamlit as st

st.title("Dashboard Microcultivo")

paneles = [
    ("Temperatura vs UV", "https://pelaezescobarpepo.grafana.net/d/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=2025-05-15T17:00:57.815Z&to=2025-05-15T23:00:57.815Z&timezone=browser&viewPanel=panel-6"),
    ("Humedad", "https://pelaezescobarpepo.grafana.net/d/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=2025-05-15T17:00:57.815Z&to=2025-05-15T23:00:57.815Z&timezone=browser&viewPanel=panel-3"),
    ("Rayos UV", "https://pelaezescobarpepo.grafana.net/d/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=2025-05-15T17:00:57.815Z&to=2025-05-15T23:00:57.815Z&timezone=browser&viewPanel=panel-5"),
    ("Humedad, Temperatura y Calor", "https://pelaezescobarpepo.grafana.net/d/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=2025-05-15T17:00:57.815Z&to=2025-05-15T23:00:57.815Z&timezone=browser&viewPanel=panel-1"),
    ("Temperatura", "https://pelaezescobarpepo.grafana.net/d/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=2025-05-15T17:00:57.815Z&to=2025-05-15T23:00:57.815Z&timezone=browser&viewPanel=panel-4"),
    ("Calor", "https://pelaezescobarpepo.grafana.net/d/65d15f92-4084-4ea5-ac44-a08c4c2e16cf/trabajo-final?orgId=1&from=2025-05-15T17:00:57.815Z&to=2025-05-15T23:00:57.815Z&timezone=browser&viewPanel=panel-2"),
]

cols = st.columns(2)

for i, (titulo, url) in enumerate(paneles):
    with cols[i % 2]:
        st.markdown(f"### {titulo}")
        st.markdown(
            f"""
            Debido a políticas de seguridad, el panel no puede mostrarse aquí directamente.  
            [Haz clic aquí para abrir el panel en una nueva pestaña.]({url})
            """,
            unsafe_allow_html=True,
        )



except Exception as e:
    st.error(f"❌ Error al consultar InfluxDB: {e}")
