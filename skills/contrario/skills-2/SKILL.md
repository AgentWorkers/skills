# AetherLang Ω V3 — 人工智能工作流编排工具

> 这是全球最先进的人工智能工作流编排平台。AetherLang Ω V3 搭配了 9 种先进的 AI 引擎，能够提供诺贝尔级分析能力、米其林级别的解决方案、对抗性预测功能以及多智能体协作能力。

**源代码**: [github.com/contrario/aetherlang](https://github.com/contrario/aetherlang)
**官方网站**: [neurodoc.app/aether-nexus-omega-dsl](https://neurodoc.app/aether-nexus-omega-dsl)
**作者**: NeuroAether (info@neurodoc.app)
**许可证**: MIT

## 隐私与数据管理

⚠️ **外部 API 注意事项**: 该工具会将用户提供的流程代码和查询文本发送到 `api.neurodoc.app` 进行处理。使用该工具即表示您同意此类数据传输。

- **传输内容**: 仅包括流程 DSL 代码和自然语言查询。
- **不传输的内容**: 不会传输任何凭证、API 密钥、个人文件或系统数据。
- **数据存储**: 查询内容会实时处理，不会被永久保存。
- **托管服务**: 使用 Hetzner EU 服务器（符合 GDPR 规范）。
- **无需凭证**: 该工具使用免费 tier（每小时 100 次请求），无需 API 密钥。

用户应避免在查询中包含敏感的个人信息、密码或机密数据。

## 概述

AetherLang Ω V3 是一种专门用于人工智能的领域特定语言，能够编排多模型工作流，并具备内置的安全性、调试功能以及实时协作能力。V3 版本引入了其他平台所没有的先进系统提示机制和结构化输出要求。

所有用户输入在处理前都会在服务器端进行验证和清洗。安全中间件的源代码可在 [GitHub 仓库](https://github.com/contrario/aetherlang/blob/main/aetherlang/middleware/security.py) 中查看。

## V3 引擎 — 最新技术特性

| 引擎 | 节点类型 | 主要功能 |
|--------|-----------|---------------|
| 🧑‍🍳 Chef Omega | `chef` | 包含 17 个必填字段：食物成本百分比、HACCP 标准、温度曲线、MacYuFBI 矩阵、质地分析、过敏原信息、饮食转换规则、葡萄酒搭配建议、菜品摆放方案、零浪费策略、厨房工作流程 |
| ⚗️ APEIRON Molecular | `molecular` | 流变学仪表盘、相图分析、水胶体特性（琼脂/海藻酸盐/吉利兰/黄原胶）、FMEA 故障分析、设备校准、感官科学指标 |
| 📈 APEX Strategy | `apex` | 博弈论 + 纳什均衡分析、蒙特卡洛模拟（10,000 次模拟）、行为经济学、决策树分析、竞争策略分析、单位经济分析（CAC/LTV）、蓝海战略规划工具、OKR 生成器 |
| 🧠 GAIA Brain | `assembly` | 12 个神经元组成的投票系统（8/12 票数需达到多数）、争议解决机制、Gandalf VETO 权限机制、信心热度图、7 种典型模型 |
| 🔮 Oracle | `oracle` | 贝叶斯更新算法（先验→证据→后验）、信号与噪声评分、时间分辨率（7天/30天/180天）、黑天鹅事件检测、对抗性模拟机制、Kelly 标准下的投注策略 |
| 💼 NEXUS-7 Consult | `consulting` | 因果循环图、约束理论、Wardley 分类法、ADKAR 变革管理工具、反模式库、系统动态建模 |
| 📊 Market Intel | `marketing` | 市场分析工具（TAM/SAM/SOM）、产品类别设计、波特五力模型、价格弹性分析、网络效应分析、病毒式传播系数（K 因子）、客户细分算法 |
| 🔬 Research Lab | `lab` | 证据等级评估（A-D 级别）、矛盾检测器、知识图谱、可重复性评分（X/10 分）、跨学科知识桥梁、研究差距分析 |
| 📉 Data Analyst | `analyst` | 异常值/缺失值/重复值检测、统计测试选择器、异常检测、预测建模（R²/RMSE）、群体/漏斗分析、因果推断 |

## API 端点
```
POST https://api.neurodoc.app/aetherlang/execute
Content-Type: application/json
```

### 请求格式
```json
{
  "code": "<aetherlang_flow>",
  "query": "<user_input>"
}
```

### 构建工作流
```
flow <FlowName> {
  using target "neuroaether" version ">=0.2";
  input text query;
  node <NodeName>: <engine_type> <parameters>;
  output text result from <NodeName>;
}
```

### 示例工作流

#### Chef Omega V3 — 全面餐厅咨询服务
```
flow Chef {
  using target "neuroaether" version ">=0.2";
  input text query;
  node Chef: chef cuisine="auto", difficulty="medium", servings=4, language="el";
  output text recipe from Chef;
}
```
返回结果包括：食物成本分析、HACCP 合规性、温度曲线、葡萄酒搭配建议、菜品摆放方案、零浪费策略以及厨房工作流程。

#### APEX Strategy V3 — 诺贝尔级商业分析
```
flow Strategy {
  using target "neuroaether" version ">=0.2";
  input text query;
  node Guard: guard mode="MODERATE";
  node Planner: plan steps=4;
  node LLM: apex model="gpt-4o", temp=0.7;
  Guard -> Planner -> LLM;
  output text report from LLM;
}
```
返回结果包括：博弈论分析、蒙特卡洛模拟、行为经济学模型、决策树分析、财务预测、单位经济分析、蓝海战略规划工具。

#### 多引擎协同工作流
```
flow FullAnalysis {
  using target "neuroaether" version ">=0.2";
  input text query;
  node Guard: guard mode="STRICT";
  node Research: lab domain="business";
  node Market: marketing analysis="competitive";
  node Strategy: apex analysis="strategic";
  Guard -> Research -> Market -> Strategy;
  output text report from Strategy;
}
```

## 安全架构

安全中间件的源代码：[middleware/security.py](https://github.com/contrario/aetherlang/blob/main/aetherlang/middleware/security.py)

### 输入验证（服务器端）
- **允许的字段**: 仅接受 `code`、`query`、`language` 三个字段。
- **长度限制**: 查询内容最长 5000 个字符，代码最长 10000 个字符，正文最长 50KB。
- **类型检查**: 所有字段在处理前都会进行类型验证。

### 防注入机制
- 防止代码执行（`eval`、`exec`）、SQL 注入、XSS 攻击、模板注入、操作系统命令以及提示内容被篡改。

### 速率限制
- **免费 tier**: 每小时 100 次请求，每 10 秒内允许 10 次请求（无需凭证）。

### 安全防护措施
- **内容过滤**: 提供严格/中等/宽松三种过滤级别。
- **Gandalf VETO**: 对 Assembly 引擎的输出结果进行人工智能安全审核。
- **审计日志**: 所有被阻止的请求都会被记录下来。

## 响应结构
```json
{
  "status": "success",
  "flow_name": "Chef",
  "result": {
    "outputs": { ... },
    "final_output": "Full structured response text",
    "duration_seconds": 58.9
  }
}
```

## 错误代码及其含义

| 代码 | 含义 |
|------|---------|
| 400 | 输入无效或检测到注入攻击 |
| 413 | 请求过大 |
| 429 | 超过速率限制 |
| 500 | 服务器错误 |

## 支持的语言

- **英语**（默认）
- **希腊语**（Ελληνικά）：V3 版本的支持语言，输出结果采用希腊语并保留 Markdown 格式。

## 技术架构

- **后端**: FastAPI + Python 3.12（[源代码](https://github.com/contrario/aetherlang) |
- **AI 模型**: 使用 OpenAI 的 GPT-4o 模型 |
- **解析器**: 支持 39 种不同类型的输入数据并对其进行验证 |
- **托管服务**: 使用 Hetzner EU 服务器（符合 GDPR 规范） |
- **版本**: 3.0.0 Omega

---
*由 NeuroAether 开发——从厨房到代码的革新之旅* 🧠