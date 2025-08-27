# Thermodynamic Property Explorer (Multi-Fluid)

A Python-based **thermodynamic property calculator and visualizer** for various fluids (Water/Steam, Nitrogen, CO2, Air) using [CoolProp](http://coolprop.org/).
This project includes:
- **Command-Line Interface (CLI)** for quick property calculations.
- **Interactive Web UI (Streamlit)** for visualization of T–s and h–s diagrams.
- **Dynamic multi-fluid support** with saturation curve plotting.

---

## 🚀 Features

- **Multi-Fluid Support**: Choose from Water, Nitrogen, CO2, and Air (easily extendable to other CoolProp-supported fluids).
- **Property Evaluation**:
  - By Pressure & Temperature (P, T)
  - By Pressure & Quality (P, x)
  - By Temperature & Quality (T, x)
- **Phase Classification**: Compressed liquid, saturated, two-phase, or superheated.
- **Interactive Visualizations**:
  - T–s (Temperature vs. Entropy) Diagram
  - h–s (Enthalpy vs. Entropy) Diagram with saturation dome
- **Dual Interface**:
  - CLI for engineers & developers
  - Streamlit Web App for interactive use

---

## 📂 Project Structure
```

steam\_table\_explorer/
├── app/
│   ├── cli.py                \# CLI entrypoint (now supports --fluid)
│   ├── streamlit\_app.py      \# Web UI with fluid selection dropdown
│   ├── thermoprops/
│   │   └── props.py          \# Core property calculations (multi-fluid)
│   ├── viz/
│   │   └── plots.py          \# T-s & h-s plotting with fluid-specific curves
├── requirements.txt
└── README.md

````

---

## 🔧 Installation & Setup

1.  **Clone repository**:
    ```bash
    git clone [https://github.com/Shivam-Rathaur/Thermodynamic-Property-Explorer.git](https://github.com/Shivam-Rathaur/Thermodynamic-Property-Explorer.git)
    cd thermodynamic-property-explorer
    ```
2.  **Create & activate virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate      # Linux/Mac
    venv\Scripts\activate         # Windows
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## 🖥️ Usage

### 1. CLI Mode
```bash
# Pressure (Pa), Temperature (K), Fluid = Nitrogen
python app/cli.py --mode PT --P 101325 --T 300 --fluid Nitrogen

# Pressure (Pa), Quality (x), Fluid = Water
python app/cli.py --mode Px --P 101325 --x 0.5 --fluid Water
````

### 2\. Streamlit Web App

```bash
streamlit run app/streamlit_app.py
```

Open your browser and navigate to `http://localhost:8501`.

Select a fluid (Water, Nitrogen, CO2, Air) from the dropdown, input the conditions, and view:

  - Numeric state properties
  - T–s and h–s diagrams

-----

## 🧪 Example Output (Streamlit)

**State Properties:**

```
P (kPa): 101.325
T (°C): 100.0
h (kJ/kg): 2676.1
s (kJ/kg-K): 7.355
v (m3/kg): 1.673
phase: two_phase
```

**T–s Diagram:** Shows the current state point plotted on the saturation dome.

-----

## 📈 Applications

  - Thermodynamics & Power Cycle Analysis
  - Steam/Natural Gas Cycle Design
  - Refrigeration & Cryogenic Engineering
  - Educational tool for students in Mechanical/Chemical Engineering

-----

## 🛠 Tech Stack

  - **Python 3.x**
  - **CoolProp** – Thermophysical property library
  - **Matplotlib** – Plotting
  - **Streamlit** – Web visualization
  - **Argparse** – CLI argument parsing

-----

## 🔮 Future Improvements

  - Support for custom fluid mixtures
  - Additional diagrams (P–h, Mollier charts)
  - Export plots as PDF/PNG
  - Save/load user sessions

-----

## 👨‍💻 Author

**Shivam Rathaur**

B.Tech (3rd Year), Materials Science & Metallurgical Engineering, IIT Hyderabad
(Second Major: Mechanical Engineering)


Note: This project was developed as part of my academic work at IIT Hyderabad, focusing on applying core thermodynamic principles to create engineering tools useful in industrial applications.
