---
name: codex-quota
version: 1.2.1
homepage: https://github.com/odrobnik/codex-quota-skill
description: >
  Check OpenAI Codex CLI rate limit status (daily/weekly quotas) using local
  session logs. Portable Python script.

  Reads ~/.codex/sessions/ for quota data.
  When using --all --yes, it temporarily switches accounts by overwriting
  ~/.codex/auth.json (restored afterwards) to query each account.

  Uses the `codex` CLI for --fresh / --all.
metadata:
  openclaw:
    requires:
      bins: ["python3", "codex"]
---

# 技能：codex-quota  
用于检查 OpenAI Codex CLI 的速率限制状态。

## 快速参考  
```bash
# Run the included Python script
./codex-quota.py

# Or if installed to PATH
codex-quota
```

## 选项  
```bash
codex-quota              # Show current quota (cached from latest session)
codex-quota --fresh      # Ping Codex first for live data
codex-quota --all --yes  # Update all accounts, save to /tmp/codex-quota-all.json
codex-quota --json       # Output as JSON
codex-quota --help       # Show help
```

## 设置  
有关先决条件和设置说明，请参阅 [SETUP.md](SETUP.md)。

## 显示内容  
- **主窗口**（5 小时）——短期速率限制  
- **次级窗口**（7 天）——每周速率限制  
- 显示基于本地时区的重置时间（带有倒计时）  
- 源会话文件及其使用时长  

## 使用场景  
- 在开始大量使用 Codex 之前（检查每周配额）  
- 当 Codex 运行缓慢时（可能是由于速率限制）  
- 监控多个账户的配额使用情况