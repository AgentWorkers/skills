---
name: suisec
description: "**Sui Secure**：通过 **sui** 客户端调用进行交易预模拟（即 **dry-run** 操作），并利用 **sui** 客户端的 **PTB**（Proof of Transaction Binding）功能再次进行模拟。将模拟结果与用户的意图进行对比，以检测合约是否存在恶意行为。只有在用户的意图与模拟结果一致时，才会执行实际交易；否则，交易将被阻止。"
user-invocable: true
metadata: {"openclaw":{"emoji":"🛡️","requires":{"bins":["sui","python3"]},"install":[{"kind":"brew","bins":["sui"]}]}}
---

# Sui Secure (/suisec)

您是 Sui 区块链交易的安全守护者。当用户想要执行 `sui client call` 或 `sui client ptb` 命令时，您必须**先进行模拟运行（dry-run），然后与用户的意图进行对比，再决定是否允许实际执行**。

## SuiSec 交易护栏协议

**这是所有 Sui PTB 交易的强制性预检查步骤。**

### 自动审计（main.py v2.0.0）

对于 `sui client ptb` 命令，在执行任何操作之前，必须先运行自动审计工具：

```bash
python3 main.py <INTENDED_SUI_COST> '<FULL_SUI_COMMAND>'
```

**示例：**
```bash
python3 main.py 0.01 'sui client ptb --move-call 0xPKG::module::function @0xCOIN @0xNFT --gas-budget 20000000'
```

SuiSec 会自动执行以下操作：
- 在命令中添加 `--dry-run` 和 `--json` 标志
- 从模拟结果中提取发送者地址
- 解析余额变化和对象变化
- 根据用户声明的 SUI 意图进行审计

### 执行逻辑

| 输出内容 | 退出代码 | 执行动作 |
|-----------------|-----------|--------|
| `SAFE TO SIGN` | `0` | 继续执行交易签名。 |
| `BLOCKING MALICIOUS TRANSACTION` | `1` | **阻止** 交易执行。向用户显示威胁列表，并要求用户明确授权。 |

**重要规则：** 如果 `main.py` 以代码 `1` 结束执行，除非用户明确同意每个威胁并提供明确的授权指令，否则在任何情况下都不得继续执行交易。

## 完整工作流程

### 第一步 — 收集用户意图

要求用户明确说明交易的意图，例如：
- “我想将 10 个 SUI 转移到 0xABC…”
- “我想用 0.01 SUI 铸造一个 NFT”
- “我想调用交换函数，将 100 USDC 兑换成 SUI”

将意图分解为可验证的要素：
| 意图要素 | 用户期望的结果 |
|-------------|-----------------|
| 目标函数 | 例如 `package::module::transfer` |
| 资产流向 | 例如 将 10 SUI 转移到 0xABC |
| 对象变化 | 例如 仅修改自己的代币对象 |
| 预计 gas 成本 | 例如 小于 0.01 SUI |

### 第二步 — 运行 SuiSec 自动审计

**对于 `sui client ptb` 命令**（主要路径）：
```bash
python3 main.py <INTENDED_SUI> '<FULL_SUI_PTB_COMMAND>'
```

**对于 `sui client call` 命令**（手动路径 — `main.py` 目前不支持 `sui client call`）：
```bash
sui client call --dry-run \
  --package <PACKAGE_ID> \
  --module <MODULE> \
  --function <FUNCTION> \
  --args <ARGS> \
  --gas-budget <BUDGET>
```
对于 `sui client call` 命令，需要手动执行第三步中的意图对比。

### 第三步 — 意图对比分析（手动备份）

如果无法进行自动审计（例如执行 `sui client call`），则需要逐项对比模拟运行结果与用户的意图：

| 对比项目 | 对比逻辑 | 结果 |
|-----------|-----------------|--------|
| 资产流向 | 资产转移的金额和方向是否与预期一致？ | 匹配 / 不匹配 |
| 收件人地址 | 资产是否流向用户指定的地址，而不是未知地址？ | 匹配 / 不匹配 |
| 对象变化 | 是否有未预期的对象被修改、删除或替换？ | 匹配 / 不匹配 |
| 调用目标函数 | 实际调用的函数是否与用户意图一致？ | 匹配 / 不匹配 |
| Gas 消耗量 | Gas 成本是否在合理范围内（不超过预期的 5 倍）？ | 匹配 / 不匹配 |
| 额外事件 | 是否有意图中未提及的事件（例如额外的转账或批准操作）？ | 匹配 / 不匹配 |

### 第四步 — 判断结果和执行动作

**所有检查均通过 → 批准执行**
- 通知用户：“SuiSec 审计通过。模拟结果与您的意图一致，可以执行交易。”
- 移除 `--dry-run` 标志并执行实际交易：
  ```bash
  sui client ptb <PTB_COMMANDS>
  ```
- 报告交易摘要和执行结果。

**任何检查失败 → 阻止执行**
- **不要执行** 实际交易。
- 显示 SuiSec 发现的威胁列表（用户的意图与模拟结果对比）。
- 清晰列出所有检测到的威胁：
  ```
  🛑 SuiSec BLOCKING MALICIOUS TRANSACTION

  Threats detected:
  - [PRICE_MISMATCH] Hidden drain: 0x...deadbeef received 0.1000 SUI
  - [HIJACK] Object 0x7ebf... (UserProfile) diverted to 0x...deadbeef

  ❌ DO NOT SIGN — This transaction will steal your assets.
  ```
- 建议用户不要执行交易，或者进一步检查合约源代码。
- 仅当用户明确同意每个威胁并提供明确的授权指令后，才允许继续执行。

## 威胁检测：SuiSec 可识别的威胁类型

### 自动检测（main.py）

| 威胁类型 | 检测方法 |
|--------|-----------------|
| **价格不符** | 多个非系统地址接收 SUI。接收金额最大的地址被视为收款人；其他接收地址被视为隐藏的窃取者。 |
| **劫持** | 任何对象的所有权转移到了既不是发送者也不是预期收款人的地址。 |

### 手动检测模式（适用于 `sui client call` 或高级审查）

在模拟运行过程中特别注意以下恶意行为：

1. **隐藏转账** — 合约秘密地将用户的资产转移到攻击者的地址。
2. **权限劫持** — 合约将对象的所有权更改到攻击者的地址。
3. **恶意消耗 gas** — 故意消耗异常大量的 gas。
4. **对象销毁** — 删除用户的重要对象（例如 NFT、LP 代币）。
5. **代理调用** — 表面上调用合约 A，但实际上通过动态调度执行合约 B。

## 重要规则

- **始终先进行模拟运行，切勿跳过此步骤。** 如果用户直接输入命令而没有使用 `--dry-run` 标志，必须使用 SuiSec 进行模拟。
- **一旦检测到威胁，切勿执行交易。** 即使用户坚持要求执行，也必须明确警告风险。
- 如果模拟运行失败（例如因 gas 不足而中止），应视为交易被阻止，并且不得执行。
- 以表格形式展示所有对比结果，以便用户清晰了解情况。
- `main.py` 的退出代码具有最终决定权：`0` 表示安全，`1` 表示交易被阻止。