---
name: gotchi-dao-voting
description: 查看当前活跃的 Aavegotchi DAO 提案，并通过 Bankr EIP-712 签名对相关提案进行投票。
homepage: https://github.com/aaigotchi/gotchi-dao-voting
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - jq
      env:
        - BANKR_API_KEY
---
# gotchi-dao-voting

用于对 `aavegotchi.eth` 的 Snapshot 提案进行投票。

## 脚本

- `./scripts/list-proposals.sh`  
  - 列出所有活跃的提案以及每个提案对应的投票结果（VP）。

- `./scripts/vote.sh [--dry-run] <proposal-id> <choice>`  
  - 通过 Snapshot 序列器提交已签名的投票结果。  
  - `--dry-run` 选项：仅打印输入的数据，不执行签名或提交操作。

## 投票格式

- 单选提案：使用数字表示，例如 `2`。  
- 权重提案：使用 JSON 对象字符串表示，例如 `{"2":2238}`。  
  - 如果仅输入 `2`，脚本会自动将其转换为 `{"2":<floor(vp)>}` 的格式。

## 配置文件（config.json）

配置文件中的关键字段：  
- `wallet`：钱包地址  
- `space`：投票间隔时间  
- `snapshotApiUrl`：Snapshot 服务的 API 地址  
- `snapshotSequencer`：用于提交投票的序列器地址  

## 安全性

- 使用 Bankr 签名 API 进行投票（无需使用本地私钥）。  
- 投票过程在链下进行（无需支付 Gas 费用）。  
- 对提案 ID、钱包地址、投票格式及可选选项范围进行严格验证。