---
name: ai-bounty-claim
description: Use when claiming the AI bounty on tDVV through RewardClaimContract. Covers the two supported paths: direct EOA Claim() and Portkey CA ClaimByPortkeyToCa(Hash ca_hash). Explains how to choose the route, prepare the correct signer, validate prerequisites, and interpret claim failures.
---

# AI 奖金领取

使用此技能通过 `RewardClaimContract` 在 `tDVV` 上领取 AI 奖金。

本技能仅支持以下领取路径：

- EOA（Externally Owned Account, 外部托管账户）路径：`Claim()`
- Portkey CA（Portkey 加密证书颁发机构）路径：`ClaimByPortkeyToCa(Hash ca_hash)`

**禁止使用的情况：**
- 已弃用的 `ClaimByPortkey` 方法
- 合同部署或升级操作
- 管理员操作（如更改领取窗口或提取剩余余额）

**推荐的执行路径：** 优先使用依赖的 Portkey 技能。  
本技能中的 `aelf-command` 代码片段仅作为已安装相应 CLI 的环境的可选手动备用方案。

## **依赖项**

将这些技能作为路由依赖项使用，而非隐含的假设条件：

- Portkey CA 技能：`https://github.com/Portkey-Wallet/ca-agent-skills/blob/main/SKILL.md`
- Portkey EOA 技能：`https://github.com/Portkey-Wallet/eoa-agent-skills/blob/main/SKILL.md`

**使用场景：**
- 当领取操作依赖于 `ca_hash`、持有人信息或管理员验证时，使用 CA 技能。
- 当领取操作依赖于 EOA 地址选择、活动签名者上下文或密码保护的 EOA 密钥库时，使用 EOA 技能。
- 默认情况下，EOA 的 `Claim()` 方法不需要 CA 工具；而 CA 的 `ClaimByPortkeyToCa()` 方法通常需要。

**注意：** 公开技能分发中不应包含私有仓库链接。

## **tDVV 的默认设置**

当用户明确在当前 AI 奖金环境中操作时，请使用以下默认值：

- 奖金合同：`ELF_2fc5uPpboX9K9e9NTiDHxhCcgP8T9nV28BLyK8rDu8JmDpn472_tDVV`
- 公共 RPC（Remote Procedure Call）地址：`https://tdvv-public-node.aelf.io`
- Portkey CA 合同：`ELF_2UthYi7AHRdfrqc1YCfeQnjdChDLaas65bW4WxESMGMojFiXj9_tDVV`

请将这些值视为环境配置，而非不可更改的常量。

## **选择领取路径**

在准备签名者信息之前，先选择正确的领取路径：

### **使用 `Claim()**

- 当用户希望直接将奖励发放到普通 EOA 地址时。
- 当不涉及 Portkey CA 身份验证流程时。
- 当没有 `ca_hash` 或不需要 `ca_hash` 时。

**重要说明：**
- `Claim()` 方法不需要 `ca_hash`。
- 接收者地址为 `Context.Sender`。
- 领取状态会在发送者的地址上记录。

### **使用 `ClaimByPortkeyToCa(Hash ca_hash)`

- 当用户希望将奖励发放到 Portkey CA 身份时。
- 当用户已经拥有或能够获取 `ca_hash` 时。
- 当发送者是该 Portkey 持有者的管理员时。

**重要说明：**
- `ClaimByPortkeyToCa()` 方法需要 `ca_hash`。
- 接收者地址为 `holderInfo.CaAddress`。
- 领取状态会在 CA 地址上记录。

**默认路由规则：**
- 如果用户仅希望进行普通地址领取，选择 `Claim()`。
- 如果用户提及 CA、持有人、管理员验证、`ca_hash` 或领取到 CA 的流程，选择 `ClaimByPortkeyToCa()`。

## **EOA `Claim()` 路径**

### **前提条件：**
- 在发送 `Claim()` 之前：
  1. 确认签名者是指定的 EOA 地址。
  2. 确认奖励合同当前可以领取：
    - `claim_enabled` 为 `true`，且在领取窗口内。
    - 奖金池中仍有余额。
  3. 确认发送者尚未领取过奖励。
  4. 如果需要解析活动钱包或管理本地签名者信息，请使用 EOA 技能。

**操作提示：**
- 如果查询到的 `ELF` 余额为 `0`，仅视为警告；应以链上的实际执行结果为准，而非钱包余额。

### **正确的发送路径：**
- 优先使用 Portkey EOA 技能来解析活动签名者，并发送交易。
- 在进行任何写入操作之前，先显示解析后的签名者信息、目标合同、方法及预期接收者信息，然后获取用户的明确确认。
- 如果用户未明确确认，切勿发送交易。

**可选的手动备用方案：**
- 仅在环境已安装 `aelf-command` 且用户明确要求通过 CLI 进行操作时使用。

**示例（直接使用 EOA 签名的调用）：**  
```bash
aelf-command send ELF_2fc5uPpboX9K9e9NTiDHxhCcgP8T9nV28BLyK8rDu8JmDpn472_tDVV Claim "" \
  -a <EOA_ADDRESS> \
  -p '<EOA_PASSWORD>' \
  -e 'https://tdvv-public-node.aelf.io'
```

