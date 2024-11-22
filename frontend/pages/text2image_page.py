import streamlit as st
from frontend.utils.api import generate_image
from PIL import Image
import io
import time
import base64

def show_text2image_page():
    # 主页面标题
    st.title("🎨 趣说趣图")
    st.write("📝 输入你的想法，让AI为你创作")

    # 创建左右两列布局，比例为1:2
    input_col, center_col, output_col = st.columns([2, 0.2, 3])      

    # 左侧列 - 输入区域和生成按钮
    with input_col:
        # 文本输入区域
        user_input = st.text_area(
            label="",
            height=400,
            placeholder="写下你的想法...",
            label_visibility="collapsed"
        )
        
        # 获取当前设置
        provider = st.session_state.get('provider', 'Ollama')
        model = st.session_state.get('model', 'qwen2.5')
        temperature = st.session_state.get('temperature', 0.7)
        max_tokens = st.session_state.get('max_tokens', 500)

        # 生成按钮
        if st.button("✨ 生成", use_container_width=True):
            if user_input:
                with st.spinner('🎭 AI正在创作中...'):
                    try:
                        # 调用API生成图片，传入所有参数
                        image_data = generate_image(
                            text=user_input,
                            provider=provider,
                            model=model,
                            temperature=temperature,
                            max_tokens=max_tokens
                        )
                        
                        if image_data is not None:
                            # 生成唯一的时间戳作为key
                            timestamp = int(time.time())
                            # 保存生成的图片和时间戳到session state
                            st.session_state.generated_image = {
                                'image': image_data,
                                'timestamp': timestamp
                            }
                            
                    except Exception as e:
                        st.error(f"生成失败: {str(e)}")
            else:
                st.warning("⚠️ 请输入内容后再生成")

    # 右侧列 - 图片显示区域
    with output_col:
        # 如果没有生成新图片，显示占位框
        if 'generated_image' not in st.session_state:
            st.markdown(
                """
                <div style="height:100%;border:2px dashed #ccc;border-radius:10px;
                display:flex;align-items:center;justify-content:center;color:#666; width: 100%; height: 500px;">
                在这里展示生成的图片
                </div>
                """,
                unsafe_allow_html=True   
            )
        else:
            # 从session state中获取生成的图片数据和时间戳
            image_data = st.session_state.generated_image['image']
            
            if image_data:
                try:
                    # 创建一个固定高度的容器
                    with st.container():
                        
                        # 如果是字节数据（PNG格式）
                        if isinstance(image_data, bytes):
                            st.image(image_data, caption="🎨 AI创作结果", use_container_width=False)
                        
                        # 如果是URL
                        elif isinstance(image_data, str) and image_data.startswith(('http://', 'https://')):
                            st.image(image_data, caption="🎨 AI创作结果", use_container_width=False)
                        
                        # 如果是SVG代码
                        elif isinstance(image_data, str) and '<svg' in image_data:
                            # 使用HTML显示SVG
                            st.markdown(f"""
                                <div style="display: flex; justify-content: center;">
                                    {image_data}
                                </div>
                                """, unsafe_allow_html=False)
                        
                        else:
                            st.error("不支持的图片格式")
                            st.write("图片数据类型:", type(image_data))                          
                        
                except Exception as e:
                    st.error(f"显示图片时出错: {str(e)}")
                    st.write("错误详情:", str(e))
