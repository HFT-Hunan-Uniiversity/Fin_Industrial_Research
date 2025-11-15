# 行业分析系统

基于LangChain框架和硅基流动模型的多智能体系统，自动完成各行业的多维数据分析、趋势判断和报告生成。

## 项目概述

本项目是一个完整的行业分析解决方案，包含后端智能分析系统和前端展示界面。后端采用多智能体架构，能够从宏观经济、财务指标、市场趋势、政策环境等多个维度进行综合分析；前端提供友好的用户界面，支持行业选择、问题输入、分析过程展示和报告查看下载等功能。

**注意**：当前演示版本以新能源汽车行业为例，但系统设计为通用型，可适用于各类行业的深度分析。

## 项目结构

```
Industry_analysis/
├── agent_analysis_project/    # 后端智能分析系统
│   ├── config/               # 配置文件
│   │   ├── project.yaml     # 项目配置
│   │   ├── agent.yaml       # 智能体配置
│   │   └── prompt.yaml      # 提示词配置
│   ├── src/                  # 源代码
│   │   ├── agents/          # 智能体实现
│   │   ├── tools/           # 工具实现
│   │   └── utils/           # 工具函数
│   ├── data/                # 数据文件
│   ├── output/              # 输出结果
│   ├── logs/                # 日志文件
│   ├── requirements.txt     # 依赖包
│   ├── .env                 # 环境变量
│   └── api_server.py        # API服务器
├── web/                      # 前端展示界面
│   ├── index.html           # 主页面
│   ├── report.html          # 报告页面
│   └── server/              # Node.js后端服务
└── output/                   # 分析结果输出
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

### 后端安装

1. 进入后端目录
```bash
cd agent_analysis_project
```

2. 安装Python依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
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
chmod +x scripts/install.sh
./scripts/install.sh

# Windows
scripts/install.bat
```

## 使用方法

### 本地运行

1. 启动后端API服务
```bash
cd agent_analysis_project
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
- **模型**：硅基流动API (deepseek-ai/DeepSeek-R1)
- **数据处理**：pandas, numpy
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

**注意**：当前演示版本使用新能源汽车行业数据，但系统可处理各行业数据。

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

本项目采用 MIT 许可证，详见 [LICENSE](agent_analysis_project/LICENSE) 文件。

## 联系方式

如有问题或建议，请通过Issue联系我们。