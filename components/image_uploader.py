import streamlit as st
from PIL import Image
import io

class ImageUploader:
    def render(self):
        st.header("图片大小调整")
        
        uploaded_file = st.file_uploader("选择图片", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            # 显示原始图片
            image = Image.open(uploaded_file)
            
            # 创建两列布局
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("原始图片")
                st.image(image, caption="原始图片")
            
            with col2:
                st.subheader("调整后的图片")
                
                # 添加尺寸调整滑块
                width = st.slider("宽度", 1, 1000, image.size[0])
                height = st.slider("高度", 1, 1000, image.size[1])
                
                # 调整图片大小
                resized_image = image.resize((width, height))
                st.image(resized_image, caption=f"调整后的图片 ({width}x{height})")
                
                # 添加下载按钮
                buf = io.BytesIO()
                resized_image.save(buf, format="PNG")
                st.download_button(
                    label="下载调整后的图片",
                    data=buf.getvalue(),
                    file_name="resized_image.png",
                    mime="image/png"
                ) 