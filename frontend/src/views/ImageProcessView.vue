<template>
  <div class="image-process-view notion-card">
    <div class="page-header">
      <h1 class="notion-title">{{ title }}</h1>
      <p class="notion-subtitle">{{ subtitle }}</p>
    </div>

    <el-row :gutter="40">
      <el-col :span="12">
        <div class="section-title">原始图片</div>
        <div class="image-container notion-card">
          <template v-if="!sourceImage">
            <ImageUploader
              v-model="sourceImage"
              @file-selected="handleFileSelected"
            />
          </template>
          <template v-else>
            <div class="image-wrapper" :class="{ 'vertical': isVerticalImage }">
              <img 
                :src="sourceImage" 
                class="display-image"
                @load="checkImageOrientation"
                ref="sourceImageRef"
              />
            </div>
            <div class="action-buttons">
              <el-button 
                @click="handleReset" 
                class="notion-button"
                size="small"
              >
                <el-icon><i-ep-refresh /></el-icon>
                重新上传
              </el-button>
            </div>
          </template>
        </div>
      </el-col>
      
      <el-col :span="12">
        <div class="section-title">处理结果</div>
        <div class="image-container notion-card">
          <template v-if="!resultImage">
            <div class="placeholder-content" v-if="sourceImage">
              <el-button
                class="notion-button notion-button-primary"
                :loading="processing"
                @click="handleProcess"
              >
                <el-icon v-if="!processing"><i-ep-magic-stick /></el-icon>
                {{ processing ? '处理中...' : '开始处理' }}
              </el-button>
            </div>
            <div class="placeholder-content" v-else>
              <el-icon class="placeholder-icon"><i-ep-picture /></el-icon>
              <p class="placeholder-text">请先上传图片</p>
            </div>
          </template>
          <template v-else>
            <div class="image-wrapper" :class="{ 'vertical': isVerticalImage }">
              <img 
                :src="resultImage" 
                class="display-image"
                @load="checkImageOrientation"
                ref="resultImageRef"
              />
            </div>
            <div class="action-buttons">
              <el-button 
                @click="handleDownload" 
                class="notion-button notion-button-primary"
                size="small"
              >
                <el-icon><i-ep-download /></el-icon>
                下载结果
              </el-button>
            </div>
          </template>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import ImageUploader from '@/components/ImageUploader.vue'
import { useImageProcessing } from '@/composables/useImageProcessing'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    required: true
  },
  workflowType: {
    type: String,
    default: 'mood'
  }
})

const sourceImage = ref('')
const resultImage = ref('')
const processing = ref(false)
const currentFile = ref(null)
const isVerticalImage = ref(false)
const sourceImageRef = ref(null)
const resultImageRef = ref(null)

const { processImage } = useImageProcessing()

const handleFileSelected = (file) => {
  currentFile.value = file
  resultImage.value = ''
}

const checkImageOrientation = () => {
  // 检查图片方向
  const img = sourceImageRef.value || resultImageRef.value
  if (img) {
    isVerticalImage.value = img.naturalHeight > img.naturalWidth
  }
}

const handleProcess = async () => {
  if (!currentFile.value) {
    ElMessage.warning('请先上传图片')
    return
  }

  processing.value = true
  try {
    const result = await processImage(currentFile.value, props.workflowType)
    resultImage.value = result.postcardImage
    ElMessage.success('处理成功')
  } catch (error) {
    ElMessage.error('处理失败：' + error.message)
  } finally {
    processing.value = false
  }
}

const handleDownload = () => {
  if (resultImage.value) {
    const link = document.createElement('a')
    link.href = resultImage.value
    link.download = `${props.workflowType}_result.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

const handleReset = () => {
  sourceImage.value = ''
  resultImage.value = ''
  currentFile.value = null
  isVerticalImage.value = false
}
</script>

<style scoped>
.image-process-view {
  max-width: 1200px;
  margin: 40px auto;
  padding: 32px;
}

.section-title {
  font-weight: 600;
  font-size: 1.125rem;
  margin-bottom: 16px;
  color: var(--notion-text);
}

.image-container {
  height: 500px;  /* 增加容器高度 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: var(--notion-white);
  border: 1px solid var(--notion-border);
  transition: all 0.3s ease;
  padding: 24px;
  position: relative;
}

.image-wrapper {
  width: 100%;
  height: calc(100% - 60px); /* 减去按钮的高度 */
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.image-wrapper.vertical {
  width: 70%;  /* 竖图宽度调整为70% */
  margin: 0 auto;
}

.display-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 6px;
}

.vertical .display-image {
  height: 100%;  /* 竖图高度占满容器 */
  width: auto;   /* 宽度自适应 */
}

.placeholder-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--notion-gray);
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.placeholder-text {
  font-size: 14px;
}

.action-buttons {
  position: absolute;
  bottom: 16px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 0 24px;
  height: 32px; /* 固定高度 */
}

.action-buttons .notion-button {
  min-width: 100px; /* 统一按钮最小宽度 */
}

.placeholder-content .notion-button {
  min-width: 120px; /* 主操作按钮稍微宽一点 */
}

/* 处理中状态的按钮样式 */
.notion-button.is-loading {
  background-color: var(--notion-blue);
  opacity: 0.8;
}

/* 禁用状态的按钮样式 */
.notion-button[disabled] {
  background-color: var(--notion-gray);
  opacity: 0.5;
}

/* 动画效果 */
.notion-card {
  animation: fadeIn 0.3s ease;
}

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