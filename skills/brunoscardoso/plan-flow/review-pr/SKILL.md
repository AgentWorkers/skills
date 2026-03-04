---
name: review-pr
description: 审核拉取请求（Review a Pull Request）
metadata: {"openclaw":{"requires":{"bins":["git","gh"]}}}
user-invocable: true
---
# 审查 Pull Request

使用 GitHub CLI 通过 Pull Request 的编号来审查它。

## 功能

1. 使用 `gh pr view` 获取 Pull Request 的信息。
2. 使用 `gh pr diff` 获取 Pull Request 的差异。
3. 根据项目规范分析所做的更改。
4. 检查是否存在安全性和性能问题。
5. 提供详细的发现结果和建议。
6. 生成一份审查文档。

## 使用方法

```
/review-pr <pr_number>
```

**参数：**
- `pr_number`（必填）：要审查的 Pull Request 的编号。

## 先决条件**

- 必须安装并登录 `gh` CLI。
- 如果尚未登录，请运行 `gh auth login`。

## 输出结果**

生成的文件名为：`flow/reviewed-pr/pr_<number>.md`

## 审查重点领域

| 领域 | 检查内容 |
|------|----------------|
| 代码质量 | 规范一致性、命名规范、代码组织结构 |
| 安全性 | 代码中是否存在敏感信息、注入攻击风险、认证问题 |
| 性能 | 是否存在冗余查询、不必要的循环、缓存问题 |
| 测试 | 测试覆盖率、边界情况是否得到覆盖 |
| 文档 | 代码注释是否完整、README 文件是否更新 |

## 审查文档的结构

```markdown
# PR Review: #<number>

## PR Information
| Field | Value |
|-------|-------|
| Title | PR title |
| Author | username |
| Branch | feature -> main |
| Files Changed | N |

## Summary
What this PR does

## Findings

### Finding 1: [Name]
| Field | Value |
|-------|-------|
| File | path/to/file |
| Severity | Major |

**Description**: What's wrong
**Suggested Fix**: How to fix it

## Security Considerations
Any security concerns

## Performance Considerations
Any performance concerns

## Recommendation
| Status | Approve / Request Changes / Comment |
```

## 示例

```
/review-pr 123
```

**输出结果：**
```
Reviewing PR #123...

Fetching PR information...
Fetching PR diff...
Analyzing changes...

PR #123 Review Complete!

Summary: Adds user authentication with OAuth
Files Changed: 12
Findings: 2 Major, 3 Minor

Review saved to: flow/reviewed-pr/pr_123.md

Recommendation: Request Changes
- Fix the 2 major issues before merging
```

## 登录问题

如果遇到登录错误，请参考以下提示：

```bash
# Authenticate with GitHub
gh auth login

# Verify authentication
gh auth status
```