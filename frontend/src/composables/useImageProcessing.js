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
    const maxRetries = 3;
    const formData = new FormData();
    formData.append('file', file);
    formData.append('workflow_type', type);
    formData.append('model', modelStore.currentModel);
    
    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        if (attempt > 0) {
          console.log(`第 ${attempt + 1} 次重试上传...`);
          // 等待一段时间后重试
          await new Promise(resolve => setTimeout(resolve, 2000 * (attempt + 1)));
        }
        
        const response = await axios.post(`${API_BASE_URL}/process-image`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          timeout: 60000  // 60秒超时
        });
        
        if (!response.data.postcard_image) {
          throw new Error('未获取到处理后的图片');
        }
        return {
          postcardImage: response.data.postcard_image,
          text: response.data.text
        };
      } catch (error) {
        console.error(`第 ${attempt + 1} 次处理失败:`, error);
        if (attempt === maxRetries - 1) {
          throw error;
        }
      }
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