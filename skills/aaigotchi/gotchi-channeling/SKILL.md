---
name: gotchi-channeling
description: 通过 Bankr 钱包实现自主化的 Aavegotchi Alchemica 功能。每天会从您在 REALM 包裹中设置的“Aaltar”装置中自动收集收益。无需签名——安全、自动化且操作简单！
homepage: https://github.com/aaigotchi/gotchi-channeling
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
        - curl
      env:
        - BANKR_API_KEY
    primaryEnv: BANKR_API_KEY
---
# Gotchi Channeling 🔮  
自动采集Aavegotchi所需的Alchemica资源，每天自动执行，安全、简单且无需签名！  

## 什么是Channeling？  
**Alchemical Channeling**允许您通过安装在REALM包裹上的Aaltar，从Gotchiverse环境中获取Alchemica（包括FUD、FOMO、ALPHA、KEK）资源。  

**奖励：**每次通道操作可获取20-70个FUD、10-35个FOMO、5-17个ALPHA或2-7个KEK  
**冷却时间：**每个Gotchi每次操作后需等待24小时  
**要求：**必须安装Aaltar，并拥有相应的REALM包裹  

## 主要功能：  
✅ **每日自动通道操作**：设置一次即可忘记后续操作  
✅ **集成Bankr钱包**：无需暴露私钥  
✅ **支持多个Gotchi**：可同时处理多个Gotchi  
✅ **智能冷却时间检查**：避免在交易被阻止时浪费资源  
✅ **无需签名**：无需后端API（忽略旧参数）  
✅ **交易追踪**：提供完整日志和历史记录  
✅ **提醒系统**：可选的通知功能  

## 工作原理：  
1. **检查冷却时间**：从合约中读取上次通道操作的时间戳  
2. **构建交易数据**：生成`channelAlchemica()`所需的calldata  
3. **通过Bankr提交**：Bankr钱包负责安全的签名和提交过程  
4. **获取Alchemica资源**：FUD、FOMO、ALPHA、KEK会被直接添加到您的钱包中  
5. **等待24小时**：冷却时间结束后，可再次进行通道操作  

## 设置步骤：  
### 1. 配置您的REALM包裹和Gotchi  
创建`~/.openclaw/workspace/skills/gotchi-channeling/config.json`文件：  
（配置示例代码见下方）  

### 2. 验证Bankr钱包配置  
（Bankr钱包配置代码见下方）  

### 3. 测试单个Gotchi的通道操作  
（单个Gotchi的通道操作代码见下方）  

## 使用方法：  
### 手动通道操作：  
（手动通道操作的代码见下方）  

### 自动化每日通道操作：  
- **设置cron作业**：  
（设置定时任务的代码见下方）  
- **或使用OpenClaw调度器**：  
（使用OpenClaw调度器的代码见下方）  

## 合约详情：  
### REALM Diamond（基础版本）  
**地址：`0x4B0040c3646D3c44B8a28Ad7055cfCF536c05372`  
**函数：`channelAlchemica`**  
（函数参数及使用说明见下方）  

**冷却时间：**24小时（43200秒）  
**要求：**  
- 必须拥有该REALM包裹的访问权限  
- 包裹上必须安装Aaltar  
- 自上次通道操作后必须已过24小时  
- 所使用的Gotchi必须存在且归您所有  

### Alchemica资源地址：  
- **FUD：`0x2028b4043e6722ea164946c82fe806c4a43a0ff4`  
- **FOMO：`0xa32137bfb57d2b6a9fd2956ba4b54741a6d54b58`  
- **ALPHA：`0x15e7cac885e3730ce6389447bc0f7ac032f31947`  
- **KEK：`0xe52b9170ff4ece4c35e796ffd74b57dec68ca0e5`  

## 奖励计算：  
Alchemica的数量取决于您的Gotchi的**亲密度得分**（Kinship score）。  
**奖励计算公式**：  
（计算公式见下方）  
**每次通道操作的典型奖励：**  
- **FUD：**135.20（20-70个范围内）  
- **FOMO：**67.60（10-35个范围内）  
- **ALPHA：**33.80（5-17个范围内）  
- **KEK：**13.52（2-7个范围内）  
**总计：**每次通道约250个Alchemica资源  

**提高奖励的方法：**  
- ✅ 提高Gotchi的亲密度（每天互动）  
- ✅ 升级Aaltar  
- ✅ 选择含有Alchemica资源的REALM包裹  

## 脚本：  
- `channel.sh`：单个Gotchi的通道操作（包含完整输出）  
- `channel-all.sh`：批量处理所有配置好的Gotchi  
- `check-cooldown.sh`：查询链上的冷却状态  
- `channel-status.sh`：显示多个Gotchi的通道状态  

## 故障排除：  
- **“只有所有者才能操作”**：必须拥有包裹或访问权限  
- **“Gotchi无法通道”**：冷却时间未到  
- **“需要安装Aaltar”**：确保包裹上安装了Aaltar  
- **“交易失败”**：检查是否有足够的ETH作为交易费用  
- **“未收到Alchemica”**：检查交易记录和钱包余额  

## 安全性：  
- **仅集成Bankr钱包**：不使用私钥  
- **安全交易签名**：由Bankr远程处理签名  
- **无密钥泄露风险**：密钥不会被加载到内存中  
- **API密钥认证**：保护Bankr访问权限  
- **仅读取冷却状态**：安全地进行链上查询  
- **完整交易记录**：提供审计追踪  

## 监控与查询：  
- **查看通道历史**：查询通道操作记录  
- **追踪Token余额**：查看Gotchi的Token余额  

## 常见问题：  
- **多久可以操作一次？**：每个Gotchi每天一次  
- **不同Gotchi需要不同包裹吗？**：不需要，多个Gotchi可以使用同一个包裹  
- **有多个Aaltar怎么办？**：每个Aaltar有独立的冷却时间  
- **签名参数重要吗？**：忽略该参数，始终传递`0x`  
- **可以操作别人的Gotchi吗？**：不可以，必须同时拥有包裹和Gotchi  
- **Alchemica去向？**：直接作为ERC20 Token添加到您的钱包  

## 成本：**  
每次通道操作的费用约为0.01-0.05美元（基于Base链的低费用）  
**自动化方式**：可以使用cron作业或OpenClaw调度器实现每日自动操作  

## 更新记录：  
### v1.0.0（2026-02-21）  
- 首次发布  
- 支持无需签名的通道操作  
- 集成Bankr钱包  
- 支持多个Gotchi  
- 实现每日自动通道操作  
- 引入冷却时间检查  
- 提供交易日志和奖励追踪  

## 支持信息：  
- **合约地址：**`0x4B0040c3646D3c44B8a28Ad7055cfCF536c05372`  
- **链版本：**Base（8453）  
- **文档：**https://docs.gotchiverse.io/  
- **Discord社区：**https://discord.gg/aavegotchi  

---

**由AAI团队精心制作✨**  
**通过Channeling获取Alchemica财富吧！**  
LFGOTCHi! 🦞🔮💎