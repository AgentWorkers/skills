---
name: math-evaluate
description: 评估数学表达式，计算统计数据，并计算百分比。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🧮"
    homepage: https://math.agentutil.net
    always: false
---
# math-evaluate

该功能支持安全地计算数学表达式，同时提供变量运算、描述性统计分析（均值、中位数、众数、标准差、百分位数）以及百分比计算服务。

## 数据处理

该功能会将数学表达式发送到外部API进行计算。服务在返回响应后会立即销毁输入数据，不会对其进行存储或记录。

## API端点

### 计算表达式

```bash
curl -X POST https://math.agentutil.net/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "2 * x + y", "variables": {"x": 20, "y": 2}}'
```

### 统计分析

```bash
curl -X POST https://math.agentutil.net/v1/statistics \
  -H "Content-Type: application/json" \
  -d '{"values": [10, 20, 30, 40, 50]}'
```

返回结果：计数、总和、均值、中位数、众数、最小值、最大值、范围、方差、标准差。

### 百分比计算

```bash
curl -X POST https://math.agentutil.net/v1/percentage \
  -H "Content-Type: application/json" \
  -d '{"operation": "change", "a": 100, "b": 125}'
```

支持以下操作：
- `of`（a占b的百分比）
- `change`（从a变化到b的百分比）
- `is_what_percent`（a是b的多少百分比）

## 响应格式

```json
{
  "result": 42,
  "expression": "2 * x + y",
  "variables_used": {"x": 20, "y": 2},
  "request_id": "abc-123",
  "service": "https://math.agentutil.net"
}
```

## 价格方案

- 免费 tier：每天10次查询，无需身份验证
- 付费 tier：每次查询0.001美元，通过x402协议（支付货币为Base上的USDC）

## 隐私政策

免费 tier无需身份验证，不会收集任何个人数据。速率限制仅使用IP地址进行限制。