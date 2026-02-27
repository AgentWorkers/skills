---
name: Clank Human Bitcoin Address
description: 这是一个以代理（Agent）为中心的服务，用于在 clank.money 平台上注册和管理人类创建的比特币地址（遵循 BIP-353 标准），并支持 L402 标准的比特币支付。
---
# “Clank Human Bitcoin Address”技能

使用此技能可以在`clank.money`下注册并更新一个人类可读的比特币地址（该地址遵循BIP-353标准，通过DNS支付指令指向一个BIP-321 URI）。

## 重要提示：

- 成功完成注册后，系统会返回`managementToken`（响应代码为`201`或`202`）。
- 你必须立即且安全地保存`managementToken`。
- **警告**：如果`managementToken`丢失，将无法对该地址进行后续的更新操作。

## API接口：

- `POST https://clank.money/api/v1/registrations`：用于注册新地址
- `GET https://clank.money/api/v1/registrations/{username}`：用于查询已注册的地址信息
- `PATCH https://clank.money/api/v1/registrations/{username}`：用于更新已注册的地址信息

## 注册所需信息：

- `username`：
  - 由小写字母、数字和连字符组成
  - 长度为3到32个字符
  - 不能以`-`开头或结尾
- `bip321Uri`：
  - 必填项
  - 必须以`bitcoin:`开头
  - 必须是有效的BIP-321地址
  **强烈建议**：包含BOLT12交易信息（格式为`lno=...`）

## 严格的注册流程：

注册费用为999sat。

1. 提交未经验证的注册请求（`POST /api/v1/registrations`）：
  - 响应代码可能为`409 username_unavailable`或`402 payment_required`。
2. 如果收到`409`错误，选择另一个用户名并重复步骤1。
  - 仍然会收到`402 payment_required`的响应。
3. 从`402`响应中获取L402挑战信息（`macaroon`、`invoice`、`paymentHash`、`amountSats`、`expiresAt`）。
  - 将这些信息保存下来（例如：`invoice`和`macaroon`）。
4. 支付Lightning网络发票并获取`preimage`。
5. 重新发送相同的`POST /api/v1/registrations`请求，但添加`Authorization`头：
    ```
    Authorization: L402 <macaroon>:<preimage>
    ```
  - 此时应收到`201`或`202`的响应，并且会包含`managementToken`。
6. 立即保存`managementToken`。
  **警告**：如果`managementToken`丢失，将无法对地址进行任何更新操作。
  - 将`managementToken`保存到安全的位置。

## 快速操作示例（Bash脚本）：

```bash
set -euo pipefail

BASE="https://clank.money"
USERNAME="satoshi"
BIP321_URI='bitcoin:?lno=lno1examplebolt12offer'
TOKEN_FILE="$HOME/.clank/${USERNAME}.management_token"

mkdir -p "$(dirname "$TOKEN_FILE")"

# 1) Create challenge (or fail fast if name taken)
curl -sS -X POST "$BASE/api/v1/registrations" \
  -H "content-type: application/json" \
  --data "{\"username\":\"$USERNAME\",\"bip321Uri\":\"$BIP321_URI\"}" \
  > /tmp/clank_register_challenge.json

ERROR_CODE="$(python3 -c 'import json; d=json.load(open("/tmp/clank_register_challenge.json")); e=d.get("error"); print((e.get("code") if isinstance(e,dict) else e) or "")')"
if [ "$ERROR_CODE" = "username_unavailable" ]; then
  echo "Username is taken. Pick another USERNAME and rerun."
  exit 1
fi
if [ "$ERROR_CODE" != "payment_required" ]; then
  echo "Unexpected challenge response:"
  cat /tmp/clank_register_challenge.json
  exit 1
fi

MACAROON="$(python3 -c 'import json; print(json.load(open("/tmp/clank_register_challenge.json"))["macaroon"])')"
INVOICE="$(python3 -c 'import json; print(json.load(open("/tmp/clank_register_challenge.json"))["invoice"])')"
echo "Pay this invoice now:"
echo "$INVOICE"

# 2) After payment, paste your preimage
read -r -p "PASTE_PREIMAGE=" PREIMAGE

# 3) Complete paid registration
curl -sS -X POST "$BASE/api/v1/registrations" \
  -H "content-type: application/json" \
  -H "Authorization: L402 $MACAROON:$PREIMAGE" \
  --data "{\"username\":\"$USERNAME\",\"bip321Uri\":\"$BIP321_URI\"}" \
  > /tmp/clank_register_result.json

MGMT="$(python3 -c 'import json; d=json.load(open("/tmp/clank_register_result.json")); print(d.get("managementToken",""))')"
if [ -z "$MGMT" ]; then
  echo "No managementToken in final response:"
  cat /tmp/clank_register_result.json
  exit 1
fi

# 4) CRITICAL: persist token securely for future updates
printf '%s\n' "$MGMT" > "$TOKEN_FILE"
chmod 600 "$TOKEN_FILE"
echo "Saved management token to $TOKEN_FILE"
```

## 更新流程：

1. 从安全文件中读取之前保存的`managementToken`。
2. 使用以下请求更新地址信息：
    ```
    PATCH /api/v1/registrations/{username}
    ```
    - 请求头：`Authorization: Bearer <managementToken>`
    - 请求体中包含新的`bip321Uri`。

示例代码：
```bash
USERNAME="satoshi"
TOKEN_FILE="$HOME/.clank/${USERNAME}.management_token"
NEW_BIP321='bitcoin:?lno=lno1newbolt12offer'
MGMT="$(cat "$TOKEN_FILE")"

curl -sS -X PATCH "https://clank.money/api/v1/registrations/$USERNAME" \
  -H "content-type: application/json" \
  -H "Authorization: Bearer $MGMT" \
  --data "{\"bip321Uri\":\"$NEW_BIP321\"}"
```