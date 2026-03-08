---
name: openclaw-memory-pensieve-algorand-v2-1
description: 操作 OpenClaw 的当前 Pensieve 内存堆栈：该堆栈支持仅写入（append-only）的本地数据层、哈希链（hash-chain）完整性机制、每日梦境周期（dream-cycle）的数据整合功能、使用 Algorand 加密技术对所有内容（包括事件、语义信息、程序逻辑以及模型数据）进行安全存储；同时具备 v2.1 版本后的数据恢复（recoverability）加固检查功能。适用于该内存系统的实现、运行、审计或数据恢复等场景。
---
# OpenClaw Memory Pensieve v2.1（安全加固）

当目标是实现可靠的长期内存存储功能，并具备从区块链节点进行数据恢复的能力时，请执行此工作流程。

## 工作流程

1. 确保 `memory/` 目录中存在所需的内存存储层。
2. 将重要事件记录到 `events.jsonl` 文件中（仅支持追加操作，数据采用哈希链形式进行存储）。
3. 每日运行 `dream_cycle_daily.py` 脚本以促进数据模式的稳定化。
4. 将加密后的数据每日通过 Algorand 区块链进行存储（包含全部内容；如有需要，可支持多次交易）。
5. 在数据存储完成后，运行 `hardening_v21_validate.py` 脚本进行安全加固验证。
6. 如需恢复数据，请根据链上的记录进行数据重构和验证。

## 强制性操作规则

- 所有 `.jsonl` 文件均只能追加数据，严禁重写或删除其中的内容。
- 保密信息需存储在 `.secrets/` 目录中，严禁在聊天中泄露。
- 仅存储加密后的数据（严禁存储明文数据）。
- 将安全加固过程中的任何故障视为影响数据恢复完整性的关键问题。

## 先决条件（必须满足）

- 搭配 `algosdk` 和 `cryptography` 的 Python 环境。
- 本地配置文件（未包含在软件包中）：
  - `.secrets/algorand-wallet-nox.json`
  - `.secrets/algorand-note-key.bin`
- 可选的环境变量（用于配置端点和身份验证）：
  - `ALGORAND_ALGOD_URL`, `ALGORAND_ALGOD_TOKEN`
  - `ALGORAND_INDEXER_URL`, `ALGORAND_INDEXER_TOKEN`

**请先运行预检查脚本：**  
`scripts/preflight_requirements.py`

## 运行时命令（当前实现）

使用解释器执行以下命令：  
`<workspace>/.venv-algo/bin/python`

该技能包中包含的脚本文件（位于 `scripts/` 目录）：  
- `auto_capture_daily.py`：自动每日数据捕获  
- `dream_cycle_daily.py`：每日数据模式维护  
- `anchor_daily_algorand.py`：每日数据存储到 Algorand  
- `read_anchor_latest.py`：读取最新的存储数据  
- `hardening_v21_validate.py`：安全加固验证  
- `recover_from_blockchain.py`：从区块链中恢复数据  
- `capture_from_logs.py`：从日志中提取数据  
- `preflight_requirements.py`：预检查脚本  

**主要执行流程：**  
`scripts/auto_capture_daily.py` → `scripts/dream_cycle_daily.py` → `scripts/anchor_daily_algorand.py` → `scripts/read_anchor_latest.py` → `scripts/hardening_v21_validate.py`

**恢复/调试工具：**  
`scripts/recover_from_blockchain.py` → `scripts/capture_from_logs.py`

## 阅读推荐资源：  
- `references/architecture.md`：了解内存存储的架构和性能保障机制。  
- `references/ops-runbook.md`：查看日常操作命令及输出结果。  
- `references/hardening-v21.md`：详细的安全加固策略说明。  
- `references/security-prereqs.md`：明确列出了所需的依赖项和保密信息。