---
name: the-sports-db
description: 通过 TheSportsDB 访问体育数据（包括球队、赛事和比分信息）。
metadata: {"clawdbot":{"emoji":"🏟️","requires":{"env":["THE_SPORTS_DB_KEY"]}}}
---

# TheSportsDB

这是一个免费的体育数据库。

## 配置
请确保 `THE_SPORTS_DB_KEY` 已经在 `~/.clawdbot/.env` 文件中设置。（默认的测试密钥通常是 `123` 或 `3`）。

## 使用方法

### 搜索球队信息
```bash
curl -s "https://www.thesportsdb.com/api/v1/json/$THE_SPORTS_DB_KEY/searchteams.php?t=Palmeiras"
```

### 最近的比赛结果（比分）
获取某个球队 ID 的最近 5 场比赛结果：
```bash
curl -s "https://www.thesportsdb.com/api/v1/json/$THE_SPORTS_DB_KEY/eventslast.php?id=134465"
```

### 下一场赛事（赛程）
获取某个球队 ID 的下一场赛事信息：
```bash
curl -s "https://www.thesportsdb.com/api/v1/json/$THE_SPORTS_DB_KEY/eventsnext.php?id=134465"
```

**注意：** 每分钟的请求次数限制为 30 次。