---
name: chonkie-deepresearch
description: "使用 Chonkie DeepResearch 执行深入的研究查询。该工具可生成包含引用的全面研究报告，适用于市场分析、竞争情报分析、技术研究以及任何需要大量研究工作的场景。"
homepage: https://chonkie.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "🔬",
        "requires": { "bins": ["chdr"] },
        "tags": ["research", "deep-research", "analysis", "reports", "chonkie"]
      }
  }
---
# Chonkie DeepResearch

您可以通过代理执行深入的研究查询，并获取包含引用信息的完整报告。

## 设置

在使用之前，请检查 `chdr` 是否已安装（使用 `which chdr` 命令）。如果未安装，请按照以下步骤操作：

1. 安装：`cargo install chdr`
   - 如果系统中没有 `cargo`，请先安装 Rust：`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. 进行身份验证：`chdr auth login`（系统会打开浏览器以获取 API 密钥）
   - 或者将 `CHONKIE_API_KEY` 设置为环境变量
   - 可以在 https://labs.chonkie.ai/settings/api-keys 获取 API 密钥

## 使用方法

**重要提示：** 研究查询可能需要 2 到 10 分钟才能完成。为了避免阻塞主线程，请始终使用子代理来执行查询。

### 使用子代理执行查询（推荐）

使用 `sessions_spawn` 在子代理中运行查询。子代理会处理耗时较长的查询，并在完成后通知您结果，这样主线程可以保持响应状态。

```json
{
  "tool": "sessions_spawn",
  "task": "Run chdr research and save results. Steps:\n1. Run: chdr research --type report --no-stream --json \"<QUERY>\" > /tmp/chdr-research-<TIMESTAMP>.json\n2. Extract ID and title: python3 -c \"import json; d=json.load(open('/tmp/chdr-research-<TIMESTAMP>.json')); print(d['id']); print(d.get('title','Untitled'))\"\n3. Extract body: python3 -c \"import json; d=json.load(open('/tmp/chdr-research-<TIMESTAMP>.json')); print(d.get('content',{}).get('body',''))\" > /tmp/chdr-research-<TIMESTAMP>.md\n4. Report back the title, ID, and URL: https://labs.chonkie.ai/research/{id}"
}
```

请将 `<QUERY>` 替换为实际的研究查询内容，将 `<TIMESTAMP>` 替换为 `$(date +%s)`。

### 监控查询状态

**切勿连续不断地轮询查询状态。** 可以设置一个定时任务（例如每 2-3 分钟执行一次）来检查查询进度：

```bash
# Add a cron entry to check research status every 2 minutes
# The cron should run: chdr view <id> --json | python3 -c "import json,sys; d=json.load(sys.stdin); s=d.get('status','unknown'); print(s)"
# and notify you when status is 'completed' or 'failed'
```

或者直接等待子代理完成查询的提示——查询完成后它会自动通知您。对于一次性查询，使用子代理的方式更为合适。

### 查询完成后

当子代理通知查询完成时：

1. 查询结果的网页地址为：`https://labs.chonkie.ai/research/{id}`
2. 完整报告保存在 `/tmp/chdr-research-<TIMESTAMP>.md` 文件中
3. 仅阅读文件的前 100 行以获取摘要——切勿加载整个文件
4. 告知用户您可以回答与报告相关的问题

### 回答后续问题

- 在阅读报告之前，使用 `grep` 命令在 `.md` 文件中查找相关内容
- 使用 `offset` 和 `limit` 参数来仅读取所需的部分
- 绝不要一次性加载整个文件——报告内容可能超过 20,000 行

### 备用方案：在没有子代理的情况下执行查询

如果子代理不可用，可以直接执行查询命令，但需提前警告用户该操作可能会导致系统阻塞几分钟：

```bash
chdr research --type report --no-stream --json "<query>" > /tmp/chdr-research.json
```

### 其他命令

```bash
chdr ls                    # List recent research
chdr ls --limit 20         # List more
chdr view <id>             # View a report (supports partial ID prefix)
chdr open <id>             # Open in browser
chdr delete <id>           # Delete a report
```

所有需要输入 ID 的命令都支持前缀匹配——例如 `chdr view 3a6b` 就是有效的命令格式。