import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import random
import time
import requests

# --- 1. GLASSMORPHISM & FLOATING FORMULAS CSS ---
st.set_page_config(page_title="KenyaNet AI Optimizer", layout="wide")

st.markdown("""
<style>
    /* Floating Formulas Background */
    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        overflow: hidden;
    }
    .main::before {
        content: "C = B log2(1 + S/N)   f = v/λ   P = IV   ∇·D = ρ   H(X) = -Σ p(x)log p(x)   Z = R + jX";
        position: absolute;
        width: 200%;
        height: 200%;
        top: -50%;
        left: -50%;
        z-index: 0;
        font-family: 'Courier New', Courier, monospace;
        font-size: 24px;
        color: rgba(0, 255, 255, 0.05);
        transform: rotate(-20deg);
        animation: float 20s linear infinite;
        white-space: pre-wrap;
    }
    @keyframes float {
        from { transform: rotate(-20deg) translateY(0); }
        to { transform: rotate(-20deg) translateY(100px); }
    }

    /* Glass Panels */
    div[data-testid="stVerticalBlock"] > div:has(div.stPlotlyChart) {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA INTEGRATION (KIXP MOCK API) ---
def get_kenya_ixp_data():
    # In a production app, you'd use: requests.get("https://peeringdb.com/api/ix/144")
    # For now, we simulate the 20Gbps/10Gbps ports found in 2026 KIXP records
    data = {
        "Nairobi (KIXP)": {"capacity": 20000, "members": 64},
        "Mombasa (KIXP)": {"capacity": 10000, "members": 18},
        "Kisumu (KIXP)": {"capacity": 1000, "members": 5}
    }
    return data

# --- 3. APP LOGIC ---
st.title("🇰🇪 KenyaNet: AI Optimization Interface")
st.write("### Advanced Infrastructure Monitoring System")

col1, col2 = st.columns([3, 1])

# Generate Real-time Simulation based on IXP Data
ixp_info = get_kenya_ixp_data()
cities = list(ixp_info.keys())
load_vals = [random.randint(40, 95) for _ in cities]
df = pd.DataFrame({"City": cities, "Load %": load_vals})

with col1:
    # --- NEW: AI CALCULATION PROGRESS BAR ---
    progress_text = "🤖 AI Engine: Analyzing KIXP Traffic Loads..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)  # Simulates 1 second of high-speed computation
        my_bar.progress(percent_complete + 1, text=progress_text)
    
    # After completion, hide the bar and show a success message
    my_bar.empty()
    st.success("Analysis Complete: Optimization routes identified.")
    # ----------------------------------------

    st.subheader("Live Traffic Heatmap")
    # ... rest of your map code follows ...
    st.subheader("Live Traffic Heatmap")
    
    # 1. DEFINE the map object first (this defines 'm')
    m = folium.Map(
        location=[-1.286389, 36.817223], 
        zoom_start=6, 
        tiles="CartoDB dark_matter"
    )
    
    # 2. NOW you can loop and add to 'm'
    for city, coords in {"Nairobi (KIXP)": [-1.28, 36.8], "Mombasa (KIXP)": [-4.04, 39.6], "Kisumu (KIXP)": [-0.1, 34.7]}.items():
        
        # Get the load and fix the float type error we saw earlier
        current_load = float(df[df["City"] == city]["Load %"].values[0])
        
        color = "red" if current_load > 80 else "cyan"
        
        # This line was failing because 'm' didn't exist yet or was defined after this
        folium.Circle(
            location=coords, 
            radius=current_load * 500, 
            color=color, 
            fill=True, 
            popup=f"{city}: {current_load}% Load"
        ).add_to(m) 
    
    # 3. Finally, display the map
    folium_static(m, height=500, width=900)
    # --- 2. UI IMPLEMENTATION (Put this after your map code) ---

st.divider()
st.subheader("🧬 The Physics of the Link: Shannon-Hartley Decomposition")

# User can tweak physical layer variables
with st.expander("Adjust Physical Layer Constants (Simulated)"):
    base_b = st.slider("Channel Bandwidth (MHz)", 10, 100, 20)
    st.write("Current Formula: $C = B \log_2(1 + \frac{S}{N})$")

col_phys1, col_phys2, col_phys3 = st.columns(3)

# Calculate metrics for the highest-load city
target_city = df.iloc[df['Load %'].idxmax()]
snr, cap, eff = calculate_detailed_metrics(base_b, target_city['Load %'])

with col_phys1:
    st.metric("Signal-to-Noise Ratio (SNR)", f"{round(snr, 2)} dB")
    st.caption("Lower SNR = Higher Interference")

with col_phys2:
    st.metric("Theoretical Capacity", f"{round(cap, 2)} Mbps")
    st.caption(f"Max throughput for {target_city['City']}")

with col_phys3:
    st.metric("Spectral Efficiency", f"{round(eff, 2)} bit/s/Hz")
    st.caption("How 'dense' the data is packed")
    # Add this inside your map creation loop
if st.session_state.fiber_cut:
    folium.PolyLine(
        locations=reroute_path,
        color="yellow",
        weight=5,
        dash_array='10',
        tooltip="AI Reroute: Terrestrial Backhaul (NOFBI)"
    ).add_to(m)

# --- 3. THE HIDDEN TRUTH: LATENCY VS JITTER ---
st.markdown("### 📉 Network Health: Beyond Bandwidth")
# Generate jitter data based on congestion
jitter = [random.uniform(1, 5) + (l/20) for l in df['Load %']]
health_df = pd.DataFrame({"City": df['City'], "Jitter (ms)": jitter})

fig_health = px.line(health_df, x="City", y="Jitter (ms)", markers=True, 
                    title="Jitter Analysis: Stability of the Data Stream")
fig_health.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
st.plotly_chart(fig_health, use_container_width=True)

with col2:
    st.subheader("AI Controller")
    opt_active = st.toggle("Activate AI Traffic Rebalancing", value=False)
    
    if opt_active:
        st.success("🤖 AI Handshake Complete.")
        
        # --- INPUT THE FIX HERE ---
        df["Load %"] = df["Load %"] * 0.7
        df["Load %"] = df["Load %"].astype(float) # This is the critical fix
        # ---------------------------
        
        st.info("Optimization: Packet-level prioritization active (M-Pesa/Gov Traffic First)")
    
    # This chart also needs clean float data to render without errors
    fig = px.bar(df, x="City", y="Load %", range_y=[0, 100], color="Load %",
                 color_continuous_scale=["#00ff00", "#ffff00", "#ff0000"])
    
    # Transparent Glassmorphism styling for the chart
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("#### Floating Core Logic (Shannon Limit Check):")
st.latex(r"C = W \log_2 \left( 1 + \frac{S}{N} \right)")
# --- 1. ADVANCED SIGNAL METRICS FUNCTION ---
def calculate_detailed_metrics(bandwidth_mhz, load_percent):
    """
    Simulates the physics of the link based on load.
    High load often increases interference (Noise).
    """
    B = bandwidth_mhz * 1e6  # Convert MHz to Hz
    
    # As load increases, Signal-to-Noise Ratio (SNR) typically drops
    # because more users create more interference.
    base_snr_db = 30 
    noise_interference = (load_percent / 10) # Simple linear noise model
    snr_db = base_snr_db - noise_interference
    
    # Linear SNR
    snr_linear = 10**(snr_db / 10)
    
    # Shannon-Hartley Expansion
    import math
    capacity_bps = B * math.log2(1 + snr_linear)
    spectral_efficiency = capacity_bps / B
    
    return snr_db, capacity_bps / 1e6, spectral_efficiency
# --- 1. SESSION STATE FOR THE FAILOVER ---
if "fiber_cut" not in st.session_state:
    st.session_state.fiber_cut = False

# --- 2. STRESS TEST CONTROLLER ---
st.sidebar.divider()
st.sidebar.subheader("🚨 Disaster Recovery Testing")
if st.sidebar.button("💥 Simulate Mombasa Fiber Cut"):
    st.session_state.fiber_cut = not st.session_state.fiber_cut

# --- 3. UPDATED LOGIC FOR THE MAP & SHANNON ---
if st.session_state.fiber_cut:
    st.error("⚠️ CRITICAL: Submarine Cable Severed in Mombasa!")
    # Physically reroute load to Nairobi & terrestrial backups
    df.loc[df['City'] == 'Mombasa (KIXP)', 'Load %'] = 100
    df.loc[df['City'] == 'Nairobi (KIXP)', 'Load %'] += 40 # Influx of rerouted traffic
    reroute_path = [[-4.04, 39.6], [-3.39, 38.5], [-1.28, 36.8]] # Mombasa -> Voi -> Nairobi
else:
    reroute_path = []

# --- 4. EXPANDED SHANNON-HARTLEY (The Math in Motion) ---
def get_shannon_deep_dive(B_mhz, S_watts, N_watts):
    """
    Decomposes the Shannon-Hartley Theorem into its constituent parts:
    B (Bandwidth), S (Signal Power), N (Noise Power)
    """
    B = B_mhz * 1e6
    SNR_linear = S_watts / N_watts
    # Capacity in bits per second
    C = B * math.log2(1 + SNR_linear)
    
    # Hidden Truth: Energy per Bit (Eb/No)
    # This shows the engineering efficiency of the transmission
    Eb_No = SNR_linear * (B / C)
    
    return C / 1e6, math.log2(1 + SNR_linear), Eb_No

# Example UI implementation of the deep dive
st.subheader("📡 Advanced Link Physics")
# Assume S = 0.5 Watts, N = 0.0001 Watts for standard fiber
cap, spec_eff, eb_no = get_shannon_deep_dive(20, 0.5, 0.0005 if st.session_state.fiber_cut else 0.0001)

st.write(f"**Current Spectral Efficiency:** `{round(spec_eff, 3)}` bits/sec/Hz")
st.progress(spec_eff / 10 if spec_eff < 10 else 1.0) 
st.caption("This bar shows how close we are to the 'Shannon Limit'. If it's full, the physics of the cable cannot carry more data without better hardware.")


# Auto-Refresh
time.sleep(2)
st.rerun()
