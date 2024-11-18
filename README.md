# AI图片处理服务

## 快速开始

1. 确保已安装以下软件：
   - Python 3.8+
   - Node.js 14+
   - npm 6+

2. 配置环境变量
   在 backend 目录下创建 .env 文件：
   ```
   COZE_API_URL=你的COZE_API地址
   COZE_API_KEY=你的COZE_API密钥
   IMGBB_API_KEY=你的IMGBB_API密钥
   WORKFLOW_ID_MOOD=心情工作流ID
   WORKFLOW_ID_SARCASTIC=毒舌工作流ID
   WORKFLOW_ID_POETRY=诗意工作流ID
   WORKFLOW_ID_STORY=故事工作流ID
   ```

3. 启动服务
   ```bash
   chmod +x start.sh stop.sh
   ./start.sh
   ```

4. 停止服务
   ```bash
   ./stop.sh
   ```

## 服务地址
- 前端: http://localhost:5173
- 后端: http://localhost:8000

## 功能列表
- 心情文案生成
- 毒舌看图
- 诗意看图
- 故事创作
- 图片尺寸调整
- 历史记录 

## 环境变量配置

1. 复制环境变量示例文件:
```bash
cp .env.example .env
```

2. 修改 .env 文件中的配置:
- COZE_API_URL: https://api.coze.cn/v1/workflow/run
- COZE_API_KEY: 你的 Coze API 密钥
- IMGBB_API_KEY: 你的 ImgBB API 密钥
- WORKFLOW_ID_MOOD: 7436280348118286387
- WORKFLOW_ID_SARCASTIC: 7436699979249254419
- WORKFLOW_ID_POETRY: 7416197020363423781
- WORKFLOW_ID_STORY: 你的故事工作流 ID

3. 开发环境配置:
前端开发环境变量位于 frontend/.env.development
后端开发环境变量位于 backend/.env

4. 生产环境配置:
前端生产环境变量位于 frontend/.env.production
后端生产环境变量通过 Vercel 环境变量配置
