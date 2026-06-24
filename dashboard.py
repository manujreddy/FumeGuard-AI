import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- 1. FUTURISTIC PAGE SETUP ---
st.set_page_config(page_title="FumeGuard OS // CORE", layout="wide", initial_sidebar_state="collapsed")

# Advanced Cyberpunk CSS Injection
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    /* Main Headings */
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #00f3ff; text-align: center; text-shadow: 0px 0px 10px rgba(0, 243, 255, 0.4); }
    
    /* The Giant Digital AQI Display */
    .huge-number {
        font-size: 85px;
        font-weight: 900;
        color: #00f3ff;
        text-align: center;
        text-shadow: 0px 0px 25px rgba(0, 243, 255, 0.7);
        font-family: 'Orbitron', sans-serif;
        margin-top: -10px;
        margin-bottom: -20px;
    }
    .huge-number-danger {
        font-size: 85px;
        font-weight: 900;
        color: #ff0055;
        text-align: center;
        text-shadow: 0px 0px 25px rgba(255, 0, 85, 0.7);
        font-family: 'Orbitron', sans-serif;
        margin-top: -10px;
        margin-bottom: -20px;
    }
    .number-label {
        font-size: 18px;
        color: #aaaaaa;
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 3px;
        margin-top: 20px;
    }
    
    /* AI Feature Cards */
    .ai-card {
        background-color: rgba(0, 243, 255, 0.05);
        border: 1px solid #00f3ff;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
        box-shadow: inset 0px 0px 10px rgba(0,243,255,0.1);
    }
    .ai-card-title { font-family: 'Orbitron', sans-serif; font-size: 12px; color: #aaaaaa; letter-spacing: 1px; }
    .ai-card-value { font-family: 'Orbitron', sans-serif; font-size: 16px; color: #ffffff; font-weight: bold; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ FUMEGUARD // NEURAL_NET OS")
st.markdown("<h4 style='text-align: center; color: #aaaaaa; font-family: Orbitron;'>INDUSTRIAL TELEMETRY & AI DIAGNOSTICS</h4>", unsafe_allow_html=True)
st.divider()

# --- 2. NATIVE STREAMLIT LIVE ENGINE ---
try:
    df = pd.read_csv('live_data.csv')
    
    if len(df) > 0:
        latest = df.iloc[-1]
        aqi = latest['AQI']
        gas_type = latest['GasType']
        fan_speed = latest['FanSpeed']
        temp = latest['Temp']

        # --- DYNAMIC AI ALERTS (CENTERED) ---
        col_alert1, col_alert2, col_alert3 = st.columns([1, 2, 1])
        with col_alert2:
            if gas_type == "Toxic Chemical Vapor":
                st.error("⚠️ BIOHAZARD DETECTED: TOXIC CHEMICAL VAPOR. EXHAUST COMPENSATING.", icon="☣️")
            elif gas_type == "Smoke / Combustible":
                st.warning("🔥 COMBUSTIBLE DETECTED: SMOKE PROFILE. EXHAUST COMPENSATING.", icon="🔥")
            else:
                st.success("✅ ATMOSPHERE STABLE. NO THREATS DETECTED.", icon="🛡️")
        
        st.write("") # Spacer

        # --- MAIN VISUALS (2 COLUMNS) ---
        # Left side gets the exact number and fan. Right side gets the wide chart.
        col_left, col_right = st.columns([1, 2])

        with col_left:
            # THE GIANT NUMERICAL AQI DISPLAY
            st.markdown("<div class='number-label'>EXACT LIVE AQI</div>", unsafe_allow_html=True)
            
            # Change color to red if AI detects danger
            css_class = "huge-number-danger" if gas_type != "Clean Air" else "huge-number"
            st.markdown(f"<div class='{css_class}'>{aqi:.1f}</div>", unsafe_allow_html=True)
            
            st.write("") # Spacer
            st.write("") # Spacer

            # PROPORTIONAL FAN SPEED GAUGE
            fig_fan_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = fan_speed,
                title = {'text': "EXHAUST RPM %", 'font': {'color': '#aaaaaa', 'family': 'Orbitron'}},
                number = {'suffix': "%", 'font': {'color': '#00f3ff'}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#00f3ff"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2, 'bordercolor': "#333333",
                    'steps': [
                        {'range': [0, 20], 'color': "rgba(0, 243, 255, 0.1)"},
                        {'range': [20, 80], 'color': "rgba(255, 204, 0, 0.2)"},
                        {'range': [80, 100], 'color': "rgba(255, 0, 85, 0.3)"}],
                }
            ))
            fig_fan_gauge.update_layout(height=280, template="plotly_dark", margin=dict(l=20, r=20, t=30, b=10))
            st.plotly_chart(fig_fan_gauge, use_container_width=True)

        with col_right:
            # NEON LINE CHART
            fig_line = go.Figure()
            line_color = '#00f3ff' if gas_type == "Clean Air" else '#ff0055'

            fig_line.add_trace(go.Scatter(
                x=df['Time'], y=df['AQI'], mode='lines', 
                name='Live AQI', 
                line=dict(color=line_color, width=4),
                fill='tozeroy',
                fillcolor=f"rgba({255 if gas_type != 'Clean Air' else 0}, {0 if gas_type != 'Clean Air' else 243}, {85 if gas_type != 'Clean Air' else 255}, 0.1)"
            ))
            
            max_y = max(500, df['AQI'].max() + 50)
            fig_line.update_layout(
                title={'text': "Atmospheric History", 'font': {'color': '#aaaaaa', 'family': 'Orbitron'}},
                height=450, xaxis_title="System Time (Ticks)", yaxis_title="Air Quality Index",
                yaxis_range=[0, max_y], template="plotly_dark",
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig_line, use_container_width=True)

        st.divider()

        # --- THE AI SUBSYSTEMS MATRIX ---
        st.markdown("<h3 style='text-align: center; color: #aaaaaa; font-size: 20px; margin-bottom: 20px;'>⚙️ ACTIVE AI SUBSYSTEMS ⚙️</h3>", unsafe_allow_html=True)
        
        col_ai1, col_ai2, col_ai3, col_ai4 = st.columns(4)
        
        with col_ai1:
            st.markdown(f"""
            <div class='ai-card'>
                <div class='ai-card-title'>ELECTRONIC NOSE</div>
                <div class='ai-card-value' style='color: {line_color};'>{gas_type}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_ai2:
            st.markdown(f"""
            <div class='ai-card'>
                <div class='ai-card-title'>SENSOR FUSION</div>
                <div class='ai-card-value'>Active (Temp Comp: {temp:.1f}°C)</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_ai3:
            st.markdown(f"""
            <div class='ai-card'>
                <div class='ai-card-title'>PROPORTIONAL CONTROL</div>
                <div class='ai-card-value'>Dynamic Scaling ({fan_speed}%)</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_ai4:
            st.markdown(f"""
            <div class='ai-card'>
                <div class='ai-card-title'>SYSTEM UPTIME</div>
                <div class='ai-card-value'>T+{latest['Time']} Cycles</div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.warning("⏳ Waiting for Engine to send data...")

except Exception as e:
    st.error(f"❌ DASHBOARD ERROR: {e}")

# --- REFRESH COMMAND ---
time.sleep(1)
st.rerun()