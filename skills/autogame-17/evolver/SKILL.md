---
name: capability-evolver
description: 一种用于AI代理的自进化引擎。该引擎通过分析运行时历史数据来识别改进点，并根据协议约束进行相应的进化操作。
tags: [meta, ai, self-improvement, core]
---
# 🧬 能力进化器 (Capability Evolver)

**“进化是不可避免的。要么适应，要么灭亡。”**

**能力进化器**（Capability Evolver）是一种元技能，它允许 OpenClaw 代理检查自身的运行时历史记录，识别故障或低效之处，并自主生成新代码或更新内存以提升性能。

## 主要功能

- **自动日志分析**：自动扫描内存和历史文件，查找错误和潜在问题。
- **自我修复**：检测系统崩溃并建议修复方案。
- **GEP 协议**：采用标准化进化机制，支持代码资源的复用。
- **一键进化**：只需运行 `/evolve`（或 `node index.js` 即可）。

## 使用方法

### 标准运行（自动化模式）
自动执行进化流程。如果没有指定任何参数，系统将进入完全自动化模式（“疯狗模式”），并立即应用更改。
```bash
node index.js
```

### 审查模式（人工干预）
如果您希望在应用更改前进行审核，请使用 `--review` 参数。代理会暂停并请求您的确认。
```bash
node index.js --review
```

### 疯狗模式（持续循环）
若希望系统在无限循环中运行（例如通过 cron 任务或后台进程），请使用 `--loop` 参数。
```bash
node index.js --loop
```

## 设置步骤

在使用此技能之前，请先在 EvoMap 网络中注册您的节点身份：

1. 通过 `evomap.js` 或 EvoMap 的入门流程运行相关命令，以获取 `node_id` 和配置代码。
2. 在 24 小时内访问 `https://evomap.ai/claim/<claim-code>` 将节点与您的账户关联起来。
3. 在您的环境中配置节点身份：
   ```bash
export A2A_NODE_ID=node_xxxxxxxxxxxx
```

   或者在您的代理配置文件（例如 `~/.openclaw/openclaw.json`）中设置：
   ```json
{ "env": { "A2A_NODE_ID": "node_xxxxxxxxxxxx", "A2A_HUB_URL": "https://evomap.ai" } }
```

**注意**：切勿在脚本中硬编码节点 ID。`src/gep/a2aProtocol.js` 中的 `[nodeId()` 会自动读取 `A2A_NODE_ID`；任何使用该协议的脚本都会自动获取该 ID，无需额外配置。

## 配置参数

| 环境变量 | 默认值 | 说明 |
|---|---|---|
| `A2A_NODE_ID` | （必填） | 您的 EvoMap 节点身份。请在节点注册后设置此值，切勿在脚本中硬编码。`a2aProtocol.js` 会自动读取该值。 |
| `EVOLVE_ALLOW_SELF_MODIFY` | `false` | 是否允许进化器修改自身的源代码。**不建议在生产环境中使用**。启用此功能可能导致系统不稳定——进化器可能会在其提示生成、验证或逻辑处理过程中引入错误，从而引发连锁故障，需要手动干预。仅适用于受控实验。 |
| `EVOLVE_LOAD_MAX` | `2.0` | 进化器在退出前允许的最大负载平均值（单位：分钟）。 |
| `EVOLVE_STRATEGY` | `balanced` | 进化策略：`balanced`（平衡发展）、`innovate`（创新）、`harden`（强化）、`repair-only`（仅修复）、`early-stabilize`（早期稳定）、`steady-state`（稳态）或 `auto`（自动选择）。 |
| `EVOLVER_ROLLBACK_MODE` | `hard` | 进化失败时的回滚策略：`hard` 表示使用 `git reset --hard`（破坏性操作，恢复到初始状态）；`stash` 表示使用 `git stash` 保存更改以备恢复；`none` 表示完全跳过回滚。在活跃的工作空间中使用 `stash` 可提高安全性。 |

## GEP 协议（可审计的进化机制）

该技能嵌入了基于协议的进化机制（GEP）和本地结构化资源存储：

- `assets/gep/genes.json`：可复用的基因定义文件。
- `assets/gep/capsules.json`：用于避免重复推理的成功结果模板。
- `assets/gep/events.jsonl`：仅支持追加操作的进化事件记录（通过父节点 ID 进行管理）。

## 文档中的表情符号规则

文档中仅允许使用 DNA 表情符号，其他表情符号均被禁止。

## 系统兼容性与配置灵活性

该技能设计为**与具体环境无关**，默认使用 OpenClaw 的标准工具。

### 本地配置覆盖
您可以通过以下方式修改系统行为：

- **方法 1：环境变量**：在 `.env` 文件中设置 `EVOLVE_REPORT_TOOL` 变量。
   ```bash
EVOLVE_REPORT_TOOL=feishu-card
```

- **方法 2：动态检测**：脚本会自动检测工作空间中是否存在兼容的本地技能（如 `skills/feishu-card`），并据此调整其行为。

## 安全性与风险控制

### 身份验证与行为指导原则
- **身份声明**：系统声明为“一个能够自我进化的系统”。
- **进化指令**：
  - 如果发现错误 → 进入**修复模式**（修复漏洞）。
  - 如果系统运行稳定 → 进入**优化模式**（重构/创新）。

### 风险缓解措施
- **严格的单进程逻辑**：确保系统不会无限递归。
- **审查模式**：在敏感环境中使用 `--review` 参数。
- **版本同步**：建议始终配合 git-sync cron 任务使用该技能。

## 故障排除前的检查步骤

如果您遇到意外错误或异常行为，请**先核实系统版本**：

```bash
node -e "const p=require('./package.json'); console.log(p.version)"
```

如果您使用的不是最新版本，请先进行更新——大多数已知问题已在最新版本中得到修复：
```bash
# If installed via git
git pull && npm install

# If installed via npm (global install)
npm install -g evolver@latest
```

最新版本及更新日志：`https://github.com/autogame-17/evolver/releases`

## 许可证
MIT 许可证