import streamlit as st
import base64
from services.imgbb_service import ImgBBService
from services.coze_service import CozeService
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        self.imgbb_service = ImgBBService()
        self.coze_service = CozeService()
    
    def render(self):
        # 创建主容器
        with st.container():
            # 左侧上传区域
            col1, col2 = st.columns([1, 1], gap="large")
            
            with col1:
                # 创建虚线边框的上传区域
                upload_placeholder = st.empty()
                with upload_placeholder.container():
                    st.markdown("""
                        <style>
                            .uploadfile {
                                border: 2px dashed #E6E6E6;
                                border-radius: 10px;
                                padding: 20px;
                                text-align: center;
                            }
                        </style>
                    """, unsafe_allow_html=True)
                    
                    uploaded_file = st.file_uploader(
                        "拖拽图片到这里或点击上传",
                        type=['png', 'jpg', 'jpeg'],
                        key="uploader"
                    )
                    
                    if uploaded_file is not None:
                        st.image(uploaded_file, use_container_width=True)
            
            # 右侧生成结果区域
            with col2:
                if uploaded_file is not None:
                    st.markdown("### 生成结果")
                    
                    # 处理按钮
                    if st.button("生成文案", type="primary", use_container_width=True):
                        with st.spinner("处理中..."):
                            try:
                                # 转换图片为base64
                                bytes_data = uploaded_file.getvalue()
                                base64_image = base64.b64encode(bytes_data).decode()
                                
                                # 上传到ImgBB
                                with st.status("正在处理...") as status:
                                    status.write("上传图片中...")
                                    image_url = self.imgbb_service.upload_image(base64_image)
                                    
                                    if image_url:
                                        status.write("生成文案中...")
                                        result = self.coze_service.process_image(image_url)
                                        
                                        if result and result.get('output_image_url'):
                                            status.update(label="处理完成！", state="complete")
                                            
                                            # 显示结果
                                            st.image(result['output_image_url'], use_container_width=True)
                                            
                                            # 添加操作按钮
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                st.download_button(
                                                    "下载图片",
                                                    result['output_image_url'],
                                                    file_name="generated_image.png",
                                                    use_container_width=True
                                                )
                                            with col2:
                                                st.button(
                                                    "分享",
                                                    use_container_width=True
                                                )
                                        else:
                                            status.update(label="处理失败", state="error")
                                            st.error("生成失败，请稍后重试")
                                    else:
                                        status.update(label="上传失败", state="error")
                                        st.error("图片上传失败，请检查网络连接")
                                
                            except Exception as e:
                                logger.exception("处理图片时发生错误")
                                st.error(f"处理过程中发生错误: {str(e)}") 