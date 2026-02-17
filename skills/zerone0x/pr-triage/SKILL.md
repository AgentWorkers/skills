---
name: pr-triage
description: 通过检测重复的 Pull Request（PR）、评估其质量以及生成优先级排序的报告来对这些 PR 进行分类和处理。当一个仓库中的 PR 数量过多而无法手动审核时，或者需要检测重复的 PR，或者希望借助人工智能来辅助确定 PR 的优先级时，可以使用这种方法。
---
# PR 分类与处理

您是一名 PR 分类处理人员，您的任务是分析待处理的 PR（Pull Requests），检测重复的 PR，评估其质量，并为维护者生成可操作的报告。

## 输入参数

参数：$ARGUMENTS

支持的命令行参数：
- `--repo <owner/repo>`：目标仓库（如果不在仓库目录中，则必须指定）
- `--days N`：仅分析过去 N 天内更新的 PR（默认值：7 天）
- `--all`：分析所有待处理的 PR（操作较为耗时，请谨慎使用）
- `--threshold N`：重复 PR 的相似度阈值（0-100，默认值：80）
- `--output <file>`：将报告写入指定文件（默认输出到标准输出）
- `--top N`：报告中仅显示排名前 N 的 PR（默认显示所有 PR）

## 注意：GitHub CLI 需要身份验证

**所有 GitHub CLI 命令都必须使用以下身份验证模式：**
```bash
env -u GH_TOKEN -u GITHUB_TOKEN gh <command>
```

## 工作流程

### 第 1 阶段：获取 PR 信息

```bash
# Get open PRs with metadata
env -u GH_TOKEN -u GITHUB_TOKEN gh pr list \
  --repo <OWNER/REPO> \
  --state open \
  --limit 500 \
  --json number,title,body,author,createdAt,updatedAt,labels,files,additions,deletions,headRefName

# If --days specified, filter by updatedAt
```

**每个 PR 收集的数据包括：**
- PR 编号
- 标题
- PR 内容（用于提取意图）
- 修改的文件（用于检测重复）
- 新增/删除的文件（用于计算文件大小）
- 标签（用于判断优先级）
- 作者（用于了解贡献者信息）

### 第 2 阶段：提取 PR 的意图

针对每个 PR，提取一个标准化的“意图”以供后续比较：

```python
def extract_intent(pr):
    """Extract searchable intent from PR"""
    return {
        "number": pr["number"],
        "title": pr["title"],
        "files": [f["path"] for f in pr["files"]],
        "keywords": extract_keywords(pr["title"] + " " + pr["body"]),
        "issue_refs": extract_issue_refs(pr["body"]),  # Fixes #123, etc.
    }
```

**关键词提取目标包括：**
- 错误信息、函数名称、文件路径
- 问题引用（例如 #123）
- 功能名称、组件名称
- 操作动词（例如修复、添加、删除、更新）

### 第 3 阶段：检测重复的 PR

使用多种方法来检测重复的 PR：

#### 3.1 文件内容重复
```python
def file_similarity(pr1, pr2):
    """Jaccard similarity of files changed"""
    files1 = set(pr1["files"])
    files2 = set(pr2["files"])
    if not files1 or not files2:
        return 0
    return len(files1 & files2) / len(files1 | files2)
```

#### 3.2 标题/关键词相似度
```python
def keyword_similarity(pr1, pr2):
    """Jaccard similarity of extracted keywords"""
    kw1 = set(pr1["keywords"])
    kw2 = set(pr2["keywords"])
    if not kw1 or not kw2:
        return 0
    return len(kw1 & kw2) / len(kw1 | kw2)
```

#### 3.3 引用相同的问题
```python
def same_issue(pr1, pr2):
    """Check if both PRs reference the same issue"""
    refs1 = set(pr1["issue_refs"])
    refs2 = set(pr2["issue_refs"])
    return bool(refs1 & refs2)
```

#### 3.4 综合相似度评分
```python
def similarity_score(pr1, pr2):
    """Combined similarity (0-100)"""
    if same_issue(pr1, pr2):
        return 100  # Definite duplicate
    
    file_sim = file_similarity(pr1, pr2)
    kw_sim = keyword_similarity(pr1, pr2)
    
    # Weighted combination
    return int((file_sim * 0.6 + kw_sim * 0.4) * 100)
```

### 第 4 阶段：质量评估

根据以下指标对每个 PR 进行质量评分：

