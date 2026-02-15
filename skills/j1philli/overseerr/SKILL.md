---
name: overseerr
description: 通过 Overseerr API 请求电影/电视剧并监控请求状态（使用的是稳定的 Overseerr 版本，而非测试版的 Seerr 重写版本）。
homepage: https://overseerr.dev/
metadata: {"clawdbot":{"emoji":"🍿","requires":{"bins":["node"],"env":["OVERSEERR_URL","OVERSEERR_API_KEY"]},"primaryEnv":"OVERSEERR_API_KEY"}}
---

# Overseerr

用于与本地或自托管的Overseerr实例进行交互（包括搜索、请求和状态查询）。

**注意：** 本技能适用于当前的稳定版本**Overseerr**，而非仍处于测试阶段的“Seerr”重写版本。

## 设置

建议通过Clawdbot配置文件来设置环境变量：

- `OVERSEERR_URL`（示例：`http://localhost:5055`）
- `OVERSEERR_API_KEY`（在“设置” → “常规” → “API密钥”中设置）

## 搜索

```bash
node {baseDir}/scripts/search.mjs "the matrix"
node {baseDir}/scripts/search.mjs "bluey" --type tv
node {baseDir}/scripts/search.mjs "dune" --limit 5
```

## 请求

```bash
# movie
node {baseDir}/scripts/request.mjs "Dune" --type movie

# tv (optionally all seasons, default)
node {baseDir}/scripts/request.mjs "Bluey" --type tv --seasons all

# request specific seasons
node {baseDir}/scripts/request.mjs "Severance" --type tv --seasons 1,2

# 4K request
node {baseDir}/scripts/request.mjs "Oppenheimer" --type movie --is4k
```

## 状态查询

```bash
node {baseDir}/scripts/requests.mjs --filter pending
node {baseDir}/scripts/requests.mjs --filter processing --limit 20
node {baseDir}/scripts/request-by-id.mjs 123
```

## 监控（轮询）

```bash
node {baseDir}/scripts/monitor.mjs --interval 30 --filter pending
```

**注意事项：**
- 本技能使用`X-Api-Key`进行身份验证。
- Overseerr也可以通过Webhook推送更新；轮询是一种基本的监控方式。