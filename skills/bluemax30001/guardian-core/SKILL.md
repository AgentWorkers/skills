---
name: guardian-core
description: 本地守护者扫描器，附带签名文件和仪表板功能。支持实时扫描和批量扫描，不依赖 Webhook、API 或 Cron 任务进行自动化操作。
version: 1.0.5
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - GUARDIAN_WORKSPACE
        - GUARDIAN_CONFIG
    permissions:
      - read_workspace
      - write_workspace
---
# Guardian Core

Guardian Core 是一个轻量级的、以本地扫描为主功能的扫描工具包。

## 包含的功能
- 实时预扫描
- 批量扫描/报告生成
- 预置的签名定义文件
- 本地 SQLite 日志记录（`guardian.db`）
- 本地控制面板文件

## 核心包不包含的功能
- Webhook 集成
- HTTP API 服务器
- Cron 任务自动化设置工具
- 远程定义更新脚本

## 安装
```bash
cd ~/.openclaw/skills/guardian-core
./install.sh
```

## 验证安装结果
```bash
python3 scripts/admin.py status
python3 scripts/admin.py threats
python3 scripts/admin.py report
```

## 环境变量/配置文件
- `GUARDIAN_WORKSPACE`
- `GUARDIAN_CONFIG`

## Python API
```python
from core.realtime import RealtimeGuard

guard = RealtimeGuard()
result = guard.scan_message(user_text, channel="telegram")
if guard.should_block(result):
    return guard.format_block_response(result)
```