---
name: x402
description: "基于HTTP 402 “Payment Required”标准的互联网原生支付方式。您可以设置为买家以支付API访问费用，或者设置为卖家来通过API实现盈利。"
metadata: {"openclaw":{"emoji":"💸"}}
---

# x402 支付协议

x402 是一种基于 HTTP `402 Payment Required` 状态码构建的开源、互联网原生的支付标准。它支持客户端与服务器之间的程序化支付，无需账户、会话或凭证管理。

**主要优势：**
- 无协议费用（仅收取区块链网络费用）
- 无摩擦（无需账户或进行 KYC 验证）
- 通过稳定币实现即时结算
- 适用于 AI 代理和自动化系统

**文档：** https://docs.x402.org | **GitHub：** https://github.com/coinbase/x402

---

## x402 的工作原理

1. 客户端向服务器请求资源。
2. 服务器返回 `402 Payment Required` 响应，并附带支付指令。
3. 客户端签名并提交支付数据。
4. 服务器验证支付（可选地通过第三方机构进行验证）。
5. 服务器返回请求的资源。

---

## 环境变量

### 对于买家（客户端）
```bash
# EVM wallet private key (Ethereum/Base/Polygon)
EVM_PRIVATE_KEY=0x...

# Solana wallet private key (base58 encoded)
SVM_PRIVATE_KEY=...

# Target server URL
RESOURCE_SERVER_URL=http://localhost:4021
ENDPOINT_PATH=/weather
```

### 对于卖家（服务器）
```bash
# Your EVM wallet address to receive payments
EVM_ADDRESS=0x...

# Your Solana wallet address to receive payments
SVM_ADDRESS=...

# Facilitator URL (see list below)
FACILITATOR_URL=https://x402.org/facilitator
```

---

## 网络标识符（CAIP-2）

| 网络 | CAIP-2 ID | 描述 |
|---------|-----------|-------------|
| **Base** | | |
| Base 主网 | `eip155:8453` | Base L2 主网 |
| Base Sepolia | `eip155:84532` | Base L2 测试网 |
| **Solana** | | |
| Solana 主网 | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | Solana 主网 |
| Solana 开发网 | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` | Solana 测试网 |
| **Polygon** | | |
| Polygon 主网 | `eip155:137` | Polygon PoS 主网 |
| Polygon Amoy | `eip155:80002` | Polygon 测试网 |
| **Avalanche** | | |
| Avalanche C-Chain | `eip155:43114` | Avalanche 主网 |
| Avalanche Fuji | `eip155:43113` | Avalanche 测试网 |
| **Sei** | | |
| Sei 主网 | `eip155:1329` | Sei EVM 主网 |
| Sei 测试网 | `eip155:713715` | Sei EVM 测试网 |
| **X Layer** | | |
| X Layer 主网 | `eip155:196` | OKX L2 主网 |
| X Layer 测试网 | `eip155:1952` | OKX L2 测试网 |
| **SKALE** | | |
| SKALE Base | `eip155:1187947933` | SKALE 主网 |
| SKALE Base Sepolia | `eip155:324705682` | SKALE 测试网 |


---

## 第三方机构（支付验证与区块链结算）

第三方机构负责处理支付验证和区块链结算。以下是可选的机构：

| 名称 | URL | 说明 |
|------|-----|-------|
| x402.org | `https://x402.org/facilitator` | 默认机构，仅支持测试网 |
| Coinbase | `https://api.cdp.coinbase.com/platform/v2/x402` | 生产环境 |
| PayAI | `https://facilitator.payai.network` | 生产环境 |
| Corbits | `https://facilitator.corbits.dev` | 生产环境 |
| x402rs | `https://facilitator.x402.rs` | 生产环境 |
| Dexter | `https://x402.dexter.cash` | 生产环境 |
| Heurist | `https://facilitator.heurist.xyz` | 生产环境 |
| Kobaru | `https://gateway.kobaru.io` | 生产环境 |
| Mogami | `https://facilitator.mogami.tech` | 生产环境 |
| Nevermined | `https://api.live.nevermined.app/api/v1/` | 生产环境 |
| Openfacilitator | `https://pay.openfacilitator.io` | 生产环境 |
| Solpay | `https://x402.solpay.cash` | 生产环境 |
| Primer | `https://x402.primer.systems` | 生产环境 |
| xEcho | `https://facilitator.xechoai.xyz` | 生产环境 |

