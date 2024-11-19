import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useModelStore = defineStore('model', () => {
  const currentModel = ref('deepseek') // 默认使用 deepseek
  
  function setModel(model) {
    currentModel.value = model
  }
  
  return {
    currentModel,
    setModel
  }
}) 