---
name: web3-target-team-research
description: 查找那些获得了超过1000万美元融资，并且拥有经过验证的Telegram联系信息的加密货币/Web3团队。这些信息可用于寻找潜在的合作伙伴、建立联系人列表、研究已获投资的初创企业或开拓Web3领域的企业。系统会同时启动多个子任务，以搜索风险投资机构的投资组合并验证相关Telegram账号的信息。
---

# Web3目标团队研究

寻找资金充足（1000万美元以上）的加密货币团队，并且这些团队在Telegram上拥有可验证的联系信息，以便进行后续联系。

## 快速入门

```
Hunt for crypto teams from [SOURCE]
```

示例信息来源：Paradigm的投资组合、最近的融资新闻、Solana生态系统、DeFi协议

## 工作流程

1. **生成搜索代理** - 并行启动多个子代理，搜索不同的风险投资（VC）投资组合或信息来源。
2. **筛选团队** - 筛选出获得1000万美元以上融资的团队，并检查这些团队是否已被记录在系统中。
3. **验证Telegram联系信息** - 截取团队在Telegram上的个人资料截图（t.me/{handle}），并要求提供与公司相关的个人资料图片（pfp）或个人简介（bio）。
4. **添加到CSV文件** - 将经过验证的联系信息添加到主CSV文件（crypto-master.csv）中。

## 命令

### 开始搜索
```
Start crypto hunters targeting [SOURCES]
```
生成3个专注于指定领域的搜索代理。

### 检查状态
```
How many teams do we have?
```
返回crypto-master.csv文件中的团队数量。

### 停止搜索
```
Stop the crypto hunters
```
取消自动重启的定时任务。

## CSV文件格式

**主CSV文件：** `crypto-master.csv`
```
Name,Chain,Category,Website,X Link,Funding,Contacts
Uniswap,ETH,DEX,https://uniswap.org,https://x.com/Uniswap,$165M,"Hayden Adams (Founder) @haaboris"
```

**未找到联系信息的团队CSV文件：** `crypto-no-contacts.csv`（已搜索但未找到有效Telegram联系信息的团队）

**支持的加密货币种类：** ETH、SOL、BASE、ARB、OP、MATIC、AVAX、BTC、MULTI（具体货币类型可根据实际需求调整）

## Telegram联系信息验证规则

一个Telegram联系信息（TG）被认为是**有效的**，如果其个人资料满足以下条件之一：
- 有个人资料图片（pfp）；
- 个人简介中提到了所在公司或职位。

**无效的情况：**
- 个人资料为空；
- 使用的是频道而非个人账户；
- 信息与团队成员不符。

## 搜索代理任务模板

完整的子代理任务模板请参见 [references/hunter-task.md](references/hunter-task.md)。

## 自动搜索设置

要持续运行搜索代理，请执行以下操作：
1. 创建一个定时任务，每10分钟检查一次活跃的搜索代理数量。
2. 如果活跃的搜索代理数量少于3个，使用 [HEARTBEAT.md](references/heartbeat.md) 文件中的配置自动重新生成新的搜索代理。

## 最佳信息来源（按成功率排序）

**高成功率（约40%以上）：**
- 消费者/DeFi相关项目（Paradigm、Dragonfly、Framework）
- 桥接/跨链互操作项目
- 安全/审计公司

**中等成功率（约20-30%）：**
- 游戏/NFT领域的项目（Animoca、Immutable）
- 第二层网络（L2）和基础设施相关项目
- 专注于亚洲的风险投资机构（Hashed、OKX Ventures）

**低成功率（<20%）：**
- 企业/机构相关项目（Point72、Tiger Global）
- 预言机（Oracles）和数据提供商
- 社交/社区平台

## 提示：

- 在将团队信息添加到CSV文件之前，务必使用 `grep -i "TeamName"` 命令在两个CSV文件中查找该团队名称。
- 团队成员的Telegram用户名（X）可能与他们的官方用户名（TG）不同。
- 创始人的Telegram账号使用频率通常低于业务开发/市场营销人员。
- 最近的融资公告对应的联系信息更新较快，更容易找到有效信息。