---

## 客户端示例（TypeScript 使用 fetch）

安装依赖项：
```bash
npm install @x402/fetch @x402/evm @x402/svm viem @solana/kit @scure/base dotenv
```

代码：
```typescript
import { config } from "dotenv";
import { x402Client, wrapFetchWithPayment, x402HTTPClient } from "@x402/fetch";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { registerExactSvmScheme } from "@x402/svm/exact/client";
import { privateKeyToAccount } from "viem/accounts";
import { createKeyPairSignerFromBytes } from "@solana/kit";
import { base58 } from "@scure/base";

config();

const evmPrivateKey = process.env.EVM_PRIVATE_KEY as `0x${string}`;
const svmPrivateKey = process.env.SVM_PRIVATE_KEY as string;
const url = `${process.env.RESOURCE_SERVER_URL}${process.env.ENDPOINT_PATH}`;

async function main(): Promise<void> {
  const evmSigner = privateKeyToAccount(evmPrivateKey);
  const svmSigner = await createKeyPairSignerFromBytes(base58.decode(svmPrivateKey));

  const client = new x402Client();
  registerExactEvmScheme(client, { signer: evmSigner });
  registerExactSvmScheme(client, { signer: svmSigner });

  const fetchWithPayment = wrapFetchWithPayment(fetch, client);

  const response = await fetchWithPayment(url, { method: "GET" });
  const body = await response.json();
  console.log("Response:", body);

  if (response.ok) {
    const paymentResponse = new x402HTTPClient(client).getPaymentSettleResponse(
      name => response.headers.get(name)
    );
    console.log("Payment:", JSON.stringify(paymentResponse, null, 2));
  }
}

main().catch(console.error);
```

## 客户端示例（TypeScript 使用 axios）

安装依赖项：
```bash
npm install @x402/axios @x402/evm @x402/svm axios viem @solana/kit @scure/base dotenv
```

代码：
```typescript
import { config } from "dotenv";
import { x402Client, wrapAxiosWithPayment, x402HTTPClient } from "@x402/axios";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { registerExactSvmScheme } from "@x402/svm/exact/client";
import { privateKeyToAccount } from "viem/accounts";
import { createKeyPairSignerFromBytes } from "@solana/kit";
import { base58 } from "@scure/base";
import axios from "axios";

config();

const evmPrivateKey = process.env.EVM_PRIVATE_KEY as `0x${string}`;
const svmPrivateKey = process.env.SVM_PRIVATE_KEY as string;
const url = `${process.env.RESOURCE_SERVER_URL}${process.env.ENDPOINT_PATH}`;

async function main(): Promise<void> {
  const evmSigner = privateKeyToAccount(evmPrivateKey);
  const svmSigner = await createKeyPairSignerFromBytes(base58.decode(svmPrivateKey));

  const client = new x402Client();
  registerExactEvmScheme(client, { signer: evmSigner });
  registerExactSvmScheme(client, { signer: svmSigner });

  const api = wrapAxiosWithPayment(axios.create(), client);

  const response = await api.get(url);
  console.log("Response:", response.data);

  if (response.status < 400) {
    const paymentResponse = new x402HTTPClient(client).getPaymentSettleResponse(
      name => response.headers[name.toLowerCase()]
    );
    console.log("Payment:", paymentResponse);
  }
}

main().catch(console.error);
```

