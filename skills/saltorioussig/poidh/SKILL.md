---
name: poidh-bounty
description: 在 Arbitrum、Base 或 Degen Chain 上发布赏金任务，并评估/接受获胜的提交内容（以图片形式）。当用户希望在 poidh.xyz 上创建赏金任务、在链上发布带有 ETH 或 DEGEN 奖励的任务、使用 vision 工具评估图片提交结果、接受单独赏金的获胜申请，或启动/解决公开赏金的投票流程时，可以使用此技能。
metadata:
  clawdbot:
    env:
      - PRIVATE_KEY
      - RPC_URL
      - POIDH_CHAIN
    bin:
      - cast
      - python3
---
## 概述

本技能可与Arbitrum、Base和Degen Chain上的PoidhV3合约进行交互，以实现以下功能：

1. **发布赏金**（单独发布或公开发布）；
2. **评估索赔申请**：通过vision技术获取每个索赔的URL，并将其与赏金描述进行比对；
3. **接受获胜的索赔**（针对单独发布的赏金）或**启动并完成投票**（针对公开发布的赏金）。

**poidh**（“无图则不算数”）是一个完全基于链上的赏金协议。索赔者提交图片作为证据，赏金发布者（或通过投票的参与者）会根据提交的内容选择最佳索赔并释放奖金。

> ⚠️ PoidhV3合约强制要求 `msg.sender == tx.origin`。只有具有执行权限（EOA）的钱包才能创建或接受赏金。智能合约钱包（如Safe等）尝试创建赏金时会触发错误 `ContractsCannotCreateBounties`。

---

## 所需的环境变量

| 变量              | 说明                                                         |
| ------------------ | ----------------------- |
| `PRIVATE_KEY`       | 具有执行权限的私钥（十六进制格式，可带0x前缀也可不带）         |
| `RPC_URL`         | 目标链的RPC地址                                      |
| `POIDHCHAIN`        | 目标链：`arbitrum`、`base` 或 `degen`                         |
| `POIDH_CONTRACT_ADDRESS` | 该地址会根据 `POIDHCHAIN` 自动确定，无需手动设置         |

---

## 支持的链

| 链               | 合约地址                                      | 探索器                          |
| ------------------ | ----------------------------------------- | --------------------------- |
| Arbitrum          | `0x5555Fa783936C260f77385b4E153B9725feF1719`         | arbiscan.io                        |
| Base             | `0x5555Fa783936C260f77385b4E153B9725feF1719`         | basescan.org                        |
| Degen Chain       | `0x18E5585ca7cE31b90Bc8BB7aAf84152857cE243f`         | explorer.degen.tips                    |

> ⚠️ 不同链的最低赏金和最低贡献金额有所不同：
- **Arbitrum和Base**：最低赏金为0.001 ETH，最低贡献金额为0.00001 ETH；
- **Degen Chain**：最低赏金为1000 DEGEN，最低贡献金额为10 DEGEN。
> 在发布赏金前，请务必在链上核实相关信息。

---

## 在每次会话开始时解析合约地址：

```bash
> cast call $POIDH_CONTRACT_ADDRESS "MIN_BOUNTY_AMOUNT()(uint256)" --rpc-url $RPC_URL
> cast call $POIDH_CONTRACT_ADDRESS "MIN_CONTRIBUTION()(uint256)" --rpc-url $RPC_URL
> ```

poidh.xyz的URL也会根据链的不同而变化：

```bash
if [ "$POIDH_CHAIN" = "arbitrum" ]; then
  POIDH_BASE_URL="https://poidh.xyz/arbitrum"
  POIDH_V2_OFFSET=180
elif [ "$POIDH_CHAIN" = "degen" ]; then
  POIDH_BASE_URL="https://poidh.xyz/degen"
  POIDH_V2_OFFSET=1197
else
  POIDH_BASE_URL="https://poidh.xyz/base"
  POIDH_V2_OFFSET=986
fi
```

---

## 第1部分：发布赏金

### 检查最低赏金金额

