---
name: hle-benchmark-evolver
description: 负责执行基于HLE（Humanity’s Last Exam）框架的基准测试结果处理以及能力评估系统的课程生成功能。当用户请求优化“Humanity’s Last Exam”考试的得分、导入问题级别的基准测试结果、优先处理简单任务、或立即获取基准测试的进度信息时，可使用该功能。
tags: [benchmark, hle, evolution, reward, curriculum]
---
# HLE基准测试进化器（HLE Benchmark Evolver）

该技能实现了基于HLE（Human-Level Evaluation）分数的进化机制，适用于OpenClaw平台。

## 使用场景

- 用户希望提升HLE分数（例如目标分数 >= 60%）。
- 用户提供了问题级别的基准测试结果，并希望将其转换为相应的奖励。
- 用户希望获得易于学习的课程内容以及下一步需要关注的问题。
- 用户希望立即获取基准测试结果的快照。

## 输入参数

- 基准测试报告的JSON文件路径（`--report=/abs/path/report.json`）
- 可选的基准测试ID（默认值为`cais/hle`）

## 工作流程

1. 验证报告JSON文件的存在性及其可解析性。
2. 将报告数据导入到`capability-evolver`系统中的基准测试奖励状态模块。
3. 生成课程相关的信号数据：
   - `benchmark_*`
   - `curriculum_stage:*`
   - `focus_subject:*`
   - `focus_modality:*`
   - `question_focus:*`
4. 返回本次运行的结果摘要。

## 运行流程

```bash
node skills/hle-benchmark-evolver/run_result.js --report=/absolute/path/hle_report.json
```

（自动执行进化循环）

```bash
node skills/hle-benchmark-evolver/run_pipeline.js --report=/absolute/path/hle_report.json --cycles=1
```

如果您的评估工具可以从shell命令行调用，可以让流程在每次循环中自动生成报告：

```bash
node skills/hle-benchmark-evolver/run_pipeline.js \
  --report=/absolute/path/hle_report.json \
  --eval_cmd="python /path/to/eval_hle.py --out {{report}}" \
  --cycles=3 --interval_ms=2000
```

如果未提供`--report`参数，系统将默认使用以下路径：
`skills/capability-evolver/assets/gep/hle_report.template.json`

## 输出格式

输出结果必须为JSON格式，包含以下字段：
- `benchmark_id`
- `run_id`
- `accuracy`
- `reward`
- `trend`
- `curriculum_stage`
- `queue_size`
- `focus_subjects`
- `focus_modalities`
- `next_questions`

## 注意事项

- 该技能仅负责处理奖励和课程内容的生成与更新，不直接解决HLE相关的问题。
- `run_pipeline.js`脚本将数据导入、进化过程以及结果整合到一个可执行的循环中。