---
name: masterswarm
description: 您可以通过 MasterSwarm 云 API，使用 15 个并行运行的 AI 引擎来分析任何文档。您可以上传收据、合同、实验结果，或提出与商业/加密/法律相关的问题，从而获得专业的情报报告。这需要从 masterswarm.net 购买付费的 MasterSwarm API 密钥。
version: 1.1.2
author: contrario
homepage: https://masterswarm.net
requirements:
  binaries: []
  env:
    - name: MASTERSWARM_API_KEY
      description: "Your MasterSwarm API key from masterswarm.net"
      required: true
metadata:
  openclaw:
    emoji: "⚡"
    homepage: https://masterswarm.net
  skill_type: api_connector
  external_endpoints:
    - https://api.neurodoc.app/aetherlang/execute
  operator_note: "api.neurodoc.app and masterswarm.net are the same operator (NeuroDoc Pro, Hetzner DE)"
license: MIT
---
# MasterSwarm AI — 15个智能引擎，31个分析工具，统一分析结果

MasterSwarm是一个基于云的分布式AI编排API，它利用15个并行运行的专业AI引擎来分析文档和问题。

## 功能概述

将任何文本或问题发送至MasterSwarm API，15个引擎会同时对其进行分析，并返回一份详细的多页分析报告。

### 可用的智能引擎

| 引擎ID | 名称 | 应用场景 |
|---|---|---|
| `chef` | Chef Omega | 食谱制作、食物成本计算、餐厅咨询 |
| `apex` | APEX Strategy | 商业策略分析、财务预测、加密货币研究 |
| `consult` | NEXUS Consulting | SWOT分析、路线图制定、系统思维研究 |
| `research` | Research Lab | 科学研究、医学数据分析、论文分析 |
| `market` | Market Intel | 市场竞争分析、目标市场分析（TAM/SAM）、增长策略 |
| `molecular` | APEIRON Lab | 分子美食学、食品科学 |
| `oracle` | Oracle | 预测分析、情景规划 |
| `assembly` | GAIA Brain | 多视角分析（包含12个认知模块） |
| `analyst` | Data Analyst | 数据统计、异常检测、模型构建 |

## 设置要求

使用MasterSwarm API需要**API密钥**进行身份验证。所有API请求均发送至`https://api.neurodoc.app`。

```
MASTERSWARM_API_KEY=your_personal_key_here
```

### 如何获取API密钥

1. 访问**https://masterswarm.net**并购买相应的服务计划：
   - Explorer（9.99欧元）——可生成5份报告
   - Professional（29.99欧元）——可生成20份报告
   - Enterprise（79.99欧元）——可生成60份报告
2. 购买后，Gumroad会通过电子邮件发送给您**许可密钥**。
3. 登录**https://masterswarm.net/app/**，点击“升级”选项，粘贴您的许可密钥并完成激活。
4. 密钥激活后，即可将其设置为`MASTERSWARM_API_KEY`。

### 数据处理与隐私政策

- **API服务器**：`api.neurodoc.app`（由NeuroDoc Pro运营，与masterswarm.net属于同一实体）
- **服务器位置**：德国Hetzner（仅限欧盟地区）
- **加密方式**：TLS 1.3端到端加密
- **数据存储**：数据实时处理后立即销毁，无长期存储
- **GDPR合规性**：遵循欧盟数据保护法规（详情见https://masterswarm.net底部的隐私政策）
- **数据使用**：所有数据仅用于分析，不会被存储或用于训练目的

## 使用方法

### 单个引擎分析

```bash
curl -s --max-time 120 -X POST https://api.neurodoc.app/aetherlang/execute \
  -H "Content-Type: application/json" \
  -H "X-Aether-Key: MASTERSWARM_API_KEY" \
  -d '{
    "code": "flow Q {\n  using target \"neuroaether\" version \">=0.2\";\n  input text query;\n  node G: guard mode=\"STANDARD\";\n  node E: ENGINE_ID style=\"professional\";\n  G -> E;\n  output text result from E;\n}",
    "query": "USER_QUESTION_OR_DOCUMENT_TEXT"
  }'
```

**注意替换以下内容：**
- `MASTERSWARM_API_KEY` — 请使用您的个人API密钥
- `ENGINE_ID` — 从上述列表中选择一个引擎的ID（例如`apex`、`chef`、`research`）
- `USER-question_OR_document_TEXT` — 用户的问题或文档文本

### 引擎选择指南

| 用户需求 | 推荐引擎ID |
|---|---|
| 食谱制作、食物相关问题 | `chef` |
| 商业策略、初创企业分析 | `apex` |
| SWOT分析、咨询服务、路线图制定 | `consult` |
| 科学研究、论文分析 | `research` |
| 市场竞争分析 | `market` |
| 加密货币、交易、DeFi相关问题 | `apex` |
| 医学数据分析 | `research` |
| 法律文件、合同审核 | `consult` |
| 财务分析 | `apex` |
| 多领域问题 | `assembly` |
| 数据统计、异常检测 | `analyst` |
| 分子美食学、食品科学 | `molecular` |
| 预测分析 | `oracle` |

### 多引擎分析

如需生成综合报告，请依次调用多个引擎：

```bash
# Example: Run apex + consult + research on the same query
for ENGINE_ID in apex consult research; do
  curl -s --max-time 120 -X POST https://api.neurodoc.app/aetherlang/execute \
    -H "Content-Type: application/json" \
    -H "X-Aether-Key: MASTERSWARM_API_KEY" \
    -d "{
      \"code\": \"flow M {\n  using target \\\"neuroaether\\\" version \\\">=0.2\\\";\n  input text query;\n  node G: guard mode=\\\"STANDARD\\\";\n  node E: $ENGINE_ID style=\\\"professional\\\";\n  G -> E;\n  output text result from E;\n}\",
      \"query\": \"USER_QUESTION\"
    }"
done
```

### 响应格式

```json
{
  "status": "success",
  "result": {
    "final_output": "## Full analysis report in markdown...",
    "outputs": {"E": "..."},
    "execution_log": [
      {"node": "G", "status": "OK"},
      {"node": "E", "status": "OK", "duration": 5.2}
    ]
  },
  "duration_seconds": 6.1
}
```

请提取`result.final_output`字段，将其呈现给用户。

**错误响应说明：**
- `"status": "error"` — 请查看`error`字段以获取详细错误信息
- `"status": "validation_error"` — 请求格式错误
- HTTP 429 — 请求次数达到限制，请稍后重试

### 重要注意事项

- **超时设置**：建议设置120-180秒的超时时间，因为多引擎分析需要一定时间
- **费用计算**：每次API调用会消耗用户购买计划中的一个信用点数
- **语言处理**：系统会自动检测输入语言，并生成相应语言的报告
- **请求限制**：每个API密钥同时支持的最大请求量为5次

## 相关链接

| 资源 | 链接 |
|---|---|
| 主页 | https://masterswarm.net |
| 购买信用点数 | https://masterswarm.net（价格页面） |
| 应用程序控制台 | https://masterswarm.net/app/ |
| Telegram机器人 | https://t.me/aetherlang_bot |
| AetherLang官方文档 | https://aetherlang.net |
| 隐私政策 | https://masterswarm.net（页面底部） |
| 技术支持邮箱 | echelonvoids@protonmail.com |