### **成功后的预期结果：**
- 交易状态为 `MINED`。
- 奖金合同方法为 `Claim`。
- 触发 `AddressClaimed` 事件。
- 接收者地址与发送者地址相同。

### **常见失败原因：**
- “地址已被领取”。
- 奖金余额不足。
- 领取功能被禁用。
- 领取窗口尚未开始或已结束。

## **Portkey CA `ClaimByPortkeyToCa(Hash ca_hash)` 路径**

### **必需输入：**
- `ca_hash`：当前属于该持有者的管理员签名者的信息。

**注意事项：**
- `ca_hash`：用于查询 Portkey CA 的持有人身份哈希。
- `ca_address`：`ClaimByPortkeyToCa` 操作的奖励接收地址。
- `manager_address`：实际的交易发送者地址。

### **获取 `ca_hash` 的方法：**
- 优先顺序：
  1. 如果 Portkey 钱包已本地恢复或解锁，从钱包状态中读取 `caHash`。
  2. 如果用户仅知道监护人标识符，通过标识符在链上查询 Portkey。
  3. 如果已有 `ca_hash` 候选值，通过 Portkey CA 的 `GetHolderInfo` 方法进行验证。

**发送最终 CA 领取交易之前的步骤：**
- 确认签名者是指定的管理员地址。
- 确认该管理员存在于 `ca_hash` 的 `managerInfos` 中。
- 确认合同处于可领取状态：
  - `claim_enabled` 为 `true`，且在领取窗口内。
- 确认 `ca_hash` 尚未被使用。
- 确认 CA 地址尚未完成 Portkey 升级领取操作。

### **管理员验证：**
- 在尝试领取之前，使用 `tDVV` 上的 Portkey CA 合同来验证签名者。

**预期结果：**
- `GetHolderInfo(ca_hash).managerInfos` 中应包含交易发送者的信息。

**如果验证失败：** 合同将返回错误信息：“Sender is not a manager of the CA holder.”（发送者不是 CA 持有者的管理员。）

### **正确的发送路径：**
- 优先使用 Portkey CA 技能来解析 `ca_hash`，验证管理员签名者，并直接从该签名者发送交易。
- 在进行任何写入操作之前，先显示解析后的管理员签名者信息、`ca_hash`、目标合同、方法及预期接收者信息，然后获取用户的明确确认。
- 如果用户未明确确认，切勿发送交易。

**可选的手动备用方案：**
- 仅在环境已安装 `aelf-command` 且用户明确要求通过 CLI 进行操作时使用。

**示例（直接使用管理员签名的奖励合同调用）：**  
```bash
aelf-command send ELF_2fc5uPpboX9K9e9NTiDHxhCcgP8T9nV28BLyK8rDu8JmDpn472_tDVV ClaimByPortkeyToCa "<CA_HASH>" \
  -a <MANAGER_ADDRESS> \
  -p '<MANAGER_PASSWORD>' \
  -e 'https://tdvv-public-node.aelf.io'
```

**对于代理驱动的流程：**
- 通过 Portkey CA 技能解锁或选择管理员签名者。
- 直接从该管理员签名者发送奖励合同调用。
- 不要通过 CA 中间层进行转发。

### **成功后的预期结果：**
- 交易状态为 `MINED`。
- 奖金合同方法为 `ClaimByPortkeyToCa`。
- 触发 `PortkeyClaimedToCa` 事件。
- 发送奖励的 `Token` 事件记录在 `holderInfo.CaAddress` 中。

**常见失败原因：**
- 需要 `ca_hash`。
- Portkey CA 合同未配置。
- 未找到 CA 持有者。
- 发送者不是 CA 持有者的管理员。
- `ca_hash` 已被领取。
- 地址已完成 Portkey 升级。
- 地址已领取最大奖励。
- 奖金余额不足。
- 领取功能被禁用或领取窗口已关闭。

## **推荐的代理工作流程：**
1. 确定用户是希望进行普通 EOA 领取还是 Portkey CA 领取。
2. 对于 EOA 领取，使用 EOA 技能解析签名者并验证所有领取前提条件。
3. 对于 CA 领取，使用 CA 技能解析 `ca_hash`，验证管理员身份，并验证所有领取前提条件。
4. 在进行任何链上写入操作之前，先显示解析后的签名者信息、目标合同、方法、密钥输入值及预期接收者信息，然后获取用户的明确确认。
5. 仅在用户明确确认后，才发送 `Claim()` 或 `ClaimByPortkeyToCa()`。
6. 报告交易 ID (`txid`)。
7. 如果调用失败，显示具体的链上错误并停止操作。

## **避免的错误做法：**
- 不要使用已弃用的 `ClaimByPortkey` 方法。
- 在普通的 EOA `Claim()` 流程中不要请求 `ca_hash`。
- 不要将 `Claim()` 描述为 Portkey 或 CA 领取路径。
- 不要用 EOA 接收者信息来解释 `ClaimByPortkeyToCa()`。
- 不要在 `ClaimByPortkeyToCa` 中使用 `CA ManagerForwardCall` 方法。
- 不要假设奖励总是发放给管理员地址。
- 在成功领取后不要重复尝试相同的 `ca_hash`。