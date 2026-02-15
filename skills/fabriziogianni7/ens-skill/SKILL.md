---
name: ens
description: 将 ENS 名称（.eth）解析为以太坊地址，反之亦然。当用户提供一个 .eth 名称（例如 “send to vitalik.eth”）时，或者在显示地址、查询 ENS 详情、帮助用户注册、续费或管理 .eth 名称时，都需要使用此功能。
homepage: https://docs.ens.domains/
metadata:
  openclaw:
    emoji: "🏷️"
    requires: { env: [] }
---

# ENS（以太坊名称服务）——技能

## 该技能的功能

该技能使Gundwane能够：
1. **将ENS名称解析为以太坊地址**（正向解析）
2. **将地址解析为ENS名称**（反向解析）
3. **查询ENS资料**（头像、社交信息、文本记录）
4. **帮助用户在以太坊主网上注册、续费和管理`.eth`名称

## 使用场景

- 当用户提到`.eth`名称时：例如“发送到vitalik.eth”、“查找nick.eth”、“谁是luc.eth”
- 向用户显示钱包地址时——在地址旁边显示ENS的名称
- 当用户询问“我的ENS名称是什么？”、“我有ENS名称吗？”、“设置我的ENS名称”
- 当用户想要注册新的`.eth`名称、续费现有名称或更新记录时
- 当用户向`.eth`地址发送或接收交易时

## ENS名称检测

用户输入中任何以`.eth`结尾的标记都可能是ENS名称。例如：
- “向vitalik.eth发送0.1 ETH” → 解析为`vitalik.eth`
- “nick.eth的地址是什么？” → 解析为`nick.eth`
- “注册myname.eth” → 检查`myname`的可用性

**使用前务必进行解析。**切勿直接将`.eth`名称传递给LI.FI或交易工具——先将其解析为`0x`地址。

## 解析方法

### 正向解析（名称 → 地址）

使用`curl`将ENS名称解析为其对应的以太坊地址。优先尝试以下方法：

#### 方法1：ENS Subgraph（The Graph）

适用于获取详细信息（有效期、注册者、解析器）。需要`GRAPH_API_KEY`环境变量。

**代码块：**
```plaintext
response: data.domains[0].resolvedAddress.id` 是 `0x` 地址。
```

#### 方法2：web3.bio API（免费，无需密钥）

适用于快速解析并一次性获取资料。

**代码块：**
```plaintext
返回包含`address`、`identity`、`displayName`、`avatar`、`description`和链接的社交资料的JSON。使用`address`字段获取解析后的`0x`地址。
```

#### 方法3：使用Node.js和viem（备用方案）

如果API不可用且Node.js可用（viem在项目依赖中）：

**代码块：**
```plaintext
将`REPLACE_NAME`替换为实际的ENS名称。
```

**优先级：** 方法1 → 方法2 → 方法3。选择可用且最快的方法。

### 反向解析（地址 → 名称）

给定一个`0x`地址，查找其对应的ENS名称：

#### 通过ENS Subgraph

**代码块：**
```plaintext
注意：查询中的地址必须为小写。
```

#### 通过web3.bio

**代码块：**
```plaintext
如果设置了主名称，则返回ENS名称和资料。
```

#### 通过viem（备用方案）

**代码块：**
```plaintext
```

### 查看资料

获取ENS资料详情：头像、描述、社交链接、文本记录。

**代码块：**
```plaintext
```

**常见的文本记录键（供参考）：**
- `com.twitter` — Twitter/X账号
- `com.github` — GitHub用户名
- `url` — 网站地址
- `email` — 电子邮件地址
- `avatar` — 头像URL或NFT引用
- `description` — 个人简介/描述
- `com.discord` — Discord账号

### ENS头像URL

直接获取头像图片：

**代码块：**
```plaintext
```
示例：`https://metadata.ens.domains/mainnet/avatar/nick.eth`
```

在消息中显示用户ENS头像时使用此URL。

## 显示规则

### 显示地址时
- 通过`defi_get_wallet`获取用户钱包信息后，可选地检查其ENS名称。
- 如果用户有主ENS名称，显示该名称：`fabri.eth (0xabc...def)`
- 在投资组合视图中，优先显示ENS名称。
- 不要在每条消息中都进行解析——为会话缓存结果。

### 进行交易解析时
- **在执行交易前务必确认解析结果：**
  **代码块：**
  **切勿盲目信任解析结果——ENS记录可能会更改。始终显示`0x`地址。**
```

### 在交易摘要中
- 使用两种格式：`0.1 ETH → vitalik.eth (0xd8d...6045) on Base`

## 注册

### `.eth`名称注册

注册仅在以太坊主网上进行。需要支付ETH作为名称费用和Gas费用。如果用户的ETH位于L2链上，需提示他们先进行桥接。

**费用标准：**
- 5个以上字符：每年5 ETH
- 4个字符：每年160 ETH
- 3个字符：每年640 ETH

**相关合约（主网）：**
| 合约 | 地址 |
|----------|---------|
| ENS Registry | `0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e` |
| ETH Registrar Controller | `0x253553366Da8546fC250F225fe3d25d0C782303b` |
| Public Resolver | `0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63` |
| Reverse Registrar | `0xa58E81fe9b61B5c3fE2AFD33CF304c454AbFc7Cb` |
| Name Wrapper | `0xD4416b13d2b3a9aBae7AcD5D6C2BbDBE25686401` |
| Universal Resolver | `0xce01f8eee7E479C928F8919abD53E553a36CeF67` |

