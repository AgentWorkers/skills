---
name: linkedin-analyzer
description: 对任何 LinkedIn 个人资料的营销策略进行逆向工程分析——包括其核心要素（pillars）、吸引用户的手段（hooks）、呼叫行动（CTAs），以及生成的 PDF 报告。
user-invocable: true
allowed-tools: Bash, Read, Write, Glob
argument-hint: "<linkedin-profile-url-or-post-url>"
---
# LinkedIn 内容策略分析工具

您可以使用 `linkedin-analyzer` 命令行工具（CLI）。该工具包含两种核心模式：**个人资料分析**（分析个人资料中所有帖子的内容策略）和 **单篇帖子分析**（深入分析某篇具有高传播效果的帖子的内容策略）。

## 可用命令

### 1. 个人资料分析
分析个人资料中所有帖子的内容策略。
```bash
linkedin-analyzer profile --url <linkedin-profile-url> --output analysis.json
# Optional:
# --limit-per-source 10 --scrape-until 2025-01-01 --skip-ai
```

### 2. 单篇帖子分析
深入分析某篇特定帖子为何具有高传播效果。
```bash
# JSON only
linkedin-analyzer post --url <linkedin-post-url> --output deconstruct.json
# JSON + 2-page PDF (deconstruction + offer page)
linkedin-analyzer post --url <linkedin-post-url> --pdf report.pdf
# Optional: --skip-ai
```

### 3. PDF 报告
根据分析结果生成一份精美的 8 页 PDF 报告。
```bash
linkedin-analyzer pdf --file analysis.json --output report.pdf
```

## 自动更新（每周一次）

在运行工具之前，系统会自动检查工具包是否需要更新（每 7 天检查一次）：

```bash
python3 - <<'EOF'
import os, time
from pathlib import Path

repo = Path.home() / "ai-native-toolkit"
stamp = repo / ".last_updated"

if repo.exists():
    last = float(stamp.read_text().strip()) if stamp.exists() else 0
    if time.time() - last > 7 * 86400:
        os.system(f"cd {repo} && git pull --quiet && pip install -e . -q")
        stamp.write_text(str(time.time()))
EOF
```

如果相关仓库不存在，工具会自动跳过更新步骤并继续执行后续操作。

## 使用说明

1. **检查依赖项**：
   - 确保已安装 `linkedin-analyzer`。如果未安装，请提示用户使用 `pip install ai-native-toolkit` 进行安装。
   - 确保已设置 `APIFY_API_KEY` 以及 `GEMINI_API_KEY`、`OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY` 中的其中一个。

2. **确定分析任务**：
   - 如果用户提供了个人资料链接，请运行 `profile` 命令。
   - 如果用户提供了帖子链接，请运行 `post` 命令。

3. **进行个人资料分析时，请提供以下信息**：
   - “需要抓取多少篇帖子？”（对应参数：`--limit-per-source`）
   - “只抓取发布日期在什么时间之后的帖子？”（对应参数：`--scrape-until`）

4. **查看分析结果（存储在 `analysis.json` 文件中）**：
   - 帖子的发布频率及平均互动量
   - 内容策略（核心要素、类型）
   - 表现最佳的 5 篇帖子和表现最差的 5 篇帖子
   - 用于吸引用户互动的元素（Hook）及其使用策略

5. **查看单篇帖子分析结果（存储在 `deconstruct.json` 文件中）**：
   - 用于吸引用户互动的元素类型及其使用方式
   - 用于引导用户采取行动的元素（CTA）类型及其使用策略
   - 该帖子为何具有高传播效果（基于 AI 的分析结果）
   - 帖子的核心内容要素及类型
   - 复制该帖子效果的步骤指南

6. **生成 PDF 报告**：
   - 可通过运行 `linkedin-analyzer pdf` 命令在分析完成后生成 PDF 报告。
   - 或者通过添加 `--pdf` 参数在单篇帖子分析完成后生成 PDF 报告。