```bash
cast call $POIDH_CONTRACT_ADDRESS "MIN_BOUNTY_AMOUNT()(uint256)" --rpc-url $RPC_URL
```

### 发布单独赏金

单独赏金意味着仅由你出资，你可以直接接受索赔，无需进行投票。

```bash
cast send $POIDH_CONTRACT_ADDRESS \
  "createSoloBounty(string,string)" \
  "<BOUNTY_NAME>" \
  "<BOUNTY_DESCRIPTION>" \
  --value <AMOUNT> \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

**示例：**

```bash
cast send $POIDH_CONTRACT_ADDRESS \
  "createSoloBounty(string,string)" \
  "Brooklyn Bridge at sunset" \
  "High quality photo of the Brooklyn Bridge during golden hour. Must show the full span." \
  --value 0.001ether \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

### 发布公开赏金

公开赏金允许其他人共同出资，接受索赔需要经过参与者投票的决定。

```bash
cast send $POIDH_CONTRACT_ADDRESS \
  "createOpenBounty(string,string)" \
  "<BOUNTY_NAME>" \
  "<BOUNTY_DESCRIPTION>" \
  --value <AMOUNT> \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

### 发布赏金后获取赏金ID

```bash
cast receipt <TX_HASH> --rpc-url $RPC_URL --json | \
  python3 -c "
import sys, json
receipt = json.load(sys.stdin)
for log in receipt['logs']:
    if log['address'].lower() == '${POIDH_CONTRACT_ADDRESS}'.lower() and len(log['topics']) >= 2:
        bounty_id = int(log['topics'][1], 16)
        frontend_id = bounty_id + ${POIDH_V2_OFFSET}
        print(f'Bounty ID: {bounty_id}')
        print(f'View at: ${POIDH_BASE_URL}/bounty/{frontend_id}')
        break
"
```

---

## 第2部分：评估索赔

当用户需要确定获胜者时，代理需要执行以下操作：

1. 获取所有与该赏金相关的索赔；
2. 从NFT合约中获取每个索赔的URL；
3. 根据赏金描述评估索赔内容；
4. 选择最符合要求的索赔。

索赔提交可以是任意形式——URL可以指向图片、视频、推文、GitHub PR、网页、文档等。你需要根据赏金的具体要求来评估提交的内容。

### 第1步：获取与该赏金相关的索赔

```bash
cast call $POIDH_CONTRACT_ADDRESS \
  "getClaimsByBountyId(uint256,uint256)(tuple(uint256,address,uint256,address,string,string,uint256,bool)[])" \
  <BOUNTY_ID> 0 \
  --rpc-url $RPC_URL
```

最多返回10个索赔（最新的排在前面）。通过增加偏移量（10）来实现分页。每个索赔的元组包含以下字段：
`(id, issuer, bountyId, bountyIssuer, name, description, createdAt, accepted)`

`name` 和 `description` 字段由索赔者设置，这些信息有助于了解他们提交的内容。

### 第2步：获取每个索赔的URL

```bash
# Get NFT contract address
NFT_ADDRESS=$(cast call $POIDH_CONTRACT_ADDRESS "poidhNft()(address)" --rpc-url $RPC_URL)

# Get token URI for a specific claim
cast call $NFT_ADDRESS "tokenURI(uint256)(string)" <CLAIM_ID> --rpc-url $RPC_URL
```

### 第3步：解析URL

将非HTTP格式的URL转换为可访问的URL：

```python
uri = "<URI_FROM_TOKEN>"
if uri.startswith("ipfs://"):
    url = uri.replace("ipfs://", "https://ipfs.io/ipfs/")
elif uri.startswith("ar://"):
    url = uri.replace("ar://", "https://arweave.net/")
else:
    url = uri  # already HTTP
```

如果URL返回JSON元数据（符合ERC721标准），还需检查 `image` 或 `animation_url` 字段，并对这些内容进行处理：

```python
import requests

