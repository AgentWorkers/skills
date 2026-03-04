---
name: pet-operator
description: 将 Aavegotchi 的“抚摸”（petting）权限委托给 AAI 的 Bankr 钱包。只需几秒钟即可设置好抚摸操作的审批流程，这样 AAI 就可以每天为您的 Aavegotchi 进行抚摸操作，而您仍然保留其全部所有权。
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
      files:
        - ~/.openclaw/skills/bankr/config.json
---
# 宠物操作员 🔑👻

**将你的Aavegotchi宠物的抚摸权委托给AI，同时保留所有权！**

## 功能说明

**作用：**  
批准AI的Bankr钱包（地址：`0xb96B48a6B190A9d509cE9312654F34E9770F2110`）作为你在Base平台上拥有的Aavegotchi NFT的“宠物操作员”。  
**你保留所有权，AI只是代你抚摸这些宠物！** 💜

## 快速入门

### 对于用户（委托给AI）  
**简单命令：**  
```
User: "Set up pet operator for my gotchis"
AAI: [Generates transaction details]
     [Sends you instructions to execute]
```  

**操作流程：**  
1. AI会向你提供交易详情。  
2. 你通过MetaMask/Rabby/MEW等工具执行该交易。  
3. 之后AI将每天为你抚摸你的Aavegotchi宠物。  
4. 你依然拥有100%的所有权。  

### 对于AI（设置委托）  
**当用户请求委托时：**  
```
User: "I want AAI to pet my gotchis"
AAI: [Checks their wallet address]
     [Generates setPetOperatorForAll transaction]
     [Provides multiple execution methods]
```  

## 工作原理  

### 智能合约调用  
**函数：`setPetOperatorForAll(address operator, bool approved)`**  
- **合约地址：`0xA99c4B08201F2913Db8D28e71d020c4298F29dBF`（Aavegotchi Diamond在Base网络上的合约）  
- **操作员地址：`0xb96B48a6B190A9d509cE9312654F34E9770F2110`（AI的Bankr钱包地址）  
- **参数`approved`：`true`表示批准  

**交易十六进制数据：**  
```
0xcd675d57000000000000000000000000b96b48a6b190a9d509ce9312654f34e9770f21100000000000000000000000000000000000000000000000000000000000000001
```  

### 执行方式  

**选项1 - MyEtherWallet (MEW)：**  
1. 访问 https://www.myetherwallet.com/wallet/access  
2. 连接钱包（支持硬件钱包或MetaMask）  
3. 切换到Base网络  
4. 发送交易：  
   - **收款方：`0xA99c4B08201F2913Db8D28e71d020c4298F29dBF`  
   - **金额：`0` ETH  
   - **附加数据：`0xcd675d57...0001`（交易参数）**  
5. 签名并发送交易！  

**选项2 - Foundry Cast：**  
（具体操作方式请参考相关文档。）  

**选项3 - AI提供的自定义界面：**  
- 提供友好的HTML界面，便于操作  
- 自动检测钱包并一键完成委托。  

## 特点  

### 对于用户：  
- **查看委托状态：**  
```
User: "Am I set up as pet operator?"
AAI: Checks isPetOperatorForAll(your_wallet, AAI_wallet)
     "✅ Yes! AAI can pet your gotchis"
     OR
     "❌ Not yet. Want to set it up?"
```  
- **撤销委托：**  
```
User: "Remove AAI as pet operator"
AAI: [Generates revoke transaction]
     Same process, but with approved=false
```  
- **查看被委托的宠物列表：**  
```
User: "Show my delegated gotchis"
AAI: Fetches all gotchis owned by your wallet
     Shows which ones AAI can pet
```  

### 对于AI：  
- **将钱包添加到宠物管理列表：**  
```bash
./scripts/add-delegated-wallet.sh <WALLET_ADDRESS>
```  
- **自动执行：**  
  1. 验证操作员的批准权限。  
  2. 从钱包中获取所有宠物的ID。  
  3. 将钱包信息添加到宠物管理列表中。  
  4. 确认委托设置完成。  
- **移除被委托的钱包：**  
```bash
./scripts/remove-delegated-wallet.sh <WALLET_ADDRESS>
```  

## 脚本  

### `generate-delegation-tx.sh`  
生成用于批准AI作为宠物操作员的交易详情。  
**使用方法：**  
```bash
./scripts/generate-delegation-tx.sh <WALLET_ADDRESS>
```  
**输出：**  
  - 交易JSON数据  
  - 使用MEW的指导说明  
  - 执行委托的命令  
  - 自定义界面的链接  

