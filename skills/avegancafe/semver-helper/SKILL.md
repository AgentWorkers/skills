---
name: semver-helper
description: 帮助根据代码变更来确定版本号的升级类型（MAJOR、MINOR、PATCH）。提供关于 SemVer 2.0.0 标准的指导。
author: Gelmir
tags: [semver, versioning, release, git]
---
# Semver 辅助工具

关于 Semantic Versioning 2.0.0 的快速参考指南。

## 版本格式

`MAJOR.MINOR.PATCH`（例如：`1.2.3`）

## 何时升级版本

| 版本级别 | 升级时机 | 例子 |
|-------|-----------|---------|
| **MAJOR**（X.0.0） | 引入破坏性变更 | 移除某个 API、更改功能行为 |
| **MINOR**（0.X.0） | 添加新功能（向后兼容） | 添加新函数、新参数 |
| **PATCH**（0.0.X） | 修复错误（向后兼容） | 修复程序崩溃、拼写错误 |

## 快速检查

```bash
# Analyze changes and suggest version bump
uv run python main.py suggest --from 1.0.0 --changes "feat: add auth, fix: null pointer"

# Or check what a specific change means
uv run python main.py check "breaking: remove old API"
```

## 规则

1. **MAJOR** — 任何导致不兼容的 API 变更
2. **MINOR** — 添加新功能（向后兼容）
3. **PATCH** — 修复错误（向后兼容）

## 预发布版本

预发布版本使用以下后缀：
- `1.0.0-alpha.1`
- `1.0.0-beta.2`
- `1.0.0-rc.1`

## 常见错误

- 不要因为添加新功能而升级 **MAJOR** 版本
- 不要因为修复错误而升级 **MINOR** 版本
- 升级到更高版本时，不要将版本号重置为更低的数字：例如，`1.2.3` 不应升级为 `2.2.3`，而应升级为 `2.0.0`