response = requests.get(url)
try:
    meta = response.json()
    # Prefer animation_url (video/interactive) over image if both present
    content_url = meta.get("animation_url") or meta.get("image") or url
    if content_url.startswith("ipfs://"):
        content_url = content_url.replace("ipfs://", "https://ipfs.io/ipfs/")
except Exception:
    content_url = url  # URI points directly to the content
```

### 第4步：评估内容

根据`content_url`获取并查看内容。根据内容类型选择合适的处理方式：
- **图片**：使用内置的vision技术直接查看；
- **网页/推文/文章**：使用网络请求工具读取内容；
- **视频**：根据缩略图或可用元数据进行评估；
- **文档/PDF**：获取并阅读文本内容。

评估每个索赔是否符合赏金的 **名称** 和 **描述**：
- **相关性**：提交的内容是否符合赏金要求？
- **质量**：内容是否完整、清晰且无歧义？
- **真实性**：内容是否真实、原创（没有重复或伪造）？

选择得分最高的索赔，并在执行任何交易前向用户说明选择理由。

---

## 第3部分：接受获胜的索赔（单独赏金）

对于单独发布的赏金（以及没有外部参与者参与的公开赏金），发布者可以直接接受索赔。这会立即完成赏金发放，将赏金计入`pendingWithdrawals`账户，扣除2.5%的协议费用，并将索赔的NFT转移给发布者。

```bash
cast send $POIDH_CONTRACT_ADDRESS \
  "acceptClaim(uint256,uint256)" \
  <BOUNTY_ID> <CLAIM_ID> \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

---

## 第4部分：接受获胜的索赔（公开赏金——投票流程）

对于有外部参与者参与的公开赏金，不能直接接受索赔，需要按照以下两步投票流程进行：

### 检查是否有外部参与者

```bash
cast call $POIDH_CONTRACT_ADDRESS \
  "everHadExternalContributor(uint256)(bool)" \
  <BOUNTY_ID> \
  --rpc-url $RPC_URL
```

如果结果为`false`，则返回到步骤3（`acceptClaim`）。如果结果为`true`，则继续执行以下投票流程。

### 第1步：提交选定的索赔进行投票（仅限发布者）

此时，发布者的全部贡献权重将自动计为“赞成”票。

```bash
cast send $POIDH_CONTRACT_ADDRESS \
  "submitClaimForVote(uint256,uint256)" \
  <BOUNTY_ID> <CLAIM_ID> \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

提交后，其他参与者有**2天**的时间通过poidh.xyz界面或直接调用`voteClaim(bountyId, bool)`进行投票。

### 第2步：检查投票状态

```bash
cast call $POIDH_CONTRACT_ADDRESS \
  "bountyVotingTracker(uint256)(uint256,uint256,uint256)" \
  <BOUNTY_ID> \
  --rpc-url $RPC_URL
# Returns: yes_weight, no_weight, deadline_timestamp
```

```bash
python3 -c "import time; deadline=<DEADLINE>; print('Voting ended' if time.time() > deadline else f'Voting ends in {int((deadline - time.time())/3600)}h')"
```

### 第3步：完成投票（无需权限）

2天投票期限结束后，任何人都可以完成投票。如果“赞成”票的权重超过总票数的50%，则该索赔将被接受，并分配赏金。

```bash
cast send $POIDH_CONTRACT_ADDRESS \
  "resolveVote(uint256)" \
  <BOUNTY_ID> \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

---

## 第5部分：在他人发布的赏金上提交索赔

任何具有执行权限的账户（除了赏金发布者）都可以对正在进行的公开或单独赏金提交索赔。此时代理以索赔者的身份进行操作，无需任何代币，只需支付Gas费用。

提交索赔时需要提供证明文件（`uri`），该文件可以是IPFS图片哈希、直接图片URL、推文链接、GitHub链接、网页链接、视频等。提交后，这些文件会被铸造成NFT。

### 检查赏金的状态

在提交前，请确认：
- 赏金是否仍然有效；
- 赏金是否尚未完成；
- 当前是否有投票进行中。

