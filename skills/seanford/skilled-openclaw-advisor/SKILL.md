---
name: skilled-openclaw-advisor
description: 查询本地 OpenClaw 文档索引，以获取关于配置、功能、命令行界面（CLI）命令、通道、提供者、插件、定时任务（cron）、会话（session）、代理（agent）、协议以及故障排除的准确信息。这种方法比依赖 OpenClaw 的训练数据更快、更准确。无需调用任何外部 API，查询响应时间小于 10 毫秒。适用于以下问题：openclaw、configure、gateway、channel、cron、provider、plugin、session、heartbeat、protocol、skill、model、agent 等相关内容。
metadata: {
  "openclaw": {
    "emoji": "📚",
    "skillKey": "skilled-openclaw-advisor",
    "requires": {
      "bins": ["python3", "openclaw"]
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

这是一个用于查询 OpenClaw 文档的本地 FTS5 索引的工具，无需调用任何外部 API，查询响应时间小于 10 毫秒。

## 该工具的功能

该工具包含三个 Python 脚本，它们会查询安装在本地机器上的 OpenClaw 文档所生成的 SQLite FTS5 索引（路径通常为 `~/.npm-global/lib/node_modules/openclaw/docs` 或类似位置）。该工具仅读取本地文档目录，并将查询结果写入 `~/.openclaw/skills-data/skilled-openclaw-advisor/` 文件夹。查询和构建脚本不会发起网络请求；当检测到文档更新时，更新脚本会通过 `openclaw message` CLI 发送本地通知（不涉及直接的网络调用）。这些脚本不会访问任何凭据或配置信息，在运行时也不会读取 `openclaw.json` 文件（下面列出的配置选项是可选的，用户可以根据需要进行设置）。

## 首次使用时的设置

在安装该工具后，请先运行以下命令来构建索引：

```bash
python3 $SKILL_DIR/scripts/build_index.py
```

该命令会扫描本地的 OpenClaw 文档，并在 `~/.openclaw/skills-data/skilled-openclaw-advisor/index.db` 文件中创建一个 SQLite 索引。

## 查询文档

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
- CLI 命令和选项的查询
- Channel、provider、cron、session、agent 的设置相关问题
- OpenClaw 错误的排查

## 不适用场景

- 与 OpenClaw 无关的编程问题
- 有关第三方服务的问题
- 如果索引尚未构建（请先运行 `build_index.py` 命令）

## 响应模式

| 响应模式 | 适用场景 | 描述 |
|------|----------|-------------|
| `agent` | 默认响应模式 | 极简化的响应格式，仅包含关键信息 |
| `human` + `standard` | 适合人类阅读的响应方式 | 提供清晰的解释和关键要点 |
| `human` + `detailed` | 详细解答 | 包含完整的文档摘录和示例 |

## 可选配置

这些配置项位于 `openclaw.json` 文件中的 `skills.entries.openclaw-docs.config` 文件中（均为可选配置）：

| 配置项 | 默认值 | 描述 |
|---------|---------|-------------|
| `defaultLang` | `"en"` | 显示语言：`en` 或 `zh-CN` |
| `defaultVerbosity` | `"standard"` | 输出详细程度：`concise`（简洁）、`standard`（标准）、`detailed`（详细） |
| `maxResults` | `5` | 返回的最大结果数量 |
| `fallbackToEnglish` | `true` | 如果请求的语言没有对应的文档，则自动切换为英文显示 |
| `includeOnlineUrl` | `true` | 在详细输出中包含 `https://docs.openclaw.ai/...` 的链接 |