## 客户端示例（Python 使用 httpx（异步）**

安装依赖项：
```bash
pip install "x402[httpx,evm,svm]" python-dotenv
```

代码：
```python
import asyncio
import os
from dotenv import load_dotenv
from eth_account import Account

from x402 import x402Client
from x402.http import x402HTTPClient
from x402.http.clients import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client
from x402.mechanisms.svm import KeypairSigner
from x402.mechanisms.svm.exact.register import register_exact_svm_client

load_dotenv()

async def main() -> None:
    evm_private_key = os.getenv("EVM_PRIVATE_KEY")
    svm_private_key = os.getenv("SVM_PRIVATE_KEY")
    base_url = os.getenv("RESOURCE_SERVER_URL")
    endpoint_path = os.getenv("ENDPOINT_PATH")

    client = x402Client()

    if evm_private_key:
        account = Account.from_key(evm_private_key)
        register_exact_evm_client(client, EthAccountSigner(account))

    if svm_private_key:
        svm_signer = KeypairSigner.from_base58(svm_private_key)
        register_exact_svm_client(client, svm_signer)

    http_client = x402HTTPClient(client)
    url = f"{base_url}{endpoint_path}"

    async with x402HttpxClient(client) as http:
        response = await http.get(url)
        await response.aread()
        print(f"Response: {response.text}")

        if response.is_success:
            try:
                settle_response = http_client.get_payment_settle_response(
                    lambda name: response.headers.get(name)
                )
                print(f"Payment: {settle_response.model_dump_json(indent=2)}")
            except ValueError:
                print("No payment response header found")

if __name__ == "__main__":
    asyncio.run(main())
```

## 客户端示例（Python 使用 requests（同步）**

安装依赖项：
```bash
pip install "x402[requests,evm,svm]" python-dotenv
```

代码：
```python
import os
from dotenv import load_dotenv
from eth_account import Account

from x402 import x402ClientSync
from x402.http import x402HTTPClientSync
from x402.http.clients import x402_requests
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client
from x402.mechanisms.svm import KeypairSigner
from x402.mechanisms.svm.exact.register import register_exact_svm_client

load_dotenv()

def main() -> None:
    evm_private_key = os.getenv("EVM_PRIVATE_KEY")
    svm_private_key = os.getenv("SVM_PRIVATE_KEY")
    base_url = os.getenv("RESOURCE_SERVER_URL")
    endpoint_path = os.getenv("ENDPOINT_PATH")

    client = x402ClientSync()

    if evm_private_key:
        account = Account.from_key(evm_private_key)
        register_exact_evm_client(client, EthAccountSigner(account))

    if svm_private_key:
        svm_signer = KeypairSigner.from_base58(svm_private_key)
        register_exact_svm_client(client, svm_signer)

    http_client = x402HTTPClientSync(client)
    url = f"{base_url}{endpoint_path}"

    with x402_requests(client) as session:
        response = session.get(url)
        print(f"Response: {response.text}")

        if response.ok:
            try:
                settle_response = http_client.get_payment_settle_response(
                    lambda name: response.headers.get(name)
                )
                print(f"Payment: {settle_response.model_dump_json(indent=2)}")
            except ValueError:
                print("No payment response header found")

if __name__ == "__main__":
    main()
```

## 客户端示例（Python 使用 Go 和 net/http）

安装依赖项：
```bash
go get github.com/coinbase/x402/go
go get github.com/joho/godotenv
```

