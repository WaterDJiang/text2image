# AI 图片生成器

## 部署到 Vercel

1. Fork 此仓库

2. 在 Vercel 中导入项目

3. 配置环境变量
   在 Vercel 项目设置中添加以下环境变量：
   - `COZE_API_URL`
   - `COZE_API_KEY`
   - `IMGBB_API_KEY`
   - `WORKFLOW_ID_MOOD`
   - `WORKFLOW_ID_SARCASTIC`

4. 部署
   Vercel 会自动部署项目

## 本地开发

1. 克隆仓库

## 功能特点

- 支持拖拽上传图片
- 支持点击上传图片
- 文件大小和格式验证
- 实时预览
- 生成内容展示
- 分享功能

## 使用方法

1. 上传图片（支持 JPG、PNG、GIF 或 WEBP 格式）
2. 点击"生成毒舌文案"按钮
3. 等待 AI 生成结果
4. 查看或分享生成的内容

## 开发说明

本项目使用原生 JavaScript 开发，无需额外依赖。