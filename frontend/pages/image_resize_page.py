import streamlit as st
from PIL import Image
import io

def show_image_resize_page():
    """
    显示图片调整工具页面,采用左右分栏布局
    """
    st.title("📐 图片尺寸调整工具")
    
    # 创建左右两列布局
    input_col, output_col = st.columns([2, 3])
    
    # 左侧列 - 输入和设置区域
    with input_col:
        # 上传图片
        uploaded_file = st.file_uploader("选择要调整大小的图片", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            # 读取上传的图片
            image = Image.open(uploaded_file)
            
            # 显示原始尺寸
            st.write(f"原始尺寸: {image.size[0]} x {image.size[1]} 像素")
            
            # 添加预览图片,限制高度为300像素并保持宽高比
            preview_height = 300
            aspect_ratio = image.size[0] / image.size[1]
            preview_width = int(preview_height * aspect_ratio)
            preview_image = image.resize((preview_width, preview_height))
            st.image(preview_image, caption="图片预览")
            
            # 调整选项
            resize_method = st.radio(
                "选择调整方式:",
                ("按比例缩放", "自定义尺寸")
            )
            
            if resize_method == "按比例缩放":
                scale = st.slider("缩放比例", 1, 200, 100) / 100
                new_width = int(image.size[0] * scale)
                new_height = int(image.size[1] * scale)
            else:
                col1, col2 = st.columns(2)
                with col1:
                    new_width = st.number_input("新宽度", min_value=1, value=image.size[0])
                with col2:
                    new_height = st.number_input("新高度", min_value=1, value=image.size[1])
            
            # 调整按钮
            if st.button("✨ 调整大小", use_container_width=True):
                # 调整图片大小
                resized_image = image.resize((new_width, new_height))
                # 保存结果到session state
                st.session_state.resized_image = {
                    'image': resized_image
                }

    # 右侧列 - 显示区域
    with output_col:
        if 'resized_image' not in st.session_state:
            # 显示占位框
            st.markdown(
                """
                <div style="height:100%;border:2px dashed #ccc;border-radius:10px;
                display:flex;align-items:center;justify-content:center;color:#666; width: 100%; height: 500px;">
                在这里展示调整后的图片
                </div>
                """,
                unsafe_allow_html=True   
            )
        else:
            # 只显示调整后的图片
            st.image(st.session_state.resized_image['image'], caption="调整后的图片")
            
            # 提供下载选项
            buf = io.BytesIO()
            st.session_state.resized_image['image'].save(buf, format="PNG")
            st.download_button(
                label="💾 下载调整后的图片",
                data=buf.getvalue(),
                file_name="resized_image.png",
                mime="image/png",
                use_container_width=True
            )