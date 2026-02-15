---
name: blockchain_attestation
description: 使用以太坊证明服务（Ethereum Attestation Service, EAS）创建可验证的代理工作证明，其中默认链为 Base。
metadata: {"clawdbot":{"emoji":"⛓️","homepage":"https://attest.org","requires":{"bins":["node"]},"primaryEnv":"EAS_PRIVATE_KEY"}}
---

# 区块链认证（EAS）

该技能使用以太坊认证服务（Ethereum Attestation Service, EAS）来生成**链上**或**链下**的已完成工作认证。

**默认设置：**
- **默认链：** Base 主网
- **默认模式：** 链下（无需支付 gas 费用，但仍可验证）
- **默认数据模型：** 存储任务的哈希值、交付物的哈希值（以及一个代理 ID 和元数据字符串）

## 安全与隐私规则
1. **切勿** 将任何秘密信息、私钥、代币或用户隐私数据放入链上认证中。
2. 在大多数使用场景中，建议使用**链下**认证。
3. 如果需要为链下认证添加公共时间戳，可以使用 `timestamp` 命令将用户 ID（UID）锚定到链上，但不要公开完整的认证内容。
4. 只有在用户明确请求或同意支付相关费用后，才执行链上交易。

## 环境变量
- **用于签名（链下或链上操作）：** `EAS_PRIVATE_KEY`
- **用于链上交易和链上读取操作：** `EAS_RPC_URL`（所选链的 RPC 端点）
- **可选：**
  - `EASCHAIN`（`base` 或 `base_sepolia`，默认值为 `base`）
  - `CLAWDBOT_AGENT_ID`（用于覆盖 `agentId` 字段）

## 一次性设置
只需安装一次 Node.js 的相关依赖项：

```bash
cd {baseDir} && npm install
```

## 每个链都需要执行的一次性操作：注册数据结构
该技能使用统一的数据结构：

```
bytes32 taskHash, bytes32 outputHash, string agentId, string metadata
```

通过链上交易注册该数据结构，并将生成的 UID 保存到 `schemas.json` 文件中：

```bash
cd {baseDir} && node attest.mjs schema register --chain base
```

**针对 Base Sepolia 链的特定操作：**

```bash
cd {baseDir} && node attest.mjs schema register --chain base_sepolia
```

## 创建认证（推荐使用链下认证）
最佳的工作流程：
1. 提供任务描述文本
2. 提供交付物的文件路径或内容文本
3. 生成链下认证
4. 将签名后的认证内容保存到文件中
5. 将 UID 以及相应的浏览器链接返回给用户

**示例：**

```bash
cd {baseDir} && node attest.mjs attest \
  --mode offchain \
  --chain base \
  --task-text "Summarize Q4 board deck into 1 page memo" \
  --output-file ./deliverables/memo.pdf \
  --recipient 0x0000000000000000000000000000000000000000 \
  --metadata '{"hashAlg":"sha256","artifact":"memo.pdf"}' \
  --save ./attestations/latest.offchain.json
```

## 将链下的 UID 时间戳锚定到链上（可选操作）**

```bash
cd {baseDir} && node attest.mjs timestamp --chain base --uid <uid>
```

## 创建链上认证（需要支付 gas 费用）

```bash
cd {baseDir} && node attest.mjs attest \
  --mode onchain \
  --chain base \
  --task-text "..." \
  --output-file ./path/to/output \
  --metadata '{"hashAlg":"sha256"}'
```

## 验证
- 验证链上的 UID：
```bash
cd {baseDir} && node attest.mjs verify --chain base --uid <uid>
```

- 验证由该技能生成的链下认证 JSON 文件：
```bash
cd {baseDir} && node attest.mjs verify --offchain-file ./attestations/latest.offchain.json
```

## 哈希值生成辅助功能
如果您仅需要哈希值而无需生成认证文件，可以使用以下功能：

```bash
cd {baseDir} && node attest.mjs hash --file ./deliverables/memo.pdf
```

## 输出结果
所有命令都会将结果以 JSON 对象的形式输出到标准输出（stdout）：
- 成功时：`{"success": true, ... }`
- 出错时：`{"success": false, "error": {"code": "...", "message": "...", "details": ... }}`

这样设计是为了确保代理能够可靠地解析输出结果。