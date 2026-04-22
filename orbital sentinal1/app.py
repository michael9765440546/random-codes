import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from skyfield.api import load, wgs84
from datetime import datetime

# ==========================================
# 1. SETUP & CONFIG
# ==========================================
st.set_page_config(page_title="Orbital Sentinel", page_icon="🛰️", layout="wide")

N2YO_API_KEY = "8BJV6K-FWTZ35-V955JT-5Q2L" 
USER_LAT = 27.67
USER_LON = 85.38
USER_ALT = 1320 

# ==========================================
# 2. DATA ENGINES
# ==========================================

# CHANGE: Using cache_resource because Skyfield objects can't be pickled
@st.cache_resource(ttl=3600)
def fetch_tle(group):
    """Downloads orbital data from CelesTrak."""
    url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=tle"
    try:
        # This returns a list of satellite objects
        return load.tle_file(url)
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def get_nepal_flyovers(norad_id):
    url = (f"https://www.n2yo.com/rest/v1/satellite/visualpasses/"
           f"{norad_id}/{USER_LAT}/{USER_LON}/{USER_ALT}/2/300/&apiKey={N2YO_API_KEY}")
    try:
        data = requests.get(url, timeout=10).json()
        return data.get('passes', [])
    except:
        return []

# ==========================================
# 3. THE INTERFACE
# ==========================================

def main():
    st.title("🛰️ Orbital Sentinel: Mission Control")
    st.sidebar.header("📡 Tracking Settings")
    
    category_map = {
        "Space Stations": "stations", 
        "Starlink": "starlink", 
        "Weather": "weather", 
        "Scientific": "science"
    }
    choice = st.sidebar.selectbox("Category", list(category_map.keys()))
    
    sats = fetch_tle(category_map[choice])
    
    if sats is None:
        st.warning("Establishing connection... Please check your data.")
        st.stop()
    
    sat_names = [s.name for s in sats]
    target_name = st.sidebar.selectbox("Target Satellite", sat_names)
    target_sat = {s.name: s for s in sats}[target_name]
    
    ts = load.timescale()
    t = ts.now()
    geocentric = target_sat.at(t)
    subpoint = wgs84.subpoint(geocentric)
    
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(f"Live Tracking: {target_name}")
        fig = go.Figure(go.Scattergeo(
            lat=[subpoint.latitude.degrees],
            lon=[subpoint.longitude.degrees],
            mode='markers+text',
            text=[target_name],
            marker=dict(size=14, color='cyan', symbol='cross')
        ))
        
        fig.update_geos(
            projection_type="orthographic",
            showocean=True, oceancolor="#00082b",
            showland=True, landcolor="#1a1a1a",
            showcountries=True, countrycolor="#444"
        )
        fig.update_layout(height=650, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📊 Telemetry")
        st.metric("Altitude", f"{subpoint.elevation.km:.2f} km")
        st.metric("Latitude", f"{subpoint.latitude.degrees:.2f}°")
        st.metric("Longitude", f"{subpoint.longitude.degrees:.2f}°")
        
        st.divider()
        
        st.subheader("🇳🇵 Nepal Flyovers")
        norad_id = target_sat.model.satnum
        passes = get_nepal_flyovers(norad_id)
        
        if passes:
            for p in passes:
                dt = datetime.fromtimestamp(p['startUTC']).strftime('%b %d, %H:%M')
                st.success(f"**{dt}**\nElev: {p['maxEl']}°")
        else:
            st.info("No visible passes for Thimi this week.")

    st.caption(f"Ground Station: Thimi | NORAD ID: {norad_id} | {t.utc_strftime('%H:%M:%S')} UTC")

if __name__ == "__main__":
    main()