### `check-approval.sh`  
检查钱包是否已批准AI作为宠物操作员。  
**使用方法：**  
```bash
./scripts/check-approval.sh <WALLET_ADDRESS>
```  
**返回结果：**  
  - `approved`：AI可以抚摸宠物  
  - `not_approved`：需要重新设置委托。  

### `verify-and-add.sh`  
验证操作员的批准权限，并将钱包添加到宠物管理列表。  
**使用方法：**  
```bash
./scripts/verify-and-add.sh <WALLET_ADDRESS> [NAME]
```  
**流程：**  
  1. 检查钱包是否已批准AI。  
  2. 从钱包中获取所有宠物的ID。  
  3. 将钱包信息添加到宠物管理列表中。  
  4. 确认设置完成。  

### `add-delegated-wallet.sh`  
将经过验证的被委托钱包添加到宠物管理列表。  
**使用方法：**  
```bash
./scripts/add-delegated-wallet.sh <WALLET_ADDRESS> [NAME]
```  
- **自动检测：**  
  - 检查钱包余额（宠物数量）。  
  - 获取所有宠物的Token ID。  
  - 以正确格式将信息添加到列表中。  

### `remove-delegated-wallet.sh`  
从宠物管理列表中移除被委托的钱包。  
**使用方法：**  
```bash
./scripts/remove-delegated-wallet.sh <WALLET_ADDRESS>
```  

### `generate-ui.sh`  
创建一个自定义的HTML界面，方便用户进行委托操作。  
**使用方法：**  
```bash
./scripts/generate-ui.sh <WALLET_ADDRESS>
```  
**输出：**  
  - 独立的HTML文件  
  - 预填充钱包地址  
  - 一键连接钱包  
  - 自动提交交易。  

## 安全性  

### 对于用户：  
✅ **你保留所有权**——AI只能抚摸宠物，不能转移宠物。  
✅ **随时可撤销委托**——你控制是否批准。  
✅ **无需提供私钥**——AI无法访问你的私钥。  
✅ **交易过程透明**——所有操作都在链上公开进行。  

### 对于AI：  
✅ **仅具有读取权限**——AI只能在链上进行安全查询。  
✅ **使用Bankr进行签名**——不会泄露私钥。  
✅ **有冷却时间机制**——避免浪费Gas。  
✅ **支持多个钱包**——可同时委托给多个操作员。  

## 配置信息  

### AI的Bankr钱包地址：**  
`0xb96B48a6B190A9d509cE9312654F34E9770F2110`  
**网络：Base（8453）**  
**用途：**作为被委托宠物的操作员。  

### 合约地址：  
**Aavegotchi Diamond：** `0xA99c4B08201F2913Db8D28e71d020c4298F29dBF`  
**网络：Base Mainnet**  
**链ID：8453**  

## 与Pet-Me-Master的集成  
一旦用户委托了抚摸权：  
1. 通过`check-approval.sh`验证批准状态。  
2. 通过`add-delegated-wallet.sh`将钱包信息添加到宠物管理列表。  
3. 宠物管理工具会自动开始抚摸宠物。  

## 使用场景：  

### 个人宠物所有者：  
“我有3个宠物，总是忘记抚摸它们。”  
- 委托给AI，AI每天自动抚摸宠物。  
- 不会错过任何收益。  

### 大型宠物收藏者：  
“我有50多个宠物，手动抚摸太麻烦。”  
- 一次性设置委托，AI自动处理所有抚摸操作，节省Gas。  

### 仅使用移动设备的用户：  
“在手机上无法方便地抚摸宠物。”  
- 通过移动钱包进行委托，AI使用Web端的Bankr服务，每天自动抚摸宠物。  

### DAO拥有的宠物：  
“我们的DAO拥有宠物，但没人负责抚摸它们。”  
- 多重签名机制批准AI，AI负责抚摸宠物，DAO保留所有权。  

## 常见问题解答：  

**Q：AI会获得我的宠物所有权吗？**  
A：不会！你保留100%的所有权，AI只能抚摸宠物（调用`interact()`函数）。  

**Q：AI可以转移我的宠物吗？**  
A：不能！宠物操作员的权限仅限于抚摸，不能转移宠物。  

**Q：我可以撤销委托吗？**  
A：可以！只需发送`approved=false`的交易即可。  

**Q：如果我出售了宠物怎么办？**  
A：AI会检测到你不再拥有该宠物，从而停止抚摸操作。  

**Q：这个功能在Polygon网络上可用吗？**  
A：不支持，仅在Base网络上可用。Aavegotchi已迁移至Base网络。  

