# app/streamlit_app.py
import streamlit as st
from thermoprops.props import state_from_PT, state_from_Px, state_from_Tx, sat_curve
from viz.plots import plot_Ts_with_point, plot_hs_with_point
import matplotlib.pyplot as plt

# Streamlit Page Config
st.set_page_config(page_title="Thermodynamic Property Explorer", layout="wide")

st.title("Thermodynamic Property Explorer")

# Fluid Selector
fluid = st.selectbox("Select Fluid", ["Water", "Nitrogen", "CO2", "Air"])

# Input Mode
mode = st.radio("Input mode", ["P & T", "P & x", "T & x"])

if mode == "P & T":
    P = st.number_input("Pressure (kPa)", value=101.325) * 1e3
    T_C = st.number_input("Temperature (°C)", value=100.0)
    T = T_C + 273.15
    try:
        st_obj = state_from_PT(P, T, fluid=fluid)
    except Exception as e:
        st.error(str(e))
        st.stop()

elif mode == "P & x":
    P = st.number_input("Pressure (kPa)", value=101.325) * 1e3
    x = st.slider("Quality (x)", 0.0, 1.0, 0.0)
    try:
        st_obj = state_from_Px(P, x, fluid=fluid)
    except Exception as e:
        st.error(str(e))
        st.stop()

else:  # T & x
    T_C = st.number_input("Temperature (°C)", value=100.0)
    T = T_C + 273.15
    x = st.slider("Quality (x)", 0.0, 1.0, 0.0)
    try:
        st_obj = state_from_Tx(T, x, fluid=fluid)
    except Exception as e:
        st.error(str(e))
        st.stop()

# Display Fluid Name
st.subheader(f"State Properties for {fluid}")
st.write({
    "P (kPa)": round(st_obj.P / 1e3, 3),
    "T (°C)": round(st_obj.T - 273.15, 3),
    "h (kJ/kg)": round(st_obj.h / 1e3, 3),
    "s (kJ/kg-K)": round(st_obj.s / 1e3, 4),
    "v (m³/kg)": round(st_obj.v, 6),
    "x": st_obj.x,
    "phase": st_obj.phase
})

# Plots
sat = sat_curve(fluid=fluid)
fig1 = plot_Ts_with_point({"state": st_obj}, sat_data=sat, title=f"T-s Diagram ({fluid})")
st.pyplot(fig1)

fig2 = plot_hs_with_point({"state": st_obj}, sat_data=sat, title=f"h-s Diagram ({fluid})")
st.pyplot(fig2)
