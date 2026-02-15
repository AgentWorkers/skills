# Epstein邮件API

通过按请求计费的API查询383,000多封由法院公开的Epstein邮件。返回格式为结构化JSON数据，使用x402协议进行支付，货币为USDC。

## 所需凭证

使用此功能需要一个已充值EVM钱包来进行支付。您必须拥有以下凭证：

| 变量 | 格式 | 是否必需 | 说明 |
| --- | --- | --- | --- |
| `XCLAW02_PRIVATE_KEY` | `0x` + 64个十六进制字符 | 是 | 用于签署支付请求的EVM钱包私钥 |

您的钱包中必须持有USDC（币种：eip155:8453）。每次API请求的费用为0.001 USDC。

**安全提示：** 请勿记录、显示或泄露您的私钥，仅使用环境变量来存储私钥。请使用专门用于支付的热钱包，并确保钱包中仅存放所需资金，避免使用持有大量资金的钱包。

## 适用场景

- 当用户询问关于Epstein、Jeffrey Epstein或Ghislaine Maxwell的邮件时；
- 当用户希望搜索与Epstein案件相关的法院公开文件或公共记录时；
- 当用户需要从Epstein的邮件档案中获取结构化邮件数据（发送者、接收者、日期、主题、正文）时；
- 当用户希望交叉查询邮件文件中的名称、日期或关联信息时。

## 使用方法

| 用户请求 | 操作建议 |
| --- | --- |
| “搜索包含‘X’的Epstein邮件” | 使用`/api/search`接口（费用：1次请求，0.001美元）。请在使用前先确认用户需求。 |
| “谁给谁发了邮件？” | 使用`/api/emails`接口，并设置`from`/`to`过滤条件（费用：1次请求）。请先确认用户需求。 |
| “显示指定日期的邮件” | 使用`/api/emails`接口，并设置`date`过滤条件（费用：1次请求）。请先确认用户需求。 |
| “有多少邮件提到了‘X’？” | 先使用免费的`/api/preview`接口（免费）查看邮件数量。如需完整结果，请用户确认后使用付费搜索。 |
| “获取所有邮件” | **请先向用户说明费用**。全量查询可能需要约0.384美元（每页384条邮件，共384次请求）。在开始之前务必获得用户明确同意。 |
| “Epstein文件里有什么内容？” | 可以向用户解释数据集的内容，无需通过API查询。 |

**重要提示：** 在进行任何付费请求之前，请务必先与用户确认。未经用户明确同意和费用估算，切勿直接遍历全部数据。

## 支付注意事项

- **在进行多次请求之前，请务必估算总费用。** 计算公式：`ceil(total_results / 1000) * 0.001`  
- **请先使用免费的`/api/preview`接口**来查看搜索结果的数量。  
- **未经用户明确同意，切勿自动遍历全部结果。**  
- **单次请求费用为0.001美元**（无论是一次搜索还是一次过滤查询）。请在使用前先确认用户需求。  
- 如果您的x402客户端支持，请设置支付限额（例如`max_amount`参数）。

## API基础URL

```
https://epsteinemails.xyz
```

## 接口详情

### GET /api/preview （免费）

提供免费预览功能，用于在付费请求前查看搜索结果数量。每分钟请求次数有限制（10次），返回的邮件正文会被截断，最多显示10条结果。**无需支付。**

**查询参数：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `q` | 字符串 | 搜索查询内容（至少2个字符） |

**响应内容：**

```json
{
  "query": "american",
  "total_matches": 15,
  "returned": 10,
  "preview": true,
  "results": [
    {
      "from": "Natalia Molotkova",
      "to": "",
      "date": "Wed 2/1/2017 8:06:26 PM",
      "subject": "Round Trip ticket Barcelona/Miami",
      "body": "Title: American Express Middle seats OK? Regards, Natal...",
      "source_file": "EFTA02205655.pdf"
    }
  ]
}
```

### GET /api/emails （付费——0.001美元）

提供邮件列表和过滤功能，支持分页。需要通过x402协议进行支付。

**查询参数：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `from` | 字符串 | 按发送者过滤（不区分大小写） |
| `to` | 字符串 | 按接收者过滤 |
| `subject` | 字符串 | 按邮件主题过滤 |
| `date` | 字符串 | 按日期过滤（例如：“2017”或“Wed”） |
| `source_file` | 字符串 | 按邮件来源PDF文件名过滤 |
| `limit` | 整数 | 每页显示的最大结果数量（默认/最大值：1000） |
| `offset` | 整数 | 分页偏移量（默认值：0） |

**响应内容：**

```json
{
  "total": 383579,
  "returned": 2,
  "offset": 0,
  "limit": 2,
  "has_more": true,
  "next_offset": 2,
  "emails": [
    {
      "from": "Natalia Molotkova",
      "to": "",
      "date": "Wed 2/1/2017 8:06:26 PM",
      "subject": "Round Trip ticket Barcelona/Miami",
      "body": "Title: American Express...",
      "cc": "",
      "bcc": "",
      "source_file": "EFTA02205655.pdf",
      "source_url": "https://www.justice.gov/epstein/files/DataSet%2011/EFTA02205655.pdf"
    }
  ]
}
```

