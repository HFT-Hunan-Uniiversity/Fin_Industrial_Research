## 目标
- 将当前零散的多Agent输出统一为一篇结构化研究报告，并自动生成PDF文件。
- 兼容现有命令行与API流程，分析结束后统一输出：JSON（留存原始结果）+ Markdown（便于审阅与版本管理）+ PDF（最终交付物）。

## 现状梳理
- 报告生成：`src/agents/report_agent.py:29-89` 返回 `{"report_content": <markdown>, "report_type": "markdown"}`。
- 结果保存：`src/coordinator.py:239-259` 保存各Agent结果；当 `ReportAgent` 时仅写入Markdown，但现用的写入函数不匹配字段。
- 文件写入：`src/utils/helpers.py:60-78` 在写入Markdown时读取 `results['content']`；与报告的 `report_content` 字段不一致，Markdown被写成整个字典字符串。
- PDF导出：项目中未实现PDF生成函数；`requirements.txt`亦未包含相关库。
- 图表：`src/tools/data_analyzer.py:404-704` 的 `ChartGenerator` 默认 Plotly 生成 HTML，不利于PDF嵌入；Matplotlib分支可输出PNG，适合PDF。

## 改造方案
1. 统一报告文本存储
   - 修改写入逻辑，保存Markdown时使用 `report_content` 字段，确保 `ReportAgent_report.md` 内容为纯报告正文。
2. 新增PDF生成能力（纯Python）
   - 引入 `reportlab`，实现 `markdown_to_pdf(markdown_text, output_pdf_path)`：
     - 支持一级/二级/三级标题（#、##、###）、段落、无序/有序列表、简单表格（可选）。
     - 中文字体自适应：优先注册系统字体（Windows: `msyh.ttc` 或 `simhei.ttf`）；找不到时降级到内置字体（可能无法完整显示中文）。
3. 图表嵌入PDF
   - 在 `generate_charts` 中根据环境变量 `CHART_ENGINE` 选择 `matplotlib`，产出PNG；将关键图表（趋势图、相关性热力图、分布图）追加到PDF末尾的“图表附录”。
4. 流程整合
   - 在 `coordinator.save_results(...)`：
     - 正确写入 `ReportAgent_report.md`；
     - 调用 `markdown_to_pdf` 生成 `ReportAgent_report.pdf`；
     - 返回 `saved_files` 中包含 `*_json`、`ReportAgent_md`、`ReportAgent_pdf`、`summary`。
5. 依赖与配置
   - `requirements.txt` 增加 `reportlab`；（如需HTML到PDF方案，后续可选增加 `weasyprint`）
   - `.env.template` 增加 `CHART_ENGINE=matplotlib` 注释说明。

## 实现步骤
- 修复Markdown写入：更新 `src/utils/helpers.py:60-78` 在 `format=="markdown"` 分支读取 `results.get('report_content', results.get('content', str(results)))`。
- 新增工具：`src/utils/pdf_export.py` 提供 `markdown_to_pdf`（ReportLab实现，含中文字体处理与基础样式）。
- 生成PDF：在 `src/coordinator.py:239-259` 的 `ReportAgent` 分支，写入MD后调用 `markdown_to_pdf` 输出PDF并记录路径。
- 图表PNG输出：在 `src/coordinator.py:261-318` 读取 `CHART_ENGINE`，调用 `ChartGenerator` 以 `matplotlib` 生成PNG，并在生成PDF时附录插入。
- 依赖与配置：更新 `requirements.txt` 和 `.env.template`（仅添加字段与说明）。

## 验证
- 命令行：`python agent_analysis_project\main.py --no-charts` 与 `--no-charts` 关闭图表核验，再开启 `CHART_ENGINE=matplotlib` 验证图表嵌入。
- API：`python agent_analysis_project\api_server.py`，调用 `/api/analyze` 后检查 `output/YYYYMMDD/ReportAgent_report.pdf` 是否生成。
- 内容检查：打开生成的MD与PDF，确认结构完整、中文可读、图表附录存在。

## 注意事项
- 字体：若在Docker环境（`python:3.9-slim`）缺少中文字体，PDF可能无法正常显示中文；建议本地Windows环境生成或在容器内安装Noto Sans CJK。
- 可扩展：后续如需更复杂版式（目录、页眉页脚、分页控制），可升级为 `WeasyPrint(HTML+CSS)` 方案。