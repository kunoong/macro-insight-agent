import streamlit as st
from agent import app as langgraph_app
import PIL.Image as Image
import os

st.title("📊 Macro Insight AI Agent")

if st.button("실시간 분석 및 PDF 생성 시작"):
    with st.spinner("데이터 분석 및 보고서 작성 중..."):
        result = langgraph_app.invoke({"messages": ["분석 시작"]})
        
        # 화면 출력
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🤖 AI 분석 리포트")
            st.markdown(result['analysis_report'])
        with col2:
            st.subheader("📈 미래 예측 차트")
            st.image('macro_trend_final.png', use_container_width=True)
            
        # PDF 다운로드 버튼 추가
        if os.path.exists("Macro_Analysis_Report.pdf"):
            with open("Macro_Analysis_Report.pdf", "rb") as f:
                st.download_button(
                    label="📄 분석 보고서 PDF 다운로드",
                    data=f,
                    file_name="Macro_Analysis_Report.pdf",
                    mime="application/pdf"
                )