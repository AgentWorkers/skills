---
name: openfunderse-strategy
description: OpenFunderse Strategy 机器人：用于提出交易意图并控制交易意图的提交流程
always: false
disable-model-invocation: false
metadata:
  openclaw:
    installCommand: npx @wiimdy/openfunderse@latest install openfunderse-strategy --with-runtime
    requires:
      env:
        - RELAYER_URL
        - BOT_ID
        - BOT_API_KEY
        - BOT_ADDRESS
        - CHAIN_ID
        - RPC_URL
        - STRATEGY_PRIVATE_KEY
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
    primaryEnv: STRATEGY_PRIVATE_KEY
    skillKey: strategy
---

# Strategy MoltBot 技能

Strategy MoltBot 负责根据最终确定的数据快照提出结构化的交易建议。它会评估市场状况、流动性以及风险政策，以决定是否进行交易或持有资产。
对于 NadFun 平台，必须使用特定的报价函数来计算 `minAmountOut`，并拒绝不匹配的路由器请求。

在运行时，首先使用 `proposeIntentAndSubmit` 函数来构建标准的交易提案，只有在满足明确的提交条件后才会实际提交交易。

## 快速入门（ClawHub 用户）

1) 安装该技能：

```bash
npx clawhub@latest install openfunderse-strategy
```

2) 安装运行时环境并生成环境模板：

```bash
npx @wiimdy/openfunderse@latest install openfunderse-strategy --with-runtime
```

3) 旋转临时启动密钥，并将新的策略钱包信息写入环境配置中：

```bash
npx @wiimdy/openfunderse@latest bot-init \
  --skill-name strategy \
  --yes
```

4) 加载当前 shell 的环境配置：

```bash
set -a; source .env; set +a
```

注意：
- 环境模板默认包含一个临时公钥占位符。
- 在进行资金注入或执行生产级操作之前，务必先运行 `bot-init` 命令。

## 凭据权限

- `STRATEGIES_PRIVATE_KEY` 是用于链上策略操作的 **策略签名密钥（EOA, Externally Owned Account）**。
- 该密钥不得用于资金管理或托管等用途。
- 建议仅使用专用的、权限最低的账户来执行策略操作。
- 尽可能将此密钥存储在安全管理系统（Secret Manager）或硬件安全模块（HSM）中，并定期更换；在测试环境中优先使用测试网密钥。

## 调用策略

- 为了提高可发现性，模型调用功能是启用的（`disable-model-invocation: false`）。
- 除非另有明确设置，否则应严格执行提交保护机制（`STRATEGIES.require_EXPLICIT_SUBMIT=true`，`STRATEGIES_AUTO_SUBMIT=false`）。
- 链上或中继器的提交操作必须经过用户的明确批准。

## 提交安全机制

`proposeIntentAndSubmit` 函数具有以下安全保护机制：

1. 默认情况下，`STRATEGIES.require_EXPLICIT_SUBMIT=true`，要求用户明确指定 `submit=true` 才能提交交易。
2. 只有在启用 `STRATEGIES_AUTO_SUBMIT=true` 时，才能允许外部自动提交交易。
3. `RELAYER_URL` 会经过验证；仅允许来自 `STRATEGIES_TRUSTED_RELAYER_HOSTS` 列表中的可信主机进行提交。
- 如果未获得提交批准，函数会返回 `decision=READY`，不会向中继器发送交易或上传到链上。
- 在生产环境中，除非特意启用自动提交功能，否则 `STRATEGIES_AUTO_SUBMIT` 应保持为 `false`。

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

### PROPOSE 决策
当市场状况符合风险政策且存在盈利交易机会时，返回 `PROPOSE`。

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
当使用 `proposeIntentAndSubmit` 并且满足所有提交条件时，系统会执行以下操作：
1. 中继器向 `/api/v1/funds/{fundId}/intents/propose` 发送请求。
2. 策略签名者（EOA）通过 `IntentBook.proposeIntent()` 函数提交交易建议。

这样可以确保链下和链上的交易记录保持一致。

### HOLD 决策
当由于风险限制或市场状况不佳而无法提出交易建议时，返回 `HOLD`。

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

## 规则

1. **最终性要求**：只有在 `snapshot.finalized` 为 `true` 时才能提交交易建议。
2. **快照引用**：输入数据中的 `snapshotHash` 必须包含在交易建议对象中。
3. **风险合规性**：如果任何风险政策阈值（如价格波动范围、允许的交易对手等）被超出，决策结果必须为 `HOLD`。
4. **NadFun 平台的特殊要求**：针对 NadFun 代币，需要分别评估流动性、价格波动情况以及债券化曲线的状态。
5. **仅限提案权限**：该技能仅具有提案权，无直接执行交易的权利。
6. **输出格式**：确保输出为有效的 JSON 格式，并遵循指定的结构。
7. **报价要求**：对于 NadFun 平台的交易路径，需要使用报价函数 `getAmountOut` 计算 `minAmountOut`。
8. **不允许 `minAmountOut` 为 0**：绝不允许提交 `minAmountOut` 为 0 的交易建议。
9. **异常处理**：如果报价失败或返回的路由器不在允许的交易对手列表中，返回 `HOLD`。
10. **优先执行卖出操作**：如果持有该代币，必须先评估是否满足卖出条件（如 `take-profit`、`stop-loss`、`time-exit` 等），再考虑买入。
11. **时间戳规范化**：`openedAt` 可能以秒或毫秒为单位；在基于时间条件的退出策略执行前需要对其进行规范化处理。
12. **禁止自动提交**：除非用户明确允许，否则不得向中继器或链上提交交易。
13. **使用可信中继器**：在生产环境中，必须设置 `STRATEGIES_TRUSTED_RELAYER_HOSTS`，避免使用不可信的中继器地址。