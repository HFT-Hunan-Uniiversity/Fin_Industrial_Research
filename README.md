# 行业深度分析系统

## 项目概述

本项目是一个完整的行业深度分析解决方案，包含后端智能分析系统和前端展示界面。后端采用多智能体架构，六大智能体构建分工明确、协同高效的虚拟分析团队，实现从数据处理到洞察输出的全流程自动化。MacroAgent借助 AI 宏观关联算法，挖掘经济指标与多行业的动态适配关系；FinanceAgent通过 AI 财报解析模型，深度解构企业财务数据与产业链价值传导逻辑；MarketAgent运用 AI 市场洞察算法，实时捕捉多行业产销趋势与竞争格局变化。PolicyAgent搭载 AI 政策解读引擎，精准识别政策对不同行业的差异化影响路径；ForecastAgent基于 AI 时序预测模型，结合多维度数据推演行业未来发展趋势；ReportAgent则以 AI 需求匹配与可视化生成技术为支撑，自动整合多智能体成果，按用户偏好输出定制化报告。各智能体通过任务调度机制与数据共享链路，实现复杂关系的智能拆解与多行业的深度适配，彻底打破传统研究的效率与维度瓶颈。

## 传统行业研究与分析面临巨大挑战：

1.*信息碎片化：* 数据散落在宏观报表、公司财报、市场数据、政策文件中，整合难

度大。

2.*专业门槛高：* 需要同时具备金融、市场、技术等多领域知识。

*3.效率瓶颈：* 从数据清洗到报告成文，流程冗长，人力成本高。

4.*视角单一：* 个人或单一团队的分析难以覆盖所有维度，容易存在盲区。

我们的解决方案： 部署一个由 6 大专业智能体 组成的“虚拟分析部门”，7x24 小时无

间断工作，提供覆盖宏观、市场、财务、政策、技术及预测的全方位、立体化分析。

## 项目结构

```
Industry_analysis/
├── config/               # 配置文件
│   ├── project.yaml     # 项目配置
│   ├── agent.yaml       # 智能体配置
│   └── prompt.yaml      # 提示词配置
├── src/                  # 源代码
│   ├── agents/          # 智能体实现
│   ├── tools/           # 工具实现
│   └── utils/           # 工具函数
├── data/                # 数据文件
├── web/                  # 前端展示界面
│   ├── index.html       # 主页面
│   ├── report.html      # 报告页面
│   └── server/         # Node.js后端服务
├── output/              # 分析结果输出
├── logs/                # 日志文件
├── requirements.txt     # 依赖包
├── .env.template        # 环境变量模板
└── api_server.py        # API服务器
```

## 功能特点

### 后端智能分析系统

- **多智能体架构**：包含宏观经济、财务、市场、政策和预测等多个专业智能体
- **自动数据分析**：支持多种数据格式的自动处理和分析
- **报告生成**：自动生成结构化的行业分析报告
- **API接口**：提供RESTful API供前端调用

### 前端展示界面

- **行业选择**：支持多个行业的分析选择
- **问题输入**：支持自定义分析问题
- **实时进度**：展示分析过程的实时进度
- **报告展示**：美观的报告展示界面
- **下载分享**：支持报告的下载和分享功能

## 安装与配置

### 环境要求

- Python 3.8+
- Node.js 14+
- 硅基流动API密钥
- 阿里百炼平添API密钥

### 后端安装

1. 安装Python依赖

```bash
pip install -r requirements.txt
```

2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.template .env

# 编辑.env文件，设置API密钥
nano .env
```

### 前端安装

1. 进入前端目录

```bash
cd web
```

2. 启动Node.js服务器

```bash
node server/server.js
```

### Docker部署

1. 配置环境变量

```bash
# 复制环境变量模板
cp .env.template .env

# 编辑.env文件，设置API密钥
nano .env
```

2. 使用部署脚本

```bash
# Linux/Mac
chmod +x deploy-docker.sh
./deploy-docker.sh

# Windows
deploy-docker.bat
```

### 一键安装脚本

```bash
# Linux/Mac
chmod +x install.sh
./install.sh

# Windows
install.bat
```

## 使用方法

### 本地运行

1. 启动后端API服务

```bash
python api_server.py
```

2. 启动前端服务

```bash
cd web
node server/server.js
```

3. 访问前端界面

```
http://localhost:8081
```

### 使用流程

1. 在主页面选择要分析的行业
2. 输入想要分析的问题或需求
3. 系统将自动进行多维度分析
4. 查看分析进度和结果
5. 在报告页面查看完整分析报告
6. 可以下载或分享报告

## 技术架构

### 后端技术栈

- **框架**：LangChain
- **模型**：DeepSeek-R1
- **数据处理**：pandas, numpy，宏观分析处理Agent
- **API框架**：FastAPI

### 前端技术栈

- **基础**：HTML5, CSS3, JavaScript
- **样式**：现代响应式设计
- **交互**：原生JavaScript，无外部依赖
- **后端**：Node.js

## 部署选项

### 本地部署

适合开发测试和个人使用，详见各子目录的README文件。

### Docker部署

```bash
# 构建镜像
docker build -t industry-analysis:latest .

# 运行容器
docker run -p 8081:8081 industry-analysis:latest
```

### 云服务器部署

适合生产环境，支持远程访问和团队协作。

## 数据说明

系统使用的数据包括：

- 宏观经济数据（GDP、CPI）
- 行业上市公司财务数据
- 行业产销数据
- 相关设施数据
- 政策文件数据

## 输出结果

分析结果保存在 `output/` 目录下，包括：

- 各智能体分析结果（JSON格式）
- 综合分析报告（Markdown格式）
- 数据可视化图表（PNG/HTML格式）

## 注意事项

1. 确保数据文件路径正确
2. API密钥需要有效额度
3. 大规模分析可能需要较长时间
4. 结果仅供参考，不构成投资建议

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 联系方式

如有问题或建议，请通过Issue联系我们。
