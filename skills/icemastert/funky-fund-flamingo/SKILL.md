---
name: funky-fund-flamingo
version: "1.0.35"
description: OpenClaw的“先修复再自我进化”功能：用于审计日志、内存使用情况以及各项技能的监控；能够执行可量化的变异循环（mutation cycles）。完成这些任务后即可获得报酬。不断进化，重复这一过程……哈哈，赚大钱啦！
homepage: https://clawhub.ai
metadata:
  short-description: Get paid. Evolve. Repeat.
  clawdbot:
    emoji: "🦩"
    requires:
      env: []
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

当你准备好**获取收益**时，就可以使用这个技能了。我们会检查系统中的问题，修复漏洞和价值流失，并通过一系列的变异操作来产生实际的收益——这样你的系统不仅能正常运行，还能持续盈利。

## 使用场景
- 当运行时日志显示严重问题时，你需要有针对性的修复措施，以确保系统能够继续稳定运行并持续产生收入。
- 当系统运行稳定但进展缓慢时，是时候进行有针对性的能力优化了。
- 你希望有一个能够整合日志、内存数据和技能的统一执行方案，以实现盈利目标。
- 你需要启用持续运行模式（`--loop` / `--funky-fund-flamingo`），让系统在后台持续进化，从而持续产生收入。

## 输入参数与所需环境
- 会话日志：`~/.openclaw/agents/<agent>/sessions/*.jsonl`
- 工作区内存数据：`MEMORY.md`、`memory/YYYY-MM-DD.md`、`USER.md`
- 工作区中安装的技能列表：`skills/`
- 可选的环境配置文件：`../../.env`

## 执行入口
- 主执行脚本：`index.js`
- 用于构建提示信息和控制执行逻辑的脚本：`evolve.js`

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

## 执行流程
每个执行周期应包括以下步骤：
1. **检查**最近的会话记录，找出系统中的问题、重复性错误以及价值流失的情况。
2. **读取**内存数据和用户配置信息，确保进化方向与实际盈利目标一致。
3. **选择**合适的变异策略（修复、优化、扩展、功能增强或个性化调整）。
4. **生成**可执行的变异指令和相应的报告，以便你能看到投资回报（ROI）。
5. **保存**当前系统状态（`memory/evolution_state.json`），并可选地安排下一次执行循环。
6. **保存**长期进化过程中的学习数据（`memory/funky_fund_flamingo_persistent_memory.json`），以便策略不断优化，收益持续增长。

## 安全限制（保护你的收益）
- 除非明确要求，否则禁止进行任何破坏性的文件操作。
- 发现系统不稳定时，优先进行修复和提升系统可靠性——**系统停机意味着没有收入**。
- 在进行重大修改之前，请确保处于审核模式。
- 保持修改的范围可控且易于解释；避免执行无意义的操作，以免浪费计算资源。
- 该技能仅限在本地执行，禁止将结果发布到远程Git仓库，也不允许在未经授权的情况下启动外部工具。

## 外部接口
| URL | 发送的数据 | 功能 |
|-----|-----------|---------|
| 无 | — | 该技能仅限在本地使用，它会读取会话日志、工作区内存数据和技能文件，不会调用任何外部API或发送数据到外部。 |

## 安全性与隐私保护
- **读取的数据**：`~/.openclaw/agents/<agent>/sessions/*.jsonl`中的会话日志、`MEMORY.md`、`memory/`、`USER.md`以及`skills/`目录中的文件。
- **写入的数据**：`memory/evolution_state.json`、`memory/funky_fund_flamingo_persistent_memory.json`，以及内存目录中的相关报告文件。除非用户另行配置，否则数据不会离开本地系统。
- **网络限制**：默认情况下，该技能不会打开网络连接或发送HTTP请求。

## 模型调用说明
进化循环可以通过手动运行`node index.js run`来执行，也可以由代理程序根据该技能的指令来执行。在持续运行模式（`--loop` / `--funky-fund-flamingo`）下，系统会自动执行相同的处理流程和生成报告；除非用户的环境设置允许，否则不会触发额外的模型调用。如需停止该技能的运行，可以取消相关配置。

## 使用声明
使用该技能意味着你将运行Node.js代码，这些代码会读取和写入你的OpenClaw工作区及代理会话目录中的文件。该技能不会向第三方发送任何数据。只有在你信任技能来源（例如ClawHub和发布者）的情况下，才建议安装该技能。

## 相关参考文档
- `ADL.md`：防止系统性能下降的策略。
- `VFM.md`：专注于提升系统价值的变异策略（仅执行能带来收益的变更）。
- `TREE.md`：系统能力的拓扑结构及可产生收益的节点信息。
- `.clawhub/FMEP.md`：强制执行的变异策略配置。

## 最小化验证要求
```bash
node index.js --help
```

---
*赚大钱吧，各位！🦩*