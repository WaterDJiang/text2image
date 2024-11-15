import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  // Vue插件配置
  plugins: [vue()],
  
  // 路径解析配置
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')  // 设置@别名指向src目录
    }
  },
  
  // 开发服务器配置
  server: {
    port: 5173,  // 开发服务器端口
    proxy: {
      // API代理配置
      '/api': {
        target: 'http://localhost:8000',  // 后端服务地址
        changeOrigin: true  // 修改请求头中的Origin
      }
    }
  }
}) 