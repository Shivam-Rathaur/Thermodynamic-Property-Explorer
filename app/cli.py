"""
Generalized CLI for Thermodynamic Property Explorer (multi-fluid).
Examples:
  python app/cli.py --mode PT --P 10e5 --T 373.15 --fluid Water
  python app/cli.py --mode Px --P 100e3 --x 0.5 --fluid Nitrogen
"""

import argparse
from thermoprops.props import state_from_PT, state_from_Px, state_from_Tx, sat_curve
from viz.plots import plot_Ts_with_point, plot_hs_with_point

def print_state(st, fluid):
    print(f"\nState for {fluid}:")
    print(f"  P = {st.P/1e3:.3f} kPa")
    print(f"  T = {st.T-273.15:.3f} °C")
    print(f"  h = {st.h/1e3:.3f} kJ/kg")
    print(f"  s = {st.s/1e3:.4f} kJ/kg-K")
    print(f"  v = {st.v:.6f} m3/kg")
    print(f"  x = {st.x}")
    print(f"  phase = {st.phase}")

def main():
    parser = argparse.ArgumentParser(description="Thermodynamic Property Explorer CLI")
    parser.add_argument("--mode", choices=["PT","Px","Tx"], default="PT", help="Input mode")
    parser.add_argument("--P", type=float, help="Pressure [Pa]")
    parser.add_argument("--T", type=float, help="Temperature [K]")
    parser.add_argument("--x", type=float, help="Quality (0..1)")
    parser.add_argument("--fluid", type=str, default="Water", help="Fluid name (Water, Nitrogen, CO2, Air, etc.)")
    parser.add_argument("--plot", action="store_true", help="Show T-s and h-s plots")
    args = parser.parse_args()

    fluid = args.fluid

    if args.mode == "PT":
        if args.P is None or args.T is None:
            parser.error("PT mode requires --P and --T")
        st = state_from_PT(args.P, args.T, fluid=fluid)

    elif args.mode == "Px":
        if args.P is None or args.x is None:
            parser.error("Px mode requires --P and --x")
        st = state_from_Px(args.P, args.x, fluid=fluid)

    elif args.mode == "Tx":
        if args.T is None or args.x is None:
            parser.error("Tx mode requires --T and --x")
        st = state_from_Tx(args.T, args.x, fluid=fluid)

    else:
        parser.error("Unknown mode")

    print_state(st, fluid)

    if args.plot:
        sat = sat_curve(fluid=fluid)
        plot_Ts_with_point({"state": st}, sat_data=sat)
        plot_hs_with_point({"state": st}, sat_data=sat)

if __name__ == "__main__":
    main()

