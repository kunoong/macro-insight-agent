# 📊 Macro Insight AI Agent (v3.0: SARIMAX-ADF Engine)

**Advanced Macroeconomic Analysis with Automated Stationarity & Lag Optimization**

> Operationalizing econometric theory (SARIMAX) into a robust, production-ready AI Agent system for emerging market analysis.

🔗 **Live Demo**: [macro-insight-agent-36u7rxpwgjksqvqbdzzugu.streamlit.app](https://macro-insight-agent-36u7rxpwgjksqvqbdzzugu.streamlit.app)

---

## 📌 Overview

This project bridges theoretical econometrics and modern Agentic AI. It implements an **ARX (Autoregressive model with Exogenous variables)** framework using **SARIMAX**, specifically tuned to analyze how global macroeconomic shocks propagate into the Cambodian used-car export market.

---

## 🚀 Key Technical Features

| Feature | Detail |
| :--- | :--- |
| **Automated Stationarity** | Implements dynamic ADF-test based differencing (d=0, 1, 2) to ensure robust modeling |
| **Optimal Lag Selection** | Automatically explores AR order (p=1 to 4) based on AIC to maximize predictive power |
| **SARIMAX Engine** | Single-equation estimation (PC1) with exogenous controls (FedRate, WTI, DXY, SCFI) |
| **Agentic Workflow** | LangGraph orchestrates data acquisition, statistical estimation, and visualization |
| **Local Data Pipeline** | Seamless integration with local Excel datasets (data.xlsx, PC_Scores.xlsx) |

---

## 📈 Statistical Framework

$$\text{PC1}_t = c + \sum_{k=1}^p \phi_k \text{PC1}_{t-k} + \gamma' \mathbf{X}_t + \epsilon_t$$
Where $\mathbf{X}_t = [\text{FedRate}_t, \text{WTI}_t, \text{DXY}_t, \text{SCFI}_t]'$

---

## 📊 Analysis Results

| Metric | Result |
| :--- | :--- |
| **Target Market** | Cambodia (PC1: Used-car Demand Index) |
| **Model** | SARIMAX (p=3, 0, 0) |
| **Key Finding (FedRate → PC1)** | $\gamma$ = -0.1533 (p < 0.05) |
| **Data Source** | Local Macro Indicators (Excel) |

---

## 🏗️ System Architecture

```text
User Input
    ↓
LangGraph Agent (Orchestrator)
    ↓
┌──────────────────────────────────────┐
│ Node 1: Dynamic ADF Stationarity Test │
│ Node 2: SARIMAX Optimal Lag Search    │
│ Node 3: Model Estimation & Inference  │
│ Node 4: IRF Visualization             │
└──────────────────────────────────────┘
    ↓
Streamlit Dashboard Output
📂 Project StructurePlaintextmacro-insight-agent/
├── agent.py          # LangGraph agent workflow
├── app.py            # Streamlit UI
├── main.py           # Core SARIMAX engine
├── data.xlsx         # Macroeconomic indicators
├── PC_Scores.xlsx    # PCA-derived demand structural index
└── README.md
```
🛠️ **Tech Stack**

| Category | Technology |
| :--- | :--- |
| **Agent Framework** | LangGraph |
| **Econometrics** | statsmodels (SARIMAX, ADF) |
| **Data Pipeline** | Pandas, Openpyxl |
| **Visualization** | Matplotlib |
| **UI** | Streamlit |
| **Language** | Python 3.12+ |

---

## 🔧 Troubleshooting & Engineering Notes

* **Dynamic Stationarity**: Resolved non-stationarity issues by implementing automated ADF-test based differencing loops (d=0, 1, 2).
* **Model Selection**: Integrated AIC-based iterative search for optimal AR order (p) to minimize model complexity.
* **Streamlit Deployment**: Optimized `requirements.txt` to minimize build time and prevent memory overhead during CI/CD.

---

## 🎓 About

Senior at **Hankuk University of Foreign Studies**, double majoring in Statistics and Computer Science. This project operationalizes the SARIMAX-ADF methodology from my undergraduate research on macroeconomic shocks in emerging used-car export markets into a functional AI agent system.

---

*Last updated: April 2026*
