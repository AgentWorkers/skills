---
name: website-monitor
description: 轻量级网站运行时间监控工具：用于检查URL是否可用、测量响应时间、通过哈希算法检测内容变化，并验证网站显示的内容是否符合预期。该工具完全不依赖任何外部库或服务。
triggers:
  - check website
  - is site up
  - monitor url
  - website status
  - uptime check
  - ping website
---
# 网站监控工具

这是一个完全依赖 Python 标准库（urllib）实现的工具，用于检查网站是否可用、测量响应时间以及检测内容变化。无需使用 requests、aiohttp 或任何外部包。

## 主要功能

- **网站运行状态检查**：验证任意 URL 是否返回预期的 HTTP 状态码。
- **响应时间测量**：对每个请求进行精确到毫秒的计时。
- **内容变化检测**：通过 SHA-256 哈希算法检测页面内容在两次检查之间的变化。
- **文本验证**：确认响应正文中是否包含指定的文本。
- **支持多个 URL**：可以通过一个命令同时检查多个网站。
- **JSON 输出**：以机器可读的格式输出结果，便于与其他工具或仪表板集成。
- **退出码**：如果有任何网站无法访问，工具会返回退出码 1，非常适合用于 shell 脚本和 cron 作业。

## 使用示例

- **简单的运行状态检查**：
  ```bash
  python website_monitor.py example.com
  ```

- **同时检查多个网站**：
  ```bash
  python website_monitor.py example.com example2.com
  ```

- **检测内容变化**（与之前的哈希值进行比较）：
  ```bash
  python website_monitor.py example.com --hash-check "previous_hash"
  ```

- **验证页面是否包含指定文本**：
  ```bash
  python website_monitor.py example.com --contains "expected_text"
  ```

- **期望特定的 HTTP 状态码（例如重定向）**：
  ```bash
  python website_monitor.py example.com --expect 301
  ```

- **以 JSON 格式输出结果，便于脚本使用**：
  ```bash
  python website_monitor.py example.com --json
  ```

- **在 cron 作业或脚本中使用**：
  ```bash
  crontab -e
  * * * * /path/to/website_monitor.py
  ```

## 命令行参数

- `urls` — 需要检查的一个或多个 URL（如果缺少协议前缀 `https://`，会自动添加）。
- `--timeout N` — 请求超时时间（以秒为单位，默认值：10 秒）。
- `--expect N` — 期望的 HTTP 状态码（默认值：200）。
- `--contains TEXT` — 验证响应正文中是否包含指定的字符串。
- `--hash-check HASH` — 用于检测内容变化的之前内容哈希值。
- `--json` — 以 JSON 数组格式输出结果。

## 退出码

- `0` — 所有网站均正常运行且符合预期。
- `1` — 有一个或多个网站无法访问或检查失败。