代码：
```go
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"

	x402 "github.com/coinbase/x402/go"
	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load()

	evmPrivateKey := os.Getenv("EVM_PRIVATE_KEY")
	svmPrivateKey := os.Getenv("SVM_PRIVATE_KEY")
	url := os.Getenv("SERVER_URL")
	if url == "" {
		url = "http://localhost:4021/weather"
	}

	// Create x402 client with EVM and SVM support
	client, err := x402.NewClientBuilder().
		WithEvmSigner(evmPrivateKey).
		WithSvmSigner(svmPrivateKey).
		Build()
	if err != nil {
		fmt.Printf("Failed to create client: %v\n", err)
		os.Exit(1)
	}

	// Wrap HTTP client with payment handling
	httpClient := client.WrapHTTPClient(&http.Client{Timeout: 30 * time.Second})

	ctx := context.Background()
	req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
	resp, err := httpClient.Do(req)
	if err != nil {
		fmt.Printf("Request failed: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	var responseData interface{}
	json.NewDecoder(resp.Body).Decode(&responseData)
	prettyJSON, _ := json.MarshalIndent(responseData, "", "  ")
	fmt.Printf("Response: %s\n", string(prettyJSON))
}
```

---

## 卖家示例（服务器端）

## 客户端示例（TypeScript 使用 Express）

安装依赖项：
```bash
npm install express @x402/express @x402/core @x402/evm @x402/svm dotenv
```

代码：
```typescript
import { config } from "dotenv";
import express from "express";
import { paymentMiddleware, x402ResourceServer } from "@x402/express";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { ExactSvmScheme } from "@x402/svm/exact/server";
import { HTTPFacilitatorClient } from "@x402/core/server";

config();

const evmAddress = process.env.EVM_ADDRESS as `0x${string}`;
const svmAddress = process.env.SVM_ADDRESS;
const facilitatorUrl = process.env.FACILITATOR_URL || "https://x402.org/facilitator";

const facilitatorClient = new HTTPFacilitatorClient({ url: facilitatorUrl });
const app = express();

app.use(
  paymentMiddleware(
    {
      "GET /weather": {
        accepts: [
          { scheme: "exact", price: "$0.001", network: "eip155:84532", payTo: evmAddress },
          { scheme: "exact", price: "$0.001", network: "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1", payTo: svmAddress },
        ],
        description: "Weather data",
        mimeType: "application/json",
      },
    },
    new x402ResourceServer(facilitatorClient)
      .register("eip155:84532", new ExactEvmScheme())
      .register("solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1", new ExactSvmScheme()),
  ),
);

app.get("/weather", (req, res) => {
  res.send({ report: { weather: "sunny", temperature: 70 } });
});

app.listen(4021, () => console.log("Server listening at http://localhost:4021"));
```

## 客户端示例（TypeScript 使用 Hono）

安装依赖项：
```bash
npm install hono @hono/node-server @x402/hono @x402/core @x402/evm @x402/svm dotenv
```

代码：
```typescript
import { config } from "dotenv";
import { paymentMiddleware, x402ResourceServer } from "@x402/hono";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { ExactSvmScheme } from "@x402/svm/exact/server";
import { HTTPFacilitatorClient } from "@x402/core/server";
import { Hono } from "hono";
import { serve } from "@hono/node-server";

config();

const evmAddress = process.env.EVM_ADDRESS as `0x${string}`;
const svmAddress = process.env.SVM_ADDRESS;
const facilitatorUrl = process.env.FACILITATOR_URL || "https://x402.org/facilitator";

const facilitatorClient = new HTTPFacilitatorClient({ url: facilitatorUrl });
const app = new Hono();

app.use(
  paymentMiddleware(
    {
      "GET /weather": {
        accepts: [
          { scheme: "exact", price: "$0.001", network: "eip155:84532", payTo: evmAddress },
          { scheme: "exact", price: "$0.001", network: "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1", payTo: svmAddress },
        ],
        description: "Weather data",
        mimeType: "application/json",
      },
    },
    new x402ResourceServer(facilitatorClient)
      .register("eip155:84532", new ExactEvmScheme())
      .register("solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1", new ExactSvmScheme()),
  ),
);

app.get("/weather", c => c.json({ report: { weather: "sunny", temperature: 70 } }));

serve({ fetch: app.fetch, port: 4021 });
console.log("Server listening at http://localhost:4021");
```

