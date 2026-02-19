---
name: nihao
description: 通过一个命令即可实现自我主权的身份认证以及不可阻挡的资金流动。使用 “nihao” 命令，可以为任何代理或用户提供完整的 Nostr 身份信息：包括密钥对、个人资料、中继列表、Lightning Network 地址以及 Cashu 电子钱包。整个过程无需创建任何账户或 API 密钥，也无需进行任何身份验证（KYC）流程。此外，该工具还能对现有的 NoPub 账户状态进行审计，评分范围为 0-8 分，评估内容涵盖个人资料、NIP-05 信息、Lightning Network 使用情况、中继节点状态以及 NIP-60 钱包的运行状况。
---
# nihao 👋

这是一个用于设置Nostr身份信息并进行健康检查的命令行工具（CLI）。它是一个单一的二进制文件，非交互式设计，适用于各种代理（agents）。

来源：https://github.com/dergigi/nihao

## 安装

```bash
go install github.com/dergigi/nihao@latest
```

验证安装结果：`nihao version`

## 设置新身份信息

```bash
nihao --name "AgentName" --about "I do things" --json
```

该命令会执行以下操作：
1. 生成一对Nostr密钥对
2. 发布个人资料元数据（类型0）
3. 发布中继列表（类型10002）
4. 发布关注列表（类型3）
5. 设置NIP-60 Cashu钱包
6. 将Lightning地址设置为`<npub>@npub.cash`
7. 发布一条带有`#nihao`标签的帖子

### 命令参数（Flags）

| 参数 | 用途 |
|---|---|
| `--name <name>` | 显示名称 |
| `--about <text>` | 个人简介 |
| `--picture <url>` | 个人资料图片URL |
| `--banner <url>` | 横幅图片URL |
| `--nip05 <user@domain>` | NIP-05标识符 |
| `--lud16 <user@domain>` | Lightning地址（默认值：npub@npub.cash） |
| `--relays <r1,r2,...>` | 替换默认的中继服务器 |
| `--mint <url>` | 自定义Cashu mint地址（可重复使用） |
| `--no-wallet` | 跳过钱包设置 |
| `--json` | 以JSON格式输出结果 |
| `--quiet` | 抑制非JSON格式的输出 |

### 密钥管理

`nihao`支持使用`--nsec-cmd`参数将密钥存储委托给密码管理工具（如`pass`或`age`）。详情请参阅项目README：https://github.com/dergigi/nihao#key-management

## 检查现有身份信息

```bash
nihao check npub1... --json
```

该命令会检查并评估现有身份信息的健康状况（评分范围：0–8）：
- 个人资料元数据的完整性（名称、简介、图片、横幅）
- 图片的可用性（是否能够正常显示，以及是否托管在Blossom平台上）
- NIP-05标识符的验证（通过实时HTTP请求）
- Lightning地址的可用性（是否能够解析为LNURL）
- 中继列表的完整性（类型10002）
- 关注列表的准确性
- NIP-60钱包和mint地址的有效性
- Nutzap信息的准确性（类型10019）

退出代码说明：
- `0`：身份信息健康
- `1`：发现问题

## JSON格式的输出

使用`--json`参数可获取结构化输出结果。请解析输出内容并根据退出代码采取相应措施。