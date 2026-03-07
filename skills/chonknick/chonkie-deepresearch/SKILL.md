---
name: chonkie-deepresearch
description: "使用 Chonkie DeepResearch 进行深入的研究查询。该工具能够生成包含引用信息的全面研究报告，非常适合用于市场分析、竞争情报收集、技术研究以及任何需要大量研究工作的场景。"
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

您可以通过该工具从您的代理服务器发起深度研究查询，并获取包含引用信息的完整报告。

## 设置

在使用之前，请检查是否已安装 `chdr`（使用 `which chdr` 命令）。如果未安装：

1. 安装：`cargo install chdr`
   - 如果系统中没有 `cargo`，请先安装 Rust：`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. 进行身份验证：`chdr auth login`（系统会打开浏览器以获取 API 密钥）
   - 或者设置 `CHONKIE_API_KEY` 环境变量
   - 密钥获取地址：https://labs.chonkie.ai/settings/api-keys

## 使用方法

当用户需要您进行某项研究时，或者您需要为某项任务收集信息时，可以按照以下步骤操作：

### 运行研究任务

```bash
# Run research and save JSON output (takes 2-10 minutes)
chdr research --type report --no-stream --json "<query>" > /tmp/chdr-research.json

# Extract markdown body for reading
python3 -c "
import json
data = json.load(open('/tmp/chdr-research.json'))
print(data.get('content', {}).get('body', ''))
" > /tmp/chdr-research.md
```

请在后台运行研究命令（因为该过程可能需要几分钟时间）。请告知用户研究任务正在执行中。

### 研究完成后

1. 从 JSON 数据中提取 `id` 和 `title`。
2. 提供研究结果的网页链接：`https://labs.chonkie.ai/research/{id}`
3. 仅读取 `.md` 文件的前 100 行作为摘要内容。
4. 告诉用户您可以回答问题——您可以根据需求阅读具体的章节内容。

### 回答后续问题

- 在阅读之前，使用 `grep` 命令在 `.md` 文件中查找相关内容。
- 使用 `offset` 和 `limit` 参数来仅读取匹配的章节。
- **切勿** 一次性读取整个文件的全部内容——报告文件可能包含超过 20,000 行。

### 其他命令

```bash
chdr ls                    # List recent research
chdr ls --limit 20         # List more
chdr view <id>             # View a report (supports partial ID prefix)
chdr open <id>             # Open in browser
chdr delete <id>           # Delete a report
```

所有需要输入 ID 的命令都支持前缀匹配功能——例如，`chdr view 3a6b` 即可正确执行相应操作。