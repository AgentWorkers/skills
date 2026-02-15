---
name: sui-move
description: Sui区块链与Move智能合约开发：当用户询问有关Sui平台、Move编程语言、智能合约、数据对象、交易机制或Sui上的区块链开发相关内容时，可参考此文档。
version: 1.1.0
metadata:
  author: EasonClawdbot1
  tags: sui, move, blockchain, smart-contract, web3
  requires:
    bins: [sui, rg]
  install:
    - id: sui-cli
      kind: brew
      formula: sui
      bins: [sui]
      label: Install Sui CLI (brew)
---

# Sui Move 开发

这是一个关于 Sui 区块链和 Move 智能合约开发的综合性知识库。

**GitHub:** <https://github.com/EasonC13-agent/sui-skills/tree/main/sui-move>

## 设置参考

克隆官方文档：

```bash
# Create skill directory
mkdir -p {baseDir}/references && cd {baseDir}/references

# Clone Move Book (The Move Language Bible)
git clone --depth 1 https://github.com/MystenLabs/move-book.git

# Clone Sui docs (sparse checkout)
git clone --depth 1 --filter=blob:none --sparse https://github.com/MystenLabs/sui.git
cd sui && git sparse-checkout set docs

# Clone Awesome Move (curated examples and resources)
# Note: Some code examples may be outdated
git clone --depth 1 https://github.com/MystenLabs/awesome-move.git
```

## 其他资源

### Awesome Move (`references/awesome-move/`)
这是一个精选的 Move 资源列表，包括：
- 示例项目和代码片段
- 库和框架
- 工具和实用程序
- 学习资源

⚠️ **注意**：由于 Move 语言和 Sui 平台的更新，awesome-move 中的一些代码示例可能会过时。请始终参考最新的 Move 官方文档和 Sui 文档。

## 参考结构

### Move 官方文档 (`references/move-book/book/`)
| 目录 | 内容 |
|-----------|---------|
| `your-first-move/` | “Hello World” 和 “Hello Sui” 教程 |
| `move-basics/` | 变量、函数、结构体、能力（abilities）、泛型（generics） |
| `concepts/` | 包（packages）、清单（manifest）、地址（addresses）、依赖关系（dependencies） |
| `storage/` | 对象存储（object storage）、UID（Unique Identifier）、转账函数（transfer functions） |
| `object/` | 对象模型（object model）、所有权（ownership）、动态字段（dynamic fields） |
| `programmability/` | 事件（events）、见证者（witnesses）、发布者（publishers）、显示功能（display） |
| `move-advanced/` | BCS（Blockchain Contract Storage）、PTB（Programmable Transfer Block）机制、加密技术（cryptography） |
| `guides/` | 测试（testing）、调试（debugging）、升级（upgrades）、BCS 相关内容 |
| `appendix/` | 术语表（glossary）、保留地址（reserved addresses） |

### Sui 官方文档 (`references/sui/docs/content/`)
- 概念（concepts）、指南（guides）、标准（standards）、参考资料（references）

## 快速搜索

```bash
# Search Move Book for a topic
rg -i "keyword" {baseDir}/references/move-book/book/ --type md

# Search Sui docs
rg -i "keyword" {baseDir}/references/sui/docs/ --type md

# Find all files about a topic
find {baseDir}/references -name "*.md" | xargs grep -l "topic"
```

## 关键概念

### Move 语言基础

**能力（Abilities）** - 对象的操作能力：
- `copy` - 可以被复制
- `drop` - 可以被销毁
- `store` - 可以存储在对象中
- `key` - 可以作为全局存储（对象）中的键使用

```move
public struct MyStruct has key, store {
    id: UID,
    value: u64
}
```

**对象模型（Object Model）**：
- 每个对象都有一个唯一的 `UID`（Unique Identifier）
- 对象可以被拥有（owned）、共享或设置为不可变（immutable）
- 转账函数：`transfer::transfer`、`transfer::share_object`、`transfer::freeze_object`

