import streamlit as st
from agent import app as langgraph_app
import os

st.set_page_config(page_title="Macro Insight AI Agent", layout="wide")
st.title("📊 Macro Insight AI Agent: Cambodia Edition")

if st.button("실시간 파이프라인 가동 및 리포트 생성"):
    with st.spinner("AI 엔진 구동 중 (데이터 전처리 -> 모형 추정 -> 시각화)..."):
        try:
            result = langgraph_app.invoke({"messages": ["Start"]})
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🤖 AI 인사이트 리포트")
                st.markdown(result['analysis_report'])
            with col2:
                st.subheader("📈 외생변수 동시적 충격 효과 (γ)")
                if os.path.exists('macro_trend_final.png'):
                    st.image('macro_trend_final.png', use_container_width=True)
        except Exception as e:
            st.error(f"파이프라인 실행 중 오류가 발생했습니다: {e}")