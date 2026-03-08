---
name: x402-x-tweet-fetcher
description: 通过 x402 在 Solana 上使用 USDC 购买 Xcatcher 积分，获取 API 密钥，创建 X 爬取任务，监控任务状态，并下载 XLSX 格式的结果文件。
homepage: https://xcatcher.top/docs/
user-invocable: true
metadata: {"openclaw":{"emoji":"🐦","homepage":"https://xcatcher.top/docs/","requires":{"bins":["curl","jq","base64"]}}}
---
# Xcatcher（x402 + X任务）

使用此技能可以执行以下操作：
- 通过Solana上的x402接口购买Xcatcher积分（使用USDC支付）；
- 获取API密钥；
- 创建X爬取任务；
- 监查任务状态；
- 下载XLSX格式的结果文件。

基础URL：`https://xcatcher.top`  
REST接口基础地址：`https://xcatcher.top/api/v1`  
可选的健康检查接口：`https://xcatcher.top/mcp/health`

## 该技能的功能

该技能提供了完整的付费X数据收集流程：
1. 请求Xcatcher积分的报价；
2. 使用Solana的USDC支付报价费用；
3. 将支付的金额兑换为API密钥；
4. 使用API密钥创建爬取任务；
5. 持续监控任务状态，直到任务完成；
6. 下载XLSX格式的结果文件。

## 所需工具

本地工具：
- `curl`
- `jq`
- `base64`

可选工具：
- `python3`（用于简单的JSON数据处理）

## 认证要求

- 在开始使用前，**不需要** `XCATCHER_API_KEY`；
- 在成功完成`buy_points`操作后，您将获得`XCATCHER_API_KEY`；
- 对于后续需要认证的请求，请设置环境变量：`export XCATCHER_API_KEY="your_api_key"`。

## 定价模式

任务费用：
- `mode=normal`：每个用户1积分；
- `mode=deep`：每个用户10积分。

预计费用：
- `estimated_cost = 用户数量 × (mode == normal ? 1 : 10)`

支持的支付链：
- `solana`；
- 如果服务器配置允许，报价信息中也可能包含其他支持的支付链。

> **注意**：切勿硬编码USDC与积分之间的转换率。始终以实时报价信息为准。

---

## 0) 可选的健康检查

```bash
BASE="https://xcatcher.top"
curl -sS "$BASE/mcp/health"
echo
```

---

## 1) 获取Xcatcher积分报价

**注意事项**：
- 报价有效期较短，请在报价生成后立即支付；
- 保存报价ID（`quote_id`）。

```bash
BASE="https://xcatcher.top"
POINTS=1

curl -sS "$BASE/api/v1/x402/quote?points=$POINTS" | tee quote.json
echo

QUOTE_ID=$(jq -r '.quote_id' quote.json)
USDC_MINT=$(jq -r '.accepts.solana.asset' quote.json)
PAY_TO=$(jq -r '.accepts.solana.payTo' quote.json)
AMOUNT_ATOMIC=$(jq -r '.accepts.solana.maxAmountRequired' quote.json)

echo "QUOTE_ID=$QUOTE_ID"
echo "USDC_MINT=$USDC_MINT"
echo "PAY_TO=$PAY_TO"
echo "AMOUNT_ATOMIC=$AMOUNT_ATOMIC"
echo "USDC_AMOUNT=$(python3 - <<'PY'
import json
q=json.load(open('quote.json'))
amt=int(q['accepts']['solana']['maxAmountRequired'])
print(amt/1_000_000)
PY
)"
echo
```

**重要提示**：
- 请保存`QUOTE_ID`，并在后续购买操作中使用它；
- 如果报价失效，请重新生成新的报价。

---

## 2) 在Solana主网上支付USDC

向`PAY_TO`地址发送至少`AMOUNT.Atomic`数量的USDC（SPL）。

然后记录Solana交易的签名：

```bash
SOL_SIG="YOUR_SOLANA_TX_SIGNATURE"
```

---

## 3) 构建`PAYMENT-SIGNATURE`头部

**规则**：
- 对签名内容进行一次base64编码；
- 避免重复编码；
- 确保签名值没有被额外的引号包围。

