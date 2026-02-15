---
name: openfunderse-strategy
description: OpenFunderse Strategy机器人：用于提出交易意图并控制交易意图的提交流程
always: false
disable-model-invocation: true
metadata:
  openclaw:
    requires:
      env:
        - RELAYER_URL
        - BOT_ID
        - BOT_API_KEY
        - CHAIN_ID
        - RPC_URL
        - STRATEGY_AA_RPC_URL
        - STRATEGY_AA_BUNDLER_URL
        - STRATEGY_AA_USER_OP_VERSION
        - STRATEGY_AA_ENTRYPOINT_ADDRESS
        - STRATEGY_AA_ACCOUNT_ADDRESS
        - STRATEGY_AA_OWNER_PRIVATE_KEY
        - INTENT_BOOK_ADDRESS
        - NADFUN_EXECUTION_ADAPTER_ADDRESS
        - ADAPTER_ADDRESS
        - NADFUN_LENS_ADDRESS
        - NADFUN_BONDING_CURVE_ROUTER
        - NADFUN_DEX_ROUTER
        - NADFUN_WMON_ADDRESS
        - VAULT_ADDRESS
        - STRATEGY_AUTO_SUBMIT
        - STRATEGY_REQUIRE_EXPLICIT_SUBMIT
        - STRATEGY_TRUSTED_RELAYER_HOSTS
        - STRATEGY_ALLOW_HTTP_RELAYER
        - STRATEGY_MAX_IMPACT_BPS
        - STRATEGY_SELL_TAKE_PROFIT_BPS
        - STRATEGY_SELL_STOP_LOSS_BPS
        - STRATEGY_SELL_MAX_HOLD_SECONDS
        - STRATEGY_DEADLINE_MIN_SECONDS
        - STRATEGY_DEADLINE_BASE_SECONDS
        - STRATEGY_DEADLINE_MAX_SECONDS
        - STRATEGY_DEADLINE_PER_CLAIM_SECONDS
        - STRATEGY_AA_INIT_CODE
        - STRATEGY_AA_CALL_GAS_LIMIT
        - STRATEGY_AA_VERIFICATION_GAS_LIMIT
        - STRATEGY_AA_PRE_VERIFICATION_GAS
        - STRATEGY_AA_MAX_PRIORITY_FEE_PER_GAS
        - STRATEGY_AA_MAX_FEE_PER_GAS
        - STRATEGY_AA_POLL_INTERVAL_MS
        - STRATEGY_AA_TIMEOUT_MS
    primaryEnv: STRATEGY_AA_OWNER_PRIVATE_KEY
    skillKey: strategy
---

# Strategy MoltBot 技能

Strategy MoltBot 负责根据最终确定的数据快照提出结构化的交易建议。它会评估市场状况、流动性以及风险政策，以决定是否进行交易或保持当前持仓状态。对于 NadFun 平台，它必须使用特定的报价函数来计算 `minAmountOut` 值，并拒绝不匹配的路由器请求。

在运行时，它首先使用 `proposeIntentAndSubmit` 函数来构建交易提案，只有在满足明确的提交条件后才会实际提交该提案。

## 快速入门（ClawHub 用户）

请先安装该技能：

```bash
npx clawhub@latest install openfunderse-strategy
```

该技能仅用于提供指导。您需要以下运行时依赖包：

```bash
npm init -y && npm i @wiimdy/openfunderse-agents@0.1.1 --ignore-scripts
```

您可以通过以下命令创建一个可编辑的环境配置文件：

```bash
cp node_modules/@wiimdy/openfunderse-agents/.env.example .env.openfunderse
```

建议在安装前验证源代码：

```bash
npm view @wiimdy/openfunderse-agents@0.1.1 repository.url homepage dist.integrity
```

然后从以下位置配置环境变量并运行相关命令：
- `packages/agents/.env.example`
- `packages/agents/README.md`

运行时依赖来源：
- npm 包：`https://www.npmjs.com/package/@wiimdy/openfunderse-agents`
- 仓库：`https://github.com/wiimdy/openfunderse/tree/main/packages/agents`

在生产环境中请不要使用 `@latest`；请指定一个具体的版本，并定期更新锁定文件（lockfile）。

## 凭据权限

- `STRATEG-AA_OWNER_PRIVATE_KEY` 是用于策略用户操作的 **策略账户所有者的签名密钥**。该密钥不能用于资金管理或托管等敏感操作，应选择权限最低的专用密钥，仅用于控制策略账户。
- 尽可能将此密钥存储在安全管理系统（secret manager/HSM）中，定期轮换密钥，并在测试环境中优先使用测试密钥。

## 调用规则

- 该技能禁止自动调用（`disable-model-invocation: true`）。
- 任何交易请求都必须经过用户的明确批准后才能通过链上或中继器（relayer）进行提交。

## 提交安全机制

`proposeIntentAndSubmit` 函数具有以下安全保护机制：
1. 默认情况下，`STRATEGRequire_EXPLICIT_SUBMIT=true`，要求用户明确指定 `submit=true` 才能提交提案。
2. 若要允许外部提交，必须启用 `STRATEG_AUTO_SUBMIT=true`。
3. `RELAYER_URL` 会经过验证，仅允许来自 `STRATEG_TRUSTED_RELAYER_HOSTS` 中列出的可信主机的请求通过。
4. 如果未获得提交批准，函数会返回 `decision=READY`，不会向中继器或链上发送交易请求。
5. 在生产环境中请保持 `STRATEG_AUTO_SUBMIT=false`，除非您有意启用无人值守的提交功能。

