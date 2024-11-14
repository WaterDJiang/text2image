# AI 图片文案生成器

基于 Flask 和 AI 技术的图片文案生成工具，支持多种风格的文字描述生成。

## 功能特点
- **多样化的生成风格**
  - 🎭 **心情描述**：分析图片情感，生成贴切的心情描述
  - 😏 **讽刺风格**：以幽默讽刺的视角解读图片
  - 📝 **诗意描述**：将图片转化为富有诗意的文字
  - 📖 **故事创作**：基于图片编织有趣的故事

## 技术特性
- 支持多种图片格式：JPG、PNG、GIF、WEBP
- 图片大小限制：5MB
- 自动图片压缩和格式验证
- API 接口安全验证
- 实时错误提示
- 响应式界面设计

## 快速开始
### 环境要求
- Python 3.6+
- pip
- 稳定的网络环境
- 现代浏览器（Chrome、Firefox、Safari 等）

### 安装步骤
1. 克隆项目
   ```bash
   git clone https://github.com/yourusername/image2text_web.git
2.安装依赖
bash
pip install -r requirements.txt
3.配置环境变量
bash
# 在.env文件中填入必要的配置信息
4.启动服务
bash
python app.py
5.使用方法
打开浏览器访问 http://localhost:5000
点击上传按钮选择图片
选择生成风格
点击生成按钮获取文案
API 文档
图片上传接口
方法：POST
路径：/api/upload
开发指南
项目结构
工具函数
开发规范
开发规范
遵循 PEP 8 编码规范
使用 Python Type Hints
编写单元测试
提交前进行代码格式化
贡献指南
Fork 本仓库
创建特性分支 (git checkout -b feature/AmazingFeature)
提交更改 (git commit -m 'Add some AmazingFeature')
推送到分支 (git push origin feature/AmazingFeature)
提交 Pull Request
许可证
本项目采用 MIT 许可证 - 详见 LICENSE 文件

联系方式
项目维护者：Water
邮箱：water@footprint.network

致谢
感谢所有贡献者对本项目的支持！
