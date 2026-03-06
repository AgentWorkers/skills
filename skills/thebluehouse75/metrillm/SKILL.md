---
name: metrillm
description: 为您的机器找到最适合的本地大型语言模型（LLM）。测试模型的速度、质量以及与系统内存（RAM）的匹配程度，之后会告诉您该模型是否适合在您的硬件上运行。
argument-hint: "[model-name]"
author: MetriLLM
source: https://github.com/MetriLLM/metrillm
license: Apache-2.0
allowed-tools: Bash, Read
install: npm install -g metrillm
---
# MetriLLM — 为您的硬件寻找最适合的 Large Language Model（LLM）

测试任何本地模型，并获得一个明确的结论：它在您的机器上运行是否值得？

## 先决条件

1. **Node.js 20+** — 通过 `node -v` 命令检查版本。
2. **已安装并运行 Ollama** 或 **LM Studio**：
   - Ollama: [ollama.com](https://ollama.com)，然后运行 `ollama serve`。
   - LM Studio: [lmstudio.ai]，加载模型并启动服务器。
3. **MetriLLM CLI** — 全局安装：

```bash
npm install -g metrillm
```

## 使用方法

### 列出可用模型

```bash
ollama list
```

### 运行完整基准测试

```bash
metrillm bench --model $ARGUMENTS --json
```

该测试会评估以下方面：
- **性能**：每秒处理的令牌数、生成第一个令牌所需的时间、内存使用情况。
- **质量**：推理能力、数学运算能力、代码执行能力、指令遵循能力、输出结构化程度以及多语言支持能力。
- **适用性评估**：优秀 / 良好 / 一般 / 不推荐。

### 仅评估性能的基准测试（更快）

```bash
metrillm bench --model $ARGUMENTS --perf-only --json
```

此测试仅测量速度和内存使用情况，不进行质量评估。

### 查看之前的测试结果

```bash
ls ~/.metrillm/results/
```

阅读任何 JSON 文件以查看完整的基准测试详细信息。

### 将结果分享到公共排行榜

```bash
metrillm bench --model $ARGUMENTS --share
```

将您的测试结果上传到 [MetriLLM 社区排行榜](https://metrillm.dev) — 这是一个由社区共同维护的、基于实际硬件环境的本地 LLM 性能排名系统。您可以与其他用户比较结果，帮助社区找到最适合您硬件环境的模型。共享的数据包括：模型名称、得分以及硬件规格（CPU、RAM、GPU）。不会发送任何个人数据。

## 解读测试结果

| 评估结果 | 得分 | 含义 |
|---|---|---|
| 优秀 | >= 80 | 性能快速且准确 — 非常适合使用 |
| 良好 | >= 60 | 性能稳定 — 适合大多数任务 |
| 一般 | >= 40 | 可以使用，但存在一定的局限性 |
| 不推荐 | < 40 | 运行速度太慢或准确性不足 |

需要重点关注的指标：
- `tokensPerSecond` > 30：适合交互式使用。
- `ttft` < 500ms：响应时间快。
- `memoryUsedGB` 与可用 RAM 的比例：模型是否能在您的硬件上正常运行？

## 提示

- 使用 `--perf-only` 选项进行快速测试。
- 在进行基准测试前关闭占用大量 GPU 资源的应用程序。
- 基准测试的持续时间会因模型性能和输出长度而有所不同。

## 开源特性

MetriLLM 是免费且开源的（基于 Apache 2.0 许可协议）。欢迎贡献代码、报告问题并提供反馈：[github.com/MetriLLM/metrillm](https://github.com/MetriLLM/metrillm)