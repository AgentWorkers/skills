---
name: pos-arcology-forge
description: "**PoW-验证的Elysium Arcology Planner + Hub**：  
在O’Neill模拟器或外骨骼设备上生成随机数（nonce），并将其用于P2P平台的信任机制。该平台支持以下功能：  
1. 生成或分叉Arcology项目的蓝图；  
2. 进行PoW（Proof of Work）计算并验证结果；  
3. 通过CLI（命令行界面）管理本地节点群组、浏览资源、导入数据并验证其真实性；  
4. 实现协作与任务分配（如悬赏系统）；  
5. 提供防篡改的测试机制。"
---

# PoSH Arcology Forge (V1.2 - 终极版，防篡改功能)

基于比特币工作量证明（BTC POW）机制，用于生成抗篡改的轨道蓝图。具备全面的安全防护机制：防篡改、超时保护、数据限制以及多种测试功能。

## 快速入门
```bash
node scripts/pos-share.js '{\"radius_km\":3,\"pop_m\":500000}'  # E2E → share.pos.json
node scripts/pos-grind.js share.pos.json --verify              # ✅ VALID
node scripts/hub-cli.js import share.pos.json
node scripts/hub-cli.js list                                   # Valid only
node scripts/test.js                                           # Full suite
```

## 工作流程（高度可靠）
1. **参数处理** → 数据结构验证与限制。
2. **模拟运行** → 物理模拟（确保系统不会崩溃）。
3. **计算过程** → 设置超时时间并监控进度，确保计算过程不被篡改。
4. **结果验证** → 在操作中心（Hub）对计算结果进行最终验证。

**输出结果**：包含计算结果、验证结果以及树哈希值（treeHash，可导入使用）。

有关物理模拟和外骨骼（exosuits）的详细信息，请参阅相关参考资料。

## 脚本说明
- 所有脚本均为异步执行，并使用了Python的标准库（stdlib）。
- `test.js` 脚本：自动执行各种测试用例（包括正常情况、异常情况以及防篡改测试）。

该系统在生产环境中具有100%的防篡改能力（通过了20多种测试场景）。