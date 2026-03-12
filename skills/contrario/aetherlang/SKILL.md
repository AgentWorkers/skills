---
name: aetherlang
description: 使用 AetherLang Ω DSL 执行 AI 工作流编排流程。可以运行多步骤的 AI 管道，应用于食谱开发、商业策略分析、分子美食学等领域。
version: 9.9.11
author: contrario
homepage: https://masterswarm.net
requirements:
  binaries: []
  env: []
metadata:
  skill_type: api_connector
  external_endpoints:
    - https://api.neurodoc.app/aetherlang/execute
  operator_note: "api.neurodoc.app operated by NeuroDoc Pro (same as masterswarm.net), Hetzner DE"
  privacy_policy: https://masterswarm.net
license: MIT
---
# AetherLang Ω V3 — 人工智能工作流编排技能

> 这是全球最先进的人工智能工作流编排平台。AetherLang Ω V3 搭载了 9 个先进的 AI 引擎，能够提供诺贝尔级分析、米其林级别的解决方案、对抗性预测以及多智能体协同处理能力。

**源代码**: [github.com/contrario/aetherlang](https://github.com/contrario/aetherlang)
**官网**: [neurodoc.app/aether-nexus-omega-dsl](https://neurodoc.app/aether-nexus-omega-dsl)
**作者**: NeuroAether (echelonvoids@protonmail.com)
**许可证**: MIT

## 隐私与数据处理

⚠️ **外部 API 注意事项**: 该技能会将用户提供的流程代码和查询文本发送到 `api.neurodoc.app` 进行处理。使用该技能即表示您同意此类数据传输。

- **传输内容**: 仅包括流程 DSL 代码和自然语言查询。
- **不传输的内容**: 不会传输任何凭证、API 密钥、个人文件或系统数据。
- **数据保留**: 查询会实时处理，不会被永久存储。
- **托管服务**: Hetzner 欧洲服务器（符合 GDPR 标准）。
- **无需凭证**: 该技能使用免费 tier（每小时 100 次请求），无需 API 密钥。

用户应避免在查询中包含敏感的个人信息、密码或机密数据。

## 概述

AetherLang Ω V3 是一种专门用于人工智能的领域特定语言，能够编排多模型工作流，并具备内置的安全性、调试功能以及实时协作能力。V3 版本引入了其他平台所没有的先进系统提示功能，要求输出结果必须结构化。

所有用户输入在处理前都会在服务器端进行验证和清洗。网络流量可以独立验证：该技能仅向 `api.neurodoc.app` 发送 DSL 代码和查询文本，请求数据中不包含系统上下文、文件或环境变量。

## V3 引擎 — 最新技术

| 引擎 | 节点类型 | V3 主要特性 |
|--------|-----------|---------------|
| 🍳 Chef Omega | `chef` | 17 个必填字段：食物成本百分比、HACCP 标准、温度曲线、MacYuFBI 矩阵、质地分析、过敏原矩阵（14 个欧盟国家适用）、饮食转换器、葡萄酒搭配建议、摆盘方案、零浪费策略、厨房时间线 |
| ⚗️ APEIRON Molecular | `molecular` | 流变学仪表盘、相图分析、水胶体规格（琼脂/海藻酸盐/瓜尔胶/黄原胶）、FMEA 故障分析、设备校准、感官科学指标 |
| 📈 APEX Strategy | `apex` | 博弈论 + 纳什均衡、蒙特卡洛模拟（10,000 次模拟）、行为经济学、决策树、竞争策略分析、单位经济分析（CAC/LTV）、蓝海战略分析工具、OKR 生成器 |
| 🧠 GAIA Brain | `assembly` | 12 个神经元投票系统（8/12 票数需达到超级多数）、异议处理机制、Gandalf VETO 权限、信心热度图、7 种原型分析方法 |
| 🔮 Oracle | `oracle` | 贝叶斯更新机制（先验→证据→后验）、信号与噪声评分、时间分辨率（7天/30天/180天）、黑天鹅事件检测、对抗性模拟测试、Kelly 标准下的投注策略 |
| 💼 NEXUS-7 Consult | `consulting` | 因果循环图、约束理论、Wardley 分类法、ADKAR 变革管理工具、反模式库、系统动态建模 |
| 📊 Market Intel | `marketing` | 市场分析工具（TAM/SAM/SOM）、产品类别设计、波特五力模型、价格弹性分析、网络效应分析、病毒式传播系数（K 因子）、客户细分算法 |
| 🔬 Research Lab | `lab` | 证据分级（A-D 级别）、矛盾检测器、知识图谱、可重复性评分（1-10 分）、跨学科研究桥梁、研究差距分析 |
| 📉 Data Analyst | `analyst` | 异常值检测、统计测试选择器、异常检测、预测建模（R²/RMSE）、群体/漏斗分析、因果推断 |

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

#### Chef Omega V3 — 全面餐厅咨询
```
flow Chef {
  using target "neuroaether" version ">=0.2";
  input text query;
  node Chef: chef cuisine="auto", difficulty="medium", servings=4, language="el";
  output text recipe from Chef;
}
```
返回结果包括：食物成本分析、HACCP 合规性、温度曲线、葡萄酒搭配建议、摆盘方案、零浪费策略以及厨房时间线。

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
返回结果包括：博弈论模型、蒙特卡洛模拟、行为经济学分析、决策树模型、财务预测、单位经济分析、蓝海战略分析工具。

#### 多引擎协同流程
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

安全中间件源代码: [middleware/security.py](https://github.com/contrario/aetherlang/blob/main/aetherlang/middleware/security.py)

### 输入验证（服务器端）
- **字段白名单**: 仅接受 `code`、`query`、`language` 三个字段。
- **长度限制**: 查询内容最长 5000 个字符，代码内容最长 10000 个字符，请求体最大 50KB。
- **类型验证**: 所有字段在处理前都会进行类型检查。

### 防注入攻击
防止以下攻击类型：代码执行（`eval`、`exec`）、SQL 注入、XSS 攻击、模板注入、操作系统命令执行、提示内容篡改。

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

## 错误响应

| 错误代码 | 含义 |
|------|---------|
| 400 | 输入无效或检测到注入攻击 |
| 413 | 请求过大 |
| 429 | 超过速率限制 |
| 500 | 服务器错误 |

## 支持的语言

- **英语**（默认）
- **希腊语**（Ελληνικά）——V3 版本的输出结果会以希腊语显示，并保留 markdown 格式。

## 技术架构

- **后端**: FastAPI + Python 3.12（[源代码](https://github.com/contrario/aetherlang) |
- **AI 模型**: 通过 OpenAI 提供的 GPT-4o 模型 |
- **解析器**: 支持 39 种不同类型的输入数据，并进行验证 |
- **托管服务**: Hetzner 欧洲服务器（符合 GDPR 标准） |
- **版本**: 3.0.0 Omega

---
*由 NeuroAether 开发——从厨房到代码的智慧之旅* 🧠

## 代理安全指南

**重要提示：数据最小化规则**

使用该技能时，代理必须遵守以下规则：
1. **仅在 `query` 字段中发送用户的明确查询内容**，严禁附加系统提示、对话记录、上传的文件或内部信息。
2. **仅在 `code` 字段中发送流程 DSL 代码**，严禁包含凭证、API 密钥、环境变量或文件路径。
3. **严禁在任何请求字段中包含**个人身份信息（PII）、密码、令牌或机密数据。
4. **在发送前去除敏感数据**：如果用户查询中包含密码、账号信息或凭证，请将其删除并通知用户。
5. **在首次调用 API 之前**，必须告知用户其查询内容将被发送到 `api.neurodoc.app` 进行处理。
6. 请求体必须包含两个字段：`code`（字符串）和 `query`（字符串），不允许添加其他字段。

这些限制确保只有最低限度的必要数据被传输到外部服务。