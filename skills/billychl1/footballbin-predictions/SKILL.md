---
name: footballbin-predictions
description: 获取英超联赛和欧冠联赛的AI驱动的比赛预测结果，包括比分、下一粒进球以及角球信息。
homepage: https://apps.apple.com/app/footballbin/id6757111871
metadata: {"clawdbot":{"emoji":"⚽","requires":{"bins":["curl","jq"]},"files":["scripts/*"]}}
---
# FootballBin 比赛预测

通过 FootballBin MCP API，您可以获取英超联赛（Premier League）和欧冠联赛（Champions League）比赛的 AI 预测结果。

## 使用方法

运行 `scripts/footballbin.sh` 并使用以下命令：

### 获取当前比赛周的预测结果
```
scripts/footballbin.sh predictions premier_league
scripts/footballbin.sh predictions champions_league
```

### 获取特定比赛周的预测结果
```
scripts/footballbin.sh predictions premier_league 27
```

### 按球队筛选预测结果
```
scripts/footballbin.sh predictions premier_league --home arsenal
scripts/footballbin.sh predictions premier_league --away liverpool
scripts/footballbin.sh predictions premier_league --home chelsea --away wolves
```

### 列出可用的工具
```
scripts/footballbin.sh tools
```

## 支持的联赛

| 输入参数 | 联赛名称 |
|---------|-----------|
| `premier_league`, `epl`, `pl`, `prem` | 英超联赛 |
| `champions_league`, `ucl`, `cl` | 欧冠联赛 |

## 支持的球队别名

常用的球队别名为：
- `united`（曼彻斯特联队）
- `city`（曼彻斯特城队）
- `spurs`（托特纳姆热刺队）
- `wolves`（沃尔夫汉普顿流浪者队）
- `gunners`（阿森纳队）
- `reds`（利物浦队）
- `blues`（切尔西队）
- `villa`（阿斯顿维拉队）
- `forest`（诺丁汉森林队）
- `palace`（水晶宫队）
- `barca`（巴塞罗那队）
- `real`（皇家马德里队）
- `bayern`（拜仁慕尼黑队）
- `psg`（巴黎圣日耳曼队）
- `juve`（尤文图斯队）
- `inter`（国际米兰队）
- `bvb`（多特蒙德队）
- `atleti`（马德里竞技队）

## 响应数据

每场比赛的预测结果包括：
- **上半场比分**（例如：“1:0”）
- **全场比分**（例如：“2:1”）
- **下一个进球者**（例如：“主队，萨拉赫”）
- **角球次数**（例如：“7:4”）
- **基于球员表现的关键球员推荐”

## 外部接口

| URL | 发送的数据 | 用途 |
|--------|------------------|--------|
| `https://ru7m5svay1.execute-api.eu-central-1.amazonaws.com/prod/mcp` | 联赛名称、比赛周、球队筛选条件 | 获取比赛预测结果 |

## 安全性与隐私

- 无需 API 密钥（公共接口，具有速率限制）
- 不会收集或存储用户数据
- 仅支持读取预测数据
- 不需要任何秘密信息或环境变量

## 链接

- iOS 应用程序：https://apps.apple.com/app/footballbin/id6757111871
- Android 应用程序：https://play.google.com/store/apps/details?id=com.achan.footballbinandroid