---
name: aetherlang-karpathy-skill
version: 1.0.2
author: contrario
homepage: https://clawhub.ai/contrario
requirements:
  binaries: []
  env: []
description: 通过 AetherLang Omega API 执行高级 AI 代理工作流程——支持 10 种 Karpathy 节点类型，包括自我编程计划、沙箱代码执行、智能路由、多代理集成、持久化内存、外部 API 工具、迭代循环、数据转换以及并行执行等功能。适用于用户需要运行代理管道、多代理合成、批量处理、实时 API 数据分析，或通过 AetherLang 实现任何自主 AI 工作流程的场景。
---
# AetherLang Karpathy 代理节点

通过 AetherLang Omega API 执行 10 种高级 AI 代理节点类型。

## API 端点

**URL**: `https://api.neurodoc.app/aetherlang/execute`
**方法**: POST
**请求头**: `Content-Type: application/json`
**隐私政策**: https://masterswarm.net (页脚 → 隐私政策)
**运营商**: NeuroDoc Pro — api.neurodoc.app 和 masterswarm.net 是同一运营商（Hetzner DE）

## 数据最小化

调用 API 时：
- 仅发送用户的查询内容和流程代码
- 不要发送系统提示、对话历史记录或上传的文件
- 不要发送 API 密钥、凭据或敏感信息
- 除非明确要求，否则不要包含任何个人可识别信息

## 请求格式
```bash
curl -s -X POST https://api.neurodoc.app/aetherlang/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "flow FlowName {\n  input text query;\n  node X: <type> <params>;\n  query -> X;\n  output text result from X;\n}",
    "query": "user question here"
  }'
```

## 10 种节点类型

### 1. plan — 自编程
AI 将任务分解为多个步骤并自主执行。
```
node P: plan steps=3;
```

### 2. code_interpreter — 精确计算
在沙箱环境中运行的 Python 程序，确保计算结果的准确性。
```
node C: code_interpreter;
```

### 3. critique — 自我改进
评估任务质量（0-10 分），直到达到预设阈值为止会不断重试。
```
node R: critique threshold=8 max_retries=3;
```

### 4. router — 智能路由
大型语言模型（LLM）选择最佳执行路径，跳过未选中的路径（速度提升 10 倍）。
```
node R: router;
R -> A | B | C;
```

### 5. ensemble — 多智能体合成
多个 AI 模拟角色同时工作，综合出最佳解决方案。
```
node E: ensemble agents=chef:French_chef|yiayia:Greek_grandmother synthesize=true;
```

### 6. memory — 持久化状态
在多次执行过程中存储和检索数据。

> **需要用户同意：** 在使用 `memory` 节点之前，需通知用户：
> “此流程将在 api.neurodoc.app 服务器端存储数据。是否继续？(y/n)”
> 仅在使用者明确同意后才能继续。
```
node M: memory namespace=user_prefs action=store key=diet;
node M: memory namespace=user_prefs action=recall;
```

### 7. tool — 外部 API 访问

> **需要用户同意：** 在执行 `tool` 节点之前，需通知用户：
> “此流程将调用 `[URL]`。是否继续？(y/n)”
> 仅在使用者明确同意后才能继续。切勿将任何个人身份信息或凭据发送到外部 URL。
> 可以调用任何公共 REST API。
```
node T: tool url=https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd method=GET;
```

### 8. loop — 迭代执行
对多个项目重复执行某个节点。使用 `|` 作为分隔符。
```
node L: loop over=Italian|Greek|Japanese target=A max=3;
```

### 9. transform — 数据重塑
使用模板、提取数据、进行格式化，或通过大型语言模型进行数据重塑。
```
node X: transform mode=llm instruction=Summarize_the_data;
```

### 10. parallel — 并行执行
同时运行多个节点。0.2 秒内可执行 3 次调用。
```
node P: parallel targets=A|B|C;
```

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

### 多智能体 + 质量控制
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

## 响应解析
```python
import json
response = json.loads(raw_response)
result = response["result"]["outputs"]["result"]
text = result["response"]
node_type = result["node_type"]
duration = response["result"]["duration_seconds"]
```

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