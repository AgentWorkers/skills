---
name: skilled-openclaw-advisor
description: 查询本地 OpenClaw 文档索引，以获取关于配置、功能、命令行界面（CLI）命令、通道、提供者、插件、定时任务（cron）、会话（session）、代理（agent）、协议以及故障排除的准确信息。这种方式比依赖 OpenClaw 的训练数据来得更快、更准确。无需进行任何 API 调用，查询响应时间小于 10 毫秒。适用于以下问题：openclaw、configure、gateway、channel、cron、provider、plugin、session、heartbeat、protocol、skill、model、agent 等相关问题。
metadata: {
  "openclaw": {
    "emoji": "📚",
    "skillKey": "skilled-openclaw-advisor",
    "requires": {
      "bins": ["python3"]
    },
    "install": [
      {
        "id": "build-index",
        "kind": "exec",
        "command": "python3 $SKILL_DIR/scripts/build_index.py",
        "label": "Build local OpenClaw docs index (reads from local OpenClaw install only)"
      }
    ]
  },
  "acceptLicenseTerms": true
}
---
# OpenClaw 文档智能

这是一个用于查询 OpenClaw 文档的本地 FTS5 索引的工具，无需调用任何 API，查询响应时间小于 10 毫秒。

## 该工具的功能

该工具整合了三个 Python 脚本，用于查询安装在本地机器上的 OpenClaw 文档所生成的 SQLite FTS5 索引（路径通常为 `~/.npm-global/lib/node_modules/openclaw/docs` 或类似位置）。它仅读取本地文档目录的数据，并将结果写入 `~/.openclaw/skills-data/skilled-openclaw-advisor/` 文件夹。该工具不会进行网络请求，也不会访问任何凭据或配置信息；在运行时也不会读取 `openclaw.json` 文件（以下配置项为可选设置，用户可以根据需要进行修改）。

## 首次使用时的设置

在安装该工具后，需要先构建索引：

```bash
python3 $SKILL_DIR/scripts/build_index.py
```

该脚本会扫描本地的 OpenClaw 文档，并在 `~/.openclaw/skills-data/skilled-openclaw-advisor/index.db` 文件中创建一个 SQLite 索引。

## 查询文档内容

```bash
# Compact output for agent use
python3 $SKILL_DIR/scripts/query_index.py --query "YOUR QUESTION" --mode agent

# Human-readable
python3 $SKILL_DIR/scripts/query_index.py --query "YOUR QUESTION"

# Full detail with online link
python3 $SKILL_DIR/scripts/query_index.py --query "YOUR QUESTION" --verbosity detailed

# Chinese results
python3 $SKILL_DIR/scripts/query_index.py --query "YOUR QUESTION" --lang zh-CN

# Index status
python3 $SKILL_DIR/scripts/query_index.py --status
```

## 索引更新

```bash
# Incremental update (checks for doc changes)
python3 $SKILL_DIR/scripts/update_index.py

# Force full re-index
python3 $SKILL_DIR/scripts/build_index.py --force
```

## 适用场景

- 有关 OpenClaw 配置的问题
- CLI 命令及选项的查询
- 通道（channel）、提供者（provider）、定时任务（cron）、会话（session）以及代理（agent）的设置相关问题
- OpenClaw 错误的排查

## 不适用场景

- 与 OpenClaw 无关的编程问题
- 与第三方服务相关的问题
- 如果索引尚未构建（请先运行 `build_index.py` 命令）

## 响应方式

| 响应模式 | 适用场景 | 描述 |
|------|----------|-------------|
| `agent` | 默认模式 | 极简化的响应格式，仅包含必要信息 |
| `human` + `standard` | 适合人类阅读的响应方式 | 提供清晰的解释和关键信息 |
| `human` + `detailed` | 详细解答 | 包含完整的文档摘录和示例 |

## 可选配置

这些配置项位于 `openclaw.json` 文件中的 `skills.entries.openclaw-docs.config` 文件中（均为可选设置）：

| 配置项 | 默认值 | 说明 |
|---------|---------|-------------|
| `defaultLang` | `"en"` | 显示语言：`en` 或 `zh-CN` |
| `defaultVerbosity` | `"standard"` | 输出格式：`concise`（简洁）、`standard`（标准）或 `detailed`（详细） |
| `maxResults` | `5` | 返回的最大结果数量 |
| `fallbackToEnglish` | `true` | 如果请求的语言没有相应结果，则自动切换为英文响应 |
| `includeOnlineUrl` | `true` | 在详细输出中包含 `https://docs.openclaw.ai/...` 等链接 |