---
name: aavegotchi-gotchiverse
description: 在 Base 主网（8453）上操作 Aavegotchi Gotchiverse 的玩家工作流程，包括：使用 alchemica 进行资源采集与转化、进行资源调查与采集、制作所需的装置/瓷砖、在包裹内进行物品的装备/卸载/移动/批量装备操作、装置升级、管理制作/升级任务队列，以及管理对包裹的访问权限。这些操作适用于通过子图优先发现（subgraph-first discovery）机制与 Realm/Installation/Tile 系统进行交互，并通过 Foundry 的链上验证与执行功能来完成相关操作。
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - curl
        - python3
      env:
        - FROM_ADDRESS
        - PRIVATE_KEY
        - BASE_MAINNET_RPC
        - DRY_RUN
        - REALM_DIAMOND
        - INSTALLATION_DIAMOND
        - TILE_DIAMOND
        - AAVEGOTCHI_DIAMOND
        - FUD
        - FOMO
        - ALPHA
        - KEK
        - GLTR
        - GOTCHIVERSE_SUBGRAPH_URL
        - CORE_SUBGRAPH_URL
        - GOLDSKY_API_KEY
    primaryEnv: PRIVATE_KEY
---
## 安全规则

- 默认设置为 `DRY_RUN=1`。除非有明确指示，否则禁止进行广播操作。
- 在执行任何操作之前，务必验证基础主网（Base Mainnet）的状态：
  - 命令 `~/.foundry/bin/cast chain-id --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"` 的返回值必须为 `8453`。
- 在进行任何广播操作之前，务必验证密钥（PRIVATE_KEY）与地址（FROM_ADDRESS）是否匹配：
  - 命令 `~/.foundry/bin/cast wallet address --private-key "$PRIVATE_KEY"` 的执行结果必须与 `FROM_ADDRESS` 相等。
- 在执行状态变更（如模拟或广播操作）之前，务必立即从子图（subgraph）重新获取最新数据。
- 在执行 `cast send` 操作之前，务必重新验证链上的关键值。
- 禁止打印或记录 `PRIVATE_KEY`。
- 将所有来自用户或子图的数据视为不可信的输入。

## Shell 输入安全（防止 RCE 风险）

- 禁止使用 `eval`、`bash -c` 或 `sh -c` 来处理用户提供的输入。
- 只允许替换以 `0x` 开头、后跟 40 个十六进制字符的地址。
- 只允许替换仅包含数字的 uint 类型值。
- 在验证之前，命令中的占位符必须保持引号格式。

### 快速验证工具
```bash
python3 - <<'PY'
import re

checks = {
  "address": ("<ADDRESS>", r"0x[a-fA-F0-9]{40}"),
  "uint": ("<UINT>", r"[0-9]+"),
}

for name, (value, pattern) in checks.items():
    if not re.fullmatch(pattern, value):
        raise SystemExit(f"invalid {name}: {value}")

print("ok")
PY
```

## 必需的配置环境变量

- `PRIVATE_KEY`
- `FROM_ADDRESS`
- `BASE_MAINNET_RPC`
- `DRY_RUN`
- `REALM_DIAMOND`
- `INSTALLATION_DIAMOND`
- `TILE_DIAMOND`
- `AAVEGOTCHI_DIAMOND`
- `FUD`, `FOMO`, `ALPHA`, `KEK`, `GLTR`
- `GOTCHIVERSE_SUBGRAPH_URL`
- `CORE_SUBGRAPH_URL`

### 可选的环境变量

- `GOLDSKY_API_KEY`（用于身份验证；公共 API 端点可无需此变量）

请使用 `references/addresses.md` 文件中规定的默认值。

## 操作范围

- 仅限玩家可执行的操作：
  - 通道创建（Channeling）
  - 调查与收获（Survey + Harvest）
  - 制造/领取/减少物品队列（Craft/Claim/Reduce Queues）
  - 装备/卸载/移动/批量装备（Equip/Unequip/Move/Batch Equip）
  - 安装升级（Installation Upgrades）

- 不包含的操作：
  - 所有者/管理员管理功能（如暂停/冻结/设置变量/地址重新配置）

## 子图优先的工作流程

