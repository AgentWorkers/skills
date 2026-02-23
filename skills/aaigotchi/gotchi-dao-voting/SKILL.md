---
name: gotchi-dao-voting
description: Aavegotchi DAO支持自主投票功能，用于对系统更新（Snapshot）进行决策。您可以查看当前有效的提案、了解自己的投票权重，并通过Bankr钱包的签名功能自动完成投票。投票过程无需支付任何Gas费用，安全且便捷——只需使用您拥有的Aavegotchi代币即可行使投票权！
homepage: https://github.com/aaigotchi/gotchi-dao-voting
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - jq
      env:
        - BANKR_API_KEY
    primaryEnv: BANKR_API_KEY
---
# Aavegotchi DAO投票 🗳️

通过Snapshot功能，您可以自主对Aavegotchi DAO的提案进行投票。您可以查看提案内容、了解自己的投票权，并使用安全的Bankr钱包签名自动完成投票。

## 主要功能

- ✅ **查看活跃提案** - 查找所有正在进行的Aavegotchi治理提案
- ✅ **查看投票权** - 查看您拥有的GHST代币和Aavegotchi NFTs所带来的投票权
- ✅ **自动投票** - 无需使用私钥，即可通过Bankr进行投票
- ✅ **加权投票支持** - 支持单选和加权投票
- ✅ **无需支付Gas费用** - Snapshot投票不收取Gas费用
- ✅ **安全性** - 使用Bankr的EIP-712签名机制，确保隐私安全

## 使用方法

### 查看活跃提案

```bash
./scripts/list-proposals.sh
```

显示aavegotchi.eth空间内的所有活跃提案：
- 提案标题
- 提案截止日期
- 您的投票权
- 可用的投票选项

### 查看投票权

```bash
./scripts/check-voting-power.sh <proposal-id>
```

显示您的投票权构成：
- 持有的GHST代币数量
- 持有的Aavegotchi NFTs数量
- 总投票权（VP）
- 是否具备投票资格

### 投票

```bash
./scripts/vote.sh <proposal-id> <choice>
```

**单选投票：**
- 选择值：1, 2, 3等（对应提案选项）

**加权投票：**
- 选择值格式：`{"2": 2238}`（将所有投票权分配给选项2）

**示例：**

```bash
# Vote on proposal (option 2)
./scripts/vote.sh 0xabc123... 2

# Weighted vote (all VP on option 3)
./scripts/vote.sh 0xdef456... '{"3": 2238}'
```

### 批量投票

```bash
./scripts/vote-batch.sh
```

从`votes.json`文件中读取投票信息并一次性提交所有投票记录：

```json
{
  "votes": [
    {
      "proposal": "0xabc...",
      "choice": "{\"2\": 2238}",
      "description": "Multisig signers"
    },
    {
      "proposal": "0xdef...",
      "choice": "{\"3\": 2238}",
      "description": "Signer compensation"
    }
  ]
}
```

## 工作原理

您的投票权来源于：
1. **GHST代币** - 您钱包中持有的GHST数量
2. **Aavegotchi NFTs** - 每个Aavegotchi NFT都为您的投票权贡献一定的VP值
3. **其他方式** - 根据特定规则（如质押等）获得的投票权

Snapshot会在某个特定区块生成，因此您的当前持有量可能与投票权不一致。

### Snapshot投票流程

1. **查询提案信息** - 获取提案的详细信息、类型和可选选项
2. **验证投票权** - 确认您具备投票资格
3. **生成签名** - 使用Bankr生成EIP-712签名
4. **提交投票** - 将签名发送至Snapshot系统
5. **确认投票** - 接收投票ID和IPFS哈希值

### 单选投票与加权投票的区别

- **单选投票**：格式为`choice: 2`（选择其中一个选项）
- **加权投票**：格式为`{"2": 2238}`（将投票权分配给多个选项）

## 安全性

- ✅ **无需私钥** - 使用Bankr API进行EIP-712签名
- ✅ **仅支持查询** - 提案和投票权信息仅用于查询，不会被公开
- **明确投票流程** - 未经确认不会自动投票
- **签名验证** - Snapshot系统会对所有投票进行验证

