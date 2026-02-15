---
name: genesis-launch
description: 使用 Metaplex Genesis 协议在 Solana 上启动代币（Launch Tokens）
metadata:
  openclaw:
    emoji: "\U0001F680"
    requires:
      config:
        - "plugins.entries.genesis.enabled"
---

# Metaplex Genesis代币发行

您可以使用Metaplex Genesis协议帮助用户在Solana平台上发行代币。该协议支持公平、透明的代币发行过程，并内置了流动性池的生成机制。

## 什么是Genesis？

Genesis是Metaplex为Solana平台开发的一种代币发行协议，它提供了以下功能：

- **LaunchPool**：用户在一个指定的时间段内存入SOL（Solana币），之后可以根据他们的存款比例来领取相应的代币。
- **Unlocked Buckets**：用于直接分配代币给团队、资金库或进行空投（airdrops）。
- **Raydium CPMM Graduation**：在代币发行结束后，会自动使用募集到的SOL创建一个Raydium流动性池，并将代币分配到该池中。

## 发行流程

1. **创建发行配置**（`genesis_create_launch`）：设置代币信息及Genesis账户。
2. **配置分配方案**：添加LaunchPool、Unlocked Buckets和/或Raydium Buckets。
3. **完成配置**（`genesisfinalize_launch`）：锁定配置，正式开始发行。
4. 用户在存款期间存入SOL。
5. 存款期结束后，SOL会被转入Raydium流动性池。
6. 用户在领取期领取代币。

## 推荐的配置流程

当用户想要发行代币时，需要准备以下信息：

- **代币详情**：名称、符号、描述以及代币图片文件的路径。
- **总发行量**：代币的总数量（默认为10亿个）。
- **分配比例**：分配给LaunchPool、流动性池和团队的比例（例如：60%给LaunchPool，20%给Raydium流动性池，20%给团队）。
- **时间安排**：存款的开始和结束时间，以及领取代币的开始时间。

## 常见的配置方案：LaunchPool + Raydium + Team

这是最常见的配置方式。以60/20/20的分配比例为例：

    第一步：`genesis_create_launch`
        - 设置代币名称、符号、描述和图片文件路径。
        - 设置总发行量（`totalSupply`为10亿个代币）。

    第二步：`genesis_add_raydium_pool`（请先执行此步骤，以便获取Raydium池的索引）：
        - 设置代币分配比例（`tokenAllocationPercent`为20%）。
        - 指定Raydium池的索引（`bucketIndex`为0）。

    第三步：`genesis_add_launchpool`：
        - 设置代币分配比例（`tokenAllocationPercent`为60%）。
        - 设置存款期限（`depositDurationHours`为72小时，即3天）。
        - 设置领取期限（`claimDurationHours`为168小时）。
        - 指定将代币发送到Raydium池的索引（`sendQuoteTokenToRaydiumBucketIndex`为0）。
        - 指定Raydium池的索引（`bucketIndex`为0）。

    第四步：`genesis_add_unlocked`：
        - 设置代币分配比例（`tokenAllocationPercent`为20%）。
        - 指定Raydium池的索引（`bucketIndex`为0）。

    第五步：`genesisfinalize_launch`：
        - 设置Raydium池的索引（`raydiumBucketIndexes`为[0]）。
        - 设置LaunchPool的索引（`launchpoolBucketIndexes`为[0]）。
        - 设置Unlocked Buckets的索引（`unlockedBucketIndexes`为[0]）。

## 重要注意事项：

- 所有分配渠道的代币比例之和必须精确为100%。
- 请在配置LaunchPool之前先配置Raydium池，以便在LaunchPool的配置中引用其索引。
- 创建Raydium池需要支付0.15个SOL的费用。
- 代币的元数据（图片和JSON文件）会通过Irys上传到Arweave存储，费用由用户的钱包中的SOL支付。
- 可以使用`genesis_launch_status`随时查看发行的当前状态。

## 钱包设置

该插件需要用户的Solana密钥对。用户可以通过以下方式配置密钥对：
- 通过插件配置文件（`keypairPath`）指定JSON格式的密钥对文件路径。
- 通过环境变量（`SOLANA_KEYPAIR_PATH`）设置密钥对路径。
- 默认路径为`~/.config/solana/id.json`。

用户的钱包中必须拥有足够的SOL来支付交易费用、Irys的上传费用以及创建Raydium池的费用。