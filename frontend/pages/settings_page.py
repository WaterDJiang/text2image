import streamlit as st
from frontend.services.api_service import APIService
import asyncio

async def check_service_health():
    """异步检查服务健康状态"""
    api_service = APIService()
    return await api_service.check_health()

def show_settings_page():
    with st.sidebar: 
        st.title("⚙️ 设置")
        
        # 模型供应商选择
        provider = st.selectbox(
            "选择模型供应商",
            ["Ollama", "DeepSeek"],
            help="选择要使用的AI模型供应商"
        )
        
        # 根据供应商显示不同的模型选项
        if provider == "Ollama":
            model = st.selectbox(
                "选择模型",
                ["qwen2.5", "llama2", "mistral"],
                help="选择要使用的具体模型"
            )
        else:  # DeepSeek
            model = st.selectbox(
                "选择模型",
                ["deepseek-chat", "deepseek-coder"],
                help="选择要使用的具体模型"
            )
        
        # 高级设置折叠面板
        with st.expander("🛠️ 高级设置"):
            temperature = st.slider(
                "温度",
                min_value=0.0,
                max_value=2.0,
                value=0.7,
                step=0.1,
                help="控制输出的随机性，值越大输出越随机"
            )
            
            max_tokens = st.slider(
                "最大输出长度",
                min_value=100,
                max_value=2000,
                value=500,
                step=100,
                help="控制输出的最大字符数"
            )
        
        # 保存设置到session_state
        st.session_state.provider = provider
        st.session_state.model = model
        st.session_state.temperature = temperature
        st.session_state.max_tokens = max_tokens
        
        # 显示系统状态
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔄 系统状态")
        
        # 使用异步方式检查服务状态
        status_data = asyncio.run(check_service_health())
        
        if status_data.get("status") == "healthy":
            st.sidebar.success("服务正常运行")
            st.sidebar.json(status_data)
        else:
            st.sidebar.error("服务异常") 