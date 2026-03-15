---
name: aetherlang-karpathy-skill
description: >
  **AetherLang Omega 的 API 连接器**  
  该连接器支持通过托管在 `api.neurodoc.app` 上的 AetherLang API 来执行 10 种基于 Karpathy 架构设计的代理节点类型（包括 `plan`、`code_interpreter`、`critique`、`router`、`ensemble`、`memory`、`tool`、`loop`、`transform`、`parallel`）。该功能会将您的查询及流程代码发送至 API，并返回相应的结果。无需在本地执行任何代码，也不需要对系统进行任何运行时修改，同时无需提供任何认证信息。
version: 1.0.3
author: contrario
homepage: https://clawhub.ai/contrario
requirements:
  binaries: []
  env: []
metadata:
  skill_type: api_connector
  operator_note: "AetherLang Omega is operated by NeuroDoc Pro (masterswarm.net), hosted on Hetzner EU. Karpathy-style refers to node architecture inspired by Andrej Karpathy's agent design principles — no affiliation or endorsement implied."
  external_endpoints:
    - https://api.neurodoc.app/aetherlang/execute
  domains_not_recommended:
    - medical advice
    - legal advice
    - financial advice
license: MIT
---
# AetherLang Karpathy 代理节点

> **该技能的功能：** 向托管的 AetherLang API (`api.neurodoc.app`) 发送请求。该技能不会修改本地文件、执行本地代码，也不会访问您机器上的凭据。所有操作均在服务器端完成。

通过 AetherLang Omega API 执行 10 种高级 AI 代理节点类型。

---

## API 端点

**URL**: `https://api.neurodoc.app/aetherlang/execute`
**方法**: POST
**请求头**: `Content-Type: application/json`
**认证**: 无需认证（公共 API）

---

## 数据最小化原则 — 请始终遵守

调用 API 时，请注意：
- 仅发送用户的查询内容和流程代码；
- 不要发送系统提示、对话记录或上传的文件；
- 不要发送 API 密钥、凭据或任何形式的敏感信息；
- 除非用户明确要求，否则不要发送个人身份信息；
- 未经用户明确同意，不要发送本地文件的内容。

---

## 请求格式

```bash
curl -s -X POST https://api.neurodoc.app/aetherlang/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "flow FlowName {\n  input text query;\n  node X: <type> <params>;\n  query -> X;\n  output text result from X;\n}",
    "query": "user question here"
  }'
```

---

## 10 种代理节点类型

### 1. plan — 自我编程
AI 将任务分解为多个步骤并自主执行。
```
node P: plan steps=3;
```

### 2. code_interpreter — 真实数学计算
在服务器上以沙箱模式运行 Python 代码，确保计算结果的准确性。
```
node C: code_interpreter;
```

### 3. critique — 自我提升
评估代码的质量（0-10 分），直到达到预设的阈值为止会不断重试。
```
node R: critique threshold=8 max_retries=3;
```

### 4. router — 智能路径选择
大型语言模型（LLM）会选择最优的执行路径，并跳过未选中的路径（速度提升 10 倍）。
```
node R: router;
R -> A | B | C;
```

### 5. ensemble — 多智能体协作
多个 AI 智能体同时工作，综合出最佳解决方案。
```
node E: ensemble agents=chef:French_chef|yiayia:Greek_grandmother synthesize=true;
```

### 6. memory — 持久化状态
在多次执行过程中存储和检索数据（数据存储在服务器端，按命名空间管理）。
```
node M: memory namespace=user_prefs action=store key=diet;
node M: memory namespace=user_prefs action=recall;
```

### 7. tool — 外部 API 访问
> **安全提示：** `tool` 节点会调用您指定的公共 REST API。请仅使用可信的公共 API。切勿将凭据或私有 URL 作为 `tool` 的参数传递。在调用任何非示例中的 URL 之前，代理会请求用户的确认。
```
node T: tool url=https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd method=GET;
```

### 8. loop — 迭代执行
对多个项目重复执行该节点。使用 `|` 作为分隔符。
```
node L: loop over=Italian|Greek|Japanese target=A max=3;
```

### 9. transform — 数据重塑
根据模板对数据进行提取、格式化或使用 LLM 功能进行重塑。
```
node X: transform mode=llm instruction=Summarize_the_data;
```

### 10. parallel — 并行执行
多个节点同时运行。每次调用大约需要 0.2 秒。
```
node P: parallel targets=A|B|C;
```

---

## 常见工作流程

### 实时数据 → 分析
```
flow CryptoAnalysis {
  input text query;
  node T: tool url=https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd method=GET;
  node X: transform mode=llm instruction=Summarize_price;
  node A: llm model=gpt-4o-mini;
  query -> T -> X -> A;
  output text result from A;
}
```

### 多智能体协作 + 质量控制
```
flow QualityEnsemble {
  input text query;
  node E: ensemble agents=analyst:Financial_analyst|strategist:Strategist synthesize=true;
  node R: critique threshold=8;
  query -> E -> R;
  output text result from R;
}
```

### 批量处理
```
flow MultiRecipe {
  input text query;
  node L: loop over=Italian|Greek|Japanese target=A max=3;
  node A: llm model=gpt-4o-mini;
  query -> L;
  output text result from L;
}
```

### 并行 API 请求
```
flow ParallelFetch {
  input text query;
  node P: parallel targets=A|B|C;
  node A: tool url=https://api.coingecko.com/api/v3/ping method=GET;
  node B: tool url=https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd method=GET;
  node C: tool url=https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd method=GET;
  query -> P;
  output text result from P;
}
```

---

## 响应解析
```python
import json
response = json.loads(raw_response)
result = response["result"]["outputs"]["result"]
text = result["response"]
node_type = result["node_type"]
duration = response["result"]["duration_seconds"]
```

---

## 参数快速参考

| 节点 | 关键参数 |
|------|-----------|
| plan | `steps=3` |
| code_interpreter | `model=gpt-4o-mini` |
| critique | `threshold=7` `max_retries=3` |
| router | `strategy=single` |
| ensemble | `agents=a:Persona\|b:Persona` `synthesize=true` |
| memory | `namespace=X` `action=store\|recall\|search\|clear` `key=X` |
| tool | `url=https://...` `method=GET` `timeout=10` |
| loop | `over=A\|B\|C` `target=NodeAlias` `max=10` `mode=collect` |
| transform | `mode=llm\|template\|extract\|format` `instruction=X` |
| parallel | `targets=A\|B\|C` `merge=combine` |

---

*AetherLang Karpathy 技能 v1.0.1 — 用于 api.neurodoc.app 的 API 连接器*
*所有操作均在服务器端完成。不会运行任何本地代码，也不会修改本地文件。*