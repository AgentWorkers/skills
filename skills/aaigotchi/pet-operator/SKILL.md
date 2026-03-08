---
name: pet-operator
description: 将 Aavegotchi 的“抚摸”（petting）权限委托给 AAI 的钱包（位于 Base 平台上）。生成用于批准/撤销操作的交易数据（tx data），检查审批结果，并在 pet-me-master 配置文件中维护被委托钱包的账务记录。
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
---
# pet-operator

用于设置或撤销用户钱包的AAI（人工智能）操作权限，并确保委托记录的一致性。

## 常量

- AAI操作员钱包地址：`0xb96B48a6B190A9d509cE9312654F34E9770F2110`
- Aavegotchi Diamond地址：`0xA99c4B08201F2913Db8D28e71d020c4298F29dBF`
- 链路：Base主网（`8453`）
- RPC默认地址：`https://mainnet.base.org`

可覆盖的环境变量：
- `AAVEGOTCHI_DIAMOND`
- `AAI_OPERATOR`
- `BASE_RPC_URL`
- `PET_ME_CONFIG_FILE`

## 脚本

- `./scripts/check-approval.sh <wallet>`
  - 检查`isPetOperatorForAll(owner, operator)`函数的结果。
- `./scripts/generate-delegation-tx.sh <wallet>`
  - 生成用于`setPetOperatorForAll(AAI_operator, true)`的调用数据。
- `./scripts/generate-revoke-tx.sh <wallet>`
  - 生成用于`setPetOperatorForAll(AAI_operator, false)`的调用数据。
- `./scripts/add-delegated-wallet.sh <wallet> [name]`
  - 验证用户授权，获取用户拥有的Aavegotchi ID，并将其添加到`pet-me-master`配置文件中。
- `./scripts/remove-delegated-wallet.sh <wallet>`
  - 从配置文件中删除用户的委托记录。

## 配置记录

`add-delegated-wallet.sh`脚本会写入以下文件：
- `.delegatedWallets`（推荐使用）
- `.wallets`（仅用于兼容旧版本）

请注意：此脚本本身不会授予链上的权限；必须先获得链上的批准才能生效。

## 安全性

- 操作员权限仅允许执行“宠物操作”（petting），不允许资产转移。
- 用户始终保留资产的所有权。
- 撤销操作只需通过一条链上交易即可完成。