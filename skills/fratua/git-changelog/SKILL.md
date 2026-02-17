---
name: git-changelog
description: 从 Git 历史中自动生成美观的变更日志，并按照常见的提交类型进行分组。
version: 1.0.0
author: Sovereign Skills
tags: [openclaw, agent-skills, automation, productivity, free, git, changelog, devops]
triggers:
  - generate changelog
  - create changelog
  - git changelog
  - release notes
---
# git-changelog — 自动生成变更日志

该工具可从 Git 提交历史中生成格式规范、分类清晰的变更日志，适用于生成 `CHANGELOG.md` 文件或用于 GitHub 发布。

## 使用步骤

### 1. 验证 Git 仓库

```bash
git rev-parse --is-inside-work-tree
```

如果验证失败，请停止操作——当前目录可能不是 Git 仓库。

### 2. 确定查询范围

用户可以指定以下查询范围：
- **标签范围**：`v1.0.0..v1.1.0`
- **从指定日期开始**：`--since="2025-01-01"`
- **最近 N 个提交**：`-n 50`
- **从最后一个标签开始**：通过 `git describe --tags --abbrev=0` 自动检测

默认行为是查找最后一个标签，并从该标签开始生成变更日志直到当前分支（HEAD）：

```bash
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
```

如果仓库中没有标签，工具将使用完整的提交历史记录。

### 3. 提取提交信息

```bash
# Tag-to-HEAD
git log ${LAST_TAG}..HEAD --pretty=format:"%H|%s|%an|%ad" --date=short

# Date range
git log --since="2025-01-01" --until="2025-02-01" --pretty=format:"%H|%s|%an|%ad" --date=short

# Full history
git log --pretty=format:"%H|%s|%an|%ad" --date=short
```

### 4. 按常规提交类型进行分类

解析每个提交的标题，并将其分类到相应的类别中：

| 前缀 | 类别 | 表示符号 |
|--------|----------|-------|
| `feat` | ✨ 新功能 | 新增的功能 |
| `fix` | 🐛 修复错误 | 修复的漏洞 |
| `docs` | 📚 文档 | 文档内容的修改 |
| `style` | 💄 格式调整 | 仅涉及格式更改，无逻辑变化 |
| `refactor` | ♻️ 代码重构 | 代码结构的调整 |
| `perf` | ⚡ 性能优化 | 提高性能 |
| `test` | ✅ 测试 | 添加/修改测试用例 |
| `build` | 📦 构建 | 构建系统或依赖项的调整 |
| `ci` | 👷 持续集成/持续部署 | 集成/部署流程的更改 |
| `chore` | 🔧 维护性工作 | 代码维护相关的操作 |
| *(其他)* | 📝 其他 | 未分类的更改 |

解析规则：`type(scope): description` 或 `type: description`

### 5. 生成 Markdown 格式的变更日志

输出格式如下：

```markdown
# Changelog

## [v1.2.0] — 2025-02-15

### ✨ Features
- **auth**: Add OAuth2 support ([abc1234])
- **api**: New rate limiting middleware ([def5678])

### 🐛 Bug Fixes
- **db**: Fix connection pool leak ([ghi9012])

### 📚 Documentation
- Update API reference ([jkl3456])
```

规则：
- 如果存在提交范围（如 `v1.0.0..v1.1.0`），请以粗体显示：`**v1.0.0..v1.1.0**`
- 提交的哈希值（如 `abc1234`）应包含在日志中以供引用
- 分类顺序为：新功能 → 修复错误 → 其他所有类别
- 空类别将被省略
- 如果提交内容中包含 `BREAKING CHANGE`，则在日志顶部添加一个 `### 💥 破坏性变更` 的章节

### 6. 标记破坏性变更

对于标记为破坏性变更的提交（如 `feat!: remove legacy API`），在提交类型后添加 `!` 标志：

### 7. 输出结果

- 默认情况下，将生成的变更日志输出到聊天界面供审核
- 如果用户要求，将日志内容写入或追加到项目根目录下的 `CHANGELOG.md` 文件中
- 如果需要更新现有的 `CHANGELOG.md` 文件，应在文件开头的 `# Changelog` 标签后插入新内容

## 特殊情况处理

- **没有常规分类的提交**：将所有提交归类为“其他”
- **合并提交**：除非用户特别要求，否则跳过合并提交（如 `Merge branch...`、`Merge pull request...`）
- **单仓库项目**：如果用户指定了路径，使用 `git log -- path/to/package` 命令获取提交信息
- **仓库中没有标签**：使用完整的提交历史记录或请求用户提供具体的日期范围
- **查询范围为空**：提示“在指定范围内未找到任何提交”

## 错误处理

| 错误类型 | 处理方法 |
|---------|-----------|
| 未找到 Git 仓库 | 告知用户请确认是否为 Git 仓库 |
| 未找到提交记录 | 重新确认查询范围或日期；建议用户提供更具体的范围 |
- 输出内容为二进制数据或格式混乱 | 确保使用了正确的命令参数 `--pretty=format` |
- 没有权限访问 `CHANGELOG.md` 文件 | 检查文件权限设置

---
*由 Clawb (SOVEREIGN) 开发——更多功能即将推出*