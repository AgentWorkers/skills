---
name: camelcamelcamel-alerts
description: 通过 RSS 监控 CamelCamelCamel 的价格下降警报，并在商品打折时发送 Telegram 通知。适用于为 Amazon 产品设置自动价格跟踪功能并使用 CamelCamelCamel 的价格警报系统的情况。
---

# CamelCamelCamel 价格监控提醒

自动监控 CamelCamelCamel 的 RSS 源，以便在亚马逊商品价格下降时通过 Telegram 收到通知。

## 快速入门

1. **获取您的 RSS 源 URL**：
   - 访问 https://camelcamelcamel.com/ 并设置价格提醒
   - 获取您的个人 RSS 源 URL（格式：`https://camelcamelcamel.com/alerts/YOUR_UNIQUE_ID.xml`）

2. **创建一个 cron 任务**，使用您的 RSS 源 URL（请确保使用的是您自己的 URL！）：

```bash
cron add \
  --job '{
    "name": "camelcamelcamel-monitor",
    "schedule": "0 */12 * * *",
    "task": "Monitor CamelCamelCamel price alerts",
    "command": "python3 /path/to/scripts/fetch_rss.py https://camelcamelcamel.com/alerts/YOUR_UNIQUE_ID.xml"
  }'
```

**重要提示**：请将 `YOUR_UNIQUE_ID` 替换为第一步中获得的唯一 ID。每个人都需要自己的 RSS 源 URL！

3. **Clawdbot 将会**：
   - 每 4 小时获取一次您的 RSS 源数据
   - 检测新的价格提醒
   - 通过 Telegram 向您发送通知

## 工作原理

该功能依赖于两个组件：

### `scripts/fetch_rss.py`
- 获取 CamelCamelCamel 的 RSS 源数据
- 解析价格提醒信息
- 与本地缓存进行对比，找出新的提醒
- 输出包含新检测到的信息的 JSON 文件
- 将提醒的哈希值缓存起来，以避免重复通知

### Cron 任务集成
- 按照您设定的时间表运行
- 触发 `fetch_rss.py` 脚本
- 可以配置为每小时、每 4 小时、每天等频率运行

## 设置与配置

请参阅 [SETUP.md](references/SETUP.md) 以了解以下内容：
- 如何获取 CamelCamelCamel 的 RSS 源 URL
- Cron 任务的详细配置步骤
- 自定义检查频率
- 缓存管理
- 故障排除

## 提醒缓存

该脚本在 `/tmp/camelcamelcamel/cache.json` 文件中维护一个缓存，用于记录已接收到的通知，从而避免重复通知。

**清除缓存** 可以重新触发通知：
```bash
rm /tmp/camelcamelcamel/cache.json
```

## 通知格式

当检测到新的价格下降时，您会收到如下格式的 Telegram 消息：

```
🛒 *Price Alert*

*PRODUCT NAME - $XX.XX (Down from $YY.YY)*

Current price: $XX.XX
Historical low: $ZZ.ZZ
Last checked: [timestamp]

View on Amazon: [link]
```

## 自定义设置

### 检查频率

调整 Cron 任务的调度时间（`schedule` 字段中的第六个参数）：
- `0 * * * *` → 每小时
- `0 */4 * * *` → 每 4 小时（默认值）
- `0 */6 * * *` → 每 6 小时
- `0 0 * * *` → 每天

### 消息格式

编辑 `scripts/notify.sh` 文件以自定义 Telegram 消息的格式和表情符号。

## 技术细节

- **编程语言**：Python 3（仅使用内置库）
- **缓存**：`/tmp/camelcamelcamel/cache.json` 文件
- **数据源格式**：标准 RSS/XML 格式
- **依赖项**：除了 Python 标准库外，无需额外依赖
- **每次请求的超时时间**：10 秒

## 故障排除

如果您没有收到通知，请尝试以下步骤：
1. **验证 RSS 源 URL** 是否能在浏览器中正常访问
2. **检查 cron 任务是否已正确设置**：使用 `cron list` 命令查看
3. **手动测试**：尝试手动触发通知
4. **清除缓存** 以重置系统设置
5. **确认 Telegram 已在 Clawdbot 中正确配置**

更多详细信息，请参阅 [SETUP.md](references/SETUP.md)。