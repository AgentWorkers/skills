---
name: ci-flake-triage
description: 通过 JUnit XML 重试机制检测出运行不稳定的测试用例，并生成一份包含最不稳定测试用例的排查报告。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# CI 故障排查（CI Fault Triage）

使用此技能将 JUnit 重试产生的大量日志信息整理成一份重点突出的故障报告。

## 功能说明
- 读取一个或多个 JUnit XML 文件（例如：首次运行结果及重试结果）
- 汇总每个测试用例的状态（“通过”、“失败”、“跳过”、“错误”）
- 当某个测试用例同时出现“失败”和“通过”两种结果时，将其标记为可能存在故障的候选项
- 区分“持续性故障”（即反复发生的故障）和“偶发性故障”
- 打印出最容易出现故障的测试用例，以便优先进行稳定性优化工作

## 输入参数
可选参数：
- `JUNIT_GLOB`（默认值：`test-results/**/*.xml`）：需要处理的 JUnit XML 文件路径
- `TRIAGE_TOP`（默认值：`20`）：报告中显示的故障用例数量上限
- `OUTPUT_FORMAT`（`text` 或 `json`，默认值：`text`）：输出格式
- `FAIL_ON_PERSISTENT`（`0` 或 `1`，默认值：`0`）：如果存在持续性故障，则程序以非零状态退出
- `FAIL_ON_FLAKE`（`0` 或 `1`，默认值：`0`）：如果存在偶发性故障，则程序以非零状态退出

## 使用方法
- **文本报告格式**：
  ```bash
JUNIT_GLOB='artifacts/junit/**/*.xml' \
TRIAGE_TOP=15 \
bash skills/ci-flake-triage/scripts/triage-flakes.sh
```

- **JSON 格式（用于 CI 系统）**：
  ```bash
JUNIT_GLOB='artifacts/junit/**/*.xml' \
OUTPUT_FORMAT=json \
FAIL_ON_PERSISTENT=1 \
bash skills/ci-flake-triage/scripts/triage-flakes.sh
```

- **配合测试 fixture 使用**：
  ```bash
JUNIT_GLOB='skills/ci-flake-triage/fixtures/*.xml' \
bash skills/ci-flake-triage/scripts/triage-flakes.sh
```

## 输出规范
- 如果未启用任何故障检测机制，程序以 `0` 状态退出（默认行为）
- 如果 `FAIL_ON_PERSISTENT` 为 `1` 且检测到持续性故障，程序以 `1` 状态退出
- 如果 `FAIL_ON_FLAKE` 为 `1` 且检测到偶发性故障，程序以 `1` 状态退出
- 在文本模式下，程序会输出故障总结、最容易出现故障的测试用例列表以及所有持续性故障的详细信息
- 在 JSON模式下，程序会输出机器可读的故障总结和测试用例详细信息