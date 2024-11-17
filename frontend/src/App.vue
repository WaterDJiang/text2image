<template>
  <el-container class="app-container">
    <el-aside width="240px" class="notion-sidebar">
      <el-menu
        router
        :default-active="$route.path"
        class="notion-menu"
      >
        <div class="menu-header">
          <h3>AI图片助手</h3>
        </div>

        <el-menu-item index="/poetry">
          <el-icon><i-ep-reading /></el-icon>
          <span>趣语趣图</span>
        </el-menu-item>        

        <el-menu-item index="/mood">
          <el-icon><i-ep-edit /></el-icon>
          <span>心情文案</span>
        </el-menu-item>
        
        <el-menu-item index="/sarcastic">
          <el-icon><i-ep-chat-dot-round /></el-icon>
          <span>毒舌看图</span>
        </el-menu-item>
        

        
        <el-menu-item index="/story">
          <el-icon><i-ep-notebook /></el-icon>
          <span>故事创作</span>
        </el-menu-item>
        
        <el-menu-item index="/resize">
          <el-icon><i-ep-picture /></el-icon>
          <span>图片调整</span>
        </el-menu-item>
        
        <el-menu-item index="/history">
          <el-icon><i-ep-time /></el-icon>
          <span>历史记录</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-main class="notion-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<style>
.app-container {
  height: 100vh;
}

.notion-sidebar {
  background: var(--notion-white);
  border-right: 1px solid var(--notion-border);
}

.notion-menu {
  border-right: none;
}

.menu-header {
  padding: 24px 20px;
  border-bottom: 1px solid var(--notion-border);
}

.menu-header h3 {
  margin: 0;
  color: var(--notion-text);
  font-weight: 500;
}

.notion-main {
  background-color: var(--notion-bg);
  padding: 0;
}

.el-menu-item {
  height: 36px;
  line-height: 36px;
  margin: 4px 0;
}

.el-menu-item.is-active {
  background-color: var(--notion-hover) !important;
  border-radius: 3px;
}

.el-menu-item:hover {
  background-color: var(--notion-hover) !important;
  border-radius: 3px;
}
</style> 