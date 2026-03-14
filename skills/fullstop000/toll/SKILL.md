---
name: toll
description: 跟踪并显示来自 Claude Code 和 Codex CLI 会话的令牌使用统计信息以及预估的 USD 成本。
version: 1.0.5
homepage: https://github.com/Fullstop000/toll
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - toll
---
# toll — 令牌使用跟踪器

`toll` 是一个命令行工具（CLI），它汇总来自 **Claude Code** 和 **Codex CLI** 的令牌使用日志，并显示会话数量、令牌总数、缓存命中率以及预估的美元成本。

## 安装

如果尚未安装 `toll`，请先进行安装：

```bash
# Quick install (Linux/macOS)
curl -fsSL https://raw.githubusercontent.com/Fullstop000/toll/refs/heads/master/install.sh | sh

# Or via cargo
cargo install toll
```

## 使用方法

当用户执行 `/toll` 时，需要根据他们的需求运行相应的 `toll` 命令：

| 用户需求 | 命令                |
|---------|-------------------|
| 查看历史统计（默认）| `toll`             |
| 仅查看今日使用情况 | `toll --today`         |
| 查看过去 N 天的数据 | `toll --days <N>`        |
| 查看每日使用情况 | `toll --by-day`         |
| 仅查看 Claude Code 的数据 | `toll --claude`         |
| 仅查看 Codex CLI 的数据 | `toll --codex`         |
| 查看详细的令牌统计 | `toll --detail`         |
| 输出 JSON 格式的数据 | `toll --json`         |
| 输出 CSV 格式的数据 | `toll --csv`         |
| 列出模型价格 | `toll --list-prices`       |

多个标志可以组合使用，例如：`toll --by-day --days 7 --claude`。

## 工作原理

1. 通过运行 `toll --version` 来检查 `toll` 是否已安装。如果未安装，系统会提示用户使用上述命令进行安装。
2. 解析用户的请求，以确定需要传递哪些标志。
3. 使用相应的标志运行 `toll` 并将结果展示给用户。
4. 如果用户对某些指标不熟悉，系统会对其进行解释：
   - **会话数（Sessions）**：记录的 AI 编码会话数量
   - **输入令牌总数（Input）**：发送给模型的总令牌数
   **缓存令牌数（Cached）**：从提示缓存中获取的令牌数（成本较低）
   **缓存命中率（Hit Rate）**：被缓存的输入令牌所占的百分比
   **非缓存输入令牌数（Net Input）**：未缓存的输入令牌数（全额费用）
   **模型生成的令牌数（Output）**：模型生成的令牌数
   **成本（Cost）**：根据模型价格估算的美元成本

## 示例交互

**用户：** `/toll`  
→ 运行 `toll` 以查看历史统计

**用户：** `/toll today`  
→ 运行 `toll --today`  

**用户：** `/toll last 7 days`  
→ 运行 `toll --days 7`  

**用户：** `/toll daily breakdown this week`  
→ 运行 `toll --by-day --days 7`  

**用户：** `/toll how much have I spent on Claude?`  
→ 运行 `toll --claude` 并突出显示“Cost”列  

**用户：** `/toll export csv`  
→ 运行 `toll --csv` 并提供将输出保存到文件的选项

## 注意事项

- 标有 `*` 的成本估算包括那些定价不准确或通过前缀匹配推断出的模型。
- 令牌计数的表示方式较为简洁：`1.2m` 表示 1,200,000 个令牌，`45.6k` 表示 45,600 个令牌。
- 日志文件位于 `~/.claude/projects/**/*.jsonl`（Claude Code）和 `~/.codex/sessions/`（Codex CLI）目录下。