### 常见模式

**创建和转移对象（Create and Transfer Objects）**：
```move
public fun create(ctx: &mut TxContext) {
    let obj = MyObject {
        id: object::new(ctx),
        value: 0
    };
    transfer::transfer(obj, tx_context::sender(ctx));
}
```

**共享对象（Shared Objects）**：
```move
public fun create_shared(ctx: &mut TxContext) {
    let obj = SharedObject {
        id: object::new(ctx),
        counter: 0
    };
    transfer::share_object(obj);
}
```

**入口函数（Entry Functions）**：
```move
public entry fun do_something(obj: &mut MyObject, value: u64) {
    obj.value = value;
}
```

## 命令行界面（CLI）命令

```bash
# Create new project
sui move new my_project

# Build
sui move build

# Test
sui move test

# Publish
sui client publish --gas-budget 100000000

# Call function
sui client call --package <PACKAGE_ID> --module <MODULE> --function <FUNCTION> --args <ARGS>

# Get object
sui client object <OBJECT_ID>
```

## 工作流程

在回答关于 Sui/Move 的问题时，请按照以下步骤操作：

1. **首先搜索相关参考资料**：
   ```bash
   rg -i "topic" {baseDir}/references/move-book/book/ -l
   ```

2. **阅读相关文档**：
   ```bash
   cat {baseDir}/references/move-book/book/<path>/<file>.md
   ```

3. **提供来自参考资料的代码示例**：

4. **在必要时提供官方文档的链接**：
   - Move 官方文档：https://move-book.com
   - Sui 官方文档：https://docs.sui.io

## 主题索引

| 主题 | 文档位置 |
|-------|----------|
| “Hello World” | `move-book/book/your-first-move/hello-world.md` |
| “Hello Sui” | `move-book/book/your-first-move/hello-sui.md` |
| 原始类型（Primitives） | `move-book/book/move-basics/primitive-types.md` |
| 结构体（Structs） | `move-book/book/move-basics/struct.md` |
| 能力（Abilities） | `move-book/book/move-basics/abilities-introduction.md` |
| 泛型（Generics） | `move-book/book/move-basics/generics.md` |
| 对象模型（Object Model） | `move-book/book/object/` |
| 存储（Storage） | `move-book/book/storage/` |
| 事件（Events） | `move-book/book/programmability/events.md` |
| 测试（Testing） | `move-book/book/guides/testing.md` |
| 升级（Upgrades） | `move-book/book/guides/upgradeability.md` |
| PTB（Programmable Transfer Block） | `move-book/book/move-advanced/ptb/` |
| BCS（Blockchain Contract Storage） | `move-book/book/move-advanced/bcs.md` |

## 相关技能

本技能属于 Sui 开发技能套件的一部分：

| 技能 | 描述 |
|-------|-------------|
| [sui-decompile](https://clawhub.ai/EasonC13/sui-decompile) | 获取并阅读链上合约的源代码 |
| **sui-move** | 编写和部署 Move 智能合约 |
| [sui-coverage](https://clawhub.ai/EasonC13/sui-coverage) | 使用安全分析工具进行测试覆盖率评估 |
| [sui-agent-wallet](https://clawhub.ai/EasonC13/sui-agent-wallet) | 构建和测试 DApp 的前端界面 |

**工作流程**：
```
sui-decompile → sui-move → sui-coverage → sui-agent-wallet
    Study        Write      Test & Audit   Build DApps
```

所有技能的详细信息请查看：<https://github.com/EasonC13-agent/sui-skills>

## 注意事项

- Move 2024 版本引入了新特性（如枚举类型、方法语法等）
- Sui 采用了一种以对象为中心的独特模型，与其他区块链不同
- 在 Sui 中，交易费用以 SUI 代币支付
- 提供了测试网（Testnet）和开发网（Devnet）用于开发工作