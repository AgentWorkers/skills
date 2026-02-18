---
name: nihao
description: 使用 `nihao CLI` 设置并验证 Nostr 身份信息。该工具适用于创建新的 Nostr 密钥对/配置文件、审核现有 Npub 的健康状况，或帮助用户开始使用 Nostr。内容包括密钥对生成、配置文件元数据（类型 0）、中继列表（类型 10002）、关注列表（类型 3）、NIP-60 Cashu 钱包、NIP-05、Lightning 地址以及身份健康评分等功能的操作。
---
# nihao 👋

这是一个用于设置身份信息并进行健康检查的命令行工具（CLI）。它是一个单一的二进制文件，非交互式设计，适用于各种代理（agents）。

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

这个命令会完成以下操作：
1. 生成一对密钥（或使用 `--sec` 或 `--stdin` 来使用现有的密钥）
2. 发布个人资料元数据（类型 0）
3. 将中继列表（类型 10002）发布到默认的中继服务器
4. 发布关注列表（类型 3）
5. 设置 NIP-60 Cashu 钱包（类型 17375 和 10019）
6. 自动将用户地址设置为 `<npub>@npub.cash`
7. 发布一条带有 `#nihao` 标签的帖子

### 密钥参数说明

| 参数 | 作用 |
|---|---|
| `--name <name>` | 显示名称 |
| `--about <text>` | 个人简介 |
| `--picture <url>` | 个人资料图片链接 |
| `--banner <url>` | 横幅图片链接 |
| `--nip05 <user@domain>` | NIP-05 标识符 |
| `--lud16 <user@domain>` | Lightning 地址（默认：npub@npub.cash） |
| `--relays <r1,r2,...>` | 替换默认的中继服务器 |
| `--mint <url>` | 自定义 Cashu 钱包地址（可重复使用） |
| `--no-wallet` | 跳过 NIP-60 钱包设置 |
| `--sec <nsec>` | 使用现有的密钥 |
| `--stdin` | 从标准输入（stdin）读取密钥 |
| `--nsec-cmd <cmd>` | 将密钥存储委托给外部工具（例如 `pass`、`age`） |
| `--json` | 以 JSON 格式输出结果 |
| `--quiet` | 忽略所有非 JSON 格式的输出（包括错误信息） |

### 密钥存储

使用 `--nsec-cmd` 将密钥存储委托给密码管理工具。该工具会从标准输入（stdin）接收密钥，并在发布前进行验证；如果验证失败，`nihao` 会立即终止操作，不会发布任何信息。

示例：

```bash
nihao --name "mybot" --nsec-cmd "pass insert -e nostr/mybot"
nihao --name "mybot" --nsec-cmd "age -r age1... -o key.age"
```

## 检查现有身份信息

```bash
nihao check <npub> --json
```

该命令会检查并评估身份信息的健康状况（评分范围：0–8）：
- 个人资料元数据的完整性（名称、简介、图片、横幅）
- 图片的可用性（是否为 404 错误或来自 Blossom 服务器）
- NIP-05 标识符的验证（通过实时 HTTP 请求）
- Lightning 地址的可用性
- 中继列表（类型 10002）
- 关注列表（类型 3）
- NIP-60 钱包及地址的验证
- Nutzap 信息的完整性（类型 10019）

退出代码说明：
- `0`：身份信息健康
- `1`：发现问题

### JSON 输出格式

使用 `--json` 选项可以获取结构化的输出结果。设置命令的输出格式为 `{npub, nsec, pubkey, relays, profile, wallet}`；检查命令的输出格式为 `{npub, score, max_score, checks: [...]}`。

## 代理工作流程

```bash
# Create identity
nihao --name "mybot" --json --quiet > /tmp/nihao-result.json

# Verify identity health
nihao check npub1... --json --quiet
```

解析 JSON 输出结果，根据退出代码采取相应的操作。