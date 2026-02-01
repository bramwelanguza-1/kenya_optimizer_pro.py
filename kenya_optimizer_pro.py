import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import math
import random
import matplotlib.pyplot as plt

# --- 1. DATA & STATE ---
if "fiber_cut" not in st.session_state: st.session_state.fiber_cut = False
if "optimize" not in st.session_state: st.session_state.optimize = False

# Base Data
data = {
    'City': ['Nairobi (KIXP)', 'Mombasa (KIXP)', 'Kisumu (KIXP)', 'Eldoret (KIXP)'],
    'Lat': [-1.286, -4.043, -0.091, 0.514], 'Lon': [36.817, 39.668, 34.767, 35.269],
    'Load %': [75, 60, 45, 40]
}
df = pd.DataFrame(data)

# --- 2. LOGIC: STRESS TEST & OPTIMIZATION ---
if st.session_state.fiber_cut:
    df.loc[df['City'] == 'Mombasa (KIXP)', 'Load %'] = 98
    df.loc[df['City'] == 'Nairobi (KIXP)', 'Load %'] += 15
    reroute = [[-4.04, 39.6], [-3.39, 38.5], [-1.28, 36.8]]
else:
    reroute = []

# AI Optimization logic (Ways of reducing traffic)
if st.session_state.optimize:
    # Simulates Compression & Cache-Hitting to reduce load
    df['Load %'] = df['Load %'] * 0.7 

# --- 3. UI LAYOUT ---
st.set_page_config(layout="wide", page_title="KenyaNet Optimizer Pro")
st.title("🇰🇪 Advanced Network Topology & Shannon Analysis")

col_map, col_stats = st.columns([2, 1])

with col_map:
    # MAP
    m = folium.Map(location=[-1.28, 36.8], zoom_start=6, tiles="CartoDB dark_matter")
    for _, r in df.iterrows():
        color = 'red' if r['Load %'] > 85 else 'orange' if r['Load %'] > 60 else 'green'
        folium.CircleMarker([r['Lat'], r['Lon']], radius=r['Load %']/5, color=color, fill=True).add_to(m)
    if reroute: folium.PolyLine(reroute, color="yellow", weight=5, dash_array='10').add_to(m)
    st_folium(m, width=800, height=450)

    # GRAPHICAL ANALYSIS
    st.subheader("📊 Load Distribution Analysis")
    fig, ax = plt.subplots(figsize=(8, 3))
    colors = ['red' if x > 80 else 'skyblue' for x in df['Load %']]
    ax.bar(df['City'], df['Load %'], color=colors)
    ax.set_ylabel("Load %")
    ax.set_ylim(0, 100)
    st.pyplot(fig)

with col_stats:
    st.subheader("🕹️ Control Center")
    if st.button("🚨 Simulate Fiber Cut (Mombasa)"):
        st.session_state.fiber_cut = not st.session_state.fiber_cut
        st.rerun()
    
    if st.button("🚀 Apply AI Traffic Optimization"):
        st.session_state.optimize = not st.session_state.optimize
        st.rerun()

    st.divider()

    # SHANNON-HARTLEY ANALYSIS
    st.subheader("🧬 Shannon-Hartley Physics")
    target_load = df['Load %'].max()
    
    # Math: C = B * log2(1 + SNR)
    B = 20 # MHz
    SNR_db = 30 - (target_load / 4)
    SNR_linear = 10**(SNR_db/10)
    Capacity = B * math.log2(1 + SNR_linear)
    
    st.latex(r"C = B \log_2(1 + \text{SNR})")
    
    st.metric("Theoretical Capacity", f"{round(Capacity, 2)} Mbps")
    st.metric("Signal-to-Noise Ratio", f"{round(SNR_db, 1)} dB")
    
    st.progress(target_load / 100)
    st.caption(f"Current bottleneck at {df.iloc[df['Load %'].idxmax()]['City']}")
    
    if st.session_state.optimize:
        st.success("✅ AI Optimization Active: Traffic compressed by 30%")
