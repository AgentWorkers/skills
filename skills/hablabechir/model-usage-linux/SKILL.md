---
name: model-usage-linux
description: "在 Linux 系统上，通过解析 session JSONL 文件来追踪 OpenClaw AI 的令牌使用情况以及每个模型的成本。该功能可用于查询以下信息：令牌使用量、API 费用、已花费的总额、使用频率最高的模型、使用情况汇总以及费用明细。它可作为仅适用于 macOS 的 model-usage/CodexBar 功能的 Linux 替代方案。"
---
# 模型使用说明（Linux）

解析 OpenClaw 会话文件，以汇总每个模型的令牌使用情况及其成本。

## 快速入门

```bash
python3 {baseDir}/scripts/usage.py
```

## 选项

```bash
# JSON output
python3 {baseDir}/scripts/usage.py --format json

# Custom sessions dir
python3 {baseDir}/scripts/usage.py --sessions-dir ~/.openclaw/agents/main/sessions
```

## 输出结果

显示每个模型的详细信息：
- 回复次数（助手的回复次数）
- 输入/输出令牌数量
- 缓存读写令牌数量
- 成本（以美元计）

会话文件存储路径：`~/.openclaw/agents/main/sessions/*.jsonl`