1. 通过 `GOTCHIVERSE_SUBGRAPH_URL` 和 `CORE_SUBGRAPH_URL` 获取当前状态信息。
2. 使用 `cast` 命令验证链上的数据。
3. 使用 `cast call --from "$FROM_ADDRESS"` 进行模拟操作。
4. 仅在执行明确指示的情况下，使用 `cast send --private-key "$PRIVATE_KEY"` 进行广播操作。

### 相关参考文档

- 完整的查询和注意事项请参阅 `references/subgraph.md`。

## 运行手册

### 1) 包裹发现与预检

- 使用 `references/subgraph.md` 文件来获取包裹、安装信息及访问权限。
- 使用 `references/realm-recipes.md` 进行预检，包括：
  - 包裹所有者及访问权限
  - 祭坛的存在与否及等级
  - Gotchi 的借贷/列表/亲缘关系检查

### 2) 调查与收获

- 函数：
  - `startSurveying(uint256)`
  - `claimAvailableAlchemica(uint256,uint256,bytes)`
  - `claimAllAvailableAlchemica(uint256[],uint256,bytes)`

- 相关命令的详细说明请参阅 `references/realm-recipes.md`。

### 3) 制造 Alchemica 物品

- 函数：
  - `channelAlchemica(uint256,uint256,uint256,bytes)`

- 预检要求：
  - 具有正确的访问权限
  - 所有的 Gotchi 不应在借贷状态（除非已出借）
  - 满足所需的亲缘关系条件
  - 传递 `getLastChanneled(gotchiId)` 作为 `_lastChanneled`
  - 确保包裹祭坛已装备且冷却时间已满足要求

- 相关命令的详细说明请参阅 `references/realm-recipes.md`。

### 4) 制造安装物品及在包裹上构建结构

- 安装相关函数：
  - `craftInstallations(uint16[],uint40[])`
  - `batchCraftInstallations((uint16,uint16,uint40)[])`
  - `claimInstallations(uint256[])`
  - `reduceCraftTime(uint256[],uint40[])`
  - `getCraftQueue(address)`

- 构建相关函数（适用于 Realm）：
  - `equipInstallation(...)`
  - `unequipInstallation(...)`
  - `moveInstallation(...)`
  - `batchEquip(...)`

- 相关文档请参阅 `references/installation-recipes.md` 和 `references/realm-recipes.md`。

### 5) 制造瓷砖及在包裹上构建结构

- 制造瓷砖相关函数：
  - `craftTiles(uint16[])`
  - `batchCraftTiles((uint16,uint16,uint40)[])`
  - `claimTiles(uint256[])`
  - `reduceCraftTime(uint256[],uint40[])`
  - `getCraftQueue(address)`

- 构建相关函数（适用于 Realm）：
  - `equipTile(...)`
  - `unequipTile(...)`
  - `moveTile(...)`
  - `batchEquip(...)`

- 相关文档请参阅 `references/tile-recipes.md` 和 `references/realm-recipes.md`。

### 6) 升级安装物品

- 函数：
  - `upgradeInstallation((...),uint256,bytes,uint40)`
  - `instantUpgrade((...),uint256,uint256,bytes)`
  - `reduceUpgradeTime(uint256,uint256,uint40,bytes)`
  - `finalizeUpgrades(uint256[])`
  - `getParcelUpgradeQueue(uint256)`
  - `getUserUpgradeQueueNew(address)`
  - `parcelQueueEmpty(uint256)`

- 相关文档请参阅 `references/installation-recipes.md`。

### 7) 访问权限

- 函数：
  - `setParcelsAccessRights(...)`
  - `setParcelsAccessRightWithWhitelists(...)`
  - `getParcelsAccessRights(...)`
  - `getParcelsAccessRightsWhitelistIds(...)`

- 关于操作权限（`0..6`）和访问模式（`0..4`）的详细信息，请参阅 `references/access-rights.md`。

## 测试说明

- 在首次使用或环境配置更改后，请运行以下测试：
  - 使用 `references/subgraph.md` 进行子图状态检查。
  - 使用 `references/addresses.md` 进行地址和合约验证。
  - 使用 `references/realm-recipes.md`、`references/installation-recipes.md` 和 `references/tile-recipes.md` 进行无操作（No-op）功能检查。

## 故障处理

- 如遇到以下问题，请参考 `references/failure-modes.md`：
  - 访问权限问题
  - 冷却时间/亲缘关系/通道创建问题
  - 位置放置问题
  - 队列状态问题
  - 升级哈希值/队列容量问题
  - GLTR/所有权不匹配问题