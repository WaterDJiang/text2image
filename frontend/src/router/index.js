import { createRouter, createWebHistory } from 'vue-router'
import MoodView from '../views/MoodView.vue'
import SarcasticView from '../views/SarcasticView.vue'
import PoetryView from '../views/PoetryView.vue'
import StoryView from '../views/StoryView.vue'
import ImageResizeView from '../views/ImageResizeView.vue'
import HistoryView from '../views/HistoryView.vue'

// 创建路由实例
const router = createRouter({
  // 使用HTML5历史模式
  history: createWebHistory(import.meta.env.BASE_URL),
  // 路由配置
  routes: [
    {
      path: '/',
      redirect: '/mood'  // 默认重定向到心情文案页面
    },
    {
      path: '/mood',
      name: 'mood',
      component: MoodView  // 心情文案页面
    },
    {
      path: '/sarcastic',
      name: 'sarcastic',
      component: SarcasticView  // 毒舌文案页面
    },
    {
      path: '/poetry',
      name: 'poetry',
      component: PoetryView  // 诗意看图页面
    },
    {
      path: '/story',
      name: 'story',
      component: StoryView  // 故事创作页面
    },
    {
      path: '/resize',
      name: 'resize',
      component: ImageResizeView  // 图片尺寸调整页面
    },
    {
      path: '/history',
      name: 'history',
      component: HistoryView  // 历史记录页面
    }
  ]
})

// 添加全局错误处理
router.onError((error) => {
  console.error('路由错误:', error)
})

export default router 