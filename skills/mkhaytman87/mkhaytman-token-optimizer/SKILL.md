---
name: token-optimizer
description: 通过上下文压缩、工具调用去重分析、模型选择指导以及会话状态检查，自动分析并减少 OpenClaw 中令牌的浪费。当会话接近上下文使用限制、成本持续上升，或在执行高成本任务之前希望进行主动的令牌优化时，可以使用该功能。
---

# 令牌优化器（Token Optimizer）

## 概述

使用此工具可以通过本地命令行界面（CLI）来优化 OpenClaw 的令牌使用情况。该工具支持执行分析、压缩快照生成、健康状况检查、清理计划制定以及飞行前（preflight）的令牌预算规划等功能。

## 快速入门

```bash
$OPENCLAW_SKILLS_DIR/token-optimizer/scripts/token-optimize --analyze --period 7d
```

## 核心命令

1) 启用本地优化器配置：
```bash
$OPENCLAW_SKILLS_DIR/token-optimizer/scripts/token-optimize --enable
```

2) 优化分析：
```bash
$OPENCLAW_SKILLS_DIR/token-optimizer/scripts/token-optimize --analyze --period 7d
```

3) 强制生成上下文压缩快照：
```bash
$OPENCLAW_SKILLS_DIR/token-optimizer/scripts/token-optimize --compress --threshold 0.7 --session agent:main:main
```

4) 会话健康状况检查：
```bash
$OPENCLAW_SKILLS_DIR/token-optimizer/scripts/token-optimize --health-check --active-minutes 120
```

5) 自动执行清理计划：
```bash
$OPENCLAW_SKILLS_DIR/token-optimizer/scripts/token-optimize --cleanup
$OPENCLAW_SKILLS_DIR/token-optimizer/scripts/token-optimize --cleanup --apply
```

## 飞行前优化（Preflight Optimization）

在执行耗时较长的任务批次之前，建议先使用飞行前优化功能进行准备：
```bash
$OPENCLAW_SKILLS_DIR/token-optimizer/scripts/token-optimize \
  --preflight /path/to/actions.json \
  --session-limit 180000
```

`actions.json` 文件应包含计划执行的操作，示例格式如下：
```json
[
  {"type": "web_search", "query": "..."},
  {"type": "web_fetch", "url": "..."},
  {"type": "summarize", "target": "youtube"}
]
```

## 输出结果

- 压缩快照：`$OPENCLAW_WORKSPACE/token-usage/compressed/`
- 可选 JSON 输出格式：`--format json --output /path/file.json`
- 基线配置文件（通过 `--enable` 选项生成）：`$OPENCLAW_WORKSPACE/token-usage/token-optimizer.config.json`

## 默认设置

默认行为配置在文件 `config/defaults.json` 中。

如需修改默认设置，请使用以下命令：
```bash
$OPENCLAW_SKILLS_DIR/token-optimizer/scripts/token-optimize --config /path/custom.json --analyze
```

## 相关资源

- `scripts/token_optimize.py`：主命令行脚本
- `src/optimizer.py`：核心优化引擎
- `src/models.py`：模型选择逻辑
- `src/compression.py`：上下文压缩辅助函数
- `src/cleanup.py`：会话状态评估模块
- `references/operating-notes.md`：实现细节及安全操作指南

## 验证机制

```bash
python3 $OPENCLAW_SKILLS_DIR/.system/skill-creator/scripts/quick_validate.py \
  $OPENCLAW_SKILLS_DIR/token-optimizer
```