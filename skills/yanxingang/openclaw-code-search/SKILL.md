# 代码搜索工具

这是一个用于快速搜索代码库的工具包，支持结构化的grep（内容搜索）、glob（文件名搜索）以及通过ripgrep、fd和tree CLI工具进行的目录结构搜索。

## 使用场景

- 在代码中查找函数/类/变量的定义或用法
- 按文件名或扩展名模式查找文件
- 了解项目的目录结构
- 探索不熟悉的代码库
- 查找配置文件、导入语句和错误信息

## 先决条件

请先运行依赖项检查：
```bash
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh check
```

## 命令

所有命令都通过一个统一的入口点执行：
```bash
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh <command> [options]
```

### grep — 搜索文件内容

```bash
# Basic search
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh grep "func main" --path /some/project

# Literal text (no regex interpretation)
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh grep "fmt.Println(" --literal --path /some/project

# Filter by file type
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh grep "import" --type go --path /some/project

# With context lines
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh grep "TODO" --context 2 --path /some/project

# Limit results
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh grep "error" --max 20 --path /some/project
```

选项：
- `--path <dir>` — 搜索目录（默认：当前目录）
- `--type <ext>` — 文件类型过滤器（如go、py、ts、js等，可重复使用）
- `--literal` — 将模式视为普通文本（而非正则表达式）
- `--max <n>` — 最多显示的结果数量（默认：100）
- `--context <n>` — 显示匹配项周围的N行上下文（默认：0）

### glob — 搜索文件名

```bash
# Find all Go files
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh glob "*.go" --path /some/project

# Find test files
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh glob "*_test.go" --path /some/project

# Find config files
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh glob "*.{json,yaml,yml,toml}" --path /some/project

# Filter by type
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh glob "config" --type f --path /some/project
```

选项：
- `--path <dir>` — 搜索目录（默认：当前目录）
- `--type <f|d>` — f=仅搜索文件，d=仅搜索目录
- `--max <n>` — 最多显示的结果数量（默认：200）

### tree — 显示目录结构

```bash
# Default (3 levels deep)
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh tree --path /some/project

# Shallow view
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh tree --path /some/project --depth 1

# With file sizes
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh tree --path /some/project --depth 2 --size
```

选项：
- `--path <dir>` — 目标目录（默认：当前目录）
- `--depth <n>` — 最大搜索深度（默认：3）
- `--size` — 显示文件大小

### check — 验证依赖关系

```bash
bash /root/.openclaw/workspace/skills/code-search/scripts/search.sh check
```

## 输出格式

所有命令的输出都是结构化文本，并使用明确的分隔符：
- `[SEARCH RESULTS: grep]` / `[SEARCH RESULTS: glob]` / `[DIRECTORY TREE]`
- `[END RESULTS]` / `[END TREE]`
- 当结果超出限制时，会显示 `[TRUNCATED: ...]`
- 出现错误时，会显示 `[ERROR] ...`

## 注意事项

- 所有操作均为只读操作，不会修改任何文件
- 自动忽略 `.git`、`node_modules`、`__pycache__`、`vendor` 和构建生成的文件
- 遵循 `.gitignore` 规则
- 对于 grep 和 glob 操作，结果会按照修改时间排序（最新文件优先显示）