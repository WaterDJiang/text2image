import streamlit as st
from frontend.pages.text2image_page import show_text2image_page
from frontend.pages.image_resize_page import show_image_resize_page
from frontend.pages.settings_page import show_settings_page

def main():
    """
    主应用程序入口
    配置页面布局和导航
    """
    # 配置页面基本设置
    st.set_page_config(
        page_title="AI 图像工具集",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 侧边栏导航设置
    with st.sidebar:
        st.title("🎨 AI 图像工具集")
        st.divider()
        
        # 使用 radio 按钮作为导航菜单
        page = st.radio(
            "选择功能:",
            options=[
                "🎨 AI 文生图",
                "📐 图片尺寸调整",
            ],
            index=0,
            key="navigation"
        )
       
    show_settings_page()

    # 根据选择的页面显示相应内容
    if page == "🎨 AI 文生图":
        show_text2image_page()
    elif page == "📐 图片尺寸调整":
        show_image_resize_page()


if __name__ == "__main__":
    main() 