<template>
  <div class="poetry-view notion-card">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="notion-title">诗意绘图</h1>
      <p class="notion-subtitle">输入任意文字，AI来绘制诗意十足的图片</p>
    </div>

    <el-row :gutter="40">
      <!-- 左侧输入区域 -->
      <el-col :span="12">
        <div class="section-title">文字输入</div>
        <div class="input-container notion-card">
          <el-input
            v-model="inputText"
            type="textarea"
            :rows="8"
            placeholder="请输入你想要表达的文字..."
            resize="none"
          />
          <div class="action-buttons">
            <el-button 
              class="notion-button notion-button-primary"
              :loading="processing"
              @click="handleProcess"
              :disabled="!inputText.trim()"
            >
              <el-icon v-if="!processing"><i-ep-magic-stick /></el-icon>
              {{ processing ? '生成中...' : '开始生成' }}
            </el-button>
          </div>
        </div>
      </el-col>
      
      <!-- 右侧果展示区域 -->
      <el-col :span="12">
        <div class="section-title">生成结果</div>
        <div class="result-container notion-card">
          <template v-if="!result">
            <div class="placeholder-content">
              <el-icon class="placeholder-icon"><i-ep-picture /></el-icon>
              <p class="placeholder-text">请先输入文字并生成</p>
            </div>
          </template>
          <template v-else>
            <div class="result-content">
              <!-- 结果卡片 -->
              <div class="poetry-card">
                <!-- 评论文字 -->
                <div class="comment-text">{{ result.comment }}</div>
                <!-- SVG图片容器 -->
                <div class="svg-container" v-html="result.svg"></div>
              </div>
              <!-- 下载按钮 -->
              <div class="action-buttons">
                <el-button 
                  @click="handleViewImage" 
                  class="notion-button"
                  size="small"
                >
                  <el-icon><i-ep-view /></el-icon>
                  查看图片
                </el-button>
              </div>
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
import html2canvas from 'html2canvas'
import { useImageProcessing } from '@/composables/useImageProcessing'

const inputText = ref('')
const processing = ref(false)
const result = ref(null)

const { processPoetry } = useImageProcessing()

// 处理生成请求
const handleProcess = async () => {
  if (!inputText.value.trim()) return
  
  processing.value = true
  try {
    const response = await processPoetry(inputText.value)
    result.value = {
      comment: response.comment,
      svg: response.svg
    }
  } catch (error) {
    ElMessage.error(error.message || '生成失败')
  } finally {
    processing.value = false
  }
}