## 客户端示例（Python 使用 FastAPI）

安装依赖项：
```bash
pip install "x402[fastapi,evm,svm]" python-dotenv uvicorn
```

代码：
```python
import os
from dotenv import load_dotenv
from fastapi import FastAPI

from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
from x402.http.middleware.fastapi import PaymentMiddlewareASGI
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.mechanisms.svm.exact import ExactSvmServerScheme
from x402.schemas import Network
from x402.server import x402ResourceServer

load_dotenv()

EVM_ADDRESS = os.getenv("EVM_ADDRESS")
SVM_ADDRESS = os.getenv("SVM_ADDRESS")
EVM_NETWORK: Network = "eip155:84532"
SVM_NETWORK: Network = "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1"
FACILITATOR_URL = os.getenv("FACILITATOR_URL", "https://x402.org/facilitator")

app = FastAPI()

facilitator = HTTPFacilitatorClient(FacilitatorConfig(url=FACILITATOR_URL))
server = x402ResourceServer(facilitator)
server.register(EVM_NETWORK, ExactEvmServerScheme())
server.register(SVM_NETWORK, ExactSvmServerScheme())

routes = {
    "GET /weather": RouteConfig(
        accepts=[
            PaymentOption(scheme="exact", pay_to=EVM_ADDRESS, price="$0.01", network=EVM_NETWORK),
            PaymentOption(scheme="exact", pay_to=SVM_ADDRESS, price="$0.01", network=SVM_NETWORK),
        ],
        mime_type="application/json",
        description="Weather report",
    ),
}

app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=server)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/weather")
async def get_weather():
    return {"report": {"weather": "sunny", "temperature": 70}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4021)
```

## 客户端示例（Python 使用 Flask）

安装依赖项：
```bash
pip install "x402[flask,evm,svm]" python-dotenv
```

代码：
```python
import os
from dotenv import load_dotenv
from flask import Flask, jsonify

from x402.http import FacilitatorConfig, HTTPFacilitatorClientSync, PaymentOption
from x402.http.middleware.flask import payment_middleware
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.mechanisms.svm.exact import ExactSvmServerScheme
from x402.schemas import Network
from x402.server import x402ResourceServerSync

load_dotenv()

EVM_ADDRESS = os.getenv("EVM_ADDRESS")
SVM_ADDRESS = os.getenv("SVM_ADDRESS")
EVM_NETWORK: Network = "eip155:84532"
SVM_NETWORK: Network = "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1"
FACILITATOR_URL = os.getenv("FACILITATOR_URL", "https://x402.org/facilitator")

app = Flask(__name__)

facilitator = HTTPFacilitatorClientSync(FacilitatorConfig(url=FACILITATOR_URL))
server = x402ResourceServerSync(facilitator)
server.register(EVM_NETWORK, ExactEvmServerScheme())
server.register(SVM_NETWORK, ExactSvmServerScheme())

routes = {
    "GET /weather": RouteConfig(
        accepts=[
            PaymentOption(scheme="exact", pay_to=EVM_ADDRESS, price="$0.01", network=EVM_NETWORK),
            PaymentOption(scheme="exact", pay_to=SVM_ADDRESS, price="$0.01", network=SVM_NETWORK),
        ],
        mime_type="application/json",
        description="Weather report",
    ),
}

payment_middleware(app, routes=routes, server=server)

@app.route("/health")
def health_check():
    return jsonify({"status": "ok"})

@app.route("/weather")
def get_weather():
    return jsonify({"report": {"weather": "sunny", "temperature": 70}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4021)
```

## 客户端示例（Python 使用 Gin）

安装依赖项：
```bash
go get github.com/coinbase/x402/go
go get github.com/gin-gonic/gin
go get github.com/joho/godotenv
```

