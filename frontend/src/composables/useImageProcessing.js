import axios from 'axios'

const API_BASE_URL = import.meta.env.PROD 
  ? 'https://image2text-web-backend.vercel.app'  // 线上后端地址
  : ''  // 开发环境使用相对路径

export function useImageProcessing() {
  /**
   * 处理图片
   * @param {File} file - 要处理的图片文件
   * @param {string} workflowType - 工作流类型
   * @returns {Promise} 处理结果
   */
  const processImage = async (file, workflowType) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('workflow_type', workflowType)

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/process-image`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          withCredentials: false  // 修改这里，跨域请求不需要携带凭证
        }
      )
      
      return {
        text: response.data.text,
        originalImage: response.data.original_image,
        postcardImage: response.data.postcard_image
      }
    } catch (error) {
      throw new Error(error.response?.data?.detail || '处理失败')
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
      const response = await axios.post(`${API_BASE_URL}/api/resize-image`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        withCredentials: false  // 修改这里
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
      const response = await axios.post(`${API_BASE_URL}/api/process-poetry`, {
        text: text
      }, {
        headers: {
          'Content-Type': 'application/json'
        },
        withCredentials: false  // 修改这里
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
