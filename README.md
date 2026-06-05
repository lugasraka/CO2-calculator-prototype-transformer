# Transformer Decarbonization Manager

A Streamlit prototype for evaluating and simulating CO₂ reduction across the transformer lifecycle — from embodied carbon in materials through to end-of-life recovery.

## Modules

| Module | Description |
|--------|-------------|
| **1. TCO & Carbon ROI** | Compares total cost of ownership between standard and high-efficiency transformer designs over 15 years, including capitalised loss costs. |
| **2. Circularity & EOL Planner** | Covers end-of-life lifecycle stages (C1–C4): mid-life retrofill vs. structured decommissioning with material recovery rates. |
| **3. Portfolio CO₂ Simulator ★** | Bottom-up embodied carbon calculator (A1–A3 scope) — translates BOM material choices into fleet-wide CO₂ outcomes across product families and annual volumes. |

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Scope

- Module 3 covers **cradle-to-gate (A1–A3)** embodied emissions only — raw material extraction through factory gate.
- Use-phase energy losses (B1–B6) are addressed in Module 1.
- End-of-life (C1–C4) and recycling credits (Module D) are addressed in Module 2.
- Full cradle-to-grave integration (A1–C4 + Module D) is planned for Phase 2.

## Author 

- Raka Adrianto | Sustainability, Product, Data [LinkedIn](https://www.linkedin.com/in/raka-adrianto/)