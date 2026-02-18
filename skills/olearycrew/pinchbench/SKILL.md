---
name: pinchbench
description: 运行 PinchBench 基准测试，以评估 OpenClaw 代理在各种实际任务中的性能。该工具适用于测试模型功能、比较模型性能、将基准测试结果提交到排行榜，以及检查您的 OpenClaw 配置在处理日历管理、电子邮件处理、研究任务、编码工作以及多步骤工作流程等方面的表现。
metadata:
  author: pinchbench
  version: "1.0.0"
  homepage: https://pinchbench.com
  repository: https://github.com/pinchbench/skill
---
# PinchBench基准测试技能

PinchBench用于评估大型语言模型（LLM）作为OpenClaw代理“大脑”的性能。测试结果会发布在[pinchbench.com](https://pinchbench.com)的公共排行榜上。

## 先决条件

- Python 3.10及以上版本
- [uv](https://docs.astral.sh/uv/)包管理器
- OpenClaw实例（该代理程序）

## 快速入门

```bash
cd <skill_directory>

# Run benchmark with a specific model
uv run benchmark.py --model anthropic/claude-sonnet-4

# Run only automated tasks (faster)
uv run benchmark.py --model anthropic/claude-sonnet-4 --suite automated-only

# Run specific tasks
uv run benchmark.py --model anthropic/claude-sonnet-4 --suite task_01_calendar,task_02_stock

# Skip uploading results
uv run benchmark.py --model anthropic/claude-sonnet-4 --no-upload
```

## 可用任务（共23个）

| 任务 | 类别 | 描述 |
|------|----------|-------------|
| `task_00_sanity` | 基础 | 验证代理程序是否正常工作 |
| `task_01_calendar` | 生产力 | 创建日历事件 |
| `task_02_stock` | 研究 | 查询股票价格 |
| `task_03_blog` | 写作 | 创建博客文章 |
| `task_04_weather` | 编程 | 编写天气相关脚本 |
| `task_05_summary` | 分析 | 文档摘要 |
| `task_06_events` | 研究 | 会议资料整理 |
| `task_07_email` | 写作 | 起草电子邮件 |
| `task_08_memory` | 记忆 | 提取上下文信息 |
| `task_09_files` | 文件处理 | 创建文件结构 |
| `task_10_workflow` | 集成 | 多步骤API工作流程 |
| `task_11_clawdhub` | 技能应用 | 与ClawHub交互 |
| `task_12_skill_search` | 技能发现 | 识别用户技能 |
| `task_13_image_gen` | 创意 | 生成图片 |
| `task_14_humanizer` | 写作 | 使文本更具人性化 |
| `task_15_daily_summary` | 生产力 | 每日总结 |
| `task_16_email_triage` | 邮件管理 | 分类收件箱邮件 |
| `task_17_email_search` | 邮件搜索 | 搜索电子邮件 |
| `task_18_market_research` | 研究 | 市场分析 |
| `task_19_spreadsheet_summary` | 分析 | 电子表格数据分析 |
| `task_20_eli5_pdf_summary` | 分析 | 简化PDF文件内容 |
| `task_21_openclaw_comprehension` | 知识理解 | 理解OpenClaw文档 |
| `task_22_second_brain` | 记忆管理 | 知识存储与检索 |

## 命令行选项

| 选项 | 描述 |
|--------|-------------|
| `--model` | 模型标识符（例如：`anthropic/claude-sonnet-4`） |
| `--suite` | `all`、`automated-only`或用逗号分隔的任务ID列表 |
| `--output-dir` | 结果输出目录（默认：`results/`） |
| `--timeout-multiplier` | 为性能较慢的模型调整任务超时时间 |
| `--runs` | 每个任务的运行次数（用于计算平均值） |
| `--no-upload` | 不将结果上传到排行榜 |
| `--register` | 申请新的API令牌以提交结果 |
| `--upload FILE` | 上传之前的结果文件（JSON格式） |

## 令牌注册

要将测试结果提交到排行榜，请执行以下操作：

```bash
# Register for an API token (one-time)
uv run benchmark.py --register

# Run benchmark (auto-uploads with token)
uv run benchmark.py --model anthropic/claude-sonnet-4
```

## 结果保存

测试结果会以JSON格式保存在指定的输出目录中：

```bash
# View task scores
jq '.tasks[] | {task_id, score: .grading.mean}' results/0001_anthropic-claude-sonnet-4.json

# Show failed tasks
jq '.tasks[] | select(.grading.mean < 0.5)' results/*.json

# Calculate overall score
jq '{average: ([.tasks[].grading.mean] | add / length)}' results/*.json
```

## 添加自定义任务

在`tasks/`目录下创建一个遵循`TASK_TEMPLATE.md`格式的Markdown文件。每个自定义任务需要包含以下内容：

- YAML格式的前言部分（包含任务ID、名称、类别和评分类型）
- 任务提示
- 预期任务执行结果
- 评分标准
- 自动化检查机制（使用Python编写的评分函数）

## 排行榜

您可以在[pinchbench.com](https://pinchbench.com)查看测试结果。排行榜会显示：

- 模型的总体排名
- 各任务的详细表现
- 测试结果的历史趋势