# AetherLang V3 — 从Claude Code集成AetherLang V3 AI工作流的功能

使用此功能可以从Claude Code中执行AetherLang V3的AI工作流。AetherLang提供了9种专门用于烹饪咨询、商业策略、科学研究等领域的AI引擎。

## API端点
```
POST https://api.neurodoc.app/aetherlang/execute
Content-Type: application/json
```

免费 tier（每小时100次请求）无需API密钥。

## 使用方法

### 1. 单个引擎调用
```bash
curl -s -X POST https://api.neurodoc.app/aetherlang/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "flow Chat {\n  using target \"neuroaether\" version \">=0.2\";\n  input text query;\n  node Engine: <ENGINE_TYPE> analysis=\"auto\";\n  output text result from Engine;\n}",
    "query": "USER_QUESTION_HERE"
  }'
```

将`<ENGINE_TYPE>`替换为以下选项之一：`chef`、`molecular`、`apex`、`consulting`、`marketing`、`lab`、`oracle`、`assembly`、`analyst`

### 2. 多引擎流水线
```bash
curl -s -X POST https://api.neurodoc.app/aetherlang/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "flow Pipeline {\n  using target \"neuroaether\" version \">=0.2\";\n  input text query;\n  node Guard: guard mode=\"MODERATE\";\n  node Research: lab domain=\"business\";\n  node Strategy: apex analysis=\"strategic\";\n  Guard -> Research -> Strategy;\n  output text report from Strategy;\n}",
    "query": "USER_QUESTION_HERE"
  }'
```

## 可用的V3引擎

| 引擎类型 | 用途 | 主要V3功能 |
|-------------|---------|-----------------|
| `chef` | 食谱制作、食品咨询 | 17个功能模块：食品成本计算、HACCP（食品安全管理体系）、热曲线分析、葡萄酒搭配建议、菜品设计 |
| `molecular` | 分子美食学 | 流变学仪表盘、相图分析、水胶体特性研究、FMEA（故障模式与影响分析） |
| `apex` | 商业策略 | 博弈论、蒙特卡洛模拟（10,000次模拟）、行为经济学、单位经济学、蓝海战略 |
| `consulting` | 战略咨询 | 因果关系分析、约束理论、Wardley矩阵、ADKAR变革管理模型 |
| `marketing` | 市场研究 | 目标市场细分（TAM/SAM/SOM）、波特五力模型、价格弹性分析、病毒式传播系数 |
| `lab` | 科学研究 | 证据评级（A-D等级）、矛盾检测工具、可重复性评估 |
| `oracle` | 预测分析 | 贝叶斯更新算法、黑天鹅事件识别工具、对抗性分析方法 |
| `assembly` | 多智能体辩论 | 12个智能体投票（8/12票需达到多数）、Gandalf VETO机制（决策否决权）、魔鬼代言人角色 |
| `analyst` | 数据分析 | 自动异常检测、统计测试、预测建模 |

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

## 示例：Python集成示例
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

## 使用限制

| 计费等级 | 请求限制 | 认证要求 |
|------|-------|------|
| 免费 | 每小时100次请求 | 无需API密钥 |
| 专业版 | 每小时500次请求 | 需在请求头中添加`X-Aether-Key`字段 |

## 注意事项

- 响应内容采用希腊语（Ελληνικά）格式，并遵循Markdown格式。
- 每个引擎的典型响应时间为30-60秒。
- 多引擎流水线的处理时间较长（各节点依次执行）。
- 所有输出均使用`##`标记来区分不同章节的结构。

## 示例：在Bash中解析响应内容
```bash
curl -s -X POST https://api.neurodoc.app/aetherlang/execute \
  -H "Content-Type: application/json" \
  -d '{"code":"flow Chef {\n  using target \"neuroaether\" version \">=0.2\";\n  input text query;\n  node Chef: chef cuisine=\"auto\";\n  output text recipe from Chef;\n}","query":"Carbonara recipe"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result',{}).get('final_output','No output'))"
```

## 示例：在Python中集成AetherLang V3
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