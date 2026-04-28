import pandas as pd
from fredapi import Fred
from statsmodels.tsa.stattools import adfuller
import warnings

# 경고 메시지 무시 (ADF 검정 시 발생하는 불필요한 경고 방지)
warnings.filterwarnings('ignore')

class MacroDataEngine:
    def __init__(self, api_key):
        """
        데이터 수집 및 전처리를 담당하는 엔진 클래스
        """
        self.fred = Fred(api_key=api_key)
        # 논문 분석 기반 핵심 외생변수 매핑 [cite: 250]
        self.indicators = {
            'FEDFUNDS': 'FedRate',   # 미국 기준금리
            'DCOILWTICO': 'WTI',     # 국제유가
            'DTWEXBGS': 'DXY'        # 달러 인덱스
        }

    def fetch_and_process(self, start_date='2019-01-01'):
        """
        데이터 수집 -> 리샘플링 -> ADF 검정 -> 조건부 차분 수행
        """
        master_df = pd.DataFrame()
        
        print("🚀 거시경제 데이터 수집 및 분석 시작...")

        for s_id, name in self.indicators.items():
            # 1. 데이터 수집 [cite: 30, 48]
            series = self.fred.get_series(s_id, observation_start=start_date)
            
            # 2. 월간 리샘플링 (일일 데이터를 월간 평균으로 변환하여 주기 일치)
            # 논문의 월별 패널 데이터 분석 방식을 준수합니다[cite: 166, 183].
            series_monthly = series.resample('MS').mean()
            df = pd.DataFrame(series_monthly, columns=[name])
            
            # 3. ADF 정상성 검정 (논문 3.3.2절 방법론 적용) [cite: 258]
            clean_series = df[name].dropna()
            if len(clean_series) > 0:
                result = adfuller(clean_series)
                p_value = result[1]
                
                print(f"\n[{name}] ADF p-value: {p_value:.4f}")
                
                # 4. 정상성 기반 처리 로직
                if p_value <= 0.05:
                    print(f"-> {name}: 정상(Stationary). 원계열을 유지합니다.")
                    master_df[name] = df[name]
                else:
                    # FedRate는 비정상이지만 정책적 지속성을 고려해 원계열 유지 [cite: 260, 469]
                    if name == 'FedRate':
                        print(f"-> {name}: 비정상이지만 논문 근거에 따라 원계열을 유지합니다.")
                        master_df[name] = df[name]
                    else:
                        # 그 외 변수는 정상성 확보를 위해 1차 차분 수행 [cite: 259, 261]
                        print(f"-> {name}: 비정상(Non-Stationary). 1차 차분을 수행합니다.")
                        master_df[f'diff_{name}'] = df[name].diff()
        
        # 5. 차분으로 인해 발생한 첫 행의 NaN 제거
        final_df = master_df.dropna()
        
        print("\n" + "="*40)
        print("✅ 전처리 완료: 분석 준비 데이터셋 확보")
        print("="*40)
        
        return final_df

# === 실행부 ===
if __name__ == "__main__":
    # 이건웅 님의 API Key 적용
    USER_API_KEY = '5bc51add4d98b30c600855acaee6391c'
    
    # 엔진 인스턴스 생성
    engine = MacroDataEngine(USER_API_KEY)
    
    # 데이터 처리 실행
    processed_data = engine.fetch_and_process()
    
    # 결과 출력
    print(processed_data.tail(10))