```bash
cast call $POIDH_CONTRACT_ADDRESS \
  "bounties(uint256)(uint256,address,string,string,uint256,address,uint256,uint256)" \
  <BOUNTY_ID> \
  --rpc-url $RPC_URL
# Returns: id, issuer, name, description, amount, claimer, createdAt, claimId
# claimer == 0x0 means active; claimer == issuer means cancelled; claimer == other means already won
```

同时确认当前没有投票正在进行中：

```bash
cast call $POIDH_CONTRACT_ADDRESS \
  "bountyCurrentVotingClaim(uint256)(uint256)" \
  <BOUNTY_ID> \
  --rpc-url $RPC_URL
# Returns 0 if no active vote — safe to submit
```

### 提交索赔

```bash
cast send $POIDH_CONTRACT_ADDRESS \
  "createClaim(uint256,string,string,string)" \
  <BOUNTY_ID> \
  "<CLAIM_NAME>" \
  "<CLAIM_DESCRIPTION>" \
  "<PROOF_URI>" \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

- `CLAIM_NAME`：索赔的简短标题；
- `CLAIM_DESCRIPTION`：说明如何完成该赏金；
- `PROOF_URI`：实际的证明文件（图片URL、IPFS URI、推文链接等）。

**示例：**

```bash
cast send $POIDH_CONTRACT_ADDRESS \
  "createClaim(uint256,string,string,string)" \
  42 \
  "Brooklyn Bridge golden hour" \
  "Took this photo at 7:43pm on the Manhattan side. Full span visible with reflection in the water." \
  "ipfs://QmXyz..." \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

### 提交后获取索赔ID

```bash
cast receipt <TX_HASH> --rpc-url $RPC_URL --json | \
  python3 -c "
import sys, json
receipt = json.load(sys.stdin)
for log in receipt['logs']:
    if log['address'].lower() == '$POIDH_CONTRACT_ADDRESS'.lower() and len(log['topics']) >= 2:
        claim_id = int(log['topics'][1], 16)
        print(f'Claim ID: {claim_id}')
        break
"
```

### 重要限制

- 代理的钱包（`PRIVATE_KEY`）不能是赏金发布者；否则会触发错误 `IssuerCannotClaim`；
- 如果赏金正在接受投票，则无法提交新的索赔；否则会触发错误 `VotingOngoing`；
- 赏金必须处于开放状态；已完成的或已取消的赏金无法再次提交索赔；
- 每个赏金的索赔数量没有限制，由发布者选择最佳索赔。

---

## 第6部分：提取奖金

作为索赔者赢得赏金后，奖金会被计入`pendingWithdrawals`账户，需要手动提取。`acceptClaim`或`resolveVote`操作完成后，奖金（扣除2.5%的协议费用）即可立即提取。

### 检查待提取的余额

```bash
cast call $POIDH_CONTRACT_ADDRESS \
  "pendingWithdrawals(address)(uint256)" \
  <YOUR_ADDRESS> \
  --rpc-url $RPC_URL
```

### 提取到自己的账户

```bash
cast send $POIDH_CONTRACT_ADDRESS \
  "withdraw()" \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

### 提取到其他账户

```bash
cast send $POIDH_CONTRACT_ADDRESS \
  "withdrawTo(address)" \
  <RECIPIENT_ADDRESS> \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

> `withdraw()` 一次操作可以提取全部待提取的余额。在提交交易前，请先确认余额是否可用。

---

## 代理的决策流程

### 发布赏金

1. 询问用户赏金的 **名称**、**描述**、**金额**（Arbitrum/Base链使用ETH，Degen Chain使用DEGEN）以及 **类型**（单独发布或公开发布，默认为单独发布）；
2. 在发送请求前与用户确认——这会消耗实际的ETH（或Degen Chain上的DEGEN）；
3. 调用 `createSoloBounty` 或 `createOpenBounty`；
4. 返回交易哈希和 `POIDH_BASE_URL/bounty/<bountyId + $POIDH_V2_OFFSET>`。

### 提交索赔