代码：
```go
package main

import (
	"net/http"
	"os"
	"time"

	x402 "github.com/coinbase/x402/go"
	x402http "github.com/coinbase/x402/go/http"
	ginmw "github.com/coinbase/x402/go/http/gin"
	evm "github.com/coinbase/x402/go/mechanisms/evm/exact/server"
	svm "github.com/coinbase/x402/go/mechanisms/svm/exact/server"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load()

	evmAddress := os.Getenv("EVM_PAYEE_ADDRESS")
	svmAddress := os.Getenv("SVM_PAYEE_ADDRESS")
	facilitatorURL := os.Getenv("FACILITATOR_URL")

	r := gin.Default()

	facilitatorClient := x402http.NewHTTPFacilitatorClient(&x402http.FacilitatorConfig{
		URL: facilitatorURL,
	})

	routes := x402http.RoutesConfig{
		"GET /weather": {
			Accepts: x402http.PaymentOptions{
				{Scheme: "exact", Price: "$0.001", Network: "eip155:84532", PayTo: evmAddress},
				{Scheme: "exact", Price: "$0.001", Network: "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1", PayTo: svmAddress},
			},
			Description: "Get weather data",
			MimeType:    "application/json",
		},
	}

	r.Use(ginmw.X402Payment(ginmw.Config{
		Routes:      routes,
		Facilitator: facilitatorClient,
		Schemes: []ginmw.SchemeConfig{
			{Network: "eip155:84532", Server: evm.NewExactEvmScheme()},
			{Network: "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1", Server: svm.NewExactSvmScheme()},
		},
		Timeout: 30 * time.Second,
	}))

	r.GET("/weather", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"weather":     "sunny",
			"temperature": 70,
			"timestamp":   time.Now().Format(time.RFC3339),
		})
	})

	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	r.Run(":4021")
}
```

---

# 支付墙 UI（服务器中间件）

`@x402/paywall` 包提供了一个预构建的支付墙 UI，当用户收到 `402 Payment Required` 响应时会显示该界面。该 UI 负责处理钱包连接（如 MetaMask、Coinbase Wallet、Phantom 等）、检查 USDC 余额以及提交支付信息。

**注意：** 该包仅适用于 **服务器端**。当服务器返回 `402` 响应时，它会生成一个完整的、自包含的 HTML 页面（约 1.9MB），其中包含 React、wagmi 和钱包适配器。它不是一个独立的 React 组件库，**不能** 直接导入到现有的 React 应用程序中。

**需要 React 组件吗？**
- **对于 Solana React 应用程序：** 使用 `@payai/x402-solana-react`——提供可定制的主题的支付墙组件。
- **对于自定义的 EVM/Solana React 应用程序：** 可以使用 `wagmi` + `viem`（EVM）或 `@solana/wallet-adapter-react`（Solana）进行开发。
- **多链 SDK：** 可以使用 `@dexterai/x402`、`x402-solana`。

