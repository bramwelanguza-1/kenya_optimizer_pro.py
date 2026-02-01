import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import math
import random
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG & STABLE STATE ---
st.set_page_config(layout="wide", page_title="KenyaNet Stable NOC")

# Set refresh to 10,000ms (10 seconds)
count = st_autorefresh(interval=10000, limit=1000, key="stable_tick")

if "fiber_cut" not in st.session_state: st.session_state.fiber_cut = False
if "optimize" not in st.session_state: st.session_state.optimize = False

# --- 2. DATA GENERATION ---
data = {
    'City': ['Nairobi (KIXP)', 'Mombasa (KIXP)', 'Kisumu (KIXP)', 'Eldoret (KIXP)'],
    'Lat': [-1.286, -4.043, -0.091, 0.514], 'Lon': [36.817, 39.668, 34.767, 35.269],
    'Base Load': [65, 55, 40, 35]
}
df = pd.DataFrame(data)
# Dynamic drift for values
df['Load %'] = df['Base Load'] + [random.randint(-3, 3) for _ in range(4)]

if st.session_state.fiber_cut:
    df.loc[df['City'] == 'Mombasa (KIXP)', 'Load %'] = 98
    df.loc[df['City'] == 'Nairobi (KIXP)', 'Load %'] += 20

if st.session_state.optimize:
    df['Load %'] = df['Load %'] * 0.7

# --- 3. UI LAYOUT ---
st.title(f"📡 Stable Network Monitor | Refreshing in 10s (Tick: {count})")

col_left, col_right = st.columns([2, 1])

with col_left:
    # THE MAP (Now with a static key so it doesn't flicker)
    m = folium.Map(location=[-1.28, 36.8], zoom_start=6, tiles="CartoDB dark_matter")
    for _, r in df.iterrows():
        # Signal logic: Red for danger, Yellow for high load, Green for OK
        status_color = 'red' if r['Load %'] > 90 else 'yellow' if r['Load %'] > 70 else 'green'
        folium.CircleMarker(
            location=[r['Lat'], r['Lon']],
            radius=12,
            color=status_color,
            fill=True,
            fill_opacity=0.7,
            popup=f"{r['City']}: {round(r['Load %'], 1)}%"
        ).add_to(m)
    
    # We use a fixed key to prevent the "disappearing/reappearing" effect
    st_folium(m, width=800, height=450, key="static_kenya_map")

    # Bar Chart updating below
    st.subheader("📊 Real-Time Signal Levels")
    fig, ax = plt.subplots(figsize=(10, 2.5))
    ax.bar(df['City'], df['Load %'], color=['red' if x > 85 else 'yellow' if x > 70 else 'green' for x in df['Load %']])
    ax.set_ylim(0, 100)
    st.pyplot(fig)

with col_right:
    st.subheader("🕹️ Mitigation Control")
    st.button("🚨 Simulate Fiber Cut", on_click=lambda: st.session_state.update({"fiber_cut": not st.session_state.fiber_cut}))
    st.button("🚀 AI Optimization", on_click=lambda: st.session_state.update({"optimize": not st.session_state.optimize}))

    st.divider()
    
    # SHANNON-HARTLEY THEOREM (Updating Values)
    st.subheader("🧬 Shannon-Hartley Analysis")
    target = df.iloc[df['Load %'].idxmax()]
    B = 20 # MHz
    SNR_db = 35 - (target['Load %'] / 3)
    Capacity = B * math.log2(1 + 10**(SNR_db/10))
    
    st.latex(r"C = B \log_2(1 + SNR)")
    st.metric("Link Capacity", f"{round(Capacity, 1)} Mbps", delta=f"{round(SNR_db, 1)} dB SNR")
    
    # MITIGATION STATUS
    if st.session_state.fiber_cut:
        st.error(f"CRITICAL: Fiber Cut at {target['City']}! Capacity drop detected.")
    elif st.session_state.optimize:
        st.success("MITIGATION ACTIVE: Spectral Efficiency maximized.")
    else:
        st.info("System Nominal: Signals within operating parameters.")
