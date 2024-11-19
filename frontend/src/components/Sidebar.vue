<template>
  <el-menu
    :default-active="route.path"
    class="sidebar-menu"
    router
  >
    <!-- 模型选择 -->
    <div class="model-selector">
      <el-radio-group v-model="modelStore.currentModel" @change="handleModelChange">
        <el-radio-button label="deepseek">DeepSeek</el-radio-button>
        <el-radio-button label="coze">Coze</el-radio-button>
      </el-radio-group>
    </div>

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
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useModelStore } from '../stores/modelStore'
import { ElMessage } from 'element-plus'

const route = useRoute()
const modelStore = useModelStore()

const handleModelChange = (value) => {
  ElMessage.success(`已切换到 ${value.toUpperCase()} 模型`)
}
</script>

<style scoped>
.model-selector {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #eee;
}
</style> 