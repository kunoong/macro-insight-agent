import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings

# 불필요한 경고 숨김
warnings.filterwarnings('ignore')

def make_stationary(series, name, verbose=False):
    """ADF 검정을 통한 동적 차분(Differencing) 수행"""
    for d in range(3):
        s = series.diff(d).dropna() if d > 0 else series.dropna()
        try:
            stat, p, _, _, _, _ = adfuller(s, autolag='AIC')
        except Exception:
            p = 1.0
        if p < 0.05:
            return series.diff(d) if d > 0 else series, d
    return series.diff(2), 2

class MacroDataEngine:
    def __init__(self):
        self.macro_file = 'data.xlsx'
        self.pc_file = 'PC_Scores.xlsx'

    def fetch_and_process(self):
        print(f"🚀 데이터 로드 시작: {self.macro_file}, {self.pc_file}")
        macro_df = pd.read_excel(self.macro_file)
        pc_df = pd.read_excel(self.pc_file)
        
        # 캄보디아 PC1 필터링 및 병합
        country_pc = pc_df[pc_df['국가명'] == '캄보디아'][['기간', 'PC1']].copy()
        country_pc = country_pc.sort_values('기간').reset_index(drop=True)
        merged = country_pc.merge(
            macro_df, left_on='기간', right_on='YearMonth', how='inner'
        ).drop(columns=['YearMonth']).set_index('기간')
        
        print("🔍 ADF 단위근 검정 및 자동 차분(Differencing) 적용 중...")
        stationary_data = {}
        for col in ['PC1', 'FedRate', 'WTI', 'DXY', 'SCFI']:
            s, d = make_stationary(merged[col], col)
            stationary_data[col] = s
            
        stat_df = pd.DataFrame(stationary_data).dropna()
        print("✅ 데이터 정상성 확보 완료")
        return stat_df

if __name__ == "__main__":
    engine = MacroDataEngine()
    stat_df = engine.fetch_and_process()
    
    endog = stat_df['PC1']
    exog = stat_df[['FedRate', 'WTI', 'DXY', 'SCFI']]
    
    print("\n🚀 SARIMAX 최적 시차(Lag) 탐색 중...")
    best_aic = np.inf
    best_lag = 1
    for lag in range(1, 5):
        try:
            m = SARIMAX(endog, exog=exog, order=(lag, 0, 0), trend='c').fit(disp=False)
            if m.aic < best_aic:
                best_aic = m.aic
                best_lag = lag
        except Exception:
            pass
            
    print(f"✅ 최적 시차(p) 선택 완료: {best_lag}")
    
    model = SARIMAX(endog, exog=exog, order=(best_lag, 0, 0), trend='c')
    results = model.fit(disp=False)
    
    gamma_1 = results.params['FedRate']
    p_val = results.pvalues['FedRate']
    
    print("\n" + "="*40)
    print("🎯 [AI 에이전트 검증 리포트]")
    print(f"최적 모형: SARIMAX(p={best_lag}, 0, 0) - 상수항 포함")
    print(f"변수: FedRate -> PC1")
    print(f"계수(γ): {gamma_1:.4f}")
    print(f"P-value: {p_val:.4f}")
    print("="*40)