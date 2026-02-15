---
name: migrate
description: 用于在多台机器之间迁移 Clawdbot 安装。当用户需要将 Clawdbot 迁移到新电脑、备份其设置或从备份中恢复时，可以使用此功能。该功能会处理工作区文件、配置文件、WhatsApp 会话记录，以及可选的凭据信息。
---

# Clawdbot 迁移

支持导出和导入完整的 Clawdbot 安装环境。

## 导出

将当前安装环境打包成一个可移植的压缩文件：

```bash
bash scripts/export.sh
```

可选参数：
- `--output, -o PATH` — 输出目录（默认：当前目录）
- `--workspace PATH` — 工作区路径（默认：`~/clawd`）
- `--include-sessions` — 包含会话记录
- `--include-credentials` — 包含凭据 ⚠️ 请谨慎操作

示例：
```bash
bash scripts/export.sh -o /tmp --include-sessions
```

生成的文件：`clawdbot-export-YYYYMMDD_HHMMSS.tar.gz`

## 导入

在新机器上从导出的压缩文件中恢复安装环境：

```bash
bash scripts/import.sh <archive.tar.gz>
```

可选参数：
- `--workspace PATH` — 目标工作区路径（默认：`~/clawd`）
- `--force, -f` — 强制覆盖现有文件（无需提示）

示例：
```bash
bash scripts/import.sh clawdbot-export-20260129_120000.tar.gz --force
```

## 包含的内容

| 组件          | 默认值    | 是否包含 |
|---------------|---------|---------|
| 工作区（`~/clawd`）    | ✓       |        |
| 配置文件（`clawdbot.json`） | ✓       |        |
| 管理的技能        | ✓       |        |
| WhatsApp 会话记录  | ✓       |        |
| 会话记录        | ✗       | （需使用 `--include-sessions`） |
| 凭据            | ✗       | （需使用 `--include-credentials`） |

**工作区中不包含的文件**（可以重新生成）：
`node_modules/`, `.next/`, `.open-next/`, `.vercel/`, `.wrangler/`, `.git/`, `dist/`, `build/`

## 迁移流程

1. 在旧机器上执行相关操作：
   ```bash
   bash scripts/export.sh -o ~/Desktop
   ```

2. 将压缩文件传输到新机器（使用 scp、U盘、云存储等方式）。

3. 在新机器上执行以下操作：
   ```bash
   npm install -g clawdbot
   bash scripts/import.sh ~/clawdbot-export-*.tar.gz
   cd ~/clawd && clawdbot gateway start
   ```

WhatsApp 会话记录会自动迁移，无需重新扫描。