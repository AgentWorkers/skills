---
name: review-evo
description: 一个能够自我提升的代码审查工具：它会随着时间的推移逐渐了解你的代码库。它会分析 Git 的历史记录，发现代码中的规律，识别潜在的风险，并且每次运行时都会变得更加智能。
homepage: https://github.com/8co/review-evo
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["git"]}}}
---
# ReviewEvo

这是一个能够自我提升的代码审查工具。它能够分析你的 Git 代码历史记录，识别潜在的风险点，学习你团队的编码规范，并构建一个持续的知识库，以提升每次代码审查的效率。

**无需使用任何外部服务、API 密钥或依赖项。** 它仅依赖 Git 以及代理程序内置的工具。

**请按照以下步骤操作。** 在进行下一步之前，请确保每个步骤都已完成。

## 先决条件

确认 Git 是否可用：

- 运行 `git --version` 并查看输出结果。

用户必须位于一个至少有 20 个提交记录的 Git 仓库中。运行 `git rev-list --count HEAD` 来验证。如果提交记录少于 20 个，应提醒用户分析结果可能不完整，但仍然可以继续进行审查。

## 第 1 步 — 检查项目并加载之前的分析结果

**如果存在 `.review-evo/learnings.md` 文件：** 全部阅读该文件。其中包含了之前审查的发现结果。在本次审查过程中参考这些信息，确认已解决的问题，追踪重复出现的模式，并在此基础上进行进一步的分析。告诉用户：“我发现了之前审查中的有用信息，我会在此基础上继续进行审查。”

**如果文件不存在：** 这是首次使用该工具。告诉用户你将在分析完成后创建知识库。

接下来，通过检查仓库根目录中的以下文件来确定项目的类型：
- `tsconfig.json` → TypeScript 项目
- `package.json` → Node.js 项目（查看 `scripts` 文件以获取构建、测试和代码检查的命令）
- `requirements.txt` 或 `pyproject.toml` → Python 项目
- `go.mod` → Go 项目
- `Cargo.toml` → Rust 项目
- `pom.xml` 或 `build.gradle` → Java 项目

将分析结果告知用户并得到确认。

## 第 2 步 — 分析 Git 历史记录

运行以下命令并记录输出结果。不要过早总结——在得出结论之前，请收集所有数据。

**最近的活动（过去 50 个提交）：**
```
git log --oneline -50
```

**贡献者分布：**
```
git log --since="6 months ago" --format="%an" | sort | uniq -c | sort -rn
```

**修改频率较高的文件：**
```
git log --since="3 months ago" --diff-filter=M --name-only --pretty=format: | sort | uniq -c | sort -rn | head -25
```

**最近有较大修改的文件（可能存在复杂性问题）：**
```
git log --since="1 month ago" --pretty=format:"%h %s" --shortstat | head -60
```

**作者分布较广的文件（存在知识传播风险）：**
```
git log --since="6 months ago" --pretty=format:"%an" --name-only | awk '/^$/{next} !author{author=$0;next} {files[author][$0]++; allfiles[$0]++} END{for(f in allfiles) {n=0; for(a in files) if(f in files[a]) n++; if(n>1) print n,f}}' | sort -rn | head -15
```

如果平台不支持 `awk` 命令，可以改为手动统计每个文件的唯一作者数量：
```
git log --since="6 months ago" --format="%an" --name-only | head -200
```

## 第 3 步 — 构建审查报告

利用第 2 步收集的数据，分析并报告以下方面：

### 高频修改的文件
在 3 个月内被修改超过 5 次的文件属于风险点。对于这些文件：
- 阅读文件内容
- 评估代码的复杂性（函数数量、嵌套深度、行数）
- 标记那些缺乏相应测试覆盖的文件（查找对应的 `*.test.*`、`*.spec.*` 或 `test_*` 文件）

### 编码规范
从最近的提交记录和文件内容中，识别以下规范：
- 文件命名规则（驼峰式、蛇形式或 kebab 式）
- 导入语句的写法（相对路径还是绝对路径）
- 错误处理方式（try/catch 结构、Result 类型、错误回调）
- 代码注释的密度和格式

### 风险指标
标记以下情况：
- 长度超过 400 行且没有测试的文件
- 长度超过 50 行的函数
- 存在超过 30 天未解决的 TODO 或 FIXME 问题（通过 `git log -1 --format=%cr` 查看相关提交记录）
- 存在已知问题的依赖项
- 关键路径上由单一作者维护的文件（存在维护风险）

### 代码库的优势
同时也要识别代码库的优点：
- 一致的编码规范
- 良好的测试覆盖范围
- 代码职责划分清晰
- Git 历史记录中可见的近期改进

## 第 4 步 — 提交审查结果

询问用户希望关注哪些方面：
> 您希望我重点审查哪些内容？
> **(a)** 全部代码库的健康状况报告
> **(b)** 特定的分支或 Pull Request 的差异（提供分支名称）
> **(c)** 当前的代码变更（`git diff`）
> **(d)** 某个具体的文件或目录

### 对于选项 (a) — 全部代码库健康状况报告
将第 3 步的所有发现结果整理成一份结构化的报告，包括风险点、问题、优势和建议。根据问题的严重程度对结果进行排序（严重、警告、信息）。

### 对于选项 (b) — 分支/Pull Request 审查
运行 `git diff main...{branch}`（或目标分支）。根据第 3 步中发现的规范来分析代码差异，标记不符合规范的之处、新引入的风险以及缺失的测试覆盖。

### 对于选项 (c) — 当前的代码变更
运行 `git diff` 和 `git diff --cached`，并应用与选项 (b) 相同的分析方法。

### 对于选项 (d) — 定向审查
阅读指定的文件，根据发现的规范和编码规则提供有针对性的反馈。

对于所有选项，每条反馈内容应包括：
- **问题或观察结果：** 具体的问题或现象
- **位置：** 文件和具体行号
- **影响：** 对代码的可维护性、可靠性或安全性的影响
- **建议：** 具体的修复方案或改进建议

## 第 5 步 — 保存分析结果

审查完成后，将分析结果保存下来以便后续使用。

如果目录不存在，请创建该目录：
```
mkdir -p .review-evo
```

将分析结果写入（或追加到）`.review-evo/learnings.md` 文件中，格式如下：
```markdown
## Review — {YYYY-MM-DD}

### Project Profile
- Language: {detected}
- Key patterns: {conventions found}
- Active contributors: {count}

### Hotspots
{list of high-churn files with context}

### Recurring Patterns
{patterns that appeared in this and prior reviews}

### Resolved
{items from prior reviews that are no longer flagged}

### Open Risks
{current findings ranked by severity}
```

如果文件已存在，只需追加新的分析内容。不要覆盖之前的记录——历史数据是非常有价值的。

告诉用户：“分析结果已保存。下次审查这个项目时，我会参考这些信息。”

另外，建议将 `.review-evo/` 添加到项目的 `.gitignore` 文件中（如果该文件还不存在的话）。这些文件属于本地分析生成的文件，不属于源代码。

## 常见问题及解决方法：

- **“不是 Git 仓库”**：请在 Git 仓库内运行该工具，或者提供仓库的路径。
- **`awk` 命令失败**：某些平台的 `awk` 功能可能有限。该工具为每个分析步骤提供了备用命令。
- **仓库规模过大（超过 10,000 个提交）**：`--since` 参数有助于限制查询范围。如果查询仍然缓慢，可以缩小时间范围。
- **单仓库项目**：请询问用户需要关注哪个子目录，并使用 `-- {path}` 来限制 Git 命令的执行范围。