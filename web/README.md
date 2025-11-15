# 前端展示系统

本目录包含金融科技行业研究系统的前端展示界面，主要功能包括：

- 首页展示
- 行业分析报告查看
- 报告下载与分享
- 数据可视化展示

## 启动方式

```bash
# 使用Python静态服务器
python3 -m http.server 8000
```

服务器启动后，可通过以下地址访问：
- 首页：http://localhost:8000/index.html#home
- 报告页：http://localhost:8000/report.html

## 文件结构

- `index.html` - 系统首页（包含多页路由：home/choose/ask/loading/ready）
- `report.html` - 报告展示页面
- `server/` - 后端服务代码目录

## 技术栈

- HTML5
- CSS3
- JavaScript
- Node.js

## 与后端交互

- 主要接口：`POST /api/report`、`GET /api/report/:id/stream`（SSE）、`GET /api/report/:id`
- 在 `index.html` 脚本部分可配置 `API_BASE`（默认 `http://localhost:8081`）

## 功能流程

1. 选择行业
2. 输入问题
3. 加载页分阶段显示处理进度
4. 点击查看报告按钮
5. 报告页输出结果并支持下载与分享

