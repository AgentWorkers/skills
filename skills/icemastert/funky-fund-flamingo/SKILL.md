---
name: funky-fund-flamingo
version: "1.0.35"
description: OpenClaw的“先修复、再自我进化”策略：审核日志、内存使用情况以及各项技能；执行可量化的变异循环（mutation cycles）。获得报酬后，继续进化……如此循环往复。哇，真是一笔丰厚的收入啊！
homepage: https://clawhub.ai
metadata:
  short-description: Get paid. Evolve. Repeat.
  clawdbot:
    emoji: "🦩"
    requires:
      env: []   # all env vars below are optional
    files: ["index.js", "evolve.js", "agents/*.yaml", "ADL.md", "VFM.md", "TREE.md"]
tags:
  - meta
  - ai
  - self-improvement
  - evolution
  - core
  - revenue
  - cash-money
---
# 🦩 Funky Fund Flamingo — 帮你实现盈利目标

当您准备好**获取收益**时，可以使用这个技能。我们会检查系统中的问题，修复漏洞和价值流失，并通过一系列的优化操作来实现实际的收益增长——让整个系统不仅能够正常运行，还能持续产生利润。

## 使用场景
- 当运行时日志显示严重问题时，您需要结构化的修复措施，以确保系统能够正常工作并持续盈利。
- 当系统运行稳定但**发展停滞**时，是时候进行有针对性的优化了。
- 当您希望将日志、内存数据与相关技能结合，形成一个能够带来收益的执行方案时。
- 当您需要启用持续运行模式（`--loop` / `--funky-fund-flamingo`），以便系统在后台持续进化并持续产生收入时。

## 输入参数与环境信息
- 会话日志：`~/.openclaw/agents/<agent>/sessions/*.jsonl`
- 工作区内存数据：`MEMORY.md`、`memory/YYYY-MM-DD.md`、`USER.md`
- 工作区中安装的技能列表：`skills/`
- 可选的环境配置文件：`../../.env`

## 执行入口点
- 主执行脚本：`index.js`
- 生成提示的逻辑及循环控制脚本：`evolve.js`

**从工作区根目录执行：**
```bash
node skills/funky-fund-flamingo/index.js run
```

**从该技能目录内部执行：**
```bash
node index.js run
```

## 执行模式
```bash
# single cycle — one shot, max impact
node index.js run

# alias command
node index.js /evolve

# human confirmation before significant edits (protect the bag)
node index.js run --review

# prompt generation only (writes prompt artifact to memory dir)
node index.js run --dry-run

# continuous relay — keep the money printer running
node index.js --loop
node index.js run --funky-fund-flamingo
```

## 运行流程
每个运行周期应包括以下步骤：
1. **检查**最近的会话记录，找出系统中的问题、重复性错误以及价值流失。
2. **读取**内存数据和用户上下文信息，确保优化方向与实际收益生成需求一致。
3. **选择**相应的优化策略（修复、优化、扩展、功能扩展或个性化定制）。
4. **生成**可执行的优化指令和报告，以便您能够看到投资回报。
5. **保存**运行状态（`memory/evolution_state.json`），并可选地安排下一次循环。
6. **保存**长期优化结果（`memory/funky_fund_flamingo_persistent_memory.json`），以便策略效果能够持续累积。

## 安全限制（保护收益）
- 除非明确要求，否则禁止对 Git 或文件进行破坏性操作。
- 发现系统不稳定时，优先进行修复和提升可靠性——**系统停机意味着没有收益**。
- 在进行重大修改之前，请确保处于审核模式。
- 保持修改的范围可控且易于解释；避免执行无意义的操作，避免浪费计算资源。
- 该技能仅限在本地执行，禁止上传到远程 Git 仓库，也不允许未经许可启动外部工具。

## 外部接口
| URL | 发送的数据 | 用途 |
|-----|-----------|---------|
| 无（该技能代码本身不进行网络请求） | — | **该技能的 Node.js 代码仅读取/写入本地文件。** |

