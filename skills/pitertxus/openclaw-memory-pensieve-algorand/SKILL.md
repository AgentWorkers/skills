---
name: openclaw-memory-pensieve-algorand-v2-1
description: 操作 OpenClaw 的当前 Pensieve 内存堆栈：该堆栈支持仅写入（append-only）的本地数据存储方式，确保数据链的完整性（hash-chain integrity）；每天自动整合梦境数据（daily dream-cycle consolidation）；所有数据（包括事件、语义信息、程序逻辑以及模型结构）都会被加密并锚定到 Algorand 网络中（encrypted Algorand anchoring）；同时，该内存系统还具备 v2.1 版本的加固机制，能够有效防止数据被篡改（v2.1 post-anchor recoverability hardening checks）。在实现、运行、审计或恢复该内存系统时，请使用此功能。
---
# OpenClaw Memory Pensieve v2.1（强化版）

当目标是实现长期可靠的存储系统，并具备从区块链锚点进行数据恢复的能力时，请执行此工作流程。

## 工作流程

1. 确保`memory/`目录中存在所需的内存层结构。
2. 将重要事件记录到`events.jsonl`文件中（仅允许追加数据，采用哈希链技术进行数据完整性保护）。
3. 每日运行“dream_cycle_daily.py”脚本以促进数据模式的稳定化。
4. 将加密后的数据通过Algorand区块链进行锚定存储（包含全部数据内容；如有需要，可支持多次交易）。
5. 锚定数据后，运行`hardening_v21_validate.py`脚本进行强化验证。
6. 如需恢复数据，可依据链上的记录进行数据重构与验证。

## 强制性操作规则

- 所有`.jsonl`文件均只能追加数据，严禁修改或删除其中的内容。
- 保密信息请存储在`.secrets/`目录中，切勿在聊天中泄露。
- 仅允许存储加密后的数据（严禁存储明文数据）。
- 将强化过程中的任何故障视为影响数据恢复完整性的关键因素。

## 运行时命令（当前实现）

使用的解释器：
- `/home/molty/.openclaw/workspace/.venv-algo/bin/python`

该技能包中包含的脚本（位于`scripts/`目录）：
- `auto_capture_daily.py`：自动每日数据捕获脚本
- `dream_cycle_daily.py`：每日数据稳定化处理脚本
- `anchor_daily_algorand.py`：每日数据锚定到Algorand区块链的脚本
- `read_anchor_latest.py`：读取最新锚定数据的脚本
- `hardening_v21_validate.py`：强化验证脚本
- `recover_from_blockchain.py`：从区块链中恢复数据的脚本
- `capture_from_logs.py`：从日志中提取数据的脚本

主要执行流程：
- `scripts/auto_capture_daily.py`：自动每日数据捕获
- `scripts/dream_cycle_daily.py`：每日数据稳定化处理
- `scripts/anchor_daily_algorand.py`：每日数据锚定到Algorand区块链
- `scripts/read_anchor_latest.py`：读取最新锚定数据
- `scripts/hardening_v21_validate.py`：强化验证

数据恢复/调试工具：
- `scripts/recover_from_blockchain.py`：从区块链中恢复数据
- `scripts/capture_from_logs.py`：从日志中提取数据

## 建议阅读的文档

- `references/architecture.md`：了解内存层架构及相关保证措施。
- `references/ops-runbook.md`：查看日常操作命令及输出结果。
- `references/hardening-v21.md`：详细了解强化后的严格验证政策。