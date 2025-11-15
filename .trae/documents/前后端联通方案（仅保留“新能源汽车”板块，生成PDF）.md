## 目标

* 将 `f:\Industry_analysis\web` 前端与后端 `FastAPI` 连通，保留“新能源汽车”板块，触发分析并生成 PDF 报告。

* 前端继续调用本地 Node 服务（`web/server/server.js`），由 Node 服务转发/适配到后端 `FastAPI`（`http://localhost:8000`）。

* 请求流：前端 → Node（SSE/轮询）→ FastAPI（/api/analyze、/api/status、/api/results、/download）。

## 现状梳理

* 前端入口：`web/index.html:323-343` 使用 `API_BASE=http://localhost:8081` 调用 `server.js` 的伪接口（POST /api/report、GET /api/report/:id、SSE /api/report/:id/stream）。

* 前端“报告页”：`web/report.html:69-95` 从 `sessionStorage` 读取报告占位数据，目前下载按钮导出 `.txt`。

* Node 服务：`web/server/server.js:66-84` 提供伪造的报告生成与 SSE 事件，未连接真实后端。

* 后端：`agent_analysis_project/api_server.py` 已提供真实接口：

  * `POST /api/analyze`（启动分析，仅“新能源汽车”板块有效）

  * `GET /api/status`（进度与状态）

  * `GET /api/results`（最终结果，含 `saved_files`）

  * `GET /download?file=...`（下载具体文件，含 PDF）

## 改造方案

1. Node 适配后端（保留前端调用地址不变）

   * 在 `web/server/server.js` 引入后端地址常量：

     * `const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';`

   * 改造 `handlePostReport`（`web/server/server.js:18-42`）：

     * 解析 `industry` 与 `question`，将行业映射为后端支持的 ID：`'新能源汽车' → 'new-energy-vehicle'`，其余行业一律回退为 `'new-energy-vehicle'`。

     * `POST ${BACKEND_URL}/api/analyze`，体为 `{ industry_id: 'new-energy-vehicle', focus_areas: ['宏观经济','财务','市场','预测'] }`。

     * 生成 `id` 写入 `store`，启动后台轮询任务：每 800ms 访问 `${BACKEND_URL}/api/status`，根据返回 `status/progress` 映射阶段：

       * progress < 30 → `analyzing`

       * 30-70 → `fetching`

       * 70-99 → `generating`

       * 100 → `done`

     * 完成后 `GET ${BACKEND_URL}/api/results`，构造前端需要的 `report` 对象，并附上 `pdf_url`：`${BACKEND_URL}/download?file=${encodeURIComponent(saved_files.ReportAgent_pdf)}`。

   * `handleStream`（`web/server/server.js:44-58`）保持 SSE 输出 `phase`，从 `store` 中读取并推送。

   * `handleGetReport`（`web/server/server.js:60-64`）返回 `report`（含 `title/date` 与 `pdf_url`，可简单映射为前端展示/下载）。

2. 报告页支持 PDF 下载/预览

   * 在 `web/report.html:69-95`：读取 `report_payload` 时若存在 `payload.pdf_url`，则：

     * “下载”按钮改为直连 `payload.pdf_url`（或新加“查看PDF”按钮，`window.open(payload.pdf_url)`）。

     * 可选：在页面主区域追加 `<iframe src="payload.pdf_url" width="100%" height="680"></iframe>` 预览。

   * 保留原有 `.txt` 下载作为兜底（无 `pdf_url` 时）。

3. 仅“新能源汽车”板块

   * 行业选择页面保持样式，但在 Node `handlePostReport` 中强制映射为 `'new-energy-vehicle'`。

   * 可选优化：`web/index.html:431-440` 的行业网格仅渲染“新能源汽车”。

4. CORS 与安全

   * 前端仅调用 Node（`8081`），Node 与后端通信无需 CORS。

   * 若未来前端直接调用后端，需在后端 `.env` 设置：`ALLOWED_ORIGINS=http://localhost:8081`（`agent_analysis_project/api_server.py:29-36` 已支持环境变量驱动）。

5. 运行方式

   * 后端：`python agent_analysis_project\api_server.py`（监听 `http://localhost:8000`）

   * 前端 Node：`node web\server\server.js`（监听 `http://localhost:8081`）

   * 浏览器打开：`web/index.html`（或用任意静态服务器）

## 代码变更摘要（确认）

* `web/server/server.js`

  * 顶部增加后端地址常量与轻量 fetch 封装

  * `handlePostReport` 调后端，存储 `id`，轮询 `/api/status` 并在完成后获取 `/api/results`，整理出 `report` 与 `pdf_url`

  * `handleGetReport` 返回整理后的 `report`

* `web/report.html`

  * 若存在 `payload.pdf_url`：

    * “下载”按钮直链到 `pdf_url`

    * 页面中可嵌入 `<iframe>` 预览 PDF（可配置开关）

      <br />

## 验证

* 启动后端与 Node；在首页选择“新能源汽车”，输入问题并点击生成

* 观察加载进度（SSE），进入“查看报告”后跳转到报告页

* 在报告页点击“下载/查看PDF”，成功获取 `output/YYYYMMDD/ReportAgent_report.pdf`

## 风险与兼容

* 若后端生成 PDF 前失败，`server.js` 将回退到文本占位报告；前端仍可正常显示

* 由于仅“新能源汽车”板块有效，其他行业将被强制映射（后续可按需开放）

* 如需在 Docker 中生成 PDF，建议安装中文字体或在本地 Windows 生成后再部署