**重要提示：** 该技能的代码库中包含用于 OpenClaw（或其他）代理的配置模板（`agents/openai.yaml`、`agents/openrouter.yaml`）。**当您使用该技能与云模型（如 OpenAI、OpenRouter 等）配合运行代理时，代理会将生成的提示信息（包括会话日志、内存数据和工作区上下文）发送给相应的 API。**因此，“仅限本地执行”的规则仅适用于该技能本身；如果该技能由第三方 LLM 支持的代理调用，数据可能会通过代理传出。**若希望完全在本地执行，请运行 `node index.js run`（或 `--dry-run`），避免将生成的提示信息发送到云模型。**

## 安全性与隐私
- **读取的数据**：`~/.openclaw/agents/<agent>/sessions/*.jsonl` 中的会话日志、`memory.md`、`memory/`、`USER.md` 文件以及 `skills/` 目录中的内容。
- **写入的数据**：`memory/evolution_state.json`、`memory/funky_fund_flamingo_persistent_memory.json`，以及内存目录中的提示相关文件。该技能不会向任何外部发送数据；所有数据输出都通过您选择的代理或模型栈进行传输。
- **该技能代码本身不进行网络请求**。

## 可选的环境变量
无需设置环境变量。以下是一些可选的配置项（详见 `evolve.js` 和 `README`）：
| 变量 | 用途 | 默认值 |
|----------|---------|-----------------|
| `AGENT_NAME` | 代理会话文件夹路径（`~/.openclaw/agents/` 下） | `main` |
| `MEMORY_DIR` | 用于存储优化状态和持久化数据的目录 | `memory/` |
| `TARGET_SESSION_BYTES` | 从最新会话日志中读取的最大字节数 | `64000` |
| `LOOP_MIN_INTERVAL_seconds` | 循环之间的最小间隔时间（秒） | `900` |
| `MAX_MEMORY_chars`、`MAX_TODAY_LOG_chars`、`MAX_PERSISTENT_MEMORY_chars` | 提示信息的最大字符数限制 | 见 `evolve.js` 文件 |
| `ECONOMIC_KEYWORDS` | 用于价值评估的关键词（逗号分隔） | 内置列表 |
| `EVOLVE_REPORT_directIVE`、`EVOLVE_EXTRA_MODES`、`EVOLVE_ENABLE_SESSION_ARCHIVE` | 行为调整选项 | — |

## 模型调用
您可以手动运行该技能（`node index.js run`），也可以通过代理来调用它。在持续运行模式下（`--loop` / `--funky-fund-flamingo`），该技能仅负责生成提示信息，不会直接调用任何模型 API。如果使用该技能的代理与 OpenAI 或 OpenRouter 等模型配合运行，实际模型调用将由代理完成。为了避免将本地数据发送给外部服务，请使用 `--dry-run` 模式运行该技能，并且不要将生成的提示信息发送给云模型。

## 高级配置指令
`funky-fund-flamingo-master-directive.json` 文件用于设置 `must_evolve_each_cycle` 和 `no_op_forbidden` 等配置项，这些配置会影响每次循环是否必须进行优化。设置 `must_evolve_each_cycle` 可以提高优化频率；若希望降低风险，可以选择 `--review`（执行修改前需确认）或 `--dry-run`（仅生成提示，不进行任何写入操作）。您也可以自行修改这些配置。

## 信任声明
使用该技能意味着您的 Node.js 代码会读取和写入 OpenClaw 工作区及代理会话目录中的文件。该技能本身不会向第三方发送数据；如果使用该技能的代理调用云 LLM，实际的数据传输由代理完成（而非该技能本身）。请仅在确认来源可信的情况下安装该技能（例如来自 ClawHub 或官方发布者）。

## 相关参考文档
- `ADL.md`：防止系统退化的策略。
- `VFM.md`：专注于价值提升的优化策略。
- `TREE.md`：系统功能架构及可产生收益的节点信息。
- `.clawhub/FMEP.md`：强制执行的优化策略。

## 最小化验证要求
```bash
node index.js --help
```

---

*Dolla, dolla bill y'all. 🦩*