// 修改处理函数：只截取卡片内容
const handleViewImage = async () => {
  if (!result.value) return
  
  try {
    // 修改为只选择 poetry-card 容器
    const cardContent = document.querySelector('.poetry-card')
    const canvas = await html2canvas(cardContent, {
      // 设置截图选项
      backgroundColor: '#ffffff', // 设置背景色
      scale: 2, // 提高图片清晰度
      useCORS: true, // 允许加载跨域图片
      logging: false // 关闭日志
    })
    
    // 获取图片的 base64 数据
    const imageData = canvas.toDataURL('image/png')
    
    // 在新标签页中打开图片
    const newWindow = window.open()
    newWindow.document.write(`
      <title>诗意图片</title>
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
      <img src="${imageData}" alt="诗意图片">
    `)
  } catch (error) {
    ElMessage.error('图片生成失败')
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;500&display=swap');

/* 整体页面容器样式 */
.poetry-view {
  max-width: 1200px;         /* 最大宽度限制 */
  margin: 40px auto;         /* 上下间距40px，左右居中 */
  padding: 32px;             /* 内部填充32px */
}

/* 输入区域和结果区域的公共样式 */
.input-container,
.result-container {
  height: 510px;             /* 固定高度500px */
  display: flex;             /* 弹性布局 */
  flex-direction: column;    /* 纵向排列 */
  background: var(--notion-white);    /* 使用预设的白色背景 */
  border: 1px solid var(--notion-border);  /* 使用预设的边框颜色 */
  transition: all 0.3s ease; /* 所有属性变化时添加0.3秒过渡效果 */
  padding: 24px;             /* 内部填充24px */
  position: relative;        /* 相对定位 */
}

/* 输入框样式调整 */
.input-container :deep(.el-textarea__inner) {
  height: calc(100% - 80px);  /* 输入框高度，预留底部按钮空间 */
  font-size: 16px;            /* 输入文字大小 */
  line-height: 1.6;           /* 行高 */
  padding: 16px;              /* 内边距 */
}

/* 结果展示区整体容器 */
.result-content {
  height: 100%;               /* 占满容器高度 */
  display: flex;              /* 弹性布局 */
  flex-direction: column;     /* 纵向排列 */
  gap: 1px;                 /* 子元素间距 */
  overflow: auto;            /* 内容过多时可滚动 */
}

/* 诗意卡片主容器样式 */
.poetry-card {
  flex: 1;                    /* 占用剩余空间 */
  display: flex;              /* 弹性布局 */
  flex-direction: column;     /* 纵向排列 */
  padding: 20px;              /* 内边距 */
  background: #fff;           /* 白色背景 */
  border-radius: 16px;        /* 圆角 */
  width: 300px;               /* 固定宽度 */
  margin: 0 auto;             /* 水平居中 */
  aspect-ratio: 3/4;          /* 长宽比 3:4 */
  position: relative;         /* 相对定位 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);  /* 阴影效果 */
}

/* 文字样式设置 */
.comment-text {
  font-family: 'Ma Shan Zheng', serif;  /* 使用马善政字体 */
  font-size: 20px;            /* 文字大小 */
  line-height: 1.2;           /* 行高 */
  color: #2c3e50;             /* 文字颜色 */
  text-align: center;         /* 居中对齐 */
  padding: 20px;              /* 内边距 */
  position: relative;         /* 相对定位 */
  z-index: 2;                 /* 层级设置 */
  letter-spacing: 4px;        /* 字间距 */
  /* 文字自动换行相关设置 */
  white-space: pre-wrap;      /* 保留空格和换行 */
  word-wrap: break-word;      /* 允许单词内换行 */
  word-break: break-all;      /* 允许在任意字符间换行 */
}

/* SVG图片容器样式 */
.svg-container {
  flex: 1;                    /* 占用剩余空间 */
  position: relative;         /* 相对定位 */
  display: flex;              /* 弹性布局 */
  align-items: center;        /* 垂直居中 */
  justify-content: center;    /* 水平居中 */
  padding: 1px;              /* 内边距 */
}

/* SVG图片样式 */
.svg-container :deep(svg) {
  width: 90%;                 /* 宽度占容器90% */
  height: 90%;                /* 高度占容器90% */
  object-fit: contain;        /* 保持比例完整显示 */
}

/* 卡片悬浮效果 */
.poetry-card:hover {
  transform: translateY(-2px);  /* 上移2像素 */
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);  /* 加深阴影 */
}

/* 悬浮时SVG放大效果 */
.poetry-card:hover .svg-container :deep(svg) {
  transform: scale(1.08);     /* 放大1.08倍 */
}

/* 下载按钮容器样式 */
.action-buttons {
  margin-top: 16px;           /* 上方间距 */
  text-align: center;         /* 居中对齐 */
  position: relative;         /* 相对定位 */
  z-index: 2;                 /* 层级设置 */
}

/* 占位提示样式（无内容时显示） */
.placeholder-content {
  display: flex;              /* 弹性布局 */
  flex-direction: column;     /* 纵向排列 */
  align-items: center;        /* 水平居中 */
  justify-content: center;    /* 垂直居中 */
  height: 100%;               /* 占满容器高度 */
  color: var(--notion-gray);  /* 使用预设的灰色 */
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.placeholder-text {
  font-size: 14px;
}
</style> 