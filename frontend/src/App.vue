<template>
  <el-container class="app-container">
    <el-aside width="240px" class="notion-sidebar">
      <div class="sidebar-header">
        <h3>AI图片助手</h3>
        <div class="model-selector">
          <el-radio-group v-model="modelStore.currentModel" @change="handleModelChange" size="small">
            <el-radio-button label="deepseek">DeepSeek</el-radio-button>
            <el-radio-button label="coze">Coze</el-radio-button>
          </el-radio-group>
        </div>
      </div>

      <el-menu
        router
        :default-active="$route.path"
        class="notion-menu"
        background-color="var(--menu-bg)"
        text-color="var(--menu-text)"
        active-text-color="var(--menu-active)"
      >
        <el-menu-item index="/poetry">
          <el-icon><i-ep-reading /></el-icon>
          <span>趣语趣图</span>
        </el-menu-item>        

        <el-menu-item index="/mood">
          <el-icon><i-ep-edit /></el-icon>
          <span>心情文案</span>
        </el-menu-item>
        
        <el-menu-item index="/sarcastic">
          <el-icon><i-ep-chat-dot-round /></el-icon>
          <span>毒舌看图</span>
        </el-menu-item>
        
        <el-menu-item index="/story">
          <el-icon><i-ep-notebook /></el-icon>
          <span>故事创作</span>
        </el-menu-item>
        
        <el-menu-item index="/resize">
          <el-icon><i-ep-picture /></el-icon>
          <span>图片调整</span>
        </el-menu-item>
        
        <el-menu-item index="/history">
          <el-icon><i-ep-time /></el-icon>
          <span>历史记录</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<script setup>
import { useModelStore } from './stores/modelStore'
import { ElMessage } from 'element-plus'

const modelStore = useModelStore()

const handleModelChange = (value) => {
  ElMessage.success(`已切换到 ${value.toUpperCase()} 模型`)
}
</script>

<style>
:root {
  /* 主题色 */
  --primary-color: #409EFF;  /* Element Plus 的主题蓝 */
  --primary-light: #79BBFF;
  --primary-dark: #337ECC;
  
  /* 背景色 */
  --bg-color: #F5F7FA;  /* 整体背景色 */
  --menu-bg: #FFFFFF;   /* 侧边栏背景色 */
  --sidebar-bg: #FFFFFF;
  --content-bg: #FFFFFF; /* 内容区背景色 */
  
  /* 文字颜色 */
  --text-primary: #303133;
  --text-regular: #606266;
  --text-secondary: #909399;
  --menu-text: #606266;
  --menu-active: var(--primary-color);
  
  /* 边框颜色 */
  --border-color: #DCDFE6;
  
  /* 阴影 */
  --shadow-light: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  --shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
}

/* 暗色主题 */
@media (prefers-color-scheme: dark) {
  :root {
    --primary-color: #409EFF;
    --primary-light: #79BBFF;
    --primary-dark: #337ECC;
    
    --bg-color: #141414;
    --menu-bg: #1F1F1F;
    --sidebar-bg: #1F1F1F;
    --content-bg: #1F1F1F;
    
    --text-primary: #E5EAF3;
    --text-regular: #CFD3DC;
    --text-secondary: #A3A6AD;
    --menu-text: #CFD3DC;
    
    --border-color: #363637;
    
    --shadow-light: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    --shadow: 0 2px 4px rgba(0, 0, 0, .24), 0 0 6px rgba(0, 0, 0, .12);
  }
}

body {
  margin: 0;
  background-color: var(--bg-color);
  color: var(--text-regular);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.app-container {
  height: 100vh;
  background-color: var(--bg-color);
}

.notion-sidebar {
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border-color);
  box-shadow: var(--shadow-light);
  transition: all 0.3s ease;
}

.sidebar-header {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--menu-bg);
}

.sidebar-header h3 {
  margin: 0 0 15px 0;
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 600;
}

.model-selector {
  margin-bottom: 10px;
}

.model-selector .el-radio-group {
  display: flex;
  gap: 8px;
}

.model-selector .el-radio-button__inner {
  background-color: var(--menu-bg);
  color: var(--text-regular);
  border-color: var(--border-color);
  padding: 8px 15px;
  transition: all 0.3s ease;
}

.model-selector .el-radio-button__original-radio:checked + .el-radio-button__inner {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  box-shadow: -1px 0 0 0 var(--primary-color);
}

.notion-menu {
  border-right: none;
  background-color: var(--menu-bg) !important;
  padding: 8px;
}

.el-menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 50px;
  padding: 0 16px;
  margin: 4px 0;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.el-menu-item:hover {
  background-color: var(--primary-light) !important;
  color: white !important;
}

.el-menu-item.is-active {
  background-color: var(--primary-color) !important;
  color: white !important;
}

.el-menu-item .el-icon {
  margin-right: 8px;
  font-size: 18px;
}

.el-main {
  padding: 24px;
  background-color: var(--content-bg);
}

/* 美化滚动条 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: var(--menu-bg);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: var(--text-secondary);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--text-regular);
}

/* 卡片样式 */
.el-card {
  background-color: var(--content-bg);
  border-color: var(--border-color);
  box-shadow: var(--shadow-light);
}

/* 按钮样式 */
.el-button {
  transition: all 0.3s ease;
}

.el-button--primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.el-button--primary:hover {
  background-color: var(--primary-light);
  border-color: var(--primary-light);
}
</style> 