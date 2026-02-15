---
name: ultrahuman-openclaw
description: 使用 Ultrahuman MCP 服务器（通过 mcporter）从 OpenClaw 中获取并汇总 Ultrahuman Ring/CGM 的各项指标。当用户询问有关 Ultrahuman 的数据（如睡眠评分、总睡眠时间、睡眠阶段、心率/心率变异性/平均心率、步数、恢复指数、活动指数、最大摄氧量）或需要每日/每周的 Ultrahuman 摘要时，可使用此功能。
---

# Ultrahuman (OpenClaw)

通过 **Ultrahuman MCP** 和 **mcporter** 获取 Ultrahuman 的各项指标，然后对这些指标进行汇总。

## 设置（一次性操作）

您需要以下内容：

1) **Ultrahuman 开发者/合作伙伴凭证**

您需要从 Ultrahuman 开发者门户获取个人认证令牌：
- https://vision.ultrahuman.com/developer

接下来，请设置以下参数：
- `ULTRAHUMAN_USER_EMAIL`
- `ULTRAHUMAN_AUTH_TOKEN`（您的个人令牌）
- （如果提供或需要的话，还需在 Ultrahuman 应用中设置您的合作伙伴 ID）

2) **Ultrahuman MCP 服务器**

仓库地址：
- https://github.com/Monasterolo21/Ultrahuman-MCP

构建该服务器（示例命令）：
- `bun install && bun run build`
- 构建完成后，您应该会得到一个名为 `dist/main.js` 的入口文件。

3) **mcporter 配置文件**，用于定义名为 `ultrahuman` 的 MCP 服务器

示例 `config/mcporter.json` 文件（请将路径替换为您实际构建后的 `main.js` 文件的路径）：

```json
{
  "mcpServers": {
    "ultrahuman": {
      "transport": "stdio",
      "command": "node",
      "args": ["/absolute/path/to/Ultrahuman-MCP/dist/main.js"],
      "env": {
        "ULTRAHUMAN_AUTH_TOKEN": "${ULTRAHUMAN_AUTH_TOKEN}",
        "ULTRAHUMAN_USER_EMAIL": "${ULTRAHUMAN_USER_EMAIL}"
      }
    }
  }
}
```

## 快速入门

### 日度汇总（推荐）

在您的 OpenClaw 工作空间中（确保 `./config/mcporter.json` 文件存在）：

```bash
cd /path/to/your/openclaw/workspace
python3 skills/local/ultrahuman-openclaw/scripts/ultrahuman_summary.py --yesterday
```

特定日期的汇总数据：

```bash
python3 skills/local/ultrahuman-openclaw/scripts/ultrahuman_summary.py --date YYYY-MM-DD
```

如果您的 `mcporter` 配置文件不在 `./config/mcporter.json` 中，请显式指定其路径：

```bash
python3 skills/local/ultrahuman-openclaw/scripts/ultrahuman_summary.py \
  --date YYYY-MM-DD \
  --mcporter-config /path/to/mcporter.json
```

### 原始 JSON 数据

```bash
mcporter --config /path/to/mcporter.json \
  call ultrahuman.ultrahuman_metrics date=YYYY-MM-DD --output json
```

## 需要报告的指标（默认设置）

除非另有要求，否则请保持汇总信息的简洁性：

- 睡眠质量评分、总睡眠时间、睡眠效率、恢复性睡眠时间、深度睡眠/REM 睡眠时间
- 步数总数
- 恢复指数、活动指数、活跃时间
- 最大摄氧量（VO2 max）、睡眠心率变异性（sleep HRV）、静息心率（RHR）

如果睡眠质量评分或总睡眠时间处于“需要关注”的状态，请务必特别指出。