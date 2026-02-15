---
name: context-builder
description: 使用 `context-builder CLI` 从任意目录生成针对 LLM（大型语言模型）优化的代码库上下文。
homepage: https://github.com/igorls/context-builder
version: 0.7.1
requires:
  - cargo
  - context-builder
---
# Context Builder — 一种智能的代码分析工具

该工具可以从任意代码库目录生成结构化的 Markdown 文件，适用于大型语言模型（LLM）的阅读。生成的文件经过优化，具备基于相关性的文件排序、自动的令牌预算控制以及智能的默认配置。

## 安装

```bash
cargo install context-builder
```

验证安装结果：`context-builder --version`

## 使用场景

- **深度代码审查**：将整个代码库输入到大型语言模型中，用于架构分析或错误排查。
- **新员工入职**：生成项目快照，帮助理解不熟悉的代码库。
- **基于差异的更新**：在代码更改后，仅生成差异部分，以更新大型语言模型的理解。
- **跨项目研究**：快速打包依赖项的源代码以供分析。

## 核心工作流程

### 1. 全项目上下文（快速生成）

```bash
context-builder -d /path/to/project -y -o context.md
```

- 使用 `-y` 选项可跳过确认提示（非交互式使用时必备）。
- 输出内容包括：头部文件、文件树以及按相关性排序的文件（配置文件、源代码文件、测试文件、文档文件）。

### 2. 指定类型的文件上下文

```bash
context-builder -d /path/to/project -f rs,toml -i docs,assets -y -o context.md
```

- 使用 `-f rs,toml` 选项仅包含 Rust 和 TOML 文件。
- 使用 `-i docs,assets` 选项可排除指定的目录。

### 3. 令牌预算限制

```bash
context-builder -d /path/to/project --max-tokens 100000 -y -o context.md
```

- 将输出长度限制在约 10 万个令牌以内。
- 文件会按相关性顺序被包含在输出中，直到令牌预算用完。
- 如果输出超过 12.8 万个令牌，系统会自动发出警告。

### 4. 令牌数量预览

```bash
context-builder -d /path/to/project --token-count
```

- 先显示令牌数量的预估值，无需生成实际输出。
- 可先使用此功能判断是否需要进一步过滤。

### 5. 增量差异分析

首先确保 `context-builder.toml` 文件存在：

```toml
timestamped_output = true
auto_diff = true
```

然后运行两次命令：

```bash
# First run: baseline snapshot
context-builder -d /path/to/project -y

# After code changes: generates diff annotations
context-builder -d /path/to/project -y
```

**（仅输出差异部分，不包含完整文件内容）**

## 智能默认配置

以下行为无需额外配置：

| 功能 | 默认设置 |
|---------|----------|
| **自动排除**：`node_modules`、`dist`、`build`、`__pycache__`、`.venv`、`vendor` 等目录会被自动排除。 |
| **自我排除**：输出文件、缓存目录以及 `context-builder.toml` 本身也会被自动排除。 |
| **`.gitignore` 文件**：如果存在 `.git` 目录，会自动应用 `.gitignore` 规则。 |
| **二进制文件检测**：通过 UTF-8 标识自动跳过二进制文件。 |
| **文件排序**：配置文件和文档文件优先显示，接着是源代码文件（入口文件在前），然后是测试文件、构建/持续集成相关文件、锁定文件。

## 命令行参考（与代理相关的语法）

| 选项 | 作用 | 使用说明 |
|------|---------|----------------|
| `-d <路径>` | 指定输入目录 | 为确保准确性，请始终使用绝对路径。 |
| `-o <输出路径>` | 指定输出文件路径 | 可将结果写入临时目录或文档目录。 |
| `-f <文件扩展名>` | 按文件扩展名过滤文件 | 例如：`-f rs,toml,md`。 |
| `-i <要排除的目录/文件>` | 指定要排除的目录或文件 | 例如：`-i tests,docs,assets`。 |
| `--max-tokens <令牌上限>` | 设置令牌使用上限 | 对于大多数模型使用 `100000`，Gemini 模型使用 `200000`。 |
| `--token-count` | 预估令牌数量 | 先运行此选项判断是否需要过滤。 |
| `-y` | 跳过所有提示 | **在代理工作流程中必须使用此选项**。 |
| `--preview` | 仅显示文件树结构 | 快速查看文件结构而不生成输出。 |
| `--diff-only` | 仅输出差异部分 | 适用于增量更新，以减少令牌消耗。 |
| `--init` | 自动创建配置文件 | 自动识别项目中的文件类型。 |

## 使用示例

### 示例：深度代码审查

生成指定范围的上下文文件，然后提交给大型语言模型进行深入分析：

```bash
# Step 1: Generate focused context
context-builder -d /path/to/project -f rs,toml --max-tokens 120000 -y -o docs/deep_think_context.md

# Step 2: Feed to LLM with a review prompt
# Attach docs/deep_think_context.md and ask for:
# - Architecture review
# - Bug hunting
# - Performance analysis
```

### 示例：比较两个版本

```bash
# Generate context for both versions
context-builder -d ./v1 -f py -y -o /tmp/v1_context.md
context-builder -d ./v2 -f py -y -o /tmp/v2_context.md

# Feed both to an LLM for comparative analysis
```

### 示例：从单仓库中提取特定部分进行分析

```bash
# Focus on a specific package within a monorepo
context-builder -d /path/to/monorepo/packages/core -f ts,tsx -i __tests__,__mocks__ -y -o core_context.md
```

### 示例：在制定策略前快速检查文件数量

```bash
# Check if the project fits in context
context-builder -d /path/to/project --token-count

# If > 128K tokens, scope it down:
context-builder -d /path/to/project -f rs,toml --max-tokens 100000 --token-count
```

## 配置文件（可选）

在项目根目录下创建 `context-builder.toml` 文件以保存配置：

```toml
output = "docs/context.md"
output_folder = "docs"
filter = ["rs", "toml"]
ignore = ["target", "benches"]
timestamped_output = true
auto_diff = true
max_tokens = 120000
```

可以使用 `context-builder --init` 自动初始化配置。

## 输出格式

生成的 Markdown 文件遵循以下结构：

    # 目录结构报告
    [项目名称、过滤规则、内容哈希值]

    ## 文件树
    [包含的文件结构可视化展示]

    ## 文件列表
    ### 文件：src/main.rs
    [代码块，文件内容按扩展名高亮显示]

    ### 文件：src/lib.rs
    ...

文件会按照**相关性顺序**显示（而非字母顺序），优先显示配置文件和入口文件，从而帮助大型语言模型更快地理解项目结构。

## 错误处理

- 如果未安装 `context-builder`，请使用 `cargo install context-builder` 进行安装。
- 如果输出超出令牌限制，可以使用 `--max-tokens` 选项设置上限，或通过 `-f` 和 `-i` 选项缩小筛选范围。
- 即使项目没有 `.git` 目录，系统也会自动排除相关文件，以防止依赖项信息过多。
- 如果差异输出显得过时或不准确，可以使用 `--clear-cache` 选项清除缓存。