import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
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
    # Interactive Map with Glow Effect
    m = folium.Map(location=[-1.286, 36.817], zoom_start=6, tiles="CartoDB dark_matter")
    for city, coords in {"Nairobi (KIXP)": [-1.28, 36.8], "Mombasa (KIXP)": [-4.04, 39.6], "Kisumu (KIXP)": [-0.1, 34.7]}.items():
        load = df[df["City"] == city]["Load %"].values[0]
        color = "red" if load > 80 else "cyan"
        folium.Circle(
            location=coords, radius=load * 500, color=color, fill=True, 
            popup=f"{city}: {load}% Load"
        ).add_to(m)
    st_folium(m, height=500, width=900)

with col2:
    st.subheader("AI Controller")
    opt_active = st.toggle("Activate AI Traffic Rebalancing", value=False)
    
    if opt_active:
        st.success("🤖 AI Handshake Complete.")
        # Re-calculating with AI Optimization formula: Load = Load * 0.7
        df["Load %"] = df["Load %"] * 0.7
        st.info("Optimization: Packet-level prioritization active (M-Pesa/Gov Traffic First)")
    
    fig = px.bar(df, x="City", y="Load %", range_y=[0, 100], color="Load %",
                 color_continuous_scale=["#00ff00", "#ffff00", "#ff0000"])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("#### Floating Core Logic (Shannon Limit Check):")
st.latex(r"C = W \log_2 \left( 1 + \frac{S}{N} \right)")

# Auto-Refresh
time.sleep(2)
st.rerun()
