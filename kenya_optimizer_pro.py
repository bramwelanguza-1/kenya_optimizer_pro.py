import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import math
import random

# --- 1. FUNCTION DEFINITIONS (Defined first so they are ready to use) ---

def calculate_detailed_metrics(bandwidth_mhz, load_percent):
    """Calculates SNR and Capacity based on real-time load."""
    B = bandwidth_mhz * 1e6 
    # Logic: As load increases, internal noise/interference rises
    base_snr_db = 30 
    current_snr_db = base_snr_db - (load_percent / 5) 
    snr_linear = 10**(current_snr_db / 10)
    
    # Shannon-Hartley Principle
    capacity_bps = B * math.log2(1 + snr_linear)
    spectral_efficiency = capacity_bps / B
    return current_snr_db, capacity_bps / 1e6, spectral_efficiency

def get_shannon_deep_dive(B_mhz, S_watts, N_watts):
    """Expanded Shannon Logic: Shows energy efficiency (Eb/No)."""
    B = B_mhz * 1e6
    SNR_linear = S_watts / N_watts
    
