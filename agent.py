import operator
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, END
from fredapi import Fred
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
from fpdf import FPDF
import os
import warnings
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('FRED_API_KEY')

# Ignore warnings
warnings.filterwarnings('ignore')

# --- 1. Define Agent State ---
class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add] 
    macro_data: dict  
    retrieved_knowledge: str 
    forecast_data: dict 
    analysis_report: str  

# --- 2. Data Engine & Knowledge Base (English Version) ---
class MacroDataEngine:
    def __init__(self, api_key):
        self.fred = Fred(api_key=api_key)
        self.indicators = {'FEDFUNDS': 'FedRate', 'DCOILWTICO': 'WTI'}

    def fetch_and_process(self, start_date='2019-01-01'):
        master_df = pd.DataFrame()
        for s_id, name in self.indicators.items():
            series = self.fred.get_series(s_id, observation_start=start_date).resample('MS').mean()
            df = pd.DataFrame(series, columns=[name])
            p_value = adfuller(df[name].dropna())[1]
            if p_value <= 0.05 or name == 'FedRate':
                master_df[name] = df[name]
            else:
                master_df[f'diff_{name}'] = df[name].diff()
        return master_df.dropna()

class ThesisKnowledgeBase:
    def __init__(self):
        # Professional knowledge based on Kun-Woong's thesis
        self.data = [
            {"keywords": ["FedRate"], "content": "Rising US FedFunds rates lead to depreciation of emerging market currencies, reducing purchasing power for used car imports in markets like Cambodia."},
            {"keywords": ["WTI"], "content": "Volatility in WTI crude oil prices precedes changes in SCFI (Shipping Freight Index), affecting export margins for low-cost used vehicles."}
        ]

    def search(self, current_data):
        fed_rate = current_data.get('FedRate', 0)
        return self.data[0]['content'] if fed_rate > 3.0 else "Macro environment remains stable based on historical analysis."

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Macro Insight AI Analysis Report', 0, 1, 'C')
        self.ln(10)

# --- 3. Node Functions ---

def fetch_data_node(state: AgentState):
    print("\n[Node 1] Fetching real-time data...")
    engine = MacroDataEngine('5bc51add4d98b30c600855acaee6391c')
    latest = engine.fetch_and_process().iloc[-1].to_dict()
    return {"messages": ["Data fetch complete"], "macro_data": latest}

def retrieve_knowledge_node(state: AgentState):
    print("[Node 2] Retrieving thesis knowledge...")
    kb = ThesisKnowledgeBase()
    context = kb.search(state['macro_data'])
    return {"messages": ["Knowledge retrieval complete"], "retrieved_knowledge": context}

def analyze_node(state: AgentState):
    print("[Node 3] Performing AI reasoning...")
    report = f"Analysis: {state['retrieved_knowledge']} (Current Rate: {state['macro_data']['FedRate']}%)"
    return {"messages": ["Analysis complete"], "analysis_report": report}

def forecast_node(state: AgentState):
    print("[Node 4] Forecasting future trends (SARIMAX)...")
    engine = MacroDataEngine('5bc51add4d98b30c600855acaee6391c')
    df = engine.fetch_and_process()
    model_fit = SARIMAX(df['FedRate'], order=(1,1,1)).fit(disp=False)
    forecast = model_fit.get_forecast(steps=3).predicted_mean.tolist()
    return {"messages": ["Forecasting complete"], "forecast_data": {"FedRate_3m": forecast}}

def visualize_node(state: AgentState):
    print("[Node 5] Generating visualization...")
    engine = MacroDataEngine('5bc51add4d98b30c600855acaee6391c')
    df = engine.fetch_and_process().tail(12)
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['FedRate'], label='Historical (Real)', color='green', marker='s')
    
    f_vals = state['forecast_data']['FedRate_3m']
    f_dates = [df.index[-1] + pd.DateOffset(months=i+1) for i in range(len(f_vals))]
    plt.plot([df.index[-1]] + f_dates, [df['FedRate'].iloc[-1]] + f_vals, '--o', color='orange', label='3-Month Forecast (AI)')
    
    plt.title('Macro Economic Trend & AI Forecast')
    plt.legend(); plt.grid(True); plt.savefig('macro_trend_final.png'); plt.close()
    return {"messages": ["Chart saved"]}

def generate_pdf_node(state: AgentState):
    print("[Node 6] Generating PDF Report...")
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=state['analysis_report'])
    pdf.ln(10)
    if os.path.exists('macro_trend_final.png'):
        pdf.image('macro_trend_final.png', x=10, w=190)
    pdf.output("Macro_Analysis_Report.pdf")
    return {"messages": ["PDF Generated Successfully"]}

# --- 4. Graph Construction ---
workflow = StateGraph(AgentState)
workflow.add_node("fetch", fetch_data_node)
workflow.add_node("retrieve", retrieve_knowledge_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("forecast", forecast_node)
workflow.add_node("visualize", visualize_node)
workflow.add_node("pdf", generate_pdf_node)

workflow.set_entry_point("fetch")
workflow.add_edge("fetch", "retrieve")
workflow.add_edge("retrieve", "analyze")
workflow.add_edge("analyze", "forecast")
workflow.add_edge("forecast", "visualize")
workflow.add_edge("visualize", "pdf")
workflow.add_edge("pdf", END)

app = workflow.compile()

if __name__ == "__main__":
    app.invoke({"messages": ["Workflow started"]})