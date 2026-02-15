---
name: pywayne-bin-gitstats
description: 分析和可视化 Git 提交时间分布。适用于用户需要分析 Git 仓库的提交模式、生成提交统计信息，以及按时间、小时或工作日来可视化提交活动的情况。该功能会在收到分析提交的请求时被触发，用于展示提交分布情况、可视化 Git 活动内容或生成提交时间统计报告。
---
# Pywayne Bin Gitstats

用于分析 Git 仓库的提交时间分布，并生成可视化图表。

## 快速入门

```bash
# Analyze current repository (default: current directory, current branch)
gitstats

# Specify custom output path
gitstats --save output.png

# Analyze with time filter
gitstats --since "2024-01-01"
```

## 使用示例

### 基本分析

```bash
# Analyze current repository
gitstats

# Analyze specific repository path
gitstats /path/to/repo

# Show plot in popup window (no file saved)
gitstats -p
```

### 时间范围过滤

```bash
# Commits since specific date
gitstats --since "2024-01-01"

# Commits within date range
gitstats --since "2024-01-01" --until "2024-12-31"

# Relative time expressions
gitstats --since "1 year ago"
gitstats --since "90 days ago"
gitstats --until "30 days ago"
```

### 分支选择

```bash
# Analyze specific branch
gitstats --branch main
gitstats --branch develop
gitstats --branch origin/main

# Analyze all branches
gitstats --all
```

### 时区配置

```bash
# Use UTC timezone
gitstats --tz UTC

# Use specific timezone
gitstats --tz "America/New_York"
gitstats --tz "Europe/London"

# Default is Asia/Shanghai
gitstats --tz "Asia/Shanghai"
```

### 自定义输出

```bash
# Custom output filename
gitstats --save my_stats.png

# Output to subdirectory
gitstats --save results/commit_analysis.png

# Absolute path
gitstats --save /tmp/git_stats.png
```

### 综合示例

```bash
# All branches, last year, custom output
gitstats --since "1 year ago" --all --save yearly_stats.png

# Main branch, last 90 days, UTC timezone
gitstats --branch main --since "90 days ago" --tz UTC

# Develop branch, date range, show plot
gitstats --branch develop --since "2024-01-01" --until "2024-06-30" -p
```

## 命令参考

| 参数 | 描述 |
|----------|-------------|
| `repo` | Git 仓库路径。默认：当前目录 |
| `--since` | 开始时间（例如："2024-01-01"、"1年前"、"90天前"） |
| `--until` | 结束时间（格式与 --since 相同） |
| `--tz` | 时区。默认："Asia/Shanghai"。示例："UTC"、"America/New_York" |
| `--branch` | 要分析的特定分支。示例："main"、"develop"、"origin/main" |
| `--all` | 分析所有分支（覆盖 --branch 的设置） |
| `--save` | 输出图像路径。默认："git_time_distribution.png" |
| `-p`, `--show-plot` | 在弹出窗口中显示图表，不保存文件 |

## 输出图表

生成一个 3×2 的子图布局可视化图表：

1. **每日提交次数** - 显示每日提交次数的折线图 |
2. **按小时划分的提交次数** - 0-23 小时的柱状图 |
3. **按工作日划分的提交次数** - 星期一至周日的柱状图 |
4. **热力图：工作日 × 小时** - 用颜色编码表示活动情况

图表标题包含：仓库名称、分支名称和时区。

## 分支选择优先级：

1. 如果指定了 `--all`，则分析所有分支 |
2. 如果指定了 `--branch`，则仅分析该分支 |
3. 如果两者均未指定，则使用当前的 HEAD 分支 |

## 系统要求：

- 必须安装 Git |
- 需要 Python 库：pandas、matplotlib（随 pywayne 一起安装）

## 注意事项：

- 时间范围可以使用 Git 的灵活日期格式（绝对日期、相对表达式） |
- 如果输出文件已存在，将会被覆盖 |
- 对于包含大量分支的仓库，使用 `--all` 时处理时间可能会较长 |
- 提交时间首先以 UTC 格式解析，然后再转换为目标时区