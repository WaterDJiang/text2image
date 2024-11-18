import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

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
      console.log('API Base URL:', API_BASE_URL)
      console.log('发送请求到:', `${API_BASE_URL}/process-image`)
      const response = await axios.post(`${API_BASE_URL}/process-image`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        validateStatus: function (status) {
          return status < 500 // 只有状态码大于等于500时才会被视为错误
        }
      })
      console.log('API响应:', response)
      
      if (!response.data.postcard_image) {
        throw new Error('未获取到处理后的图片')
      }
      return {
        postcardImage: response.data.postcard_image,
        text: response.data.text
      }
    } catch (error) {
      console.error('处理图片失败:', error)
      console.error('错误详情:', error.response || error)
      throw new Error(error.response?.data?.detail || error.message || '处理失败')
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
      const response = await axios.post(`${API_BASE_URL}/resize-image`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
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
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
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