---
name: sports-betting
description: "您可以通过 Pinwin 和 Azuro 在链上进行去中心化的体育投注：实时赔率、高流动性、无需托管服务。从数据源获取赛前和比赛中的赛事信息，选择投注选项，然后完成签名并提交投注。无论用户是想通过 Pinwin 进行体育投注、浏览赛事信息、下注，还是查看或领取奖金，都可以使用这些功能。"
compatibility: "Requires Node, viem and @azuro-org/dictionaries (for human-readable market/selection names). Required env: BETTOR_PRIVATE_KEY (wallet private key; high-sensitivity). Optional env: POLYGON_RPC_URL (Polygon RPC); if unset, use default RPC(s) in references/polygon.md."
homepage: "https://github.com/skinnynoizze/pinwin-agent"
disable-model-invocation: true
metadata: {"openclaw":{"requires":{"bins":["node"],"env":["BETTOR_PRIVATE_KEY"]},"primaryEnv":"BETTOR_PRIVATE_KEY"}}
---
# 体育博彩（Pinwin）

您可以通过 [Pinwin](https://pinwin.xyz) 和 Azuro 在 **Polygon** 上进行 **去中心化** 的体育博彩，并实现链上执行。代理会从数据源获取 **赛前** 和 **实时** 比赛信息，您选择投注选项后，系统会调用 Pinwin 进行投注操作（可选择是否批准 USDT），最后提交投注请求。

**使用说明：**  
此功能仅支持 **主动调用**——除非您明确请求（例如：“使用 Pinwin 下注”），否则助手不会自动使用该功能，以避免意外投注。

---

## 如何使用（OpenClaw）  
- **调用方式：** 使用 `/sports_betting` 命令（或 `/skill sports-betting`），并根据需要添加请求参数，例如：`/sports_betting place 5 USDT on the first Premier League game` 或 `/sports_betting show my bets`。  
- **灵活性：** 如果未指定参数，助手会询问您的偏好设置：获取多少场比赛（`first`）、排序方式（`turnover` 或 `startsAt`）、运动项目/国家/联赛筛选条件，以及您希望选择的投注选项。除非您明确要求建议，否则助手不会自动推荐或选择投注选项（有意义的建议可能需要外部数据，例如新闻或统计数据，这可能需要单独的技能支持）。

---

## 适用场景  
- 当用户希望 **下注**（赛前或实时比赛）时：  
  1. 从数据源获取比赛信息；  
  2. 选择投注选项；  
  3. 调用 Pinwin 的 `/agent/bet` 功能；  
  4. 如有需要，批准 USDT；  
  5. 签署 EIP-712 签名；  
  6. 将签名后的数据发送到返回的 `apiUrl`。

---

## 先决条件  
### 必需的环境变量  
- **BETTOR_PRIVATE_KEY**：用于签署投注和领取奖金的交易私钥（十六进制格式）。该密钥具有高度敏感性，请勿记录或泄露。仅用于下注和领取奖金操作，建议使用专门用于博彩的钱包，并确保钱包中有足够的资金，切勿使用您的主钱包。  

### 可选配置  
- **POLYGON_RPC_URL**：Polygon 的 RPC 端点。如果未设置，代理将使用 [references/polygon.md](references/polygon.md) 中指定的默认 RPC 端点（例如 Pocket Network 或 PublicNode）。  

### 其他配置  
- **@azuro-org/dictionaries**：此包是必需的，因为它可以将比赛结果 ID 和赔率映射为人类可读的市场名称和投注选项名称（例如 “Total Goals” 或 “Over (2.5”)。详情请参阅 [references/dictionaries.md](references/dictionaries.md)。  
- **相关地址：** 中继器地址、博彩代币地址、原生气体代币（POL）地址、数据源 URL 和投注子图 URL 都在 [references/polygon.md](references/polygon.md) 中有详细说明。  
- **资金检查：** 代理会使用 viem 检查用户的 **POL**（气体代币）和 **USDT**（投注金额 + 中继费）余额；如果余额不足，系统会通知用户并拒绝下注。详情请参阅 [references/viem.md](references/viem.md)。  

---

## 下注流程  
0. **可选步骤：** 检查余额：确保用户的 USDT 余额大于或等于投注金额加上所需的气体代币费用（`POL`）。具体计算公式为：`USDT = 投注金额 + payload.relayerFeeAmount`。详情请参阅 [references/viem.md](references/viem.md)。  
1. **获取比赛信息：** 根据 [references/subgraph.md](references/subgraph.md) 的说明，通过 POST 请求从数据源获取比赛信息（赛前或实时比赛）。获取比赛信息时需指定条件（`conditionId` 和结果 ID `outcomeId`），并使用 [references/dictionaries.md](references/dictionaries.md) 中提供的函数 `getSelectionName()` 将结果名称转换为人类可读的形式。  
2. **选择投注选项：** 从符合条件的比赛中选择一个或多个选项（`conditionId` 和 `outcomeId`）。单选时的赔率计算公式为 `Math.round(parseFloat(currentOdds) * 1e12`；组合投注的赔率计算公式为各选项赔率的乘积（保留 12 位小数）。  
3. **调用 Pinwin：** 使用 JSON 格式的数据发送请求到 `https://api.pinwin.xyz/agent/bet`（详情请参阅 [references/api.md]）。响应内容为 `{ "encoded": "<base64>" }`，解码后得到 `payload`。  
4. **向用户说明情况：** 显示 `signableClientBetData.bets` 中的投注金额、选项信息、中继费金额、API 地址以及客户端数据（使用 [references/dictionaries.md] 中提供的函数转换为人类可读的名称），并简要说明投注详情。  
5. **批准操作（如需）：** 检查用户在 Polygon 上的投注代币是否具有足够的 `allowance`（允许的投注金额）。如果不足，需要用户批准 `approve(relayer, bet amount + relayer fee + 0.2 USDT)`。为安全起见，每次批准的交易金额会有一定的缓冲区；下次下注时可能需要再次获取批准。具体步骤请参阅 [references/polygon.md](references/polygon.md) 和 [references/viem.md》。  
6. **验证信息：** 确认 `payload` 中的投注金额和选项信息与用户的实际意图一致（`clientData.core` 必须与 [references/polygon.md](references/polygon.md) 中定义的 `claimContract` 匹配）。如果有任何不符，切勿批准并通知用户。  
7. **签署并提交：** 使用 viem 的 `signTypedData` 函数，传入 `payload.domain`、`payload.types`、`primaryType`（详情请参阅 [references/api.md]）以及 `message: payload.signableClientBetData`。然后将请求发送到 `payload.apiUrl`，并附带 `environment`、`bettor`、`betOwner`、`clientBetData`（即 `payload.apiClientBetData`）和 `bettorSignature`。订单 ID 可从响应中获取（`response.id`）。如果订单尚未完成，请持续轮询（详情请参阅 [references/api.md]，使用 URL `GET {apiBase}/bet/orders/{orderId}`）。成功时响应中会包含 `txHash`；失败时响应状态为 `Rejected` 或 `Canceled`（此时请查看 `errorMessage`）。  

---

## 查看投注状态（领取奖金前）  
要了解投注是否已 **完成**、是否 **中奖** 或 **失败**，以及用户是否可以 **领取奖金**，请查询投注子图（与数据源不同）。详情请参阅 [references/bets-subgraph.md]：  
1. **查询投注信息：** 向投注子图发送 GraphQL 请求（URL 位于 [references/polygon.md]），使用 `where: { bettor: "<bettor address>"` 来筛选用户下的所有投注。若要仅获取可领取的投注，需在查询条件中添加 `isRedeemable: true`。至少需要查询的字段包括 `betId`、`status`、`result`、`isRedeemable`、`isRedeemed`、`amount` 和 `payout`。  
2. **结果解析：** `status` 可能为 `Accepted`（待处理）、`Resolved`（已完成）或 `Canceled`。当 `status` 为 `Resolved` 时，`result` 为 `Won` 或 `Lost`。如果 `isRedeemable` 为 `true` 且 `isRedeemed` 为 `false`，则表示用户可以领取奖金；此时需要收集这些投注的 `betId` 值以进行后续操作。  

---

## 领取奖金的流程  
仅适用于已完成的投注（或被取消的投注），且满足 `isRedeemable` 为 `true` 且 `isRedeemed` 为 `false` 的情况：  
1. **调用 Pinwin：** 使用 `betIds`（链上投注 ID 的数组）和 `chain: "polygon"` 发送请求到 `https://api.pinwin.xyz/agent/claim`。解码响应中的 `encoded` 数据。  
2. **向用户解释操作内容：** 说明用户正在领取的奖金金额（例如 X、Y 号投注的奖金），并说明交易将发送到 Polygon 上的 Azuro ClientCore 合同；此时不会发送任何实际的资金（ETH 或 POL）。  
3. **验证合同信息：** 确认 `payload.to` 是否与 [references/polygon.md](references/polygon.md) 中定义的领取奖金合同（`claimContract`）匹配。如果不匹配，切勿执行交易并报告错误。  
4. **发送交易：** 使用 viem 的 `sendTransaction` 函数发送交易，参数包括 `to: payload.to`、`data: payload.data`、`value: 0n` 和 `chainId: payload.chainId`。等待交易完成。详情请参阅 [references/viem.md]。  

---

## 示例（单次投注）  
在获取比赛信息并选择投注选项后：  
- 解码 `response.encoded`；  
- 使用 viem 的 `signTypedData` 函数签署 `payload.signableClientBetData`；  
- 将 `clientBetData` 和 `bettorSignature` 发送到 `payload.apiUrl`。  

## 示例（领取奖金）  
1. 从投注子图中获取 `betIds`（例如，使用 `isRedeemable: true` 进行查询）。  
2. 解码 `response.encoded`；  
3. 将结果显示给用户；  
4. 确认 `payload.to` 是否与 [references/polygon.md](references/polygon.md) 中定义的领取奖金合同（`claimContract`）匹配；  
5. 使用 viem 的 `sendTransaction` 函数发送领取奖金的交易；  
6. 等待交易完成。  

---

## 所需工具  
| 功能 | 工具 | 用途 |  
|------|------|---------|  
| 获取比赛信息 | 数据源子图（GraphQL） | 获取比赛信息、条件、结果和赔率 |  
| 查看投注状态 | 投注子图（GraphQL） | 获取用户的投注信息（状态、结果、是否可领取、投注 ID） |  
| 显示名称 | @azuro-org/dictionaries | 将结果 ID 映射为人类可读的名称 |  
| 下注/领取奖金 | Pinwin API | 获取编码后的数据和解码后的 API 地址 |  
| 连接管理 | viem + RPC | 获取余额（POL）、查看合同信息、发送交易（批准/领取奖金）、签署交易数据 |  

**所需安装的包：** `npm install viem @azuro-org/dictionaries`。配置和链上操作请参考 [references/viem.md](references/viem.md)；字典的使用方法请参阅 [references/dictionaries.md](references/dictionaries.md)。  

## 常见错误  
- **Pinwin**：检查响应中的 `error` 或 `message` 错误代码。  
- **数据源问题：** 查看响应中的 HTTP 状态码和 `data.errors`（GraphQL 可以返回 200 状态码并附带 `data.errors`）。  
- **链上问题：** 交易失败或资金不足——请报告交易哈希值。  

## 参考文件  
在需要完整的请求/响应格式、查询语句或地址时，请参考以下文件：  
- [references/api.md](references/api.md)：Pinwin 的 `/agent/bet` 和 `/agent/claim` 请求及响应格式。  
- [references/subgraph.md](references/subgraph.md)：数据源 URL、GraphQL 查询语句示例、过滤条件及响应格式。  
- [references/bets-subgraph.md](references/bets-subgraph.md)：投注子图 URL、查询用户投注信息及领取奖金所需的字段。  
- [references/dictionaries.md](references/dictionaries.md)：用于将结果 ID 映射为人类可读名称的词典。  
- [references/polygon.md](references/polygon.md)：Polygon 的数据源 URL、投注子图 URL、原生气体代币（POL）、中继器信息及投注代币（USDT）设置。  
- [references/viem.md](references/viem.md)：viem 的安装和配置方法、余额查询、交易发送等功能。