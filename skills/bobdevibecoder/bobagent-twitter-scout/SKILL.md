---
name: twitter-scout
description: 使用 Grok AI 实时浏览和分析 Twitter/X 平台的内容。可以发现热门话题、病毒式传播的帖子、加密货币领域的最新动态以及科技新闻等有用信息。当需要执行以下操作时，可以调用该工具：检查 Twitter 上的内容、查找与特定主题相关的推文、了解 X 平台上的热门趋势、在 Twitter 上搜索特定信息，或进行任何与 Twitter/X 相关的研究工作。
---

# Twitter Scout（基于Grok技术）

利用Grok AI对Twitter和X平台的数据进行实时智能分析。

## 使用场景

- “Twitter上当前的热门话题是什么？”
- “查找关于[主题]的推文”
- “在Twitter上搜索与加密货币相关的信息”
- “人们对于[公司/代币]有什么看法？”
- “查找关于[主题]的病毒式传播的内容”
- “分析Twitter上对[主题]的舆论倾向”
- “在X平台上寻找潜在的机会”

## 工作原理

该工具基于Grok AI，后者具备对Twitter和X平台的**原生实时访问权限**。与其他无法直接访问Twitter数据的AI模型不同，Grok能够：
- 实时查看推文和话题讨论
- 分析热门话题
- 识别病毒式传播的内容
- 跟踪任何主题的舆论趋势
- 发现突发新闻

## 使用方法

```bash
# Search for tweets on a topic
python3 scripts/twitter_scout.py search "bitcoin ETF"

# Get trending topics
python3 scripts/twitter_scout.py trending

# Analyze sentiment
python3 scripts/twitter_scout.py sentiment "ethereum"

# Find alpha/opportunities
python3 scripts/twitter_scout.py alpha "crypto"

# Get viral posts
python3 scripts/twitter_scout.py viral "AI agents"
```

## 环境要求

需要设置`GROK_API_KEY`环境变量。

## 输出格式

返回结构化的JSON数据，包含以下内容：
- `tweets`：相关推文的数组
- `sentiment`：整体舆论分析结果
- `trending`：相关热门话题
- `summary`：AI生成的发现总结
- `opportunities`：发现的潜在机会

## 示例

**查找与加密货币相关的信息：**
```
twitter_scout.py alpha "solana memecoins"
```

**交易前分析舆论倾向：**
```
twitter_scout.py sentiment "NVIDIA stock"
```

**研究某个项目：**
```
twitter_scout.py search "OpenClaw AI agent"
```

## 使用限制

Grok免费 tier：每天约25次请求
Grok付费 tier：提供更高的请求次数限制

## 使用建议

- 使用具体的搜索词以获得更准确的结果
- 适用于市场研究、趋势发现和舆论分析
- 可与其他工具结合使用，形成完整的研究流程
- 非常适合在相关内容流行之前捕捉到早期信号