## 输入参数

该技能接受一个遵循以下结构的 `propose_intent` 任务：

```json
{
  "taskType": "propose_intent",
  "fundId": "string",
  "roomId": "string",
  "epochId": "number",
  "snapshot": {
    "snapshotHash": "string",
    "finalized": "boolean",
    "claimCount": "number"
  },
  "marketState": {
    "network": "number",
    "nadfunCurveState": "object",
    "liquidity": "object",
    "volatility": "object",
    "positions": [
      {
        "token": "string",
        "quantity": "string | number",
        "costBasisAsset": "string | number (optional)",
        "openedAt": "unix seconds or milliseconds (optional)"
      }
    ]
  },
  "riskPolicy": {
    "maxNotional": "string",
    "maxSlippageBps": "number",
    "allowlistTokens": ["string"],
    "allowlistVenues": ["string"]
  }
}
```

### 示例输入
```json
{
  "taskType": "propose_intent",
  "fundId": "fund-001",
  "roomId": "telegram-room-abc",
  "epochId": 12,
  "snapshot": {
    "snapshotHash": "0xabc123...",
    "finalized": true,
    "claimCount": 19
  },
  "marketState": {
    "network": 10143,
    "nadfunCurveState": {},
    "liquidity": {},
    "volatility": {},
    "positions": [
      {
        "token": "0xtoken1...",
        "quantity": "1200000000000000000",
        "costBasisAsset": "1000000000000000000",
        "openedAt": 1730000000
      }
    ]
  },
  "riskPolicy": {
    "maxNotional": "1000",
    "maxSlippageBps": 80,
    "allowlistTokens": ["0xtoken1...", "0xtoken2..."],
    "allowlistVenues": ["NadFun", "UniswapV3"]
  }
}
```

## 输出结果

该技能会返回 `PROPOSE` 或 `HOLD` 两种决策结果：
- 当市场状况符合风险政策且存在盈利交易机会时，返回 `PROPOSE`。
```json
{
  "status": "OK",
  "taskType": "propose_intent",
  "fundId": "string",
  "epochId": "number",
  "decision": "PROPOSE",
  "intent": {
    "intentVersion": "V1",
    "fundId": "string",
    "roomId": "string",
    "epochId": "number",
    "vault": "string",
    "action": "BUY | SELL",
    "tokenIn": "string",
    "tokenOut": "string",
    "amountIn": "string",
    "minAmountOut": "string",
    "deadline": "number",
    "maxSlippageBps": "number",
    "snapshotHash": "string"
  },
  "executionPlan": {
    "venue": "NADFUN_BONDING_CURVE | NADFUN_DEX",
    "router": "string",
    "quoteAmountOut": "string"
  },
  "reason": "string",
  "riskChecks": {
    "allowlistPass": "boolean",
    "notionalPass": "boolean",
    "slippagePass": "boolean",
    "deadlinePass": "boolean"
  },
  "confidence": "number",
  "assumptions": ["string"]
}
```

### 提交流程（在满足明确提交条件时）

当使用 `proposeIntentAndSubmit` 并且所有提交条件都得到满足时，系统会执行以下操作：
1. 中继器向 `/api/v1/funds/{fundId}/intents/propose` 发送请求。
2. 策略账户（Strategy AA）会调用 `IntentBook.proposeIntent()` 函数来处理交易提案。

这样可以确保链下和链上的交易记录在相同的时间点得到更新。

### HOLD 决策

当由于风险限制或市场状况不佳而无法提出交易建议时，系统会返回 `HOLD`。

```json
{
  "status": "OK",
  "taskType": "propose_intent",
  "fundId": "string",
  "roomId": "string",
  "epochId": "number",
  "decision": "HOLD",
  "reason": "string",
  "confidence": "number",
  "assumptions": ["string"]
}
```

## 其他规则：
1. **最终性要求**：只有在 `snapshot.finalized` 为 `true` 时才能提交交易提案。
2. **快照引用**：输入数据中必须包含 `snapshotHash` 值。
3. **风险合规性**：如果任何风险政策阈值（如价格波动范围、允许的交易对手等）被超出，系统必须返回 `HOLD` 决策。
4. **NadFun 平台的特殊要求**：针对 NadFun 代币，需要分别评估流动性、价格波动情况以及代币的绑定曲线状态（交易前后的变化）。
5. **仅限提案权限**：该技能仅具有提交提案的权限，无直接执行交易的能力。
6. **输出格式**：输出结果必须是有效的 JSON 格式，并遵循指定的数据结构。
7. **报价要求**：对于 NadFun 平台的交易路径，需要使用报价函数 `getAmountOut` 来计算 `minAmountOut` 值。
8. **不允许零金额交易**：严禁提交 `minAmountOut` 为 0 的交易提案。
9. **异常处理**：如果报价请求失败或返回的路由器不在允许的交易列表中，系统会返回 `HOLD`。
10. **优先执行卖出操作**：如果存在未平仓的代币头寸，系统会先评估卖出操作（如实现利润、设置止损点或提前平仓），然后再考虑买入。
11. **时间戳标准化**：`openedAt` 可能以秒或毫秒为单位；在计算退出条件时需进行时间标准化处理。
12. **禁止自动提交**：除非用户明确允许，否则系统不会自动向中继器或链上发送交易请求。
13. **使用可信中继器**：在生产环境中，请设置 `STRATEG_TRUSTED_RELAYER_HOSTS`，避免使用不可信的中继器地址。