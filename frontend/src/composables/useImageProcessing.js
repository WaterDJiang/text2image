import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

export const useImageProcessing = () => {
  /**
   * 处理图片
   * @param {File} file - 要处理的图片文件
   * @param {string} workflowType - 工作流类型
   * @returns {Promise} 处理结果
   */
  const processImage = async (file, type) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('workflow_type', type)
    
    try {
      const response = await axios.post(`${API_BASE_URL}/process-image`, formData)
      console.log('处理结果:', response.data)
      
      if (!response.data.postcard_image) {
        throw new Error('未获取到处理后的图片')
      }
      return {
        postcardImage: response.data.postcard_image,
        text: response.data.text
      }
    } catch (error) {
      console.error('处理图片失败:', error)
      throw error
    }
  }

  /**
   * 调整图片大小
   * @param {File} file - 要调整的图片文件
   * @param {number} width - 目标宽度
   * @param {number} height - 目标高度
   * @returns {Promise} 调整结果
   */
  const resizeImage = async (file, width, height) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('width', width)
    formData.append('height', height)

    try {
      const response = await axios.post(`${API_BASE_URL}/resize-image`, formData)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || '调整失败')
    }
  }

  /**
   * 处理诗意文本
   * @param {string} text - 输入的文字
   * @returns {Promise} 处理结果，包含评论和SVG
   */
  const processPoetry = async (text) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/process-poetry`, {
        text: text
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || '处理失败')
    }
  }

  return {
    processImage,
    resizeImage,
    processPoetry
  }
} 