| 评分指标 | 分值 | 判断标准 |
|--------|--------|-----------|
| 是否有描述 | +10 | PR 内容长度大于 50 行 |
| 是否引用问题 | +15 | PR 内容包含 “Fixes #” 或 “Closes #” 等字样 |
| 是否包含测试代码 | +20 | PR 文件中包含 test_*.py、*.test.ts 等测试文件 |
| PR 代码量较少（<100 行） | +10 | 新增/删除的代码行数少于 100 行 |
| 是否有标签 | +5 | PR 中有标签 |
| 是否近期有更新 | +10 | PR 在过去 7 天内被更新 |
| 是否是首次贡献者 | -5 | 检查作者是否为首次贡献者 |

**质量等级：**
- A：60 分及以上
- B：40-59 分
- C：20-39 分
- D：低于 20 分

### 第 5 阶段：生成报告

输出一份 Markdown 格式的报告：

```markdown
# PR Triage Report

**Repository:** owner/repo
**Generated:** 2024-01-15 10:30 UTC
**PRs Analyzed:** 127
**Duplicates Found:** 12 groups

## 🔴 Duplicate Groups (Action Required)

### Group 1: Fix login validation
**Issue:** #456
| PR | Title | Author | Quality | Recommendation |
|----|-------|--------|---------|----------------|
| #789 | Fix login validation bug | @alice | A | ✅ Keep |
| #801 | Login fix | @bob | C | ❌ Close |
| #812 | Fix #456 login issue | @charlie | B | ❌ Close |

**Recommendation:** Keep #789 (most complete, has tests)

### Group 2: Update dependencies
...

## 📊 Quality Summary

| Grade | Count | PRs |
|-------|-------|-----|
| A | 15 | #123, #456, ... |
| B | 42 | ... |
| C | 58 | ... |
| D | 12 | ... |

## ⚠️ Stale PRs (>30 days no activity)
- #234: "Add feature X" (45 days, no response to review)
- #345: "Fix Y" (62 days, waiting on author)

## 🚀 Ready to Merge (High Quality + No Duplicates)
- #567: "Add dark mode" (Grade A, 3 approvals)
- #678: "Fix memory leak" (Grade A, tests passing)
```

### 第 6 阶段：可选操作

如果使用了 `--action` 参数，可以执行以下操作：

#### 对重复的 PR 进行评论
```bash
env -u GH_TOKEN -u GITHUB_TOKEN gh pr comment <NUMBER> --body "This PR appears to duplicate #XXX. Please coordinate with the other author or close if redundant."
```

#### 为 PR 添加标签
```bash
env -u GH_TOKEN -u GITHUB_TOKEN gh pr edit <NUMBER> --add-label "duplicate"
env -u GH_TOKEN -u GITHUB_TOKEN gh pr edit <NUMBER> --add-label "needs-review"
```

## 功能限制

**能够执行的任务：**
- 获取并分析待处理的 PR
- 通过多种方式检测重复的 PR
- 客观地评估 PR 的质量
- 生成可操作的报告
- 建议保留哪些重复的 PR

**无法执行的任务：**
- ❌ 自动关闭 PR（仅提供建议）
- ❌ 合并 PR
- ❌ 阅读完整的代码差异（操作耗时较高）
- ❌ 对代码质量做出主观判断
- ❌ 在没有 `--action` 参数的情况下对 PR 进行评论

## 运算资源优化

**耗时较多的操作（请谨慎使用）：**
- 阅读完整的 PR 代码差异
- 获取所有评论
- 同时分析超过 100 个 PR

**耗时较少的操作（可自由使用）：**
- PR 的元数据（标题、文件、标签）
- 相似度计算（在本地进行）
- 生成报告

**推荐的工作流程：**
1. 首次运行时使用 `--days 7` 来处理最近的 PR
2. 每周运行一次 `--days 30` 来进行全面的检查
3. 极少数情况下使用 `--all` 来进行全面的审计（请注意计算成本）

## 示例

### 基本用法
```
/pr-triage --repo opencode/opencode --days 7
```
分析过去 7 天内更新的 PR，并生成报告。

### 全面审计
```
/pr-triage --repo anthropics/claude --all --output report.md
```
分析所有待处理的 PR，并将报告写入文件。

### 高相似度阈值
```
/pr-triage --repo microsoft/vscode --threshold 90
```
仅标记出非常明显的重复 PR。

### 仅显示排名前 N 的 PR
```
/pr-triage --repo facebook/react --days 30 --top 20
```
仅显示质量得分排名前 20 的 PR。