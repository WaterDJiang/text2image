<template>
  <div class="poetry-view notion-card">
    <div class="page-header">
      <h1 class="notion-title">趣语趣图</h1>
      <p class="notion-subtitle">输入文字，AI来说趣话</p>
    </div>

    <div class="poetry-container">
      <!-- 输入区域 -->
      <div class="input-section">
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="4"
          placeholder="请输入文字..."
          resize="none"
        />
        <el-button 
          class="generate-button notion-button notion-button-primary"
          :loading="processing"
          @click="handleGenerate"
        >
          <el-icon v-if="!processing"><i-ep-magic-stick /></el-icon>
          {{ processing ? '生成中...' : '生成趣图' }}
        </el-button>
      </div>

      <!-- 结果展示区域 -->
      <div v-if="result" class="result-section">
        <div class="poetry-card notion-card">
          <div class="poetry-content">
            <!-- 文字区域 -->
            <div class="text-section">
              <div class="comment-text" v-html="result.comment"></div>
              <!-- 添加装饰分隔线 -->
              <div class="divider">
                <div class="divider-line"></div>
              </div>
            </div>
            <!-- SVG图片区域 -->
            <div class="svg-container" v-html="result.svg"></div>
          </div>
        </div>
        
        <div class="action-buttons">
          <el-button 
            @click="handleViewImage" 
            class="notion-button"
            size="small"
          >
            <el-icon><i-ep-view /></el-icon>
            查看图片
          </el-button>
          <el-button 
            @click="handleReset" 
            class="notion-button"
            size="small"
          >
            <el-icon><i-ep-refresh /></el-icon>
            重新生成
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useImageProcessing } from '@/composables/useImageProcessing'
import html2canvas from 'html2canvas'

const inputText = ref('')
const result = ref(null)
const processing = ref(false)

const { processPoetry } = useImageProcessing()

// 生成趣语
const handleGenerate = async () => {
  if (!inputText.value.trim()) {
    ElMessage.warning('请入文字')
    return
  }

  processing.value = true
  try {
    result.value = await processPoetry(inputText.value)
    ElMessage.success('生成成功')
  } catch (error) {
    ElMessage.error('生成失败：' + error.message)
  } finally {
    processing.value = false
  }
}

// 查看图片
const handleViewImage = async () => {
  if (!result.value) return
  
  try {
    const cardContent = document.querySelector('.poetry-card')
    const canvas = await html2canvas(cardContent, {
      backgroundColor: '#ffffff',
      scale: 2,
      useCORS: true,
      logging: false
    })
    
    const imageData = canvas.toDataURL('image/png')
    
    const newWindow = window.open()
    newWindow.document.write(`
      <title>趣语趣图</title>
      <style>
        body {
          margin: 0;
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 100vh;
          background: #f5f5f5;
        }
        img {
          max-width: 100%;
          max-height: 100vh;
          object-fit: contain;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
          border-radius: 16px;
        }
      </style>
      <img src="${imageData}" alt="趣语趣图">
    `)
  } catch (error) {
    ElMessage.error('片生成失败')
  }
}

// 重
const handleReset = () => {
  inputText.value = ''
  result.value = null
}
</script>

<style scoped>
/* 主容器样式 */
.poetry-view {
  max-width: 800px;
  margin: 40px auto;
  padding: 32px;
}

/* 内容布局容器 */
.poetry-container {
  display: flex;
  flex-direction: column;
  gap: 32px; /* 区块间距 */
}

/* 输入区域样式 */
.input-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 生成按钮样式 */
.generate-button {
  align-self: flex-end;
  min-width: 120px;
}

/* 结果展示区域 */
.result-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 诗词卡片主容器 - 保持9:16比例 */
.poetry-card {
  padding: 20px;
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 450px; /* 限制最大宽度 */
  aspect-ratio: 9/16; /* 保持固定宽高比 */
  overflow: hidden;
  margin: 0 auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

/* 诗词内容布局 - 明确分配空间 */
.poetry-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 0; /* 移除内边距，由子元素控制 */
}

/* 文字区域样式 - 固定高度比例 */
.text-section {
  flex: 0 0 40%; /* 固定占用40%高度 */
  padding: 20px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 文字垂直居中 */
}

/* 评论文字样式 */
.comment-text {
  font-size: 1.2rem;
  line-height: 1.8;
  color: var(--notion-text);
  text-align: center;
  white-space: pre-line;
  margin-bottom: 10px; /* 减小底部边距 */
  font-weight: 500;
  max-width: 90%;
  overflow-wrap: break-word;
}

/* 分隔线调整 */
.divider {
  width: 80%;
  margin: 10px auto;
}

/* 渐变分隔线 */
.divider-line {
  width: 100%;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent,
    var(--notion-border) 20%,
    var(--notion-border) 80%,
    transparent
  );
}

/* SVG容器 - 固定比例和位置 */
.svg-container {
  flex: 0 0 60%; /* 固定占用60%高度 */
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  position: relative;
  padding: 10px; /* 添加内边距作为边框 */
  box-sizing: border-box;
}

/* SVG图片样式 - 自适应填充 */
.svg-container :deep(svg) {
  width: 95%; /* 占用容器95%宽度，留5%作为边框 */
  height: 95%; /* 占用容器95%高度，留5%作为边框 */
  object-fit: contain;
  display: block;
  margin: auto;
  background-color: transparent;
}

/* 确保容器在卡片中正确显示 */
.poetry-content {
  height: 30%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px 0; /* 增加上下内边距 */
}

/* 卡片样式穿透 */
:deep(.poetry-card) {
  box-sizing: border-box;
  position: relative;
}

/* 卡片阴影和边框 */
.poetry-card {
  animation: fadeIn 0.4s ease;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
  border: 1px solid var(--notion-border);
}

/* 内容背景渐变 */
.poetry-content {
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(249, 250, 251, 0.5) 100%
  );
}

/* 文字阴影效果 */
.comment-text {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

/* 操作按钮容器 */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
}

/* 淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 