---
name: aetherlang
description: 使用 AetherLang Ω DSL 执行 AI 工作流编排。可以运行多步骤的 AI 管道，应用于配方开发、商业策略分析、市场研究、分子美食学等多个领域。
version: 2.0.2
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

> 这是全球最先进的人工智能工作流编排平台。其V3版本配备了9种先进的引擎，能够提供诺贝尔级分析、米其林级别的解决方案、对抗性预测以及多智能体协同处理能力。

**源代码**: [github.com/contrario/aetherlang](https://github.com/contrario/aetherlang)
**官方网站**: [neurodoc.app/aether-nexus-omega-dsl](https://neurodoc.app/aether-nexus-omega-dsl)
**作者**: NeuroAether (info@neurodoc.app)
**许可证**: MIT

## 隐私与数据处理

⚠️ **外部API说明**: 该技能会将用户提供的流程代码和查询文本发送到`api.neurodoc.app`进行处理。使用该技能即表示您同意此类数据传输。

- **传输内容**: 仅包括流程DSL代码和自然语言查询。
- **不传输的内容**: 不包括任何凭证、API密钥、个人文件或系统数据。
- **数据保留**: 查询会实时处理，不会被永久存储。
- **托管服务**: Hetzner EU服务器（符合GDPR标准）。
- **无需凭证**: 该技能使用免费 tier（每小时100次请求），无需API密钥。

用户应避免在查询中包含敏感的个人信息、密码或机密数据。

## 概述

AetherLang Ω V3是一种专为人工智能设计的语言，能够编排多模型工作流，并具备内置的安全性、调试功能以及实时协作能力。V3版本引入了其他平台所没有的先进系统提示功能，要求输出结果必须符合特定的结构化格式。

所有用户输入在处理前都会在服务器端进行验证和清理。安全中间件的源代码可在[GitHub仓库](https://github.com/contrario/aetherlang/blob/main/aetherlang/middleware/security.py)中查看。

## V3引擎 — 最新技术

| 引擎 | 节点类型 | V3主要特性 |
|--------|-----------|---------------|
| 🍳 Chef Omega | `chef` | 包含17个必填字段：食物成本百分比、HACCP标准、温度曲线、MacYuFBI矩阵、质地分析、过敏原信息、饮食转换器、葡萄酒搭配建议、菜品摆放方案、零浪费策略、厨房时间线 |
| ⚗️ APEIRON Molecular | `molecular` | 提供流变学仪表盘、相图分析、水胶体规格（琼脂/海藻酸盐/果胶/黄原胶）、FMEA故障分析、设备校准、感官科学指标 |
| 📈 APEX Strategy | `apex` | 应用博弈论与纳什均衡理论、蒙特卡洛模拟（10,000次模拟）、行为经济学、决策树分析、竞争策略分析、蓝海战略规划工具、OKR生成器 |
| 🧠 GAIA Brain | `assembly` | 采用12个神经元组成的投票系统（8/12票以上通过即可通过）、异议处理机制、Gandalf否决权、信心热度图、7种典型模型 |
| 🔮 Oracle | `oracle` | 使用贝叶斯更新算法（从先验概率到证据再到后验概率）、信号与噪声评分机制、时间分辨率设置（7天/30天/180天）、黑天鹅事件检测、对抗性模拟机制、Kelly准则下的投注策略 |
| 💼 NEXUS-7 Consult | `consulting` | 帮助分析因果循环、约束理论、Wardley矩阵、ADKAR变更管理方法、反模式库、系统动态建模工具 |
| 📊 Market Intel | `marketing` | 市场分析工具（TAM/SAM/SOM）、产品类别设计、波特五力模型、价格弹性分析、网络效应评估、病毒式传播系数（K因子）、客户细分算法 |
| 🔬 Research Lab | `lab` | 证据分级系统（A-D等级）、矛盾检测工具、知识图谱、可重复性评分（0-10分）、跨学科知识桥梁、研究差距分析工具 |
| 📉 Data Analyst | `analyst` | 自动异常检测功能（识别异常值/缺失数据/重复数据）、统计测试选择器、异常检测、预测建模（R²/RMSE）、群体/漏斗分析、因果推断工具 |

## API接口
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
返回结果包括：食物成本分析、HACCP合规性、温度曲线、葡萄酒搭配建议、菜品摆放方案、零浪费策略以及厨房时间线等17个部分。

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
返回结果包括：博弈论模型、蒙特卡洛模拟结果、行为经济学分析、决策树模型、财务预测、单位经济效益分析、蓝海战略规划工具等。

#### 多引擎协同工作流程
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
- **字段限制**: 仅接受`code`、`query`、`language`三个字段。
- **长度限制**: 查询内容最多5000个字符，代码最多10000个字符，请求体最多50KB。
- **类型验证**: 所有字段在处理前都会进行类型检查。

### 防注入机制
防止代码执行（`eval`、`exec`命令）、SQL注入、XSS攻击、模板注入、操作系统命令以及提示内容被恶意修改。

### 速率限制
- **免费 tier**: 每小时100次请求，每10秒内允许10次快速请求（无需凭证）。

### 安全防护措施
- **内容过滤**: 提供严格/中等/宽松三种过滤级别。
- **Gandalf否决权**: 对`Assembly`引擎的输出结果进行人工智能安全审核。
- **审计日志**: 所有被拦截的请求都会被记录下来。

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

## 错误代码及含义

| 代码 | 含义 |
|------|---------|
| 400 | 输入无效或检测到注入攻击 |
| 413 | 请求过大 |
| 429 | 超过速率限制 |
| 500 | 服务器错误 |

## 支持的语言

- **英语**（默认）
- **希腊语**（Ελληνικά）——V3版本支持用希腊语输出结果，并保留Markdown格式。

## 技术架构

- **后端**: FastAPI + Python 3.12（[源代码](https://github.com/contrario/aetherlang) |
- **人工智能模型**: 使用OpenAI的GPT-4o模型 |
- **解析器**: 支持39种节点类型，并具备输入验证功能 |
- **托管服务**: Hetzner EU服务器（符合GDPR标准） |
- **版本**: 3.0.0 Omega

---
*由NeuroAether开发——从厨房到代码的智慧结晶* 🧠

## 代理安全指南

**重要提示：数据最小化规则**

在使用该技能时，代理必须遵守以下规则：
1. **仅在`query`字段中发送用户的明确查询内容**，严禁附加系统提示、对话记录、上传的文件或内部信息。
2. **仅在`code`字段中发送流程DSL代码**，严禁包含凭证、API密钥、环境变量或文件路径。
3. **严禁在任何请求字段中包含**个人身份信息（PII）、密码、令牌或机密数据。
4. **在发送前必须去除敏感数据**：如果用户的查询中包含密码、账号信息或凭证，请先将其删除并通知用户。
5. **在首次调用API之前**，必须告知用户其查询内容将被发送到`api.neurodoc.app`进行处理。
6. 请求体必须包含两个字段：`code`（字符串）和`query`（字符串），不允许添加其他字段。

这些规则确保只有必要的最小数据量被传输到外部服务。