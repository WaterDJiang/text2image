<template>
  <div class="image-uploader">
    <el-upload
      class="upload-area"
      drag
      action="#"
      :auto-upload="false"
      :show-file-list="false"
      :on-change="handleFileChange"
    >
      <template #trigger>
        <div class="upload-trigger">
          <el-icon class="upload-icon"><i-ep-upload-filled /></el-icon>
          <div class="upload-text">
            拖拽图片到这里或点击上传
            <div class="upload-tip">支持 PNG、JPG、JPEG 格式图片</div>
          </div>
        </div>
      </template>
    </el-upload>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: String
})

const emit = defineEmits(['update:modelValue', 'file-selected'])

const handleFileChange = (file) => {
  if (file) {
    const url = URL.createObjectURL(file.raw)
    emit('update:modelValue', url)
    emit('file-selected', file.raw)
  }
}
</script>

<style scoped>
.image-uploader {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.upload-area {
  flex: 1;
  border: 2px dashed var(--notion-border);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-area:hover {
  border-color: var(--notion-blue);
  background-color: var(--notion-hover);
}

.upload-trigger {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.upload-icon {
  font-size: 48px;
  color: var(--notion-gray);
  margin-bottom: 16px;
}

.upload-text {
  color: var(--notion-text);
  font-size: 14px;
  line-height: 1.6;
}

.upload-tip {
  font-size: 12px;
  color: var(--notion-gray);
  margin-top: 8px;
}
</style> 