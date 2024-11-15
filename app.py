import streamlit as st
from components.image_uploader import ImageUploader
from components.image_processor import ImageProcessor
import urllib3
import warnings
import os

# 禁用SSL验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

def main():
    # 设置页面配置
    st.set_page_config(
        layout="wide", 
        page_title="AI图片处理工具",
        initial_sidebar_state="expanded"
    )
    
    # 侧边栏配置
    with st.sidebar:
        # 使用emoji作为logo
        st.markdown("# 🤖")  # 使用emoji替代logo图片
        st.title("Wattter AI创作助手")
        
        # 功能选择
        selected_function = st.radio(
            "",
            ["心情文案", "毒舌看图", "诗意看图", "故事创作", "历史记录"],
            key="function_selector",
            index=0
        )
        
        # 添加设置选项
        with st.expander("设置"):
            st.checkbox("自动保存")
            st.selectbox("语言", ["简体中文", "English"])
        
        # 添加版本信息
        st.sidebar.caption("版本: 1.0.0")
    
    # 主要内容区域
    if selected_function == "心情文案":
        st.title("心情文案生成")
        st.caption("上传图片，AI秒变文案高手")
        ImageProcessor().render()
    elif selected_function == "毒舌看图":
        st.title("毒舌看图")
        st.caption("上传图片，AI来毒舌")
        ImageProcessor().render()

if __name__ == "__main__":
    main() 