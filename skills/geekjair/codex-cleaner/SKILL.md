---
name: codex-cleaner
description: 监控并清理来自 CPA（Codex Provider Agent）的无效认证文件。系统会检查配额使用情况，禁用存在 401 错误的文件，并在删除前进行双重验证。当用户提及“清理认证文件”、“清理无效文件”或需要管理认证文件时，请使用此功能。
---
# Codex Auth File Cleaner

该工具通过 CPA（Codex Authentication Provider）管理 API 来清理无效的 Codex 认证文件。完全依赖 Python 标准库，无需额外依赖任何第三方库。

## 首次运行

运行设置向导以配置 CPA 的 URL 和管理员密钥：

```bash
python3 scripts/codex_cleaner.py setup
```

配置信息将保存到 `config.json` 文件中（该文件会自动生成，并被 Git 忽略）。配置的优先级顺序为：命令行参数 > 环境变量（`CPA_URL`/`CPA_KEY`）> `config.json`。

## 命令

```bash
# View status
python3 scripts/codex_cleaner.py status
python3 scripts/codex_cleaner.py status --json

# Check active files, disable 401s
python3 scripts/codex_cleaner.py check

# Double-verify disabled files, then delete confirmed 401s
python3 scripts/codex_cleaner.py delete

# Full clean (check + delete), output human-readable report
python3 scripts/codex_cleaner.py clean --report

# Full clean, output JSON
python3 scripts/codex_cleaner.py clean --json

# Loop mode (default 300s interval)
python3 scripts/codex_cleaner.py monitor -i 300
```

## 工作流程

```
clean = check + delete

check:  fetch active codex files → concurrent quota check → disable 401s
delete: fetch disabled files → verify#1 (401?) → wait 2s → verify#2 (still 401?) → delete
```

采用双重验证机制，以防止误删除暂时出现故障的文件。

## 与 Nanobot 的集成

为了实现定期监控，可以通过 HEARTBEAT 或 cron 任务运行 `clean --report` 命令，然后将输出结果通过 `message` 工具发送给用户。

示例：
```bash
cd ~/.nanobot/workspace/skills/codex-cleaner && python3 scripts/codex_cleaner.py clean --report
```

## 报告格式

```
🧹 Codex 认证清理报告
⏰ 2026-02-26 13:50:00

📊 清理前
  总计: 100 | 可用: 85 | 已禁用: 15

🔍 检查阶段
  检测: 85 | 失效(401): 3 | 已禁用: 3

🗑️ 删除阶段
  待删: 18 | 验证通过: 15 | 已删除: 15 | 跳过: 3

📊 清理后
  总计: 85 | ✅可用: 82 | ⛔已禁用: 3

⚡ 本次清理: 禁用 3 + 删除 15 = 18 个无效文件
```

## 配置文件

`config.json` 文件由设置向导自动生成：

```json
{
  "cpa_url": "http://YOUR_CPA_HOST:PORT",
  "cpa_key": "YOUR_ADMIN_KEY",
  "concurrency": 20,
  "monitor_interval": 300,
  "notify": {
    "enabled": true,
    "channel": "telegram",
    "chat_id": "YOUR_CHAT_ID"
  }
}
```