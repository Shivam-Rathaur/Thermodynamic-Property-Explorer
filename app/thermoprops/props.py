"""
Generalized Thermodynamic Property Wrapper using CoolProp.
Supports any fluid available in CoolProp (Water, Nitrogen, CO2, Air, etc.).
Provides functions to query states by (P,T), (P,Q), or (T,Q)
and to classify the phase.
"""

from dataclasses import dataclass
from typing import Optional, Dict
from CoolProp.CoolProp import PropsSI
import math

# Default fluid (can be overridden by passing fluid argument to functions)
DEFAULT_FLUID = "Water"

@dataclass
class State:
    P: float        # Pa
    T: float        # K
    h: float        # J/kg
    s: float        # J/kg-K
    v: float        # m3/kg
    x: Optional[float]  # quality (0..1) if two-phase else None
    phase: str      # 'compressed_liquid', 'saturated_liquid', 'two_phase', 'superheated'

def safe_propsSI(output: str, a1: str, v1, a2: str, v2, fluid=DEFAULT_FLUID):
    """Wrapper to catch CoolProp errors and return None if unavailable."""
    try:
        return PropsSI(output, a1, v1, a2, v2, fluid)
    except Exception as e:
        raise RuntimeError(f"CoolProp error for {fluid}, {output} with {a1}={v1}, {a2}={v2}: {e}")

def state_from_PT(P: float, T: float, fluid=DEFAULT_FLUID) -> State:
    """Build state from Pressure [Pa] and Temperature [K]."""
    h = safe_propsSI("H", "P", P, "T", T, fluid)
    s = safe_propsSI("S", "P", P, "T", T, fluid)
    rho = safe_propsSI("D", "P", P, "T", T, fluid)  # density kg/m3
    v = 1.0 / rho if rho != 0 else float('nan')

    x = None
    phase = "unknown"

    # Try to see if inside two-phase region
    try:
        q = safe_propsSI("Q", "P", P, "T", T, fluid)
        if 0.0 <= q <= 1.0:
            x = float(q)
            phase = "two_phase"
    except Exception:
        pass

    # If not two-phase, classify phase based on T vs T_sat
    if phase != "two_phase":
        try:
            T_sat = safe_propsSI("T", "P", P, "Q", 0.0, fluid)
            if abs(T - T_sat) < 1e-3:  # at saturation
                phase = "saturated"
            elif T < T_sat:
                phase = "compressed_liquid"
            else:
                phase = "superheated"
        except Exception:
            phase = "unknown"

    return State(P=P, T=T, h=h, s=s, v=v, x=x, phase=phase)

def state_from_Px(P: float, x: float, fluid=DEFAULT_FLUID) -> State:
    """Build state from P [Pa] and quality x (0..1)."""
    T = safe_propsSI("T", "P", P, "Q", x, fluid)
    h = safe_propsSI("H", "P", P, "Q", x, fluid)
    s = safe_propsSI("S", "P", P, "Q", x, fluid)
    rho = safe_propsSI("D", "P", P, "Q", x, fluid)
    v = 1.0 / rho if rho != 0 else float('nan')
    return State(P=P, T=T, h=h, s=s, v=v, x=float(x), phase="two_phase")

def state_from_Tx(T: float, x: float, fluid=DEFAULT_FLUID) -> State:
    """Build state from T [K] and quality x."""
    P = safe_propsSI("P", "T", T, "Q", x, fluid)
    return state_from_Px(P, x, fluid)

def sat_curve(fluid=DEFAULT_FLUID, n=200) -> Dict[str, list]:
    """
    Return saturation curve arrays for plotting:
    arrays of (s_liq, T_sat), (s_vap, T_sat),
    and (h_liq, s_liq), (h_vap, s_vap), etc.
    """
    T_crit = PropsSI("Tcrit", fluid)
    T_min = PropsSI("Tmin", fluid)
    T_vals = [T_min + (T_crit - T_min) * i / (n-1) for i in range(n)]

    s_liq, s_vap, h_liq, h_vap, T_list = [], [], [], [], []

    for T in T_vals:
        try:
            h_l = PropsSI("H", "T", T, "Q", 0, fluid)
            h_v = PropsSI("H", "T", T, "Q", 1, fluid)
            s_l = PropsSI("S", "T", T, "Q", 0, fluid)
            s_v = PropsSI("S", "T", T, "Q", 1, fluid)

            T_list.append(T)
            h_liq.append(h_l)
            h_vap.append(h_v)
            s_liq.append(s_l)
            s_vap.append(s_v)

        except Exception:
            continue  # skip invalid points near critical

    return {
        "T": T_list,
        "s_liq": s_liq,
        "s_vap": s_vap,
        "h_liq": h_liq,
        "h_vap": h_vap,
    }
