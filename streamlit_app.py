import streamlit as st
import requests
import json
from frontend.pages.home_page import render_home_page
from frontend.pages.settings_page import render_settings_sidebar

# 页面配置
st.set_page_config(
    page_title="Wattter 趣说趣图",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
    <style>
        .stApp {
            max-width: 100%;
            padding: 1rem;
        }
        
        .main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    try:
        # 从 Streamlit secrets 获取配置
        api_key = st.secrets["DEEPSEEK_API_KEY"]
        api_base = st.secrets["DEEPSEEK_API_BASE"]
        
        # 渲染侧边栏设置
        render_settings_sidebar()
        
        # 渲染主页面
        render_home_page()
        
        # 添加页脚
        st.markdown("---")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown(
                "<div style='text-align: center;'>"
                "<p style='color: #666666; font-size: 14px; margin: 10px 0;'>"
                "Wattter AI © 2024 | 让创意触手可及"
                "</p>"
                "</div>",
                unsafe_allow_html=True
            )
            
    except Exception as e:
        st.error(f"应用启动错误: {str(e)}")
        if "DEEPSEEK_API_KEY" not in st.secrets:
            st.error("未找到 DEEPSEEK_API_KEY，请检查 .streamlit/secrets.toml 配置")
        if "DEEPSEEK_API_BASE" not in st.secrets:
            st.error("未找到 DEEPSEEK_API_BASE，请检查 .streamlit/secrets.toml 配置")

if __name__ == "__main__":
    main() 