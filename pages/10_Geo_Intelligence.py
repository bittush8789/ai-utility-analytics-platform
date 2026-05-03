import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils.auth_manager import verify_page_access, render_access_denied
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="Geo Intelligence", page_icon="🗺️", layout="wide")

# RBAC Check
if not verify_page_access("10_Geo_Intelligence"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🗺️ Geo Intelligence V2.0")
st.markdown("UK Geographic insights mapping utility activity across operational zones.")

@st.cache_data(ttl=3600)
def fetch_geo_data():
    try:
        conn = sqlite3.connect('utility_analytics.db')
        complaints = pd.read_sql("SELECT city, COUNT(*) as count FROM complaints GROUP BY city", conn)
        incidents = pd.read_sql("SELECT region, COUNT(*) as count FROM incidents GROUP BY region", conn)
        conn.close()
        return complaints, incidents
    except Exception:
        return pd.DataFrame(), pd.DataFrame()

complaints, incidents = fetch_geo_data()

uk_cities_lat_lon = {
    'London': {'lat': 51.5074, 'lon': -0.1278},
    'Manchester': {'lat': 53.4808, 'lon': -2.2426},
    'Birmingham': {'lat': 52.4862, 'lon': -1.8904},
    'Leeds': {'lat': 53.8008, 'lon': -1.5491},
    'Glasgow': {'lat': 55.8642, 'lon': -4.2518},
    'Bristol': {'lat': 51.4545, 'lon': -2.5879},
    'Liverpool': {'lat': 53.4084, 'lon': -2.9916},
    'Sheffield': {'lat': 53.3811, 'lon': -1.4701},
    'Newcastle': {'lat': 54.9783, 'lon': -1.6178},
    'Oxford': {'lat': 51.7520, 'lon': -1.2577}
}

if not complaints.empty:
    complaints['lat'] = complaints['city'].apply(lambda x: uk_cities_lat_lon.get(x, {}).get('lat', 54.0))
    complaints['lon'] = complaints['city'].apply(lambda x: uk_cities_lat_lon.get(x, {}).get('lon', -2.0))

add_global_ai_helper("Geo Intelligence V2.0", f"Mapping complaints across {len(complaints)} UK cities. High alert sectors identified in Manchester, London, and Bristol.")

c1, c2 = st.columns([3, 1])

with c1:
    if not complaints.empty:
        fig = px.scatter_mapbox(
            complaints, 
            lat="lat", 
            lon="lon", 
            size="count", 
            color="count",
            hover_name="city", 
            color_continuous_scale=px.colors.cyclical.IceFire, 
            size_max=35, 
            zoom=5,
            mapbox_style="carto-darkmatter",
            title="Geographic Alert Intensity Heatmap (UK Network & Cities)"
        )
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, height=550)
        st.plotly_chart(fig, use_container_width=True)
        render_ai_insight_popover("geo_map", "💡 Ask AI About Risk Clusters", f"Analyze geographic clusters across UK: {complaints.head(10).to_string(index=False)}")

with c2:
    st.markdown("### 🏷️ Regional Metrics")
    if not incidents.empty:
        st.dataframe(incidents.rename(columns={"region": "Network Zone", "count": "Incidents"}), use_container_width=True)
        render_ai_insight_popover("geo_table", "💡 Ask AI About Worst Zones", f"Operational zone incidents: {incidents.to_string(index=False)}")
    else:
        st.info("No data found.")
