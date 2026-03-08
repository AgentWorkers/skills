---
name: aetherlang-claude-code
description: 使用九种专门针对烹饪、商业、研究、市场营销和战略分析设计的引擎，通过 Claude Code 执行 AetherLang V3 人工智能工作流。
version: 1.0.3
author: contrario
homepage: https://masterswarm.net
requirements:
  binaries: []
  env:
    - name: AETHER_KEY
      required: false
      description: "Optional Pro tier API key for X-Aether-Key header (500 req/hour). Get from masterswarm.net."
metadata:
  skill_type: api_connector
  external_endpoints:
    - https://api.neurodoc.app/aetherlang/execute
  operator_note: "api.neurodoc.app operated by NeuroDoc Pro (same as masterswarm.net), Hetzner DE"
  privacy_policy: https://masterswarm.net
license: MIT
---
# AetherLang V3 — 从Claude Code集成AetherLang V3 AI工作流的技能

使用此技能可以从Claude Code中执行AetherLang V3 AI工作流。AetherLang提供了9种专门用于烹饪咨询、商业策略、科学研究等领域的AI引擎。

## API端点
```
POST https://api.neurodoc.app/aetherlang/execute
Content-Type: application/json
```

免费 tier（每小时100次请求）无需API密钥。

## 数据最小化

调用API时：
- 仅发送用户的查询和流程代码
- 不要发送系统提示、对话历史记录或上传的文件
- 不要发送API密钥、凭证或机密信息
- 除非明确要求，否则不要包含个人身份信息

> **专业API密钥：** 如果使用Pro tier（`X-Aether-Key`头部），请将密钥存储在环境变量中——切勿将其硬编码在流程代码或脚本中。
> 使用`export AETHER_KEY=your_key_here`，然后使用`-H "X-Aether-Key: $AETHER_KEY"`。

## 使用方法

### 1. 简单的引擎调用
```bash
curl -s -X POST https://api.neurodoc.app/aetherlang/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "flow Chat {\n  using target \"neuroaether\" version \">=0.2\";\n  input text query;\n  node Engine: <ENGINE_TYPE> analysis=\"auto\";\n  output text result from Engine;\n}",
    "query": "USER_QUESTION_HERE"
  }'
```

将`<ENGINE_TYPE>`替换为以下选项之一：`chef`、`molecular`、`apex`、`consulting`、`marketing`、`lab`、`oracle`、`assembly`、`analyst`。

### 2. 多引擎流程
```bash
curl -s -X POST https://api.neurodoc.app/aetherlang/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "flow Pipeline {\n  using target \"neuroaether\" version \">=0.2\";\n  input text query;\n  node Guard: guard mode=\"MODERATE\";\n  node Research: lab domain=\"business\";\n  node Strategy: apex analysis=\"strategic\";\n  Guard -> Research -> Strategy;\n  output text report from Strategy;\n}",
    "query": "USER_QUESTION_HERE"
  }'
```

## 可用的V3引擎

| 引擎类型 | 用途 | V3关键特性 |
|-------------|---------|-----------------|
| `chef` | 食谱制作、食品咨询 | 17个功能模块：食品成本、HACCP（食品安全管理）、热曲线分析、葡萄酒搭配建议、零浪费方案 |
| `molecular` | 分子美食学 | 流变学仪表板、相图分析、水胶体特性研究、FMEA（故障模式与效应分析） |
| `apex` | 商业策略 | 博弈论、蒙特卡洛模拟（10,000次模拟）、行为经济学、单位经济学、蓝海战略 |
| `consulting` | 战略咨询 | 因果关系分析、约束理论、Wardley模型、ADKAR变革管理方法 |
| `marketing` | 市场研究 | 目标市场细分（TAM/SAM/SOM）、波特五力模型、价格弹性分析、病毒式传播系数 |
| `lab` | 科学研究 | 证据评级（A-D等级）、矛盾检测工具、可重复性评估 |
| `oracle` | 预测分析 | 贝叶斯更新算法、黑天鹅事件检测、对抗性分析工具、Kelly决策标准 |
| `assembly` | 多智能体辩论 | 12个智能体投票（8/12票以上通过）、Gandalf否决权机制、魔鬼代言人角色 |
| `analyst` | 数据分析 | 自动检测工具、统计测试、异常检测、预测建模 |

## 流程语法参考
```
flow <Name> {
  using target "neuroaether" version ">=0.2";
  input text query;
  node <NodeName>: <engine_type> <params>;
  node <NodeName2>: <engine_type2> <params>;
  <NodeName> -> <NodeName2>;
  output text result from <NodeName2>;
}
```

### 节点参数
- `chef`：`cuisine="auto"`、`difficulty="medium"`、`servings=4`
- `apex`：`analysis="strategic"`
- `guard`：`mode="STRICT"` 或 `"MODERATE"` 或 `"PERMISSIVE"`
- `plan`：`steps=4`
- `lab`：`domain="business"` 或 `"science"` 或 `"auto"`
- `analyst`：`mode="financial"` 或 `"sales"` 或 `"hr"` 或 `"general"`

## 响应格式
```json
{
  "status": "success",
  "result": {
    "outputs": { ... },
    "final_output": "Full structured markdown response",
    "execution_log": [...],
    "duration_seconds": 45.2
  }
}
```

从`result.final_output`中提取主要响应内容。

## 示例：在Bash中解析响应
```bash
curl -s -X POST https://api.neurodoc.app/aetherlang/execute \
  -H "Content-Type: application/json" \
  -d '{"code":"flow Chef {\n  using target \"neuroaether\" version \">=0.2\";\n  input text query;\n  node Chef: chef cuisine=\"auto\";\n  output text recipe from Chef;\n}","query":"Carbonara recipe"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result',{}).get('final_output','No output'))"
```

## 示例：Python集成
```python
import requests

def aetherlang_query(engine, query):
    code = f'''flow Q {{
  using target "neuroaether" version ">=0.2";
  input text query;
  node E: {engine} analysis="auto";
  output text result from E;
}}'''
    r = requests.post("https://api.neurodoc.app/aetherlang/execute",
        json={"code": code, "query": query})
    return r.json().get("result", {}).get("final_output", "")

# Usage
print(aetherlang_query("apex", "Strategy for AI startup with 1000 euro"))
print(aetherlang_query("chef", "Best moussaka recipe"))
print(aetherlang_query("oracle", "Will AI replace 50% of jobs by 2030?"))
```

## 速率限制

| 计费等级 | 每小时请求次数 | 认证要求 |
|------|-------|------|
| 免费 | 100次请求/小时 | 无需认证 |
| 专业 | 500次请求/小时 | 需要`X-Aether-Key`头部 |

## 注意事项

- 响应内容采用希腊语（Ελληνικά）格式，并使用markdown标记。
- 典型响应时间：每个引擎的响应时间为30-60秒。
- 多引擎流程需要更长时间（每个节点依次执行）。
- 所有输出都使用`##`标记来分隔不同的部分。