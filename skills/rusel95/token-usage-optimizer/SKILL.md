---
name: token-usage-optimizer
version: 1.0.5
description: 通过智能的使用监控和成本优化策略，最大限度地提升您的 Claude Code 订阅价值。您可以追踪每 5 小时的使用情况以及每周的用量上限，接收一次性提醒，并查看每日报告，了解自己是否在使用每月 20 美元至 200 美元套餐范围内的资源。该工具具有超轻量级的设计（仅使用 10 分钟的缓存，且 API 调用次数极少），非常适合 Pro、Max 100 和 Max 200 订阅者使用——帮助您充分利用每一分钱订阅费用。
metadata:
  clawdbot:
    emoji: "📊"
    os:
      - darwin
      - linux
    requires:
      bins:
        - curl
        - date
        - grep
---
# 令牌使用优化器

**版本：** 1.0.5

通过实时监控使用情况并优化您的每日消耗速率，充分利用您的 Claude Code 订阅服务。

## 为什么使用这个工具？

您每月为 Claude Code 支付 20 至 200 美元。您是否：
- ✅ 充分利用了它的所有功能？
- ❌ 过早达到了使用限制？
- ❌ 在订阅重置时仍有未使用的配额？

该工具会跟踪您的 **5 小时会话** 和 **每周 7 天** 的使用配额，计算您的 **每日消耗速率**，并告诉您是否应该增加使用量或减少使用。

## 主要功能

- 📊 **消耗速率跟踪** — 您的使用情况是否低于、高于或符合最佳使用标准？
- ⚡ **智能提醒** — 当会话时间超过 50% 时发送一次性警告（无垃圾信息）
- 🎯 **计划感知** — 自动检测您使用的计划（Pro：20 美元；Max 100 美元；Max 200 美元）
- 💾 **超轻量级** — 10 分钟缓存，极少调用 API
- 📅 **每日报告** — 晚间总结：会话时间、每周使用情况、消耗速率
- 🔄 **令牌健康检查** — 每小时检查一次；如需手动刷新则发出警报（大约每周一次）

## 快速开始

### 1. 设置

运行设置向导来配置您的 OAuth 令牌：

```bash
cd {baseDir}
./scripts/setup.sh
```

您需要以下信息：
- **访问令牌** (`sk-ant-oat01-...`)
- **刷新令牌** (`sk-ant-ort01-...`)

请参阅 `references/token-extraction.md` 以获取这些令牌的获取方法。

### 2. 检查使用情况

```bash
./scripts/check-usage.sh
```

输出：
```
SESSION=22.0
WEEKLY=49.0
BURN_RATE=OK
CACHED_AT=1771583780
```

### 3. 人类可读的报告

```bash
./scripts/report.sh
```

输出：
```
📊 Claude Code Daily Check:

⏱️  SESSION (5h): 22%
📅 WEEKLY (7d): 49%

⚪ На темпі — оптимальне використання
```

## 消耗速率解读

- **🟢 使用不足** — 您的订阅使用量不足。请增加使用量以获得更高的性价比！
- **⚪ 合适** — 使用情况符合您的计划要求。
- **🔴 使用过量** — 您可能会在订阅重置前达到使用限制。

## 按计划划分的每日预算

| 计划 | 每月费用 | 每周预算 | 每日预算 |
|------|---------|---------------|--------------|
| Pro | $20 | 约 14% | 约 2% |
| Max 100 | $100 | 约 14% | 约 2% |
| Max 200 | $200 | 约 14% | 约 2% |

*（7 天的周期每周重置一次，因此每天约 14% 的使用量等于每周 100% 的使用量）*

## 与 Heartbeat 的集成

将以下代码添加到您的 `HEARTBEAT.md` 文件中：

```markdown
### Evening Check (18:00-20:00)
- Claude Code usage: `/path/to/token-usage-optimizer/scripts/report.sh`
```

## 警报阈值

- **会话时间超过 50%** → 发送一次性警告（直到下一次订阅重置前不会重复）
- **每周使用量超过 80%** → 发送一次性警告

警报系统使用状态跟踪（`/tmp/claude-usage-alert-state`）来避免发送垃圾信息。