1. 询问用户赏金的 **ID**、**证明文件URL**（图片、链接、IPFS哈希等）、**索赔名称**以及 **描述**；
2. 确认赏金是否有效且当前没有投票进行中；
3. 确认代理的钱包不是赏金发布者；
4. 在发送请求前与用户确认；
5. 调用 `createClaim(bountyId, name, description, uri)`；
6. 返回索赔ID和交易哈希。

### 评估和接受索赔

1. 询问赏金的ID；
2. 根据 `everHadExternalContributor` 确定正确的处理方式；
3. 通过 `getClaimsByBountyId` 获取所有未接受的索赔；
4. 对每个索赔：获取`tokenURI`，解析URL，并使用相应工具评估内容；
5. 向用户展示推荐的获胜者及选择理由，确认后再执行交易；
6. **单独发布/无外部参与者**：调用 `acceptClaim(bountyId, claimId)`；
7. **有外部参与者**：调用 `submitClaimForVote(bountyId, claimId)`，通知用户参与者有2天的投票时间，投票结束后调用 `resolveVote`。

---

## 原生代币金额参考

| 人类可读金额 | 对应的代币数量 |
| ---------- | -------------- |
| 0.001 ETH    | `0.001ether`     |
| 0.01 ETH     | `0.01ether`     |
| 1 ETH        | `1ether`       |
| 1000 DEGEN   | `1000ether`     |
| 10 DEGEN     | `10ether`     |

> `cast` 使用 `ether` 作为18位小数代币的统一单位。在Degen Chain上，`ether`代表DEGEN，而非ETH。

---

## 费用说明

PoidhV3会对已接受的赏金收取**2.5%的费用**，该费用仅在赏金发放时扣除。在费用扣除之前，所有交易金额（`msg.value`）会暂存在托管账户中。费用以链上的原生代币支付：Arbitrum和Base链使用ETH，Degen Chain使用DEGEN。

---

## 错误处理

| 错误类型            | 原因                                                         | 处理方法                                                         |
| --------------------------- | -------------- | --------------------------- |
| `ContractsCannotCreateBounties()` | 使用的钱包不是智能合约钱包 | 使用具有执行权限的私钥                         |
| `MinimumBountyNotMet()` | 提交的金额低于最低要求 | 调整 `--value`（Arbitrum/Base链为0.001 ETH，Degen Chain为1000 DEGEN） |
| `MinimumContributionNotMet()` | 提交的贡献金额低于最低要求 | 参与公开赏金时调整 `--value`                     |
| `NoEther()`         | `--value` 为0或未提供                   | 添加 `--value`                         |
| `WrongCaller()`        | 提交者不是赏金发布者                   | 使用赏金发布者的私钥                         |
| `VotingOngoing()`     | 投票正在进行中                     | 等待投票期限结束后再执行 `resolveVote`                 |
| `VotingEnded()`     | 投票期限已过但尚未完成投票                 | 调用 `resolveVote`                     |
| `NotSoloBounty()`      | 公开赏金但有外部参与者尝试直接接受           | 使用 `submitClaimForVote`                     |
| `ClaimAlreadyAccepted()`   | 索赔已被接受                     | 无需处理                                         |
| `BountyClaimed()`      | 赏金已被完成                     | 无需处理                                         |
| `BountyClosed()`      | 赏金已被取消                     | 无需处理                                         |
| `BountyNotFound()`     | 无效的赏金ID                         | 检查赏金ID                         |
| `ClaimNotFound()`     | 无效的索赔ID                         | 检查索赔ID                         |
| `IssuerCannotClaim()`     | 发布者尝试提交自己的赏金                 | 使用其他参与者的钱包提交索赔                     |
| `NotActiveParticipant()`    | 提交者不是参与者或已退出投票                 | 必须是活跃的参与者                     |
| `MaxParticipants Reached()` | 公开赏金的参与者数量达到上限                 | 等待空闲的投票名额                     |
| `NothingToWithdraw()`     | 无待提取的余额                     | 先检查 `pendingWithdrawals(address)`                 |
| `VoteWouldPass()`     | 尝试重置已通过的投票                   | 无法更改已通过的投票结果                     |