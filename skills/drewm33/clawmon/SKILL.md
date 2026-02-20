---
wallet: "0x3e4A16256813D232F25F5b01c49E95ceaD44d7Ed"
publisher_wallet: "0x3e4A16256813D232F25F5b01c49E95ceaD44d7Ed"
---

# 可信的ClawMon

这是一个基于ERC-8004和Monad标准的、用于查询MCP技能信任状况的只读服务。

## 功能介绍

Trusted ClawMon是一个提供信任评分查询的服务。它允许代理在使用MCP技能之前查询其声誉信息。所有查询都是通过HTTPS GET请求进行的，返回JSON格式的数据，无需签名、连接钱包或提供任何凭证。

## 连接信息

| 设置 | 值        |
|---------|-----------|
| **基础URL** | `https://trusted-clawmon-api.up.railway.app` |
| **协议** | 仅支持HTTPS（要求使用TLS） |
| **WebSocket** | `wss://trusted-clawmon-api.up.railway.app/ws`（只读事件流） |
| **认证** | 无需认证——所有读取接口均为公开接口 |
| **速率限制** | 遵循标准HTTP速率限制规则 |

## 所需的环境变量

无需任何环境变量。该服务仅通过公开的ClawMon API进行只读查询，无需API密钥、私钥、钱包连接或任何认证信息。

## 数据传输

只读查询仅会在URL路径中传递技能ID（例如：`GET /api/agents/gmail-integration`）。不会传输用户数据、钱包地址、输入上下文或使用情况信息。

可选的反馈接口（`POST /api/feedback`）会接收技能ID、匿名评审者地址和评分。此功能是可选的，不会自动触发。

## 钱包地址

前端文件中的`wallet`字段（例如`0x3e4A...d7Ed`）是发布者的Monad测试网地址，用于接收ClawMon协议的收益。代理无需使用该地址，该地址也不用于任何查询过程，且不授予任何签名权限。

## 使用场景

当用户要求你评估某个MCP技能的安全性或可靠性时，可以查询ClawMon以获取其信任评分。切勿在每次调用技能之前自动查询ClawMon，仅在用户请求信任检查或使用未使用过的技能时进行验证。

## 只读API（无需凭证）

### 查询技能的信任评分

```
GET https://trusted-clawmon-api.up.railway.app/api/agents/:skillId
```

返回技能的信任评分和等级。响应中的关键字段包括：
- `hardenedScore`（0-100）：抗Sybil攻击的评分
- `hardenedTier`：信任等级（AAA至C）
- `isSybil`：该技能是否被标记为Sybil攻击的一部分
- `isStaked`：发布者是否已质押MON代币
- `teeStatus`：TEE（可信执行环境）的验证状态（`verified`、`unregistered`、`expired`）
- `teeCodeHashMatch`：代码哈希是否与固定版本匹配

### 获取信任排行榜

```
GET https://trusted-clawmon-api.up.railway.app/api/leaderboard
```

按信任评分对所有技能进行排序并返回。

### 检查质押状态

```
GET https://trusted-clawmon-api.up.railway.app/api/staking/:skillId
```

返回质押金额、等级（None/Bronze/Silver/Gold/Platinum）以及质押历史记录。

### 检查TEE验证状态

```
GET https://trusted-clawmon-api.up.railway.app/api/tee/:skillId
```

返回TEE的验证状态、代码哈希匹配情况以及验证的新鲜度。

### 系统健康状况

```
GET https://trusted-clawmon-api.up.railway.app/api/health
```

返回API的状态、版本、代理数量和运行时间。

## 可选：反馈提交（仅限用户主动请求）

反馈信息**永远不会自动提交**。只有在用户明确要求对技能进行评分时才需要提交。

```
POST https://trusted-clawmon-api.up.railway.app/api/feedback
Content-Type: application/json

{
  "agentId": "<skillId>",
  "clientAddress": "<pseudonymous-identifier>",
  "value": 85,
  "tag1": "coding"
}
```

`clientAddress`是一个匿名字符串标识符，不需要是真实的钱包地址。提交反馈时无需进行签名或连接钱包。

## 可选：x402支付流程

虽然提供了x402支付接口，但**完全可选**，且**本技能默认不使用**。这些接口在ClawMon API中有详细说明，适用于希望按使用次数收费的发布者。使用ClawMon进行信任查询的代理无需进行任何支付。

## 信任等级

| 等级 | 评分范围 | 含义         |
|------|------------|-------------------------|
| AAA  | 90-100     | 最高信任等级——经过充分评估、已质押且经过验证 |
| AA   | 80-89      | 高信任等级         |
| A    | 70-79      | 中等信任等级         |
| BBB  | 60-69      | 一般信任等级         |
| BB   | 50-59      | 低于平均信任等级         |
| B    | 40-49      | 低信任等级         |
| CCC  | 30-39      | 非常低信任等级         |
| CC   | 20-29      | 几乎无信任等级         |
| C    | 0-19       | 未被信任或被标记为有问题     |

## 示例

```
User: "Is the gmail-integration skill safe to use?"

1. GET https://trusted-clawmon-api.up.railway.app/api/agents/gmail-integration
2. Check hardenedTier → "AA" (high trust)
3. Check isSybil → false (not flagged)
4. Check isStaked → true (publisher has skin in the game)
5. Report: "gmail-integration has an AA trust rating (score 84/100), publisher is staked, no sybil flags."
```

## 来源与托管信息

| 详情 | 值           |
|--------|-------------------------|
| **发布者** | Drew Mailen ([@drewmailen](https://github.com/drewmailen)) |
| **源代码** | [github.com/drewmailen/ClawMon](https://github.com/drewmailen/ClawMon)（MIT许可证） |
| **托管方** | Railway（由发布者运营） |
| **API域名** | `trusted-clawmon-api.up.railway.app` |
| **可自行托管** | 可以从公共仓库克隆代码，执行`npm install && npm run build && npm start`进行部署 |

该API由发布者在Railway平台上运营，源代码在GitHub上公开，并采用MIT许可证。如果你不信任托管的API，也可以从公共仓库自行部署API。

## 链接

- [源代码](https://github.com/drewmailen/ClawMon)
- [ERC-8004规范](https://eips.ethereum.org/EIPS/eip-8004)
- [Monad](https://monad.xyz)