---
name: git-commit-helper
description: 生成符合 Conventional Commits 格式的标准化 Git 提交信息。当用户需要提交代码、编写提交信息或创建 Git 提交时，请使用此技能。确保遵循团队关于类型前缀、范围命名、消息长度以及重大变更文档化的约定。
---
# Git 提交信息指南

## 格式

每个提交信息都必须遵循以下结构：

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## 类型（必填）

| 类型 | 使用场景 |
|------|-------------|
| feat | 新功能或功能的添加 |
| fix | 修复错误 |
| docs | 仅用于文档更新 |
| refactor | 代码重构（既不修复问题也不添加新功能） |
| test | 添加或更新测试用例 |
| chore | 构建流程、持续集成（CI）或工具相关的更改 |

## 作用域（必填）

作用域必须是指该项目中的某个实际模块名称。请参阅 [references/modules.md](references/modules.md) 以获取完整模块列表。

如果不确定作用域，请查看被修改的文件路径——通常顶层目录就是正确的模块名称。

## 主题（必填）

- 使用祈使句式（例如：“add feature” 而不是 “added feature”）
- 主题结尾不能有句号
- 总长度不得超过 72 个字符（包括类型和作用域前缀）
- 首字母需小写

## 正文（可选）

- 需要解释修改的原因，而不是具体修改了什么（差异信息已经说明了修改内容）
- 每行内容长度控制在 72 个字符以内
- 正文需用空行与主题分隔

## 引入破坏性变更

如果提交引入了破坏性变更，请在提交信息末尾添加以下说明：

```
BREAKING CHANGE: <description of what breaks and migration path>
```

## 示例

**正确示例：**

```
feat(auth): add JWT token refresh endpoint

Tokens now auto-refresh 5 minutes before expiry.
Previously users had to re-login after token expiration.
```

```
fix(parser): handle empty input without crashing
```

```
refactor(db): extract connection pooling to separate module

BREAKING CHANGE: DatabaseClient constructor no longer accepts
pool config. Use PoolConfig.create() instead.
```

**错误示例：**

```
updated some stuff          ← no type, no scope, vague
feat: Add new Feature.      ← capitalized, period, missing scope
fix(misc): various fixes    ← "misc" is not a real module
```