### 检查可用性

通过ENS Subgraph检查：

**代码块：**
```plaintext
```
如果没有结果或`expiryDate`在过去（+90天宽限期内），则名称可用。
```

或者直接链接让用户自行查看：`https://ens.app/myname.eth`

### 注册流程

注册分为两步：提交和确认：

1. **检查可用性**（使用上述Subgraph查询）。
2. **查看费用**：5个以上字符的名称每年费用约为5 ETH。实际费用取决于当前ETH价格。
3. **展示信息**：
   **代码块：**
4. **步骤1 — 提交**：通过`defi_send_transaction`调用`ETH Registrar Controller`的`commit(bytes32)`（chainId: 1）。提交哈希值需根据名称、所有者地址、期限和随机密钥计算得出。
5. **等待60秒**（告知用户：“提交已完成。注册将在约1分钟后完成。”）
6. **步骤2 — 注册**：通过`defi_send_transaction`调用`register(name, owner, duration, secret, resolver, data, reverseRecord, fuses)`，并将名称费用作为`value`参数传递。
7. **确认**：“myname.eth已注册！有效期为1年（截止日期2027年2月）。[查看交易详情](...)”
8. **存储在策略中**并建议设置主名称。

**更简单的注册方式：**直接引导用户使用ENS Manager App进行注册：`https://ens.app/myname.eth`——该应用提供友好的用户界面。建议首次注册时使用此方式。

## 续费

比注册简单——只需一次交易，无需提交步骤。

当用户请求“续费myname.eth”时：

1. 通过Subgraph或策略查询当前有效期。
2. 获取续费费用（与注册费用相同）。
3. 展示信息：
   **代码块：**
4. 经用户确认后，通过`defi_send_transaction`调用`ETH Registrar Controller`的`renew(string name, uint256 duration)`（chainId: 1），并将续费费用作为`value`参数传递。期限以秒为单位（1年=31536000秒）。
5. 在策略中更新有效期。

**宽限期：**名称在过期后有90天的宽限期。仅原所有者可以在此期间续费。宽限期过后，名称将进入公开拍卖，价格会逐渐降低。

## 设置记录

### 设置主名称（反向记录）

当用户请求“设置我的ENS主名称”或“将myname.eth设为主名称”时：

- 通过`defi_send_transaction`在主网上调用`Reverse Registrar`（`0xa58E81fe9b61B5c3fE2AFD33CF304c454AbFc7Cb`）的`setName(string name)`方法。
- 这会使用户的地址在反向查询中解析为`myname.eth`。
- 用户必须拥有该名称，并且该名称必须指向他们的地址。

### 设置文本记录

通过Public Resolver（`0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63`）更新社交/文本记录：

- 函数：`setText(bytes32 node, string key, string value)`
- `node`是完整名称的哈希值。
- 常见的键包括：`com.twitter`、`com.github`、`url`、`email`、`avatar`、`description`

对于复杂的记录更新，建议使用ENS Manager App：`https://ens.app/myname.eth`

## 到期监控

将注册的ENS名称存储在用户的策略中以进行定期检查：

**代码块：**
```plaintext
```
在定期检查期间，从每个用户的策略中获取`ensNames`：
- **到期前30天**：`您的名称fabri.eth将在30天后过期。需要续费吗？`
- **到期前7天**：`fabri.eth将在7天后过期。立即续费以保持有效。`
- **已过期（在宽限期内）**：`fabri.eth已过期！您有90天时间进行续费。`
```

## 数据存储——策略JSON

ENS数据存储在用户的策略JSON文件中（通过`defi_set_strategy`）：

**代码块：**
```plaintext
```
通过`defi_get_strategy`读取数据，通过`defi_set_strategy`写入数据。数据按用户单独存储。
```

**其他注意事项：**
- **交易前务必进行解析。**切勿将`.eth`名称直接传递给LI.FI或交易工具。先将其解析为`0x`地址。
- **确认解析结果。**在发送资金前始终向用户显示解析后的`0x`地址。ENS记录可能会更改。
- **仅限主网进行注册/续费**。`.eth`名称存储在以太坊主网上。如果用户需要，需提示他们桥接ETH以支付Gas费用。
- **禁止查询功能**。ENS解析和资料查询属于只读操作，应默默执行。
- **会话内缓存结果**。如果在对话中解析了名称，可重用结果，无需每次都重新解析。
- **优雅处理错误**。如果解析失败（名称不存在或API不可用），请向用户明确说明情况。切勿猜测地址。
- **定期检查到期时间**。在定期检查中检查用户的策略中的`ensNames`。
- **用户数据隔离**。ENS数据存储在用户的策略JSON文件中，禁止跨用户访问。
- **建议使用ENS**。如果用户没有ENS名称但经常使用原始地址，建议提醒他们使用ENS。不要强行推荐。
- **注意ENSv2的更新**。ENS正在迁移到新的L2基础系统（ENSv2）。当前的主网注册方式仍然有效，但未来可能会有变化。