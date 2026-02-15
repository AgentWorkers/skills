---
name: manifold
description: 在 Manifold Markets 上进行阅读和交易（搜索市场、获取概率信息、查看用户/投注记录、下注/出售/发表评论）。未经用户明确确认，切勿进行任何下注、出售或评论操作。
homepage: https://manifold.markets
metadata:
  {
    "openclaw":
      {
        "emoji": "🔮",
        "requires": { "bins": ["curl"], "env": ["MANIFOLD_API_KEY"] },
        "primaryEnv": "MANIFOLD_API_KEY",
      },
  }
---

# Manifold Markets

使用此技能可以读取Manifold Markets的数据（搜索市场、获取概率信息、查看用户公开信息），以及进行需要用户明确确认的交易或评论操作。

执行相关操作需要`MANIFOLD_API_KEY`（该密钥可以在环境中设置，或通过OpenClaw技能配置文件进行配置）。

基础URL：`https://api.manifold.markets/v0`

文档链接：https://docs.manifold.markets/api

## 读取操作

### 搜索市场

```bash
curl -s "https://api.manifold.markets/v0/search-markets?term=AI+safety&limit=5"
```

提示：请将空格替换为`+`（或使用URL编码）。如果使用`jq`工具，可以按以下格式化搜索结果：

```bash
curl -s "https://api.manifold.markets/v0/search-markets?term=AI+safety&limit=5" | jq '.[] | {id, slug, question, outcomeType, probability, createdTime, creatorUsername}'
```

### 列出最新市场

```bash
curl -s "https://api.manifold.markets/v0/markets?limit=10"
```

使用`jq`工具时：

```bash
curl -s "https://api.manifold.markets/v0/markets?limit=10" | jq '.[] | {id, slug, question, outcomeType, probability, closeTime}'
```

### 获取市场详情（通过市场ID）

```bash
curl -s "https://api.manifold.markets/v0/market/MARKET_ID"
```

二元市场通常会提供一个`probability`字段（值范围为0到1）。其他类型的市场可能没有这个字段。

### 获取市场详情（通过市场slug）

市场slug是指Manifold URL中用户名之后的部分（例如：`.../Alice/my-market-slug` → `my-market-slug`）。

```bash
curl -s "https://api.manifold.markets/v0/slug/MARKET_SLUG"
```

### 查看用户信息（通过用户名）

```bash
curl -s "https://api.manifold.markets/v0/user/USERNAME"
```

### 列出用户的投注记录

如果使用`jq`工具：

```bash
USER_ID="$(curl -s "https://api.manifold.markets/v0/user/USERNAME" | jq -r '.id')"
curl -s "https://api.manifold.markets/v0/bets?userId=$USER_ID&limit=50"
```

如果不使用`jq`，则需要先获取用户的JSON数据并读取`id`字段，然后再进行后续操作：

```bash
curl -s "https://api.manifold.markets/v0/user/USERNAME"
curl -s "https://api.manifold.markets/v0/bets?userId=USER_ID&limit=50"
```

## 安全规则

- 除非用户明确表示同意（例如：“是的，进行操作”、“确认”等），否则严禁进行任何交易、出售股份或发布评论。
- 在执行任何操作前，务必先获取市场相关信息，并再次确认以下内容：市场名称、市场ID/slug、操作类型（投注/出售/评论）、方向/答案、交易金额/股份数量以及任何限制条件。
- 如果用户未明确指定交易金额或方向，请立即停止操作并询问用户。

## 写入操作

### 认证

- 在请求头中添加`MANIFOLD_API_KEY`：`Authorization: Key $MANIFOLD_API_KEY`
- 请确保`MANIFOLD_API_KEY`已在`~/.openclaw/openclaw.json`文件中配置。

### 进行投注（二元市场）

1. 先获取市场信息，并确认目标市场无误：

```bash
curl -s "https://api.manifold.markets/v0/market/MARKET_ID"
```

2. 预览你打算发送的请求数据（在用户确认之前不要发送POST请求）：

```bash
cat <<'JSON'
{"amount":10,"contractId":"MARKET_ID","outcome":"YES"}
JSON
```

3. 在用户明确确认后，执行投注操作：

```bash
curl -s -X POST "https://api.manifold.markets/v0/bet" \
  -H "Authorization: Key $MANIFOLD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount":10,"contractId":"MARKET_ID","outcome":"YES"}'
```

注意事项：
- `amount`参数以“Mana”为单位（整数）。
- 对于二元市场，`outcome`参数的值为`YES`或`NO`。
- 对于非二元市场，请参考Manifold API文档以获取正确的请求数据格式。

### 出售股份

- 在执行出售操作前，请先预览相关信息（在用户确认之前不要发送请求）。
- 要出售所有股份，请省略`shares`参数：
   ```bash
curl -s -X POST "https://api.manifold.markets/v0/market/MARKET_ID/sell" \
  -H "Authorization: Key $MANIFOLD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"outcome":"YES"}'
```

- 要出售特定数量的股份，请使用以下格式：
   ```bash
curl -s -X POST "https://api.manifold.markets/v0/market/MARKET_ID/sell" \
  -H "Authorization: Key $MANIFOLD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"outcome":"YES","shares":10}'
```

### 发布评论

通过API发布的评论可能会产生费用（详情请参考Manifold API文档）。在发布评论前，请务必确认评论内容及目标市场信息。

```bash
curl -s -X POST "https://api.manifold.markets/v0/comment" \
  -H "Authorization: Key $MANIFOLD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contractId":"MARKET_ID","content":"Your comment here."}'
```

## 其他注意事项

- 请注意存在请求速率限制（详情请参考Manifold API文档）。
- 根据当前平台规则，某些私有或未公开的市场可能无法通过公共API访问。