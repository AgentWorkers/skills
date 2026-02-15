# AetherLang Ω — 人工智能工作流编排技能

> 一款用于构建人工智能工作流的商用级DSL（Domain-Specific Language），支持39种节点类型，并具备企业级安全防护功能。

**源代码**: [github.com/contrario/aetherlang](https://github.com/contrario/aetherlang)
**官方网站**: [neurodoc.app/aether-nexus-omega-dsl](https://neurodoc.app/aether-nexus-omega-dsl)
**作者**: NeuroAether (info@neurodoc.app)
**许可证**: MIT

## 隐私与数据处理

⚠️ **外部API说明**: 该技能会将用户提供的流程代码和查询文本发送到`api.neurodoc.app`处的AetherLang API进行处理。使用该技能即表示您同意此类数据传输。

- **传输内容**: 仅包括流程DSL代码和自然语言查询。
- **不传输的内容**: 不会传输任何凭证、API密钥、个人文件或系统数据。
- **数据保留**: 查询内容会实时处理，不会被永久存储。
- **托管服务**: Hetzner EU服务器（符合GDPR法规）。
- **无需凭证**: 该技能使用免费 tier，每小时允许100次请求，无需API密钥。

用户应避免在查询中包含敏感的个人信息、密码或机密数据。

## 概述

AetherLang Ω 是一种专为人工智能设计的语言，能够编排多模型工作流，并内置了安全防护、调试功能以及实时协作机制。

所有用户输入在处理前都会在服务器端进行验证和清洗。安全中间件的源代码可在[GitHub仓库](https://github.com/contrario/aetherlang/blob/main/aetherlang/middleware/security.py)中查看。

## 支持的引擎

| 引擎 | 触发关键词 | 描述 |
|--------|-----------------|-------------|
| `chef` | recipe, cook, food | 配备HACCP标准的米其林级食谱，包含成本信息 |
| `molecular` | molecular, spherification | 分子美食烹饪技术 |
| `apex` | strategy, business, analysis | 诺贝尔级分析（麦肯锡/HBR质量标准） |
| `assembly` | debate, perspectives, council | 26种人工智能架构模型，支持Gandalf Veto机制 |
| `consulting` | consulting, SWOT, roadmap | 带有KPI的战略咨询服务 |
| `lab` | science, research, experiment | 涵盖50个领域的科学分析 |
| `marketing` | campaign, viral, social media | 基于内容日历的营销活动生成工具 |
| `oracle` | lottery, OPAP, lucky numbers | 希腊彩票的统计与分析服务 |
| `cyber` | security, threat, vulnerability | 危险评估及防御策略 |
| `academic` | paper, arXiv, PubMed | 多源研究整合工具 |
| `vision` | image, analyze, detect | 计算机视觉分析 |
| `brain` | think, analyze, comprehensive | 通用人工智能分析工具 |

## API端点
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

#### Chef工作流示例
```
flow Chef {
  using target "neuroaether" version ">=0.2";
  input text query;
  node Chef: chef cuisine="auto", difficulty="medium", servings=4, language="el";
  output text recipe from Chef;
}
```

#### APEX策略工作流示例
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

## 安全架构

安全中间件的源代码: [middleware/security.py](https://github.com/contrario/aetherlang/blob/main/aetherlang/middleware/security.py)

### 输入验证（服务器端）
- **字段白名单**: 仅接受`code`、`query`、`language`字段。
- **长度限制**: 查询内容最长5000个字符，代码最长10000个字符，请求体最大50KB。
- **类型验证**: 所有字段在处理前都会进行类型检查。

### 防注入机制
- 防止代码执行（`eval`、`exec`）、SQL注入、XSS攻击、模板注入、操作系统命令以及提示框篡改等安全问题。

### 速率限制
- **免费 tier**: 每小时100次请求，每10秒内允许10次请求（无需凭证）。

### 安全防护措施
- **GUARD节点**: 提供严格/中等/宽松三种内容过滤级别。
- **Gandalf Veto**: 对`assembly`引擎的输出内容进行人工智能安全审核。
- **审计日志**: 所有被阻止的请求都会被记录下来。

## 响应结构
```json
{
  "status": "success",
  "flow_name": "Chef",
  "result": {
    "outputs": {
      "recipe": {
        "response": "{ structured JSON }",
        "engine": "chef",
        "model": "gpt-4o"
      }
    },
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
- **希腊语**（Ελληνικά）——在节点配置中添加`language="el"`即可使用。

## 技术架构

- **后端**: FastAPI + Python 3.12（[源代码](https://github.com/contrario/aetherlang) |
- **人工智能模型**: 通过OpenAI提供的GPT-4o模型 |
- **解析器**: 支持39种节点类型并进行类型验证 |
- **托管服务**: Hetzner EU服务器（符合GDPR法规）

---
*由NeuroAether开发——从厨房到代码的智慧之旅* 🧠