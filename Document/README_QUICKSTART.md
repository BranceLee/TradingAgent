# TradingAgents 快速入门指南

## 项目简介
TradingAgents 是一个多智能体金融交易框架，通过模拟专业投资机构的工作流程，利用大语言模型进行金融分析和交易决策。

## 核心架构

### 双AI服务商设计
- **DeepSeek**: 主要大语言模型，负责所有分析和决策
  - API地址: `https://api.deepseek.com/v1`
  - 主要模型: `deepseek-chat`, `deepseek-reasoner`

- **Doubao (火山引擎)**: 向量服务，负责经验记忆和相似性检索
  - API地址: `https://ark.cn-beijing.volces.com/api/v3/`
  - 嵌入模型: `doubao-embedding-large-text-240915`

### 工作流程
```
数据获取 → 多维度分析 → 投资辩论 → 风险评估 → 决策执行 → 经验学习
    ↓         ↓          ↓          ↓          ↓          ↓
  工具节点   DeepSeek    多智能体    DeepSeek    状态管理    Doubao+ChromaDB
```

## 快速开始

### 1. 环境配置
```bash
# 克隆项目
git clone <repository-url>
cd TradingAgents

# 创建虚拟环境
conda create -n tradingagents python=3.13
conda activate tradingagents

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export OPENAI_API_KEY=your_deepseek_api_key
export VOLCES_API_KEY=your_volces_api_key
```

### 2. 运行方式

#### Web 界面
```bash
streamlit run app.py
```

#### 命令行界面
```bash
python -m cli.main
```

#### 编程接口
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph

ta = TradingAgentsGraph(debug=True)
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

## 核心功能模块

### 分析师团队
- **市场分析师**: 技术指标分析
- **基本面分析师**: 财务数据分析
- **新闻分析师**: 宏观新闻解读
- **社交媒体分析师**: 情绪和舆情分析

### 辩论机制
- **多方研究员**: 支持投资观点
- **空方研究员**: 反对投资观点
- **研究经理**: 评估辩论并制定投资计划

### 风险管理
- **激进分析师**: 高风险高回报观点
- **保守分析师**: 低风险稳健观点
- **中立分析师**: 平衡风险观点
- **风险经理**: 最终风险评估和决策

## 数据流向

### 分析阶段
```
用户输入 → 初始化状态 → 分析师分析 → 工具调用 → 数据返回 → 报告生成
```

### 决策阶段
```
投资辩论 → 风险评估 → 最终决策 → 状态更新 → 报告生成
```

### 学习阶段
```
决策结果 → 反思分析 → Doubao向量化 → ChromaDB存储 → 经验复用
```

## 配置选项

### 主要配置项
```python
config = {
    "deep_think_llm": "deepseek-r1",      # 深度思考模型
    "quick_think_llm": "deepseek-chat",   # 快速思考模型
    "max_debate_rounds": 1,               # 投资辩论轮次
    "max_risk_discuss_rounds": 1,         # 风险讨论轮次
    "online_tools": True,                 # 是否使用在线工具
    "market_type": "US"                   # 市场类型 (US/CN)
}
```

## 常见问题

### Q: 为什么使用两个不同的AI服务商？
A: 采用专业分工设计，DeepSeek专长推理分析，Doubao专长向量处理，发挥各自优势。

### Q: 如何添加新的数据源？
A: 在 `tradingagents/dataflows/` 添加数据工具，在 `interface.py` 添加接口，在 `Toolkit` 中注册工具。

### Q: 系统如何学习和改进？
A: 通过向量记忆系统，将每次决策的经验向量化存储，后续决策时检索相似情况并复用历史经验。

### Q: 如何处理API调用限制？
A: 支持在线/离线模式切换，具备缓存机制和错误重试功能。

## 项目文档
详细技术架构和业务流程请参考: [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

---
*更多技术细节请查看完整文档*