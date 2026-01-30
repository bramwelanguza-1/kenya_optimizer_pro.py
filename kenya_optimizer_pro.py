import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import math
import random



# 1. Function Definitions (Must be BEFORE they are used)
def calculate_detailed_metrics(bandwidth_mhz, load_percent):
    B = bandwidth_mhz * 1e6 
    base_snr_db = 30 
    snr_db = base_snr_db - (load_percent / 5) 
    snr_linear = 10**(snr_db / 10)
    capacity_bps = B * math.log2(1 + snr_linear)
    spectral_efficiency = capacity_bps / B
    return snr_db, capacity_bps / 1e6, spectral_efficiency

def get_shannon_deep_dive(B_mhz, S_watts, N_watts):
    B = B_mhz * 1e6
    SNR_linear = S_watts / N_watts
    C = B * math.log2(1 + SNR_linear)
    eb_no = SNR_linear * (B / C)
    return C / 1e6, math.log2(1 + SNR_linear), eb_no

# --- 2. APP INITIALIZATION ---
st.set_page_config(layout="wide")
if "fiber_cut" not in st.session_state:
    st.session_state.fiber_cut = False

# --- 3. SIDEBAR & STRESS TEST ---
st.sidebar.title("🛠️ Admin Controls")
if st.sidebar.button("💥 Toggle Mombasa Fiber Cut"):
    st.session_state.fiber_cut = not st.session_state.fiber_cut

# ... (Insert your DataFrame 'df' creation code here) ...

# --- 4. DISASTER RECOVERY LOGIC ---
if st.session_state.fiber_cut:
    st.error("🚨 CRITICAL FAILOVER: Mombasa Submarine Cable Severed.")
    # AI Mitigation: Shift load to Nairobi Terrestrial Backup
    df.loc[df['City'] == 'Mombasa (KIXP)', 'Load %'] = 100
    df.loc[df['City'] == 'Nairobi (KIXP)', 'Load %'] += 25 
    reroute_path = [[-4.04, 39.6], [-3.39, 38.5], [-1.28, 36.8]] # Mombasa -> Voi -> Nairobi
else:
    reroute_path = []

# --- 5. UI LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    m = folium.Map(location=[-1.28, 36.8], zoom_start=6, tiles="CartoDB dark_matter")
    # Add reroute line if fiber is cut
    if reroute_path:
        folium.PolyLine(reroute_path, color="yellow", weight=5, dash_array='10').add_to(m)
    folium_static(m, height=500, width=700)

with col2:
    st.subheader("🧬 Physics Deep-Dive")
    # Using our defined functions safely
    snr, cap, eff = calculate_detailed_metrics(20, df['Load %'].max())
    
    st.metric("Signal Stability (SNR)", f"{round(snr, 1)} dB")
    st.metric("Spectral Efficiency", f"{round(eff, 2)} b/s/Hz")
    
    st.write("---")
    st.write("**Shannon-Hartley Expansion:**")
    st.latex(r"C = B \cdot \log_2\left(1 + \frac{S}{N}\right)")
    st.info(f"The current link efficiency is {round(eff,2)}. To increase capacity without more fiber, the AI is optimizing Signal Power (S).")
