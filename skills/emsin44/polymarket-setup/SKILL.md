---
name: polymarket-setup
description: 在 Polymarket 上设置自动化交易系统。内容包括钱包设置、代币审批、API 认证、市场探索、订单下达、WebSocket 数据流以及持仓管理。
metadata:
  {
    "openclaw": {
      "requires": {
        "env": [
          "POLYMARKET_PRIVATE_KEY",
          "POLYMARKET_PUBLIC_ADDRESS",
          "POLYMARKET_PROXY_ADDRESS",
          "POLYMARKET_SIGNATURE_TYPE",
          "POLYMARKET_API_KEY",
          "POLYMARKET_API_SECRET",
          "POLYMARKET_API_PASSPHRASE"
        ],
        "optionalEnv": [
          "POLYMARKET_BUILDER_API_KEY",
          "POLYMARKET_BUILDER_SECRET",
          "POLYMARKET_BUILDER_PASSPHRASE"
        ]
      }
    }
  }
---
# 技能：Polymarket 交易设置

当用户需要执行以下操作时，请使用此技能：
- 在 Polymarket 上设置自动化交易
- 从零开始构建 Polymarket 交易机器人
- 配置钱包、API 凭据或 Polymarket 的代币使用权限
- 了解如何连接到 Polymarket 的 API
- 调试现有的 Polymarket 机器人设置中的问题

完整的技术参考资料请参阅 `GUIDE.md`（与本文件位于同一目录中）。在开始之前，请先阅读该文件。

---

## 需要设置的内容

在 Polymarket 上进行交易需要以下四个条件：
1. 一个已充值且绑定了 USDC 的代理钱包（位于 Polygon 网络上）
2. 代币使用权限（允许使用 USDC 进行交易合约操作）
3. CLOB API 凭据（从钱包中获取并存储在环境变量 `env` 中）
4. 确保所有四个 API 接口的连接都已验证

---

## 逐步操作指南

### 第一步：检查现有配置

在开始之前，请检查以下内容：
- 是否存在包含 `POLYMARKET_PRIVATE_KEY` 和 `POLYMARKET_PROXY_ADDRESS` 的 `.env` 文件？
- 是否存在包含 Polymarket 配置的 `config.json` 文件？
- 是否已有可使用的机器人目录？

如果凭据已经存在，请直接加载并验证这些凭据，无需从头开始设置。

### 第二步：环境配置

如果需要从头开始设置，请创建一个 `.env` 文件，内容如下：

```bash
POLYMARKET_PRIVATE_KEY=0x...
POLYMARKET_PUBLIC_ADDRESS=0x...     # proxy wallet address
POLYMARKET_PROXY_ADDRESS=0x...      # same as PUBLIC_ADDRESS for type 2
POLYMARKET_SIGNATURE_TYPE=2
POLYMARKET_WEBSOCKET_URL=wss://ws-subscriptions-clob.polymarket.com
POLYMARKET_DATA_API=https://data-api.polymarket.com
```

代理钱包地址可以从用户的 Polymarket 账户设置页面获取。

### 第三步：安装依赖项

```bash
pip install "py-clob-client>=0.28.0" httpx "websocket-client>=1.9.0" orjson pandas python-dotenv
```

或者将依赖项添加到 `pyproject.toml` 文件中，然后运行 `uv sync` 命令。

### 第四步：获取代币使用权限

**推荐新用户使用的方法：** 通过 Polymarket 的 Web 应用程序充值 USDC——系统会自动处理权限审批。

**服务器端部署方法：** 使用 `GUIDE.md` 第 4 节中描述的程序化权限审批流程。此过程需要 Polymarket Builder API 凭据（与 CLOB 凭据分开）。

需要审批的四个交易合约在 `GUIDE.md` 的第 2 节中有详细说明。

### 第五步：获取并保存 API 凭据

```python
from py_clob_client.client import ClobClient

client = ClobClient(
    "https://clob.polymarket.com",
    key=os.getenv("POLYMARKET_PRIVATE_KEY"),
    chain_id=137,
    signature_type=int(os.getenv("POLYMARKET_SIGNATURE_TYPE", "2")),
    funder=os.getenv("POLYMARKET_PROXY_ADDRESS"),
)
creds = client.derive_api_key()
# Write credentials to .env — do not log or print them
```

将获取到的 API 凭据添加到 `.env` 文件中：

```bash
POLYMARKET_API_KEY=...
POLYMARKET_API_SECRET=...
POLYMARKET_API_PASSPHRASE=...
```

在后续启动程序时，直接从环境变量 `env` 中读取这些凭据，无需重新生成（详见 `GUIDE.md` 第 3 节）。

### 第六步：验证连接是否正常

依次测试所有 API 接口的连接是否正常。如果某个步骤失败，请立即停止并排查问题。

```python
import httpx, json

# 1. Gamma API
event = httpx.get("https://gamma-api.polymarket.com/events/slug/bitcoin-price-on-february-11").json()
print(f"Gamma OK: {event.get('title')}")

# 2. CLOB REST - order book
book = httpx.get("https://clob.polymarket.com/book", params={"token_id": "<any_token_id>"}).json()
print(f"CLOB OK: {len(book.get('bids', []))} bids, {len(book.get('asks', []))} asks")

# 3. Data API - positions
positions = httpx.get(
    "https://data-api.polymarket.com/positions",
    params={"user": os.getenv("POLYMARKET_PROXY_ADDRESS")}
).json()
print(f"Data API OK: {len(positions)} open positions")
```

### 第七步：下达测试订单

下达一个数量为 2 的订单，价格应远低于市场价（在实际市场中这种订单成交的概率非常低），以验证整个交易流程（包括签名和提交过程），同时确保不会因价格问题导致订单无法成交：

```python
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

# Use a real token ID from Step 6, price far from market
order = OrderArgs(price=0.02, side=BUY, size=2, token_id="<token_id>")
signed = client.create_order(order)
resp = client.post_order(signed, OrderType.FAK)
print(resp)  # Should show success: true
```

---

## 需要记住的关键信息

- **区块链网络：** Polygon 主网（ID：137）
- **货币：** USDC（地址：`0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`）
- **签名类型 2** 是程序化交易的标准格式
- **代理钱包地址 ≠ 签名密钥地址**——持仓记录保存在代理钱包中，订单由外部账户（EOA）签署
- **clobTokenIds[0] = 是，clobTokenIds[1] = 否**——请勿混淆这两个字段
- **最小订单金额：$1.00**——`订单数量 * 价格 >= 1.0`
- **订单数量必须是整数**——始终使用 `int()` 类型
- **仅在对订单状态为 `MINED` 时更新持仓记录**——状态为 `MATCHED` 的订单可能无法更新持仓

---

## 常见的首次使用失败原因

| 错误症状 | 可能原因 |
|---|---|
| 账户余额不足 | 使用了错误的地址（应使用代理钱包地址而非外部账户地址），或者未充值 USDC |
| 订单被默默拒绝 | 价格的小数位数过多——将价格四舍五入到小数点后两位（如果价格小于 0.04 或大于 0.96，则保留三位小数） |
| 订单金额错误 | `订单数量 * 价格 < 1.0` |
- WebSocket 无法发送数据 | 订阅消息格式错误，或者使用了数组而非对象格式 |
- 持仓记录始终为空 | 查询了外部账户地址而非代理钱包地址 |
- 交易后持仓记录未更新 | 在订单状态为 `MATCHED` 时尝试更新持仓记录 |

---

## 参考资料

完整的 API 参考、所有代码示例及详细说明请参阅：**GUIDE.md**（与本文件位于同一目录中）。