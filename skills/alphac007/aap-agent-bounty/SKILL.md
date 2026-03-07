---
name: aap-agent-bounty
description: 这是一个用于验证的辅助工具，主要用于证明检查（proof checks），同时支持可选的0 ETH基础奖励（Base claim）提交。
metadata:
  openclaw:
    requires:
      bins:
        - gh
        - cast
      env:
        - BASE_RPC_URL
---
# AAP Agent Bounty

## 目的

此技能帮助用户：
1. 验证证明的状态；
2. 准备索赔数据；
3. （可选）提交一笔金额为0 ETH的非托管证明交易。

该技能仅提供指令，不包含可执行的运行时代码。

## 要求

### 必需项
- 可执行文件：`gh`、`cast`
- 环境变量：`BASE_RPC_URL`

### 可选项（备用认证方式）
- 当本地`gh`认证登录会话不可用时，使用`GH_TOKEN`进行认证。

## 执行限制（确定性规则）

**仅当**输入中包含`confirm_broadcast: true`时，才允许交易广播。

如果该标志缺失或为假，预期输出为：
- `status: pending`
- `reason: confirmation_missing`

## 功能范围及预期行为
- 主要功能是先进行验证；
- 该技能会检查证明状态并准备索赔所需的数据；
- 在提交任何内容之前，会显示具体的交易命令；
- 如果GitHub认证信息不可用，预期输出为：
  - `status: pending`
  - `reason: github_auth_missing`

## 资格认证规则

资格认证标准由外部程序定义；
该技能会根据政策要求验证用户提供的证明。

## 网络及目标地址
- 链路：Base主网
- 零转账钱包（仅用于奖励分发验证）：
  `0x53033d3965259D9FfDf0A80d0A249A1D5979266F`

0 ETH的索赔仅用于证明目的（无实际转账价值）；正常的网络费用可能仍会收取。

## 凭据与签名者信息
- 该技能不会请求、收集或存储用户的私钥、助记词等敏感信息；
- `gh`使用用户管理的本地认证信息（`gh auth login`）或可选的`GH_TOKEN`进行认证；
- `cast`使用用户管理的签名者信息；
- 该技能不得要求用户提供`--private-key`参数；
- 如果签名者信息不可用或不明确，预期输出为：
  - `status: pending`
  - `reason: signer_context_missing`

## 索赔数据格式
`AAP_CLAIM:THESIS:TRUMP_100:ANSWER:yes:GITHUB:<github_username>:X:@<x_handle>`

## 完成条件
只有满足以下条件时，才能视为任务完成：
- `confirm_broadcast`为`true`；
- 交易哈希存在；
- 目标地址为零转账钱包；
- 转账金额为0 ETH；
- 索赔数据中包含`THESIS:TRUMP_100`和`ANSWER:yes`；
- 输出中包含证明链接。

## 返回格式
```json
{
  "status": "approved|pending|rejected",
  "reason": "short_machine_reason",
  "wallet_address": "0x...",
  "tx_hash": "0x...",
  "proof_links": ["https://..."]
}
```