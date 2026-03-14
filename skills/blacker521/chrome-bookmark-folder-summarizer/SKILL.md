---
name: chrome-bookmark-summarizer
description: 该工具能够读取 Chrome 书签中的网址，并根据用户指定的文件夹名称进行筛选。随后，它会生成这些网页的摘要。适用于以下场景：用户提及 Chrome 书签/收藏夹、书签文件夹、链接摘要功能，或要求对某个书签文件夹下的网站进行摘要处理时使用。
---
# Chrome 书签摘要生成工具

该工具可以从指定的 Chrome 书签文件夹中提取网页内容，并生成结构化的摘要。

## 使用场景

- 当用户提及“Chrome 书签”、“收藏夹”或“生成链接摘要”时；
- 需要根据文件夹名称批量读取链接并生成摘要时；
- 需要在对网页内容进行摘要处理之前，先从本地书签文件中过滤出符合条件的 URL。

## 工作流程

1. 确认输入参数：
   - 必需参数：目标文件夹名称（例如：`AI Research`）
   - 可选参数：匹配模式（`exact` 或 `contains`）
   - 可选参数：是否递归处理子文件夹（默认值：递归）

2. 运行提取脚本（输出格式为 JSON）

```bash
python3 "scripts/extract_chrome_bookmarks.py" --folder "AI Research"
```

## 常见选项：

```bash
# Fuzzy folder-name matching
python3 "scripts/extract_chrome_bookmarks.py" --folder "AI" --match-mode contains

# If multiple folders share the same name, return only the first match
python3 "scripts/extract_chrome_bookmarks.py" --folder "AI Research" --pick-first

# Extract only direct links (no subfolders)
python3 "scripts/extract_chrome_bookmarks.py" --folder "AI Research" --non-recursive
```

3. 解析输出结果并处理错误：
   - 如果 `ok` 为 `false`，则向用户返回明确的错误信息（例如：文件夹未找到、路径无效等）；
   - 如果 `ok` 为 `true`，则读取 `results[].urls[]` 以进行后续的摘要生成操作。

4. 批量生成网页摘要：
   - 为每个 URL 获取页面内容（优先获取完整正文；如果获取失败，则使用页面标题和简短描述）；
   - 推荐的输出结构包括：
     - 页面标题
     - 核心要点（1-2 句）
     - 关键内容（2-4 条）
     - 与用户目标的相关性（1 句）

5. 最终结果汇总：
   - 保持书签的原始顺序；
   - 在输出结果末尾添加跨页面的对比信息：
     - 共同的主题
     - 不同的观点
     - 推荐的阅读顺序

## 输出模板

```markdown
## Folder: {folder_name}

### 1) {page_title}
- URL: {url}
- Core takeaway: {summary}
- Key points:
  - {point_1}
  - {point_2}
  - {point_3}
- Relevance: {relevance}

### 2) {page_title}
...

## Cross-Page Summary
- Shared themes: ...
- Differences: ...
- Suggested reading order: ...
```

## 注意事项

- macOS 上 Chrome 书签的默认路径为：
  - `~/Library/Application Support/Google/Chrome/Default/Bookmarks`
- 如果用户使用多个 Chrome 账户，请询问具体的书签文件路径，并通过 `--bookmarks` 参数传递该路径；
- 可能存在重复的文件夹名称；默认情况下会返回所有匹配的结果。可以使用 `--pick-first` 参数仅保留一个重复的文件夹。