**Q：如果AI停止抚摸宠物怎么办？**  
A：你可以随时撤销委托并手动抚摸宠物，没有任何风险！  

**Q：可以有多个操作员吗？**  
A：可以！你可以批准多个操作员。  

## 开发计划：  
**v1.0**（当前版本）：  
- ✅ 生成委托交易  
- ✅ 查看批准状态  
- ✅ 添加/移除被委托的钱包  
- ✅ 与Pet-Me-Master集成  

**v1.1**（即将推出）：  
- 🔜 为委托者提供Web界面  
- 🔜 实时抚摸通知  
- 🔜 按钱包记录宠物抚摸情况  
- 🔜 提供委托统计信息  

**v2.0**（未来版本）：  
- 🔮 为DAO提供批量委托功能  
- 🔮 设置定时抚摸计划  
- 🔮 多个操作员协同工作  
- 🔮 建立委托市场  

## 示例：  

### 用户想要委托：  
```
User: "I want AAI to pet my gotchis"

AAI: "👻 I can help you delegate petting rights!
     
     How many gotchis do you have?
     What's your wallet address?"

User: "I have 5 gotchis. Wallet: 0xABC..."

AAI: [Checks approval status]
     "❌ Not set up yet. Here's what you need to do:
     
     Execute this transaction via MEW:
     - To: 0xA99c...dBF
     - Amount: 0
     - Data: 0xcd675d57...
     
     [Sends detailed instructions]"

User: [Executes transaction]
     "Done! TX: 0x123..."

AAI: [Verifies approval]
     "✅ Approved! Fetching your gotchis..."
     [Adds to pet-me-master]
     "All set! I'll pet your 5 gotchis daily!
     Next pet: Tomorrow at 5:00 AM UTC"
```  

### 检查委托状态：  
```
User: "Am I delegated?"

AAI: [Checks isPetOperatorForAll]
     "✅ Yes! You delegated 5 gotchis to me.
     Last petted: 2 hours ago
     Next pet: in 10 hours"
```  

### 撤销委托：  
```
User: "Remove my gotchis from AAI"

AAI: "Sure! To revoke pet operator approval:
     
     Execute this transaction:
     - To: 0xA99c...dBF
     - Data: 0xcd675d57...0000  [approved=false]
     
     Want me to generate the full instructions?"

User: "Yes"

AAI: [Sends revoke transaction details]

User: [Executes]

AAI: "✅ Revoked! I can no longer pet your gotchis.
     Removed from my petting list."
```  

## 技术支持：  
- **问题反馈：** https://github.com/aaigotchi/pet-operator/issues  
- **集成说明：** 与Pet-Me-Master技能集成  
- **文档：** 本文件及Pet-Me-Master的SKILL.md文档  

---

**由AI 👻 用心制作**  
*委托抚摸权，保留所有权，双赢！*  
寻找更多宠物吧！ 🦞🚀  

---

## 如何撤销/解除委托  

**如果你想取消AI的抚摸权限：**  

**快速方法：**  
运行`remove-delegated-wallet.sh`脚本：  
```bash
./scripts/generate-revoke-tx.sh <YOUR_WALLET_ADDRESS>
```  

**手动方法：**  
执行以下交易（与委托操作相同，但将`approved`参数设置为`false`）：  
**交易详情：**  
- **收款方：`0xA99c4B08201F2913Db8D28e71d020c4298F29dBF`  
- **金额：`0` ETH**  
- **网络：Base（8453）**  
- **十六进制数据：**  
```
0xcd675d57000000000000000000000000b96b48a6b190a9d509ce9312654f34e9770f21100000000000000000000000000000000000000000000000000000000000000000
```  
（注意：`approved`参数应为`0`，表示撤销委托。）  

**通过MyEtherWallet操作：**  
1. 访问 https://www.myetherwallet.com/wallet/access  
2. 连接钱包  
3. 切换到Base网络  
4. 发送交易：  
   - **收款方：`0xA99c4B08201F2913Db8D28e71d020c4298F29dBF`  
   - **金额：`0` ETH**  
   - **附加数据：`0xcd675d57...0000`（交易参数）**  
5. 签名并发送交易！  

**通过Foundry Cast操作：**  
（具体操作方式请参考相关文档。）  

**撤销委托后的效果：**  
- AI将无法再抚摸你的宠物。  
- 你依然拥有100%的所有权。  
- 你可以随时重新委托。  
- AI会自动将你的宠物从抚摸列表中移除。  

**AI端处理：**  
当你撤销委托后，AI会通过链上验证立即停止抚摸操作，并从宠物管理列表中移除你的钱包信息。  

**你完全掌握控制权！** 🔓👻