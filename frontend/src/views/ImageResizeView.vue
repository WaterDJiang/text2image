<template>
  <div class="image-resize-view notion-card">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="notion-title">图片尺寸调整</h1>
      <p class="notion-subtitle">调整图片尺寸大小</p>
    </div>

    <el-row :gutter="40">
      <!-- 左侧原始图片区域 -->
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
            <!-- 重新上传按钮 -->
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
      
      <!-- 右侧调整结果区域 -->
      <el-col :span="12">
        <div class="section-title">调整结果</div>
        <div class="image-container notion-card">
          <!-- 尺寸调整控制区 -->
          <div v-if="sourceImage" class="resize-controls">
            <!-- 预览区域 -->
            <div class="preview-container">
              <img
                v-if="resultImage"
                :src="resultImage"
                class="preview-image"
                @load="checkImageOrientation"
                ref="resultImageRef"
              />
            </div>
            
            <!-- 控制面板 -->
            <div class="control-panel">
              <el-form :model="resizeForm" label-position="left" :label-width="50">
                <!-- 宽度控制 -->
                <el-form-item label="宽度">
                  <div class="size-control">
                    <el-input-number
                      v-model="resizeForm.width"
                      :min="10"
                      :max="2000"
                      :step="1"
                      @change="handleResize"
                      class="size-input"
                      controls-position="right"
                    />
                    <div class="slider-wrapper">
                      <el-slider
                        v-model="resizeForm.width"
                        :min="10"
                        :max="2000"
                        @change="handleResize"
                      />
                    </div>
                  </div>
                </el-form-item>
                
                <!-- 高度控制 -->
                <el-form-item label="高度">
                  <div class="size-control">
                    <el-input-number
                      v-model="resizeForm.height"
                      :min="10"
                      :max="2000"
                      :step="1"
                      @change="handleResize"
                      class="size-input"
                      controls-position="right"
                    />
                    <div class="slider-wrapper">
                      <el-slider
                        v-model="resizeForm.height"
                        :min="10"
                        :max="2000"
                        @change="handleResize"
                      />
                    </div>
                  </div>
                </el-form-item>
              </el-form>
              
              <!-- 操作按钮 -->
              <div class="action-buttons">
                <el-button
                  class="notion-button notion-button-primary"
                  @click="handleDownload"
                  :disabled="!resultImage"
                >
                  <el-icon><i-ep-download /></el-icon>
                  下载结果
                </el-button>
              </div>
            </div>
          </div>
          
          <!-- 未上传图片时的提示 -->
          <div v-else class="placeholder-content">
            <el-icon class="placeholder-icon"><i-ep-picture /></el-icon>
            <p class="placeholder-text">请先上传图片</p>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import ImageUploader from '@/components/ImageUploader.vue'
import { useImageProcessing } from '@/composables/useImageProcessing'

// 状态管理
const sourceImage = ref('')
const resultImage = ref('')
const currentFile = ref(null)
const isVerticalImage = ref(false)
const sourceImageRef = ref(null)
const resultImageRef = ref(null)

// 尺寸表单数据
const resizeForm = reactive({
  width: 800,
  height: 600
})

// 导入图片处理方法
const { resizeImage } = useImageProcessing()

// 处理文件选择
const handleFileSelected = async (file) => {
  currentFile.value = file
  // 获取原始图片尺寸
  const img = new Image()
  img.src = URL.createObjectURL(file)
  img.onload = () => {
    resizeForm.width = img.width
    resizeForm.height = img.height
    handleResize()
  }
}

// 检查图片方向
const checkImageOrientation = () => {
  const img = sourceImageRef.value || resultImageRef.value
  if (img) {
    isVerticalImage.value = img.naturalHeight > img.naturalWidth
  }
}

// 处理尺寸调整
const handleResize = async () => {
  if (!currentFile.value) return
  
  try {
    const result = await resizeImage(
      currentFile.value,
      resizeForm.width,
      resizeForm.height
    )
    resultImage.value = result.resized_image
  } catch (error) {
    ElMessage.error('调整失败：' + error.message)
  }
}

// 处理下载
const handleDownload = () => {
  if (resultImage.value) {
    const link = document.createElement('a')
    link.href = resultImage.value
    link.download = 'resized_image.png'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

// 重置状态
const handleReset = () => {
  sourceImage.value = ''
  resultImage.value = ''
  currentFile.value = null
  isVerticalImage.value = false
  resizeForm.width = 800
  resizeForm.height = 600
}
</script>

<style scoped>
/* 容器样式 */
.image-resize-view {
  max-width: 1200px;
  margin: 40px auto;
  padding: 32px;
}

/* 图片容器样式 */
.image-container {
  height: 500px;
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

/* 图片包装器样式 */
.image-wrapper {
  width: 100%;
  height: calc(100% - 60px);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* 竖图样式 */
.image-wrapper.vertical {
  width: 70%;
  margin: 0 auto;
}

/* 图片显示样式 */
.display-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 6px;
}

/* 竖图显示样式 */
.vertical .display-image {
  height: 100%;
  width: auto;
}

/* 调整控制区样式 */
.resize-controls {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* 预览容器样式 */
.preview-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 20px;
  min-height: 200px;
}

/* 控制面板样式 */
.control-panel {
  padding: 24px;
  border-top: 1px solid var(--notion-border);
  background: #f9f9f9;
  border-radius: 0 0 12px 12px;
}

/* 尺寸控制组合样式 */
.size-control {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
}

/* 数字输入框样式 */
.size-input {
  width: 120px;
  flex-shrink: 0;
}

/* 滑块包装器样式 */
.slider-wrapper {
  flex: 1;
  min-width: 200px; /* 确保滑块有最小宽度 */
  padding: 0 10px; /* 添加内边距 */
}

/* 调整表单项样式 */
:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-form-item__content) {
  flex: 1;
  display: flex;
}

/* 调整滑块样式 */
:deep(.el-slider) {
  width: 100%;
  margin: 0;
}

/* 调整输入框样式 */
:deep(.el-input-number.size-input .el-input__wrapper) {
  padding: 0 8px;
}

/* 操作按钮样式 */
.action-buttons {
  display: flex;
  justify-content: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--notion-border);
}

/* 占位内容样式 */
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

/* 诗意卡片主容器样式 */
.poetry-card {
  background: var(--notion-white);
  border: 1px solid var(--notion-gray);
  box-shadow: 0 4px 20px rgba(75, 96, 127, 0.08);  /* 使用深蓝灰色阴影 */
}

/* 文字样式设置 */
.comment-text {
  color: var(--notion-text);  /* 使用深蓝灰色文字 */
}

/* 按钮样式 */
.notion-button-primary {
  background: var(--notion-brown);  /* 使用橙色作为主按钮 */
  color: white;
  border: none;
}

.notion-button-primary:hover {
  background: #ff8534;  /* 橙色的亮色版本 */
}
</style> 