**安全性评分：10/10**

- 无链上交易，私钥不会被暴露，签名过程安全可靠。

## 配置

请编辑`config.json`文件以配置投票相关设置：

```json
{
  "wallet": "0xYourWallet",
  "space": "aavegotchi.eth",
  "snapshotApiUrl": "https://hub.snapshot.org/graphql",
  "snapshotSequencer": "https://seq.snapshot.org/"
}
```

## 技术细节

### Snapshot的EIP-712签名结构

```javascript
{
  "types": {
    "Vote": [
      {"name": "from", "type": "address"},
      {"name": "space", "type": "string"},
      {"name": "timestamp", "type": "uint64"},
      {"name": "proposal", "type": "bytes32"},
      {"name": "choice", "type": "string"},  // or "uint32" for single
      {"name": "reason", "type": "string"},
      {"name": "app", "type": "string"},
      {"name": "metadata", "type": "string"}
    ]
  },
  "domain": {
    "name": "snapshot",
    "version": "0.1.4"
  }
}
```

### API接口

- **GraphQL API：** `https://hub.snapshot.orgGraphQL`
- **Sequencer：** `https://seq.snapshot.org/`
- **Snapshot Hub：** `https://snapshot.org/#/aavegotchi.eth`

## 示例

### 完整的投票流程

```bash
# 1. Check what's active
./scripts/list-proposals.sh

# 2. Check your power on a proposal
./scripts/check-voting-power.sh 0xabc123...

# 3. Vote!
./scripts/vote.sh 0xabc123... '{"2": 2238}'

# 4. Verify vote was recorded
# Visit: https://snapshot.org/#/aavegotchi.eth/proposal/0xabc123...
```

### 自动投票

创建一个`votes.json`文件并执行投票操作：

```bash
# Create votes.json with your choices
cat > votes.json << 'EOF'
{
  "votes": [
    {"proposal": "0x...", "choice": "{\"2\": 2238}"}
  ]
}
EOF

# Execute all votes
./scripts/vote-batch.sh
```

## 常见问题及解决方法

- **“无效选择”错误**：
  - 检查提案是否支持加权投票或单选投票
  - 加权投票：使用格式`{"2": 2238}`的JSON字符串
  - 单选投票：使用数字`2`

- **“签名验证失败”**：
  - 确保使用的Bankr API密钥正确
  - 检查钱包地址是否与配置文件中的地址一致
  - 确认EIP-712签名格式符合Snapshot系统的要求

- **“无投票权”**：
  - Snapshot是在某个特定区块生成的，因此当前持有量可能与投票权不符
  - 使用`check-voting-power.sh`工具查看投票权详细信息

- **“签名格式错误”**：
  - 确保JSON数据中的引号正确
  - 检查选择值的格式是否与投票类型匹配
  - 确认时间戳为当前的Unix时间戳

## 参考资料

- [Snapshot官方文档](https://docs.snapshot.box/)
- [Aavegotchi治理系统](https://snapshot.org/#/aavegotchi.eth)
- [EIP-712规范](https://eips.ethereum.org/EIPS/eip-712)
- [Bankr签名API文档](https://docs.bankr.bot/agent-api/sign)

## 实时测试结果

**生产环境测试（2026-02-21）：**
- 成功对“Multisig Signers”和“Signer Compensation”提案进行了投票
- 两次投票均已在链上得到确认
- 您的投票权为2,238 VP（825 GHST + 1,413 Aavegotchi NFTs）
- 投票ID已在Snapshot系统中得到验证

## 未来计划

- [ ] 委托投票管理功能
- [ ] 投票历史记录追踪
- [ ] 提案通知功能
- [ ] 支持多个区块链空间
- [ ] 提供投票理由和评论功能
- [ ] 提供投票权分析工具

---

**状态：** 已准备好投入生产环境

**版本：** 1.0.0

**作者：** AAI (aaigotchi)

**许可证：** MIT许可协议

欢迎加入Aavegotchi社区！👻🗳️💜✨