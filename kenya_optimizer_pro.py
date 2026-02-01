import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import math
import datetime
import random
import matplotlib.pyplot as plt

# --- 1. CONFIG & SESSION STATE ---
st.set_page_config(layout="wide", page_title="KenyaNet NOC Pro")

# Initialize logs and state if they don't exist
if "logs" not in st.session_state:
    st.session_state.logs = []
if "fiber_cut" not in st.session_state:
    st.session_state.fiber_cut = False
if "optimize" not in st.session_state:
    st.session_state.optimize = False

# --- 2. DYNAMIC DATA GENERATION ---
def get_current_data():
    base_data = {
        'City': ['Nairobi', 'Mombasa', 'Kisumu', 'Eldoret'],
        'Lat': [-1.286, -4.043, -0.091, 0.514], 'Lon': [36.817, 39.668, 34.767, 35.269],
        'Load %': [65, 55, 42, 38]
    }
    df = pd.DataFrame(base_data)
    
    # Add random jitter (+/- 2%)
    df['Load %'] = df['Load %'] + [random.randint(-2, 2) for _ in range(4)]
    
    if st.session_state.fiber_cut:
        df.loc[df['City'] == 'Mombasa', 'Load %'] = 98
        df.loc[df['City'] == 'Nairobi', 'Load %'] += 20
        
    if st.session_state.optimize:
        df['Load %'] = df['Load %'] * 0.7
        
    return df

# --- 3. THE STATIC MAP (No Flicker) ---
def render_stable_map(df):
    m = folium.Map(location=[-1.28, 36.8], zoom_start=6, tiles="CartoDB dark_matter")
    for _, r in df.iterrows():
        color = 'red' if r['Load %'] > 90 else 'yellow' if r['Load %'] > 75 else 'green'
        folium.CircleMarker([r['Lat'], r['Lon']], radius=15, color=color, fill=True).add_to(m)
    return st_folium(m, width=800, height=450, key="noc_map_fixed")

# --- 4. THE LIVE FRAGMENT (Updates every 10s) ---
@st.fragment(run_every="10s")
def live_dashboard_fragment():
    df = get_current_data()
    
    col_stats, col_logs = st.columns([1, 1])
    
    with col_stats:
        st.subheader("📊 Live Metrics (10s interval)")
        target_load = df['Load %'].max()
        # Shannon-Hartley Calculation
        B = 20 
        SNR = 35 - (target_load / 3)
        Capacity = B * math.log2(1 + 10**(SNR/10))
        
        st.metric("Peak System Load", f"{round(target_load, 1)}%")
        st.metric("Effective Capacity", f"{round(Capacity, 1)} Mbps", delta=f"{round(SNR, 1)} dB SNR")
        
        # Mini chart
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.bar(df['City'], df['Load %'], color=['red' if x > 85 else 'green' for x in df['Load %']])
        ax.set_ylim(0, 105)
        st.pyplot(fig)

    with col_logs:
        st.subheader("📜 System Incident Log")
        # Display the log as a clean table
        if st.session_state.logs:
            log_df = pd.DataFrame(st.session_state.logs).iloc[::-1] # Show newest first
            st.table(log_df.head(5))
        else:
            st.info("No incidents recorded in current session.")

# --- 5. MAIN UI ---
st.title("🇰🇪 Kenya National Network Operations Center")

c_left, c_right = st.columns([2, 1])

with c_left:
    # Map stays steady here
    render_stable_map(get_current_data())
    # This part "ticks" every 10s without refreshing the map!
    live_dashboard_fragment()

with c_right:
    st.subheader("🛠️ Control Center")
    
    if st.button("🚨 Toggle Fiber Cut"):
        st.session_state.fiber_cut = not st.session_state.fiber_cut
        status = "CRITICAL: Fiber Cut" if st.session_state.fiber_cut else "RESOLVED: Link Restored"
        st.session_state.logs.append({"Timestamp": datetime.datetime.now().strftime("%H:%M:%S"), "Event": status})
        st.rerun()

    if st.button("🚀 Apply AI Mitigation"):
        st.session_state.optimize = not st.session_state.optimize
        status = "MITIGATION: Active" if st.session_state.optimize else "MITIGATION: Offline"
        st.session_state.logs.append({"Timestamp": datetime.datetime.now().strftime("%H:%M:%S"), "Event": status})
        st.rerun()

    st.divider()
    st.latex(r"C = B \log_2(1 + \frac{S}{N})")
    st.caption("Theoretical limit monitoring based on current SNR.")
