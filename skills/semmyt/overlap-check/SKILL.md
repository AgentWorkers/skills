---
name: overlap-check
description: "在创建新问题或提交新的 Pull Request (PR) 之前，请先检查是否存在相关的问题或 PR。当代理（agent）打算提交问题、打开 PR 或在某个讨论帖下发表评论时，该功能会自动触发。系统会搜索目标仓库中的重复内容，并显示搜索结果，以便代理可以决定是继续处理新问题，还是参与现有的讨论。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["gh"] },
      },
  }
---
# 重复检查

在创建新的问题（issue）或拉取请求（PR）之前，请先在目标仓库中搜索是否已有讨论相同主题的帖子。

## 触发条件

- 当您准备运行 `gh issue create` 或 `gh pr create` 命令时
- 当用户要求您“创建一个问题”、“提交一个拉取请求”或“报告这个错误”时
- 当您正在尚未阅读的问题或拉取请求上撰写评论时

## 应该怎么做

### 1. 确定目标仓库和主题

确定您要操作的目标仓库。如果您位于已克隆的仓库中，请执行以下操作：

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

用几个关键词概括您的问题或拉取请求的内容。

### 2. 搜索现有帖子

执行两次搜索。请在关键词中去除无关的词汇（如 the、a、is、for、with、this、that、when、not、but、and、from 等）。

```bash
gh search issues --repo OWNER/REPO "KEYWORDS" --limit 5 --json number,title,state,comments
gh search prs --repo OWNER/REPO "KEYWORDS" --limit 5 --json number,title,state,comments
```

### 3. 评估搜索结果

查看搜索到的帖子的标题和评论数量。如果发现有相关的内容：
- 打开相应的帖子：`gh issue view NUMBER --repo OWNER/REPO` 或 `gh pr view NUMBER`
- 仔细阅读帖子内容，判断您的主题是否已被讨论过
- 检查该帖子是活跃的、过时的还是已关闭的

### 4. 采取相应行动

| 情况 | 应采取的行动 |
|-----------|--------|
| 已有开放的帖子恰好讨论了您的主题 | 在该帖子下发表评论，而不是创建新的帖子 |
| 已有的关闭帖子已经解决了您的问题 | 不要重新创建新的帖子；如果相关，请提供该帖子的链接 |
| 已有的帖子相关但内容不同 | 继续创建新的问题/拉取请求，并引用相关帖子 |
| 没有找到匹配的帖子 | 按正常流程进行操作 |

### 5. 如果发现重复内容，请告知用户

在继续操作之前，请向用户展示您的发现结果：

```
Found existing threads that may cover this:
  #13738 — WSL2 clipboard paste broken (16 comments, open)
  #14635 — Paste not working in WSL (3 comments, open)

Should I comment on an existing thread or create a new one?
```

## 不应该做的事情

- 即使您确信自己的主题是新的，也不要跳过此检查步骤
- 仅仅因为现有帖子的表述略有不同，就不要创建新的问题
- 不要进行复杂的分析——两次 `gh search` 就足够了
- 不要阻止用户；如果用户坚持要创建新帖子，请允许他们这样做