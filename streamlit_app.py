import streamlit as st
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

with st.sidebar:
        col1_1, col1_2 = st.columns([1,2])
        with col1_1:
            try:
                image_path = "frontend/static/images/im3.png"
                st.image(image_path, width=70)
            except Exception as e:
                st.error(f"加载图片失败: {str(e)}")
        with col1_2:
            st.title("Wattter.AI")
            # 显示固定的版本信息
            st.sidebar.caption("作者：[ Water.D.J ]")
            st.sidebar.caption("版本： 0.1.0.1")
            st.sidebar.caption("https://github.com/WaterDJiang/text2image")

def main():
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

if __name__ == "__main__":
    main() 