# FinTech Industry Research Frontend + Backend

## 本地运行

### 前端
1. 在项目根目录运行：
   - `python3 -m http.server 8000`
2. 打开 `http://localhost:8000/index.html#home`

### 后端（Node，无依赖）
1. 在项目根目录运行：
   - `node server/server.js`
2. 服务监听 `http://localhost:8081`

### 功能流程
- 选择行业 → 输入问题 → 加载页分阶段显示 → 查看报告按钮 → 报告页输出并支持下载与分享
- 与后端接口：`POST /api/report`、`GET /api/report/:id/stream`（SSE）、`GET /api/report/:id`

## 部署到 GitHub
1. 初始化并推送：
   - `git init`
   - `git add .`
   - `git commit -m "feat: frontend + backend integration"`
   - `git branch -M main`
   - `git remote add origin <your_repo_url>`
   - `git push -u origin main`
2. 前端静态页面可用 GitHub Pages（Settings → Pages → Source 选择 `main` 分支 `/(root)`）。
3. 后端需部署到你的服务器或云平台（保持接口路径一致），并将 `index.html` 中的 `API_BASE` 替换为生产域名。

## 目录结构
- `index.html`：多页路由（home/choose/ask/loading/ready）
- `report.html`：报告输出页
- `server/server.js`：后端示例服务（原生 Node http）

## 配置
- 在 `index.html` 脚本部分设置 `API_BASE`（默认 `http://localhost:8081`）。

