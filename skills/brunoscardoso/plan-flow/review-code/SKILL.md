---
name: review-code
description: 审查本地未提交的代码更改
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---
# 代码审查

用于审查仓库中未提交的本地更改。

## 功能概述

1. 获取更改的 `git diff` 命令输出（包括已暂存的更改、未暂存的更改或所有更改）
2. 识别出发生变化的文件及其修改内容
3. 在代码库中查找类似的实现方式
4. 根据项目规范和规则对更改进行评估
5. 提供问题的严重程度及修复建议
6. 生成一份审查报告

## 使用方法

```
/review-code [path] [scope]
```

**参数：**
- `path`（可选）：需要审查的具体文件或目录
- `scope`（可选）：`staged`（已暂存的更改）、`unstaged`（未暂存的更改）或 `all`（默认值：所有更改）

## 输出结果

生成文件：`flow/reviewed-code/review_<scope>.md`

## 问题分类

| 严重程度 | 描述 | 需要采取的行动 |
|----------|-------------|-----------------|
| Critical | 安全问题、重大错误 | 提交前必须修复 |
| Major | 严重的问题 | 应该修复 |
| Minor | 代码质量问题 | 可以考虑修复 |
| Suggestion | 改进建议 | 可选 |

## 审查报告结构

```markdown
# Code Review: [Scope]

## Review Information
| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Files Reviewed | N |
| Scope | all/staged/unstaged |

## Changed Files
| File | Status | Lines Changed |
|------|--------|---------------|
| path/to/file | modified | +10/-5 |

## Findings

### Finding 1: [Name]
| Field | Value |
|-------|-------|
| File | path/to/file |
| Line | 42 |
| Severity | Major |
| Fix Complexity | 3/10 |

**Description**: What's wrong
**Suggested Fix**: How to fix it

## Commit Readiness
| Status | Ready to Commit / Needs Changes |
```

## 示例

```
/review-code
```

**范围化审查：**
```
/review-code src/components staged
```

## 审查内容

- 代码与现有代码库的一致性
- 错误处理的完整性
- 类型安全性（针对 TypeScript）
- 安全隐患（如硬编码的敏感信息、注入风险）
- 性能优化
- 代码的组织结构和命名规范

## 下一步操作

修复问题后，提交您的更改；或者在创建 Pull Request（PR）后运行 `/review-pr` 命令。