有关详细信息，请参阅 [自定义 React 前端集成](#custom-react-frontend-integration) 部分。

---

## 安装（服务器端）

```bash
npm install @x402/paywall
```

**按导入方式划分的包大小：**
| 导入方式 | 大小 | 支持的网络 |
|--------|------|----------|
| `@x402/paywall` | 3.5MB | EVM + Solana |
| `@x402/paywall/evm` | 3.4MB | 仅支持 EVM |
| `@x402/paywall/svm` | 1.0MB | 仅支持 Solana |

## 使用方法（服务器中间件）

### 仅支持 EVM

```typescript
import { createPaywall } from "@x402/paywall";
import { evmPaywall } from "@x402/paywall/evm";

const paywall = createPaywall()
  .withNetwork(evmPaywall)
  .withConfig({
    appName: "My App",
    appLogo: "/logo.png",
    testnet: true,
  })
  .build();
```

### 仅支持 Solana

```typescript
import { createPaywall } from "@x402/paywall";
import { svmPaywall } from "@x402/paywall/svm";

const paywall = createPaywall()
  .withNetwork(svmPaywall)
  .withConfig({
    appName: "My Solana App",
    testnet: true,
  })
  .build();
```

### 支持多网络

```typescript
import { createPaywall } from "@x402/paywall";
import { evmPaywall } from "@x402/paywall/evm";
import { svmPaywall } from "@x402/paywall/svm";

const paywall = createPaywall()
  .withNetwork(evmPaywall)  // First-match priority
  .withNetwork(svmPaywall)  // Fallback option
  .withConfig({
    appName: "Multi-chain App",
    testnet: true,
  })
  .build();
```

## 配置选项

```typescript
interface PaywallConfig {
  appName?: string;    // App name shown in wallet connection
  appLogo?: string;    // App logo URL
  currentUrl?: string; // URL of protected resource
  testnet?: boolean;   // Use testnet (default: true)
}
```

## 与 Express 的集成

```typescript
import express from "express";
import { paymentMiddleware, x402ResourceServer } from "@x402/express";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { HTTPFacilitatorClient } from "@x402/core/server";
import { createPaywall } from "@x402/paywall";
import { evmPaywall } from "@x402/paywall/evm";

const app = express();

const facilitatorClient = new HTTPFacilitatorClient({ url: "https://x402.org/facilitator" });

const paywall = createPaywall()
  .withNetwork(evmPaywall)
  .withConfig({ appName: "My API", testnet: true })
  .build();

app.use(
  paymentMiddleware(
    {
      "GET /premium": {
        accepts: [{ scheme: "exact", price: "$0.01", network: "eip155:84532", payTo: "0x..." }],
        description: "Premium content",
        mimeType: "application/json",
      },
    },
    new x402ResourceServer(facilitatorClient).register("eip155:84532", new ExactEvmScheme()),
    undefined,  // paywallConfig (using custom paywall instead)
    paywall,    // custom paywall provider
  ),
);

app.get("/premium", (req, res) => res.json({ content: "Premium data" }));
app.listen(4021);
```

## 自动检测（简单用法）

如果您传递的是 `paywallConfig` 对象而非自定义支付墙配置，中间件会自动使用已安装的 `@x402/paywall`：

```typescript
app.use(
  paymentMiddleware(
    routes,
    server,
    { appName: "My App", testnet: true },  // paywallConfig - auto-detects @x402/paywall
  ),
);
```

## 首选支付方式的确定机制

当服务器返回多个支付选项时，支付墙会自动选择已注册处理程序的第一个选项：

```typescript
// Server returns:
{ "accepts": [
  { "network": "solana:5eykt...", ... },  // First option
  { "network": "eip155:8453", ... }       // Second option
]}

// If both handlers registered, Solana is selected (first in accepts)
const paywall = createPaywall()
  .withNetwork(evmPaywall)
  .withNetwork(svmPaywall)
  .build();
```

---

## 定价配置

### 简单的 USD 定价

```typescript
{ scheme: "exact", price: "$0.001", network: "eip155:84532", payTo: evmAddress }
```

### 自定义代币金额（ERC-20）

```typescript
{
  scheme: "exact",
  price: {
    amount: "10000",  // atomic units ($0.01 USDC = 10000 because USDC has 6 decimals)
    asset: "0x036CbD53842c5426634e7929541eC2318f3dCF7e",  // USDC on Base Sepolia
    extra: { name: "USDC", version: "2" }  // EIP-712 params
  },
  network: "eip155:84532",
  payTo: evmAddress
}
```

---

## 测试

测试时，请使用：
- **网络：** `eip155:84532`（Base Sepolia）或 `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1`（Solana 开发网）
- **第三方机构：** `https://x402.org/facilitator`（仅支持测试网）
- **资金获取：** 从 Base Sepolia 测试网获取 USDC。

生产环境请切换到主网并使用生产环境的第三方机构。