### GET /api/search （付费——0.001美元）

支持在所有邮件字段中进行全文搜索。需要通过x402协议进行支付。

**查询参数：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `q` | 字符串 | 搜索查询内容（必须在查询中包含，可搜索发送者、接收者、主题、正文、日期或抄送/密送字段） |
| `limit` | 整数 | 每页显示的最大结果数量（默认/最大值：1000） |
| `offset` | 整数 | 分页偏移量（默认值：0） |

**响应内容：**

```json
{
  "query": "schedule",
  "total_matches": 42,
  "returned": 2,
  "offset": 0,
  "limit": 2,
  "has_more": true,
  "next_offset": 2,
  "results": [
    {
      "index": 5,
      "email": {
        "from": "Jeffrey Epstein",
        "to": "Ghislaine Maxwell",
        "date": "Thu 3/15/2017 10:30:00 AM",
        "subject": "Schedule",
        "body": "...",
        "cc": "",
        "bcc": "",
        "source_file": "EFTA02205700.pdf",
        "source_url": "https://www.justice.gov/epstein/files/DataSet%2011/EFTA02205700.pdf"
      }
    }
  ]
}
```

## 快速入门（Python示例）

```python
# pip install "x402[httpx,evm]" eth_account

import asyncio
import os
from eth_account import Account
from x402 import x402Client
from x402.http.clients import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

# Load private key from environment variable — never hardcode
account = Account.from_key(os.environ["XCLAW02_PRIVATE_KEY"])
client = x402Client()
register_exact_evm_client(client, EthAccountSigner(account))

async def main():
    async with x402HttpxClient(client) as http:
        resp = await http.get(
            "https://epsteinemails.xyz/api/search?q=schedule&limit=10"
        )
        data = resp.json()
        print(f"Found {data['total_matches']} matches")
        for r in data["results"]:
            e = r["email"]
            print(f"  {e['from']} -> {e['to']}: {e['subject']}")

asyncio.run(main())
```

## 分页说明

所有支持付费的接口都支持分页。每次请求最多返回1000条结果。

**在分页之前，请先估算费用并获得用户同意：**

```python
# Step 1: Use free preview to check total matches
preview = await http.get(
    "https://epsteinemails.xyz/api/preview?q=travel"
)
total = preview.json()["total_matches"]
est_cost = ((total + 999) // 1000) * 0.001
print(f"{total} matches — full retrieval will cost ~${est_cost:.3f} ({(total + 999) // 1000} requests)")
# Step 2: Only proceed with user approval

# Step 3: Paginate
all_results = []
offset = 0
while True:
    resp = await http.get(
        f"https://epsteinemails.xyz/api/search?q=travel&limit=1000&offset={offset}"
    )
    data = resp.json()
    all_results.extend(data["results"])
    if not data["has_more"]:
        break
    offset = data["next_offset"]
```

## 支付详情

| 参数 | 值 | 说明 |
| --- | --- | --- |
| 协议 | x402（需要通过HTTP 402协议进行支付） |
| 费用 | 每次请求0.001美元 |
| 使用的区块链网络 | Base（币种：eip155:8453） |
| 代币 | USDC（地址：0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913） |
| 手续费 | 无需支付（由Coinbase CDP平台协助处理） |
| 支付平台 | Coinbase CDP（地址：https://api.cdp.coinbase.com/platform/v2/x402） |
| 收款方地址 | 0xF9702D558eAEC22a655df33b1E3Ac996fAC2f1Ea |

使用兼容x402协议的客户端时，支付流程如下：

1. 客户端发送GET请求。
2. 服务器返回402状态码，并在响应头中说明支付要求。
3. 客户端使用USDC进行支付，并在请求头中包含支付信息。
4. 服务器通过Coinbase CDP平台验证支付信息，完成链上结算后返回数据。

## 数据来源

所有邮件内容均来自美国司法部发布的PDF文件（网址：https://www.justice.gov/epstein）。每封邮件的记录中包含`source_file`和`source_url`字段，这些字段可直接链接到原始PDF文件。

## 错误处理

| 状态码 | 含义 |
| --- | --- |
| 200 | 请求成功 |
| 400 | 请求错误（例如缺少`q`参数） |
| 402 | 需要支付（x402协议会自动处理支付请求） |
| 429 | 请求次数达到限制（仅适用于预览接口，请等待60秒后重试） |

## 相关链接

- API接口：https://epsteinemails.xyz  
- x402协议：https://x402.org  
- x402 Python SDK：`pip install "x402[httpx,evm]"`  
- 数据来源文件：https://www.justice.gov/epstein