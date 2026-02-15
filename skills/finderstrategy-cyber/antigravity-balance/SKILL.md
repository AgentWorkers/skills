---
name: antigravity-balance
description: 检查 Google Antigravity AI 模型的配额/令牌余额。当用户询问其 Antigravity 的使用情况、剩余令牌数、模型限制、配额状态或速率限制时，可以使用此功能。该功能通过检测本地的 Antigravity 语言服务器进程并查询其 API 来实现。
---

# Antigravity 平衡检查

请查看您的 Antigravity AI 模型配额和令牌余额。

## 快速入门

```bash
# Check quota (auto-detects local Antigravity process)
node scripts/agquota.js

# JSON output for parsing
node scripts/agquota.js --json

# Verbose output (debugging)
node scripts/agquota.js -v
```

## 工作原理

1. **进程检测**：查找正在运行的 `language_server_macos_arm`（或对应平台的进程）。
2. **提取连接信息**：从进程参数中解析 `--extension_server_port` 和 `--csrf_token`。
3. **端口扫描**：扫描附近的端口以找到 HTTPS API 端点（通常是 `extensionPort + 1`）。
4. **查询本地 API**：发送请求到 `https://127.0.0.1:{port}/exa/language_server_pb.LanguageServerService/GetUserStatus`。
5. **显示配额信息**：显示剩余的配额百分比、重置时间以及模型相关信息。

## 输出格式

默认输出包括：
- 用户名称、电子邮件和等级
- 模型名称及剩余配额百分比
- 可视化进度条（颜色编码：绿色 >50%，黄色 >20%，红色 ≤20%）
- 重置倒计时（例如：“4小时32分钟”）

JSON 输出（使用 `--json` 参数）会返回结构化数据：
```json
{
  "user": { "name": "...", "email": "...", "tier": "..." },
  "models": [
    { "label": "Claude Sonnet 4.5", "remainingPercent": 80, "resetTime": "..." }
  ],
  "timestamp": "2026-01-28T01:00:00.000Z"
}
```

## 系统要求

- 需要安装 Node.js（使用内置的 `https` 模块）。
- Antigravity（或 Windsurf）必须正在运行。

## 故障排除

如果脚本失败，请尝试以下步骤：
1. 确保 Antigravity/Windsurf 正在运行。
2. 检查 `language_server` 进程是否存在：`ps aux | grep language_server`。
3. 该进程的参数中必须包含 `--app_data_dir antigravity`（以区分其他 Codeium 分支版本）。

## 不同平台的进程名称

| 平台 | 进程名称 |
|----------|--------------|
| macOS (ARM) | `language_server_macos_arm` |
| macOS (Intel) | `language_server_macos` |
| Linux | `language_server_linux` |
| Windows | `language_server_windows_x64.exe` |