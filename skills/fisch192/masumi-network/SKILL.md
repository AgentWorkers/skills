---
name: masumi-network
description: Masumi Network 提供的技能用于保修金库的验证。该技能支持 OCR 技术进行收据扫描、记录 Cardano 区块链上的购买证明、处理不可更改的决策记录、实现代理之间的协作机制以及支持智能钱包的支付功能。它可以应用于保修申请处理、产品验证、代理之间的服务费用结算，以及在 Cardano 上生成不可篡改的审计记录。
---

# Masumi Network 保修服务

## 快速入门
运行以下脚本以实现核心功能：
- `scripts/register-agent.py` – 注册 Franz AI 代理
- `scripts/verify-warranty.py --receipt "保修文本"` – 验证保修单
- `scripts/collaborate.py` – 寻找合作伙伴

## 工作流程：
1. 使用 OCR 技术扫描保修单并提取数据
2. 生成证明哈希值（proof-hash）
3. 将相关记录记录到 Cardano 区块链中
4. 通过智能钱包收取费用

详细端点信息请参阅 `references/api.md`。

## 盈利模式：
- 每次验证操作收取 1% 的费用
- 将处理后的数据发布到 ClawHub 平台以获得被动收入