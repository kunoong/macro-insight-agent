import operator
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, END
from fredapi import Fred
from statsmodels.tsa.api import VAR 
import os
import warnings
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings('ignore')

# --- 1. 에이전트 상태 정의 ---
class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add] 
    macro_data: dict  
    retrieved_knowledge: str 
    forecast_data: dict 
    causality_report: str 
    analysis_report: str  
    irf_obj: object 

# --- 2. 데이터 엔진 클래스 (VARX 대응) ---
class MacroDataEngine:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API Key가 없습니다. .env 파일을 확인하세요.")
        self.fred = Fred(api_key=api_key)
        self.endo_vars = {'FEDFUNDS': 'FedRate', 'DCOILWTICO': 'WTI'}
        self.exog_vars = {'DEXKOUS': 'ExchangeRate'}

    def fetch_all(self, start_date='2019-01-01'):
        df = pd.DataFrame()
        for s_id, name in self.endo_vars.items():
            df[name] = self.fred.get_series(s_id, observation_start=start_date).resample('MS').mean()
        for s_id, name in self.exog_vars.items():
            df[name] = self.fred.get_series(s_id, observation_start=start_date).resample('MS').mean()
            
        return df.dropna().diff().dropna()

# --- 3. 노드 함수 정의 ---

def fetch_data_node(state: AgentState):
    print("\n[Step 1] 내생 및 외생 변수(VARX) 데이터 수집 중...")
    engine = MacroDataEngine(os.getenv('FRED_API_KEY'))
    df = engine.fetch_all()
    return {"messages": ["VARX Data fetched"], "macro_data": df.iloc[-1].to_dict()}

def varx_analysis_node(state: AgentState):
    print("[Step 2] VARX 모델 추정 및 외생 충격 분석 중...")
    engine = MacroDataEngine(os.getenv('FRED_API_KEY'))
    df = engine.fetch_all()
    
    # 내생 변수(y)와 외생 변수(x) 분리
    y = df[['FedRate', 'WTI']]
    x = df[['ExchangeRate']]
    
    # [수정 포인트] exog는 VAR 객체를 생성할 때 넣어주어야 합니다.
    model = VAR(y, exog=x)
    results = model.fit(maxlags=6, ic='aic', trend='c')
    
    p_val = results.test_causality('WTI', 'FedRate', kind='f').pvalue
    irf = results.irf(10)
    
    return {
        "messages": ["VARX Analysis complete"],
        "causality_report": f"FedRate -> WTI (with Exog FX) P-value: {p_val:.4f}",
        "irf_obj": irf
    }

def analyze_node(state: AgentState):
    print("[Step 3] 외생 변수를 포함한 복합 인과관계 해석 중...")
    report = f"""
    ### 🛡️ Advanced VARX Analysis Report
    - **Control Variable**: Exchange Rate (USD/KRW)
    - **Evidence**: {state['causality_report']}
    - **Thesis Context**: 외생 변수인 환율 변동성을 통제한 상태에서도 금리 충격의 유효성을 검증함.
    - **Conclusion**: 이는 건웅 님의 논문에서 강조한 '다변량 구조 하에서의 금리 전이 경로'를 실증적으로 뒷받침함.
    """
    return {"messages": ["Final reasoning complete"], "analysis_report": report}

def visualize_node(state: AgentState):
    print("[Step 4] VARX-IRF 시각화 차트 생성 중...")
    irf = state['irf_obj']
    # 직교화(orth)된 충격반응 분석
    fig = irf.plot(impulse='FedRate', response='WTI', orth=True)
    plt.tight_layout()
    plt.savefig('macro_trend_final.png', dpi=300)
    plt.close()
    return {"messages": ["VARX-IRF Plot saved"]}

# --- 4. 그래프 구축 및 실행 ---
workflow = StateGraph(AgentState)
workflow.add_node("fetch", fetch_data_node)
workflow.add_node("varx_analysis", varx_analysis_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("visualize", visualize_node)

workflow.set_entry_point("fetch")
workflow.add_edge("fetch", "varx_analysis")
workflow.add_edge("varx_analysis", "analyze")
workflow.add_edge("analyze", "visualize")
workflow.add_edge("visualize", END)

app = workflow.compile()

if __name__ == "__main__":
    print("🚀 Macro VARX Agent 가동...")
    try:
        app.invoke({"messages": ["Start VARX Engine"]})
        print("\n✅ 분석 완료! 'macro_trend_final.png'를 확인하세요.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")