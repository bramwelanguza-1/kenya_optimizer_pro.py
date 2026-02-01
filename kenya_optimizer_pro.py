import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium # Swapped to st_folium for speed
import math
import random

# --- 1. DATA FIRST ---
if "fiber_cut" not in st.session_state:
    st.session_state.fiber_cut = False

data = {
    'City': ['Nairobi (KIXP)', 'Mombasa (KIXP)', 'Kisumu (KIXP)', 'Eldoret (KIXP)'],
    'Lat': [-1.286, -4.043, -0.091, 0.514],
    'Lon': [36.817, 39.668, 34.767, 35.269],
    'Load %': [random.randint(50, 85) for _ in range(4)]
}
df = pd.DataFrame(data)

# --- 2. FUNCTIONS ---
def calculate_metrics(load_percent):
    B = 20 * 1e6 
    snr_db = 30 - (load_percent / 5) 
    snr_linear = 10**(snr_db / 10)
    cap = (B * math.log2(1 + snr_linear)) / 1e6
    eff = math.log2(1 + snr_linear)
    return snr_db, cap, eff

# --- 3. LOGIC ---
if st.session_state.fiber_cut:
    df.loc[df['City'] == 'Mombasa (KIXP)', 'Load %'] = 100
    df.loc[df['City'] == 'Nairobi (KIXP)', 'Load %'] += 20
    reroute = [[-4.04, 39.6], [-3.39, 38.5], [-1.28, 36.8]]
else:
    reroute = []

# --- 4. UI ---
st.set_page_config(layout="wide")
st.title("🇰🇪 KenyaNet AI Optimizer")

col1, col2 = st.columns([2, 1])

with col1:
    m = folium.Map(location=[-1.28, 36.8], zoom_start=6)
    for i, r in df.iterrows():
        folium.CircleMarker([r['Lat'], r['Lon']], radius=8, color='red' if r['Load %'] > 90 else 'green').add_to(m)
    if reroute:
        folium.PolyLine(reroute, color="yellow", weight=5).add_to(m)
    
    # NEW: Faster rendering component
    st_folium(m, width=700, height=500)

with col2:
    if st.button("💥 Toggle Stress Test"):
        st.session_state.fiber_cut = not st.session_state.fiber_cut
        st.rerun()
    
    target = df.iloc[df['Load %'].idxmax()]
    snr, cap, eff = calculate_metrics(target['Load %'])
    st.metric("Signal Stability", f"{round(snr, 1)} dB")
    st.metric("Capacity", f"{round(cap, 1)} Mbps")
    st.info(f"Current Efficiency: {round(eff, 2)} bits/Hz")
