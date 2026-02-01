import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import math
import random
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh # NEW: Add this to requirements.txt

# --- 1. CONFIG & AUTO-REFRESH ---
st.set_page_config(layout="wide", page_title="KenyaNet NOC - Live")

# This "pings" the app every 3000ms (3 seconds) to simulate live data flow
count = st_autorefresh(interval=3000, limit=100, key="network_tick")

# --- 2. PERSISTENT STATE ---
if "fiber_cut" not in st.session_state: st.session_state.fiber_cut = False
if "optimize" not in st.session_state: st.session_state.optimize = False

# --- 3. LIVE DATA SIMULATION ---
# We add "drift" so the numbers change slightly every 3 seconds
data = {
    'City': ['Nairobi (KIXP)', 'Mombasa (KIXP)', 'Kisumu (KIXP)', 'Eldoret (KIXP)'],
    'Lat': [-1.286, -4.043, -0.091, 0.514], 'Lon': [36.817, 39.668, 34.767, 35.269],
    'Base Load': [65, 55, 40, 35]
}
df = pd.DataFrame(data)

# Add random live fluctuation (+/- 5%)
df['Load %'] = df['Base Load'] + [random.randint(-5, 5) for _ in range(4)]

# --- 4. INCIDENT & MITIGATION LOGIC ---
mitigation_log = []

if st.session_state.fiber_cut:
    df.loc[df['City'] == 'Mombasa (KIXP)', 'Load %'] = 99 # Critical failure
    df.loc[df['City'] == 'Nairobi (KIXP)', 'Load %'] += 25 # Congestion spike
    reroute = [[-4.04, 39.6], [-3.39, 38.5], [-1.28, 36.8]]
    mitigation_log.append("⚠️ DETECTED: Sea-Link Failure. Rerouting via Terrestrial Backhaul.")
else:
    reroute = []

if st.session_state.optimize:
    # Mitigation Technique: Traffic Shaping
    df['Load %'] = df['Load %'] * 0.7 
    mitigation_log.append("🛡️ ACTIVE: AI Traffic Shaping & Edge Caching enabled.")

# --- 5. UI LAYOUT ---
st.title(f"📡 Kenya National NOC Dashboard (Live Tick: {count})")

col_map, col_stats = st.columns([2, 1])

with col_map:
    # Map with pulsing colors based on live load
    m = folium.Map(location=[-1.28, 36.8], zoom_start=6, tiles="CartoDB dark_matter")
    for _, r in df.iterrows():
        color = 'red' if r['Load %'] > 85 else 'orange' if r['Load %'] > 65 else 'green'
        folium.CircleMarker([r['Lat'], r['Lon']], radius=r['Load %']/4, color=color, fill=True).add_to(m)
    if reroute: folium.PolyLine(reroute, color="yellow", weight=4).add_to(m)
    st_folium(m, width=800, height=400, key=f"map_{count}") # Key forces refresh

    # Live Bar Chart
    st.subheader("📊 Real-Time Node Saturation")
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.bar(df['City'], df['Load %'], color=['red' if x > 85 else 'skyblue' for x in df['Load %']])
    ax.set_ylim(0, 110)
    st.pyplot(fig)

with col_stats:
    st.subheader("🕹️ Control Center")
    st.button("🚨 Toggle Fiber Cut", on_click=lambda: st.session_state.update({"fiber_cut": not st.session_state.fiber_cut}))
    st.button("🚀 Apply Mitigation", on_click=lambda: st.session_state.update({"optimize": not st.session_state.optimize}))

    st.divider()
    
    # HOW TO MITIGATE (The Logic)
    st.subheader("📝 Mitigation Protocol")
    if not mitigation_log:
        st.write("✅ System Nominal. No active threats.")
    else:
        for note in mitigation_log:
            st.info(note)

    # SHANNON-HARTLEY MATH
    st.subheader("🧬 Physics Audit")
    B = 20 # MHz
    SNR_db = 35 - (df['Load %'].max() / 3)
    Capacity = B * math.log2(1 + 10**(SNR_db/10))
    st.metric("Live Link Capacity", f"{round(Capacity, 1)} Mbps", delta=f"{round(SNR_db, 1)} dB SNR")
    st.latex(r"C = B \log_2(1 + \frac{S}{N})")
