---
name: tonscan-wallet-balance
description: 您可以使用免费的 TonScan API 来查询 TON 区块链钱包的余额、地址信息以及持有的代币数量——无需 API 密钥。无论用户想要查看某个 TON 钱包的余额、查询某个地址的链上数据、转换 nanoton 的数值，还是获取 TON 账户的详细信息，都可以使用这项功能。即使对于像“这个钱包里有多少 TON？”或“帮我检查这个地址”这样的简单请求，也可以通过 TonScan API 来完成。
---
# TonScan钱包余额查询技能

使用TonScan提供的免费公共API查询TON区块链的实时数据，无需进行身份验证。

---

## 核心概念

### 单位：Nanotons与TON
TON区块链将所有余额存储在**Nanotons**（最小的不可分割单位）中。

| 单位 | 值       |
|------|---------|
| 1 TON  | 1,000,000,000 Nanotons |
| 1 Nanoton | 0.000000001 TON |

在向用户显示数据之前，务必将API返回的原始值除以`1_000_000_000`（即1e9）。

**示例：**
```
Raw API value:  1296986856910034000
Divide by 1e9:  1296986856.910034 TON
```

---

## 主要接口：地址信息
```
GET https://api.tonscan.com/api/bt/getAddressInformation?address={ADDRESS}
```

### 快速余额查询（一行代码）
```bash
curl -s "https://api.tonscan.com/api/bt/getAddressInformation?address=EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2" \
  | jq '.json.data.detail.balance'
```

### 包含可读余额的完整响应
```bash
ADDRESS="EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"
curl -s "https://api.tonscan.com/api/bt/getAddressInformation?address=${ADDRESS}" \
  | jq '{
      address: .json.data.detail.address,
      balance_nanoton: .json.data.detail.balance,
      balance_TON: (.json.data.detail.balance | tonumber / 1000000000),
      status: .json.data.detail.status
    }'
```

**示例输出：**
```json
{
  "address": "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
  "balance_nanoton": 1296986856910034000,
  "balance_TON": 1296986856.910034,
  "status": "active"
}
```

---

## 响应结构

完整响应的数据嵌套在`.json.data.detail`中。关键字段包括：

| 字段    | 路径      | 描述         |
|--------|-----------|--------------|
| Balance (raw) | `.json.data.detail.balance` | 余额（以Nanotons为单位，字符串形式） |
| Address | `.json.data.detail.address` | 标准化地址字符串 |
| Status | `.json.data.detail.status` | 状态：`active`、`uninitialized`或`frozen` |
| Last activity | `.json.data.detail.last_activity` | 最后一次交易的Unix时间戳 |

---

## 地址格式说明

TON地址有两种格式，但它们都指向同一个钱包：

- **用户友好格式（EQ...）：** `EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2`
- **原始格式（0:...）：** `0:ED169130705004711...`

TonScan API支持这两种格式。在向用户展示地址时，始终使用用户友好的`EQ...`或`UQ...`格式。

---

## Python示例
```python
import requests

def get_ton_balance(address: str) -> dict:
    url = "https://api.tonscan.com/api/bt/getAddressInformation"
    resp = requests.get(url, params={"address": address})
    resp.raise_for_status()

    detail = resp.json()["json"]["data"]["detail"]
    nanotons = int(detail["balance"])

    return {
        "address": detail["address"],
        "balance_ton": nanotons / 1_000_000_000,
        "balance_nanoton": nanotons,
        "status": detail.get("status", "unknown"),
    }

# Example
info = get_ton_balance("EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2")
print(f"Balance: {info['balance_ton']:,.9f} TON")
# → Balance: 1,296,986,856.910034000 TON
```

---

## JavaScript / Node.js示例
```javascript
async function getTonBalance(address) {
  const url = new URL("https://api.tonscan.com/api/bt/getAddressInformation");
  url.searchParams.set("address", address);

  const res = await fetch(url);
  const data = await res.json();
  const detail = data.json.data.detail;

  const nanotons = BigInt(detail.balance);
  const ton = Number(nanotons) / 1e9;

  return {
    address: detail.address,
    balanceTon: ton,
    balanceNanoton: nanotons.toString(),
    status: detail.status,
  };
}

// Usage
const info = await getTonBalance("EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2");
console.log(`Balance: ${info.balanceTon.toLocaleString()} TON`);
```

> ⚠️ **JavaScript精度说明：** TON余额可能超过`Number.MAX_SAFE_INTEGER`的范围。对于原始的Nanotons值，应使用`BigInt`类型；仅在显示时转换为`Number`类型。

---

## 错误处理

| HTTP状态码 | 含义         | 处理方式       |
|---------|-------------|--------------|
| 200     | 成功         | 解析`.json.data.detail`数据   |
| 400     | 地址格式无效     | 确保地址以`EQ`、`UQ`或`0:`开头 |
| 404     | 地址未找到     | 地址可能有效，但未收到任何TON（余额为0） |
| 429     | 请求速率限制     | 实施指数级重试机制（此为免费API） |
| 5xx     | 服务器错误     | 短暂延迟后重试     |

**检查账户是否为空或未初始化：**
```bash
curl -s "https://api.tonscan.com/api/bt/getAddressInformation?address=..." \
  | jq 'if .json.data.detail.balance == "0" then "Empty wallet" else "Has funds" end'
```

---

## 请求速率限制与使用注意事项

- **免费 tier，无需API密钥**  
- 公司未公布官方的请求速率限制；请将其视为共享的公共资源。  
- 对于生产环境或高频率的查询请求，需添加带有指数级重试机制的逻辑。  
- 对于探索性或一次性查询，无需特殊处理。

---

## 向用户展示结果

在向用户展示余额时，务必保持数据的完整精度，并使用逗号作为分隔符：  
```
✅  1,296,986,856.910034 TON
❌  1296986856.910034
❌  1296986857 TON  (rounded — loses nanoton precision)
```

对于非技术用户，可以将余额保留2-4位小数进行展示，以提高可读性；不过请注意，系统支持完整的精度显示。