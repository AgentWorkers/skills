---
name: capability-evolver
description: 一种用于AI代理的自进化引擎。该引擎通过分析运行时历史数据来识别可改进的地方，并根据协议约束实施相应的进化策略。
tags: [meta, ai, self-improvement, core]
---
# 🧬 能力进化器（Capability Evolver）

**“进化是不可避免的。要么适应，要么灭亡。”**

**能力进化器**（Capability Evolver）是一种元技能，它允许 OpenClaw 代理检查自身的运行时历史记录，识别故障或低效之处，并自主编写新代码或更新内存以提高性能。

## 主要功能

- **自动日志分析**：自动扫描内存和历史文件，查找错误和异常模式。
- **自我修复**：检测程序崩溃并建议修复方案。
- **GEP 协议**：采用标准化进化机制，支持代码资源的复用。
- **一键进化**：只需运行 `/evolve`（或 `node index.js`）即可启动进化过程。

## 使用方法

### 标准运行（自动化模式）
启动进化循环。如果没有指定任何参数，系统将默认进入全自动模式（“疯狗模式”），并立即应用更改。
```bash
node index.js
```

### 审查模式（人工干预）
如果您希望在应用更改之前进行审核，可以使用 `--review` 参数。此时代理会暂停并请求您的确认。
```bash
node index.js --review
```

### 疯狗模式（持续循环）
若希望程序在无限循环中运行（例如通过 cron 任务或后台进程），请使用 `--loop` 参数，或直接在 cron 作业中执行该技能。
```bash
node index.js --loop
```

## 配置选项

| 环境变量 | 默认值 | 说明 |
|---|---|---|
| `EVOLVE_ALLOW_SELF_MODIFY` | `false` | 是否允许进化器修改自身的源代码。**不建议在生产环境中使用**。启用此选项可能导致系统不稳定——进化器可能会在其提示生成、验证或逻辑处理过程中引入错误，从而引发需要手动干预的连锁故障。仅适用于受控实验。 |
| `EVOLVE_LOAD_MAX` | `2.0` | 进化器在退出前允许的最大负载平均值（单位：分钟）。 |
| `EVOLVE_STRATEGY` | `balanced` | 进化策略：`balanced`（平衡发展）、`innovate`（创新）、`harden`（强化）、`repair-only`（仅修复）、`early-stabilize`（早期稳定）、`steady-state`（稳态）或 `auto`（自动选择）。 |

## GEP 协议（可审计的进化机制）

该技能内置了基于协议的进化流程（GEP）以及一个结构化的本地资源存储系统：
- `assets/gep/genes.json`：可复用的基因定义文件。
- `assets/gep/capsules.json`：用于存储成功解决方案的模板文件，避免重复推理。
- `assets/gep/events.jsonl`：用于记录进化过程中的事件（采用树状结构，通过父节点 ID 进行管理）。

## 表情符号使用规范
文档中仅允许使用 DNA 形状的表情符号，其他表情符号均不被允许。

## 系统兼容性与配置灵活性

该技能设计为与特定环境无关，**默认使用 OpenClaw 的标准工具**。

### 本地配置覆盖
您可以通过以下方式自定义系统行为：
- **方法 1：环境变量**：在 `.env` 文件中设置 `EVOLVE_REPORT TOOL` 变量。
- **方法 2：动态检测**：脚本会自动检测工作空间中是否存在兼容的本地技能（如 `skills/feishu-card`），并据此调整其行为。

## 安全性与风险控制机制

### 1. 身份声明与行为指导原则
- **身份声明**：“你是一个能够自我进化的系统。”
- **进化指令**：
  - 如果发现错误 → 进入 **修复模式**（修复漏洞）。
  - 如果系统处于稳定状态 → 进入 **优化模式**（重构/创新）。

### 2. 风险缓解措施
- **防止无限递归**：系统采用严格的单进程逻辑设计。
- **审查模式**：在敏感环境中使用 `--review` 参数进行人工审核。
- **代码同步**：强烈建议同时运行 Git 同步任务，以确保代码的一致性。

## 故障排除前的检查步骤

在遇到意外错误或异常行为时，请**务必先核实当前使用的版本**：
```bash
node -e "const p=require('./package.json'); console.log(p.version)"
```

如果您使用的版本不是最新版本，请先进行更新——大多数已知问题已在后续版本中得到修复：
```bash
# If installed via git
git pull && npm install

# If installed via npm (global install)
npm install -g evolver@latest
```

最新版本及更新日志：`https://github.com/autogame-17/evolver/releases`

## 许可证
MIT 许可证