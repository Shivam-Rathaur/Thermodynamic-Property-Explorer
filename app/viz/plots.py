import matplotlib.pyplot as plt
import numpy as np

def plot_Ts_with_point(states_dict, sat_data=None, title="T - s Diagram", fluid="Fluid"):
    """
    Plot Temperature vs. Entropy diagram with saturation curve and a point.
    fluid: name of the working fluid for labeling.
    """
    fig, ax = plt.subplots(figsize=(7, 5))

    # Saturation Curve
    if sat_data is not None:
        s_liq = np.array(sat_data["s_liq"]) / 1e3
        s_vap = np.array(sat_data["s_vap"]) / 1e3
        T = np.array(sat_data["T"]) - 273.15
        ax.plot(s_liq, T, linestyle='-', label=f"Sat. Liquid ({fluid})")
        ax.plot(s_vap, T, linestyle='-', label=f"Sat. Vapor ({fluid})")

    # State Points
    for name, st in states_dict.items():
        ax.scatter(st.s / 1e3, st.T - 273.15, label=f"{name} ({fluid})")
        ax.text(st.s / 1e3 + 0.02, st.T - 273.15, name)

    ax.set_xlabel("Entropy, s (kJ/kg·K)")
    ax.set_ylabel("Temperature, T (°C)")
    ax.set_title(f"{title} - {fluid}")
    ax.grid(True)
    ax.legend()
    return fig


def plot_hs_with_point(states_dict, sat_data=None, title="h - s Diagram", fluid="Fluid"):
    """
    Plot Enthalpy vs. Entropy diagram with saturation curve and a point.
    fluid: name of the working fluid for labeling.
    """
    fig, ax = plt.subplots(figsize=(7, 5))

    # Saturation Curve
    if sat_data is not None:
        s_liq = np.array(sat_data["s_liq"]) / 1e3
        s_vap = np.array(sat_data["s_vap"]) / 1e3
        h_liq = np.array(sat_data["h_liq"]) / 1e3
        h_vap = np.array(sat_data["h_vap"]) / 1e3
        ax.plot(s_liq, h_liq, linestyle='-', label=f"Sat. Liquid ({fluid})")
        ax.plot(s_vap, h_vap, linestyle='-', label=f"Sat. Vapor ({fluid})")

    # State Points
    for name, st in states_dict.items():
        ax.scatter(st.s / 1e3, st.h / 1e3, label=f"{name} ({fluid})")
        ax.text(st.s / 1e3 + 0.02, st.h / 1e3, name)

    ax.set_xlabel("Entropy, s (kJ/kg·K)")
    ax.set_ylabel("Enthalpy, h (kJ/kg)")
    ax.set_title(f"{title} - {fluid}")
    ax.grid(True)
    ax.legend()
    return fig

