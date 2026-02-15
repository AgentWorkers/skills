---
name: conventional-commits
description: 使用“Conventional Commits”规范来格式化提交信息。在创建提交、编写提交消息时，或者当用户提到提交、Git提交或提交消息时，都应遵循这一规范。这能确保提交信息符合自动化工具、变更日志生成以及语义版本控制的标准格式。
license: MIT
metadata:
  author: github.com/bastos
  version: "2.0"
---

# 常规提交规范

所有提交信息都应遵循 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) 规范进行格式化。这有助于自动生成变更日志、实现语义版本控制，并提升提交历史的可读性。

## 格式结构

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## 提交类型

### 必需的类型

- **`feat:`** - 新功能的添加（在语义版本控制中对应于 MINOR 版本更新）
- **`fix:`** - 错误的修复（在语义版本控制中对应于 PATCH 版本更新）

### 常见的附加类型

- **`docs:`** - 仅涉及文档的修改
- **`style:`** - 代码风格的调整（如格式问题、缺少分号等）
- **`refactor:`** - 代码重构（不涉及错误修复或新功能的添加）
- **`perf:`** - 性能优化
- **`test:`** - 测试用例的添加或更新
- **`build:`** - 构建系统或外部依赖关系的更改
- **`ci:`** - 持续集成/持续部署（CI/CD）配置的更改
- **`chore:`** - 不修改源代码或测试文件的其他操作
- **`revert:`** - 回滚之前的提交

## 提交范围

可选的提交范围可以提供关于代码库中具体修改部分的额外上下文信息：

```
feat(parser): add ability to parse arrays
fix(auth): resolve token expiration issue
docs(readme): update installation instructions
```

## 描述

- 描述应紧跟在类型/范围之后，使用祈使句式（例如：“添加功能”而非“added feature”或“adds feature”）
- 首字母不需大写
- 描述末尾不要加句号
- 保持简洁（通常 50-72 个字符）

## 提交正文

- 可以提供更详细的解释性内容
- 描述后应换行开始
- 可以包含多段文字
- 说明修改的内容及其原因，而非具体的实现方式

## 预示性变更（Breaking Changes）

可以通过以下两种方式标记预示性变更：

### 1. 在类型/范围中添加 `!` 标识

```
feat!: send an email to the customer when a product is shipped
feat(api)!: send an email to the customer when a product is shipped
```

### 2. 使用专门的 `BREAKING CHANGE` 底部注释

```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

### 3. 结合使用这两种方式

```
chore!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

## 示例

### 简单的功能添加

```
feat: add user authentication
```

### 带有范围的功能添加

```
feat(auth): add OAuth2 support
```

### 带有详细说明的错误修复

```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.
```

### 预示性变更

```
feat!: migrate to new API client

BREAKING CHANGE: The API client interface has changed. All methods now
return Promises instead of using callbacks.
```

### 文档更新

```
docs: correct spelling of CHANGELOG
```

### 多段描述并包含底部注释

```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```

## 编写指南

1. **必须使用类型**：每个提交都应以类型开头，后跟冒号和空格。
2. **使用祈使句式**：描述应明确表达“如果应用该提交，将会发生什么”。
3. **具体说明**：描述应清晰地说明修改的内容。
4. **保持专注**：每次提交只针对一个逻辑上的修改。
5. **在必要时使用范围**：范围有助于对代码库中的修改进行分类。
6. **明确标注预示性变更**：务必清楚地标记出预示性变更。

## 语义版本控制对应关系

- **`fix:`** → 表示 PATCH 版本更新（例如：1.0.0 → 1.0.1）
- **`feat:`** → 表示 MINOR 版本更新（例如：1.0.0 → 1.1.0）
- **BREAKING CHANGE** → 表示 MAJOR 版本更新（例如：1.0.0 → 2.0.0）

## 使用场景

- 所有 Git 提交
- 生成提交日志时
- 在合并 Pull Request 时
- 当用户询问提交信息或 Git 提交操作时

## 需避免的常见错误

❌ `Added new feature`（使用过去时态，首字母大写）
✅ `feat: add new feature`（使用祈使句式，首字母小写）
❌ `fix: bug`（描述过于模糊）
✅ `fix: resolve null pointer exception in user service`（描述不够具体）
❌ `feat: add feature`（描述重复）
✅ `feat: add user profile page`（描述冗余）
❌ `feat: Added OAuth support.`（使用过去时态，描述末尾加句号）
✅ `feat: add OAuth support`（描述简洁明了）