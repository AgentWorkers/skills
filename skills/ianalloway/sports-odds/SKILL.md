---
name: sports-odds
description: "获取实时体育博彩赔率，并在多个体育博彩网站之间比较不同的赔率。支持NFL（美国国家橄榄球联盟）、NBA（美国国家篮球联盟）、MLB（美国职业棒球大联盟）、NHL（美国国家冰球联盟）等赛事。"
homepage: https://the-odds-api.com/
metadata:
  {
    "openclaw":
      {
        "emoji": "🏈",
        "requires": { "bins": ["curl", "jq"] },
        "credentials":
          [
            {
              "id": "odds-api-key",
              "name": "The Odds API Key",
              "description": "Free API key from https://the-odds-api.com/",
              "env": "ODDS_API_KEY",
            },
          ],
      },
  }
---
# 体育博彩赔率

使用 The Odds API 从多家体育博彩公司获取实时投注赔率。免费套餐每月包含 500 次请求。

## 设置

1. 在 https://the-odds-api.com/ 获取免费的 API 密钥。
2. 设置环境变量：`export ODDS_API_KEY=your_key_here`

## 可用的体育项目

列出所有可用的体育项目：

```bash
curl -s "https://api.the-odds-api.com/v4/sports?apiKey=$ODDS_API_KEY" | jq '.[] | {key, title, active}'
```

常见的体育项目代码：
- `americanfootball_nfl` - 美国国家橄榄球联盟（NFL）
- `basketball_nba` - 美国职业篮球联赛（NBA）
- `baseball_mlb` - 美国职业棒球大联盟（MLB）
- `icehockey_nhl` - 美国国家冰球联盟（NHL）
- `soccer_epl` - 英格兰足球超级联赛（EPL）
- `soccer_usa_mls` - 美国职业足球大联盟（MLS）

## 获取赔率

获取某项运动的当前赔率（以 NFL 为例）：

```bash
curl -s "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds?apiKey=$ODDS_API_KEY&regions=us&markets=h2h,spreads,totals" | jq '.'
```

### 简洁赔率显示：

```bash
curl -s "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds?apiKey=$ODDS_API_KEY&regions=us&markets=h2h" | jq '.[] | {game: "\(.home_team) vs \(.away_team)", commence: .commence_time, bookmakers: [.bookmakers[] | {name: .title, odds: .markets[0].outcomes}]}'
```

### 比较不同博彩公司的赔率差异：

```bash
curl -s "https://api.the-odds-api.com/v4/sports/basketball_nba/odds?apiKey=$ODDS_API_KEY&regions=us&markets=spreads" | jq '.[] | {matchup: "\(.away_team) @ \(.home_team)", books: [.bookmakers[] | {book: .title, spread: .markets[0].outcomes[0]}]}'
```

## 投注类型

- `h2h` - 正负赔率（直接对决）
- `spreads` - 分差赔率
- `totals` - 总分胜负

## 地区

- `us` - 美国博彩公司（DraftKings、FanDuel、BetMGM 等）
- `uk` - 英国博彩公司
- `eu` - 欧洲博彩公司
- `au` - 澳大利亚博彩公司

## 最佳赔率查找器

查找某场比赛的最佳赔率：

```bash
# Get best moneyline odds
curl -s "https://api.the-odds-api.com/v4/sports/basketball_nba/odds?apiKey=$ODDS_API_KEY&regions=us&markets=h2h" | jq '
  .[] | 
  {
    game: "\(.away_team) @ \(.home_team)",
    best_home: (.bookmakers | map(.markets[0].outcomes[] | select(.name == .home_team)) | max_by(.price)),
    best_away: (.bookmakers | map(.markets[0].outcomes[] | select(.name == .away_team)) | max_by(.price))
  }
'
```

## 检查 API 使用情况

```bash
curl -s "https://api.the-odds-api.com/v4/sports?apiKey=$ODDS_API_KEY" -D - 2>&1 | grep -i "x-requests"
```

页面显示以下信息：`x-requests-used` 和 `x-requests-remaining`（已使用的请求次数和剩余请求次数）

## 提示

- 为节省 API 调用次数，可以缓存响应结果。
- 可使用参数 `oddsFormat=american` 或 `oddsFormat=decimal` 来指定赔率格式。
- 免费套餐每月包含 500 次请求，更多请求需购买付费套餐。