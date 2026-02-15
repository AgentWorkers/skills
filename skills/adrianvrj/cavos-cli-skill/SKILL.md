---
name: cavos-cli
description: 与 Starknet 钱包的 Cavos CLI 进行交互。该 CLI 可用于转账、审批、合约调用、会话管理以及交易监控等操作。
metadata: { "openclaw": { "requires": { "bins": ["npx"] } } }
---

# Cavos CLI 技能

此技能允许您与 Cavos CLI (`@cavos/cli`) 进行交互，以管理 Starknet 钱包、执行转账以及调用合约。

## 核心命令

尽可能使用 `--json` 标志来获取结构化的输出。

### 1. 身份与会话
- **我是谁**：检查当前会话和钱包地址。
  ```bash
  npx @cavos/cli whoami --json
  ```
- **会话状态**：检查会话是否处于活动状态或已过期。
  ```bash
  npx @cavos/cli session-status --json
  ```
- **导入会话**：从 [仪表板](https://agent.cavos.xyz/) 导入会话令牌。
  ```bash
  npx @cavos/cli session import <token>
  ```

### 2. 资产与转账
- **检查余额**：
  ```bash
  npx @cavos/cli balance --token <STRK|ETH|address> --json
  ```
- **转账代币**：
  ```bash
  npx @cavos/cli transfer --to <address> --amount <amount> --token <token> --json
  ```

### 3. 合约交互
- **批准支出**：
  ```bash
  npx @cavos/cli approve --spender <address> --amount <amount> --token <token> --json
  ```
- **执行合约调用**：
  ```bash
  npx @cavos/cli execute --contract <address> --entrypoint <method> --calldata <comma_separated_vals> --json
  ```
- **读取合约调用结果**：
  ```bash
  npx @cavos/cli call --contract <address> --entrypoint <method> --calldata <vals> --json
  ```

### 4. 高级操作
- **批量调用**：批量执行多个合约调用。
  ```bash
  npx @cavos/cli multicall --calls '<json_array>' --json
  ```
- **模拟/估算**：在发送交易前进行验证。
  ```bash
  npx @cavos/cli simulate --contract <addr> --entrypoint <method> --calldata <vals> --json
  ```
- **交易状态**：
  ```bash
  npx @cavos/cli tx status <hash> --json
  ```

## 最佳实践
1. **验证余额**：在执行转账前，务必先运行 `balance` 命令。
2. **检查会话状态**：在工作流程开始时，运行 `whoami` 或 `session-status` 命令以确保身份验证正确。
3. **使用 JSON**：解析 JSON 输出比使用正则表达式处理标准输出更安全。
4. **Calldata**：`execute` 和 `call` 命令所需的 Calldata 应该是以逗号分隔的字符串（例如：`0x1,100`）。