import axios from 'axios'
import { useModelStore } from '../stores/modelStore'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'  // 获取API基础URL

export const useImageProcessing = () => {
  const modelStore = useModelStore()

  /**
   * 处理图片
   * @param {File} file - 要处理的图片文件
   * @param {string} workflowType - 工作流类型
   * @returns {Promise} 处理结果
   */
  const processImage = async (file, type) => {
    const formData = new FormData()  // 创建表单数据
    formData.append('file', file)  // 添加文件
    formData.append('workflow_type', type)  // 添加工作流类型
    formData.append('model', modelStore.currentModel)  // 添加当前模型
    
    try {
      console.log('API Base URL:', API_BASE_URL)  // 打印API基础URL
      console.log('发送请求到:', `${API_BASE_URL}/process-image`)  // 打印请求URL
      const response = await axios.post(`${API_BASE_URL}/process-image`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'  // 设置请求头
        }
      })
      
      if (!response.data.postcard_image) {
        throw new Error('未获取到处理后的图片')  // 如果未获取到图片，抛出错误
      }
      return {
        postcardImage: response.data.postcard_image,  // 返回处理后的图片
        text: response.data.text  // 返回文本
      }
    } catch (error) {
      console.error('处理图片失败:', error)  // 打印错误信息
      if (error.response) {
        console.error('错误响应:', error.response.data)  // 打印错误响应
        console.error('状态码:', error.response.status)  // 打印状态码
      }
      throw new Error('处理图片失败')  // 抛出处理失败的错误
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
        text: text,
        model: modelStore.currentModel
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