```bash
PAYMENT_SIGNATURE_B64=$(jq -nc --arg sig "$SOL_SIG" \
  '{"x402Version":1,"scheme":"exact","network":"solana:mainnet","payload":{"signature":$sig}}' \
  | base64 | tr -d '\n')

echo "PAYMENT_SIGNATURE_B64=$PAYMENT_SIGNATURE_B64"
echo
```

---

## 4) 购买积分并获取API密钥

```bash
BASE="https://xcatcher.top"

curl -sS -X POST "$BASE/api/v1/x402/buy_points" \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: $PAYMENT_SIGNATURE_B64" \
  -d "$(jq -nc --arg q "$QUOTE_ID" '{quote_id:$q}')" \
  | tee buy.json
echo

API_KEY=$(jq -r '.api_key' buy.json)
echo "API_KEY=$API_KEY"

export XCATCHER_API_KEY="$API_KEY"
echo "XCATCHER_API_KEY exported."
echo
```

---

## 5) 核对账户余额

```bash
BASE="https://xcatcher.top"

curl -sS "$BASE/api/v1/me" \
  -H "Authorization: Bearer $XCATCHER_API_KEY" \
  | jq .
echo
```

如果收到错误代码`402`，可能表示：
- 报价已失效；
- 支付凭证无效；
- 请使用新的报价和新的支付凭证重新执行步骤1至4。

---

## 6) 创建爬取任务

**规则**：
- `users`表示用户的X用户名（不包含`@`符号）；
- 必须提供`idempotency_key`；
- 如果重复执行相同的请求，请使用相同的`idempotency_key`。

```bash
BASE="https://xcatcher.top"
MODE="normal"
IDEM="test-idem-001"
USERS_JSON='["user1","user2"]'

export MODE USERS_JSON

echo "ESTIMATED_COST_POINTS=$(python3 - <<'PY'
import json, os
users=json.loads(os.environ.get('USERS_JSON', '[]'))
mode=os.environ.get('MODE', 'normal')
per=1 if mode == 'normal' else 10
print(len(users) * per)
PY
)"
echo

curl -sS -X POST "$BASE/api/v1/tasks" \
  -H "Authorization: Bearer $XCATCHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -nc --arg mode "$MODE" --arg idem "$IDEM" --argjson users "$USERS_JSON" \
        '{mode:$mode, users:$users, idempotency_key:$idem}')" \
  | tee task.json | jq .
echo

TASK_ID=$(jq -r '.task_id' task.json)
echo "TASK_ID=$TASK_ID"
echo
```

---

## 7) 监控任务状态，直到任务完成

当`download_url`或`result_path`信息出现时，表示任务已完成。

```bash
BASE="https://xcatcher.top"

while true; do
  J=$(curl -sS "$BASE/api/v1/tasks/$TASK_ID" \
      -H "Authorization: Bearer $XCATCHER_API_KEY")

  echo "$J" | jq '{task_id,status,status_code,updated_time,error_message,result_path,download_url}'

  HAS=$(echo "$J" | jq -r '(.download_url // .result_path // "") | length')
  if [ "$HAS" -gt 0 ]; then
    echo "DONE"
    break
  fi

  sleep 5
done
echo
```

---

## 8) 下载XLSX结果文件

```bash
BASE="https://xcatcher.top"

curl -sS -L -o "task_${TASK_ID}.xlsx" \
  -H "Authorization: Bearer $XCATCHER_API_KEY" \
  "$BASE/api/v1/tasks/$TASK_ID/download"

echo "Saved: task_${TASK_ID}.xlsx"
echo
```

---

## 错误处理

- **错误代码401**：承载令牌（Bearer token）缺失或无效 → 请重新获取API密钥或正确设置`XCATCHER_API_KEY`；
- **错误代码402**：报价无效、支付凭证无效或报价已失效 → 请使用新的报价重新执行购买操作；
- **错误代码429**：达到请求频率限制 → 暂停请求，并根据提示等待一段时间后再试；
- 如果任务延迟或上游服务不可用 → 增加请求间隔并明确显示错误信息。

**给代理的建议**：
- 优先使用实时报价信息，避免依赖缓存数据；
- 重试请求时必须提供明确的`idempotency_key`；
- 将任务结果视为私有数据，始终使用相同的承载令牌（Bearer token）进行下载；
- 不要假设结果文件是公开可访问的URL。