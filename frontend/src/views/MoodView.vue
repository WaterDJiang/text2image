<template>
  <!-- 使用通用的图片处理组件，传入特定的标题、副标题和工作流类型 -->
  <ImageProcessView 
    title="心情文案"
    subtitle="上传图片，AI说出你的心情"
    workflow-type="mood"
  />
</template>

<script setup>
// 导入通用图片处理组件
import ImageProcessView from './ImageProcessView.vue'
</script> 