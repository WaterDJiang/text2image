import streamlit as st
from frontend.utils.api import generate_image
from PIL import Image
import io
import time

def render_home_page():
    # 主页面标题
    st.title("🎨 趣说趣图")
    st.write("📝 输入你的想法，让AI为你创作")

    # 创建左右两列布局，比例为1:2
    input_col, output_col = st.columns([2, 3])      

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
                        # 调用API生成图片
                        image_data = generate_image(
                            user_input,
                            provider,
                            model,
                            temperature,
                            max_tokens
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
            timestamp = st.session_state.generated_image['timestamp']
            
            # 直接使用image_data显示图片，移除未使用的字节流转换代码
            st.image(
                image_data,
                caption="🎨 AI创作结果",
                use_column_width=True,
            )
