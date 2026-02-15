---
name: polymarket-latest-events
description: 从 Polymarket 预测市场中获取最新事件。当用户询问有关 Polymarket 的事件、预测市场、热门投注信息，或想要了解 Polymarket 的最新动态时，可以使用此功能。
---

# Polymarket 最新事件

从 Polymarket 预测市场平台获取最新事件。

## 使用场景

当用户有以下需求时，可以使用此功能：
- 询问 Polymarket 的最新事件或市场情况
- 查看热门的预测市场
- 提到 Polymarket、预测市场或投注赔率
- 提出类似“Polymarket 有什么新内容”之类的问题

## 获取方法

使用 `web_fetch`（或通过 Bash 使用 `curl`）调用 Polymarket 的 Gamma API。无需 API 密钥或身份验证。

### 获取最新的 10 个事件

```bash
curl -s "https://gamma-api.polymarket.com/events?active=true&closed=false&limit=10&order=createdAt&ascending=false"
```

或者使用 `web_fetch`：

```bash
web_fetch url="https://gamma-api.polymarket.com/events?active=true&closed=false&limit=10&order=createdAt&ascending=false"
```

### 响应格式

API 返回一个 JSON 数组。每个事件对象包含以下字段：

| 字段 | 描述 |
|-------|-------------|
| title | 事件标题/问题 |
| slug | 事件的 URL 断言 |
| description | 详细描述 |
| startDate | 事件开始日期 |
| createdAt | 事件创建时间 |
| volume | 总交易量 |
| liquidity | 可用流动性 |
| markets | 包含结果和价格的子市场数组 |
| tags | 分类标签 |

### 构建事件链接

每个事件的 Polymarket 链接格式为：

```https://polymarket.com/event/{slug}
```

### 查看市场价格

每个事件都有一个 `markets` 数组。每个子市场包含：
- `question`：具体的问题 |
- `outcomes`：以 ["Yes", "No"] 形式的 JSON 字符串（结果） |
- `outcomePrices`：以 ["0.65", "0.35"] 形式的 JSON 字符串（概率）

## 输出格式

将结果以清晰的列表形式展示：

```
{title} — {简短描述或第一个标签}
   - 赔率：Yes {价格}% / No {价格}%
   - 链接：https://polymarket.com/event/{slug}
```

## 过滤选项

您可以自定义 API 查询：
- 按类别过滤：添加 `&tag_id={id}`（从 `https://gamma-api.polymarket.com/tags?limit=100` 获取标签 ID）
- 按交易量过滤：使用 `&order=volume&ascending=false` 获取交易量最大的事件
- 按运动项目过滤：使用 `https://gamma-api.polymarket.com/sports` 查找联赛，然后通过 `&series_id={id}` 进行过滤
- 获取更多结果：将 `&limit=10` 更改为任意数字
```