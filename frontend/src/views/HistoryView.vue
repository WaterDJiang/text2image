<template>
  <div class="history-container">
    <!-- 页面标题区域 -->
    <div class="page-header">
      <h1>历史记录</h1>
      <p class="subtitle">查看历史创作</p>
    </div>

    <!-- 无数据时显示空状态 -->
    <el-empty v-if="!historyList.length" description="暂无历史记录" />
    
    <!-- 历史记录时间线 -->
    <el-timeline v-else>
      <el-timeline-item
        v-for="item in historyList"
        :key="item.id"
        :timestamp="item.createTime"
        placement="top"
      >
        <el-card>
          <div class="history-item">
            <!-- 图片展示区域 -->
            <div class="history-images">
              <img :src="item.sourceImage" class="source-image" />
              <el-icon class="arrow-icon"><i-ep-arrow-right /></el-icon>
              <img :src="item.resultImage" class="result-image" />
            </div>
            <!-- 操作区域 -->
            <div class="history-info">
              <span class="type-tag">{{ item.type }}</span>
              <el-button-group>
                <el-button size="small" @click="handleDownload(item)">
                  <el-icon><i-ep-download /></el-icon>
                </el-button>
                <el-button size="small" @click="handleDelete(item)">
                  <el-icon><i-ep-delete /></el-icon>
                </el-button>
              </el-button-group>
            </div>
          </div>
        </el-card>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 历史记录列表
const historyList = ref([])

// 下载处理结果
const handleDownload = (item) => {
  const link = document.createElement('a')
  link.href = item.resultImage
  link.download = `${item.type}_result.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// 删除历史记录
const handleDelete = (item) => {
  ElMessageBox.confirm(
    '确定要删除这条记录吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 实现删除逻辑
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style scoped>
/* 容器样式 */
.history-container {
  padding: 20px;
}

/* 页面标题样式 */
.page-header {
  margin-bottom: 40px;
}

/* 副标题样式 */
.subtitle {
  color: #909399;
  margin-top: 8px;
}

/* 历史记录项样式 */
.history-item {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 图片展示区域样式 */
.history-images {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 图片样式 */
.source-image,
.result-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
}

/* 箭头图标样式 */
.arrow-icon {
  color: #909399;
  font-size: 20px;
}

/* 信息区域样式 */
.history-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 类型标签样式 */
.type-tag {
  padding: 2px 8px;
  background-color: #f0f2f5;
  border-radius: 4px;
  font-size: 12px;
  color: #606266;
}
</style> 