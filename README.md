# 📊 Macro Insight AI Agent (v2.0: VARX-IRF Engine)
**Advanced Macroeconomic Analysis with Exogenous Control & Impulse Response Analysis**

This project is an advanced AI Agent system that bridges theoretical econometrics and modern Agentic AI. It implements a **VARX (Vector Autoregression with Exogenous variables)** model to analyze the dynamic interaction between interest rates and energy costs, controlled by currency fluctuations.

## 🚀 Key Technical Evolution
- **VARX Modeling**: Moves beyond simple forecasting by incorporating **Exchange Rate (USD/KRW)** as an exogenous variable ($\mathbf{x}_t$) to isolate pure interest rate shocks.
- **Impulse Response Function (IRF)**: Analyzes how a 1-unit shock in the FedFunds Rate propagates through the system over a 10-month horizon.
- **Granger Causality Test**: Statistically validates the leading indicators for emerging market export margins, as discussed in my undergraduate thesis.
- **Agentic Workflow**: Managed by **LangGraph**, orchestrating data acquisition, statistical estimation, and automated visualization.

## 📈 Statistical Framework
The system estimates the following multivariate structure:
$$\mathbf{y}_t = \mathbf{c} + \sum_{i=1}^p \mathbf{A}_i \mathbf{y}_{t-i} + \mathbf{B} \mathbf{x}_t + \mathbf{\epsilon}_t$$
Where $\mathbf{y}_t = [\text{FedRate}_t, \text{WTI}_t]'$ and $\mathbf{x}_t = [\text{ExchangeRate}_t]'$

## 🎓 About the Author
I am a senior at **Hankuk University of Foreign Studies**, double majoring in **Statistics and Computer Science**. This project demonstrates my ability to operationalize complex statistical theories into functional AI services, a core skill I aim to bring to the **SCAI Lab**.