## 缓存

默认缓存位置：`/tmp/claude-usage.cache`，缓存有效期为 10 分钟。

如需自定义缓存设置，请修改以下代码：
```bash
CACHE_FILE=/custom/path CACHE_TTL=300 ./scripts/check-usage.sh
```

## 相关文件

- `scripts/setup.sh` — 初始令牌配置脚本
- `scripts/check-usage.sh` — 核心使用情况检查脚本（包含消耗速率计算）
- `scripts/report.sh** — 人类可读的每日报告脚本
- `references/api-endpoint.md` — Anthropic OAuth API 文档
- `references/token-extraction.md` — OAuth 令牌获取方法
- `references/plans.md` — Claude Code 订阅计划说明

## API 端点

```
GET https://api.anthropic.com/api/oauth/usage
Authorization: Bearer <access-token>
anthropic-beta: oauth-2025-04-20
```

API 响应：
```json
{
  "five_hour": {
    "utilization": 22.0,
    "resets_at": "2026-02-20T14:00:00.364238+00:00"
  },
  "seven_day": {
    "utilization": 49.0,
    "resets_at": "2026-02-24T10:00:01.364256+00:00"
  }
}
```

## 所需工具

- `curl` — 用于发送 API 请求
- `date` — 用于时间戳解析
- `grep`, `cut`, `printf` — 用于文本处理

无需依赖其他外部工具（如 jq）。

## 隐私政策

令牌存储在 `{baseDir}/.tokens` 文件夹中（Git 会忽略该文件夹）。

请勿分享您的访问令牌或刷新令牌。

## 令牌健康检查（推荐）

OAuth 令牌的有效期约为 1 周，之后需要手动刷新。建议设置每 30 分钟进行一次健康检查以提高可靠性：

```bash
# Add cron job to check token health every 30 minutes
openclaw cron add \
  --name "claude-token-refresh" \
  --every 30m \
  --announce \
  --message "Запусти {baseDir}/scripts/auto-refresh-cron.sh"
```

**功能说明：**
- ✅ 令牌有效 → 不会发送任何警报。
- 🔴 令牌过期 → 发送一次性警告，并提供手动刷新说明。

**手动刷新步骤（每周一次，耗时约 30 秒）：**
```bash
claude auth login
# Browser opens → sign in to claude.ai → done!
```

成功登录后，令牌会自动同步到 `{baseDir}/.tokens` 文件夹中。

## 故障排除

- **“未配置令牌”** → 运行 `./scripts/setup.sh` 进行配置。
- **“令牌过期” / “API 请求失败”** → OAuth 令牌通常在 1 周后过期。请手动刷新令牌：通过浏览器登录 Claude 系统。
- **消耗速率显示为空** → 可能是 API 响应中缺少 `resets_at` 字段，请稍后再试。
- **自动刷新失败** → 可能是 OAuth 刷新端点发生了变化。请手动刷新令牌：登录 Claude 系统，然后复制新的令牌并运行 `./scripts/setup.sh`。

## 更新日志

### v1.0.5 (2026-02-22)
- 🐛 **修复问题：** 修复了 `auto-refresh-cron.sh` 脚本中的引号处理问题。
- ⚡ **性能提升：** 将 cron 任务间隔从 1 小时改为 30 分钟，以更可靠地刷新令牌。
- 📝 提高了与 `~/.claude/.credentials.json` 文件同步 OAuth 令牌的可靠性。

### v1.0.4 (2026-02-21)
- 🔄 将自动刷新机制替换为健康检查 + 手动刷新的工作流程。
- 📚 更新了文档，添加了手动刷新的详细说明。
- ⏰ 当需要手动刷新令牌时，系统会发出警报（大约每周一次）。

### v1.0.3 (2026-02-20)
- 🏱️ 将自动刷新间隔从 5 小时改为 30 分钟。
- 📊 提高了消耗速率计算的准确性。

## 贡献建议

发现漏洞或有功能需求？
- 请在 ClawHub 上提交问题：https://clawhub.ai/friday/token-usage-optimizer

## 许可证

MIT 许可证