---
name: telegram-usage
description: 显示会话使用统计信息（配额、会话时长、令牌、上下文）
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["node"]}}}
---

# Telegram 使用统计

通过运行处理脚本，可以显示全面的会话使用统计信息。

## 功能说明

该脚本会显示以下内容的快速状态信息：
- **剩余配额**：剩余的 API 配额百分比，并配有可视化指示器
- **重置计时器**：距离配额重置还剩的时间

## 使用方法

当用户请求使用统计信息、配额详情或会话数据时，执行以下代码：

```bash
node /home/drew-server/clawd/skills/telegram-usage/handler.js
```

该脚本会生成符合 Telegram 的解析模式（parseMode）的格式化 HTML 响应。

## 输出格式

响应内容以清晰的 Telegram 消息形式呈现，包括：
- 标题（加粗显示）
- 明确的百分比和剩余时间
- 可视化指示器（使用表情符号）
- 所有信息都包含在同一条消息中，便于快速查看

## 示例输出

```
📊 API Usage

🔋 Quota: 🟢 47%
⏱️ Resets in: 53m
```

## 注意事项

- 该脚本从 `clawdbot models status` 中获取实时数据
- 每次调用时都会更新当前的 API 配额值
- 为确保与 Telegram 兼容，采用纯文本格式进行输出