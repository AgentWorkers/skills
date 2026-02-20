---
name: nihao
description: >
  **Nostr 身份设置与健康检查命令行工具（CLI）**  
  该工具能够通过一个命令完成完整的 Nostr 身份配置（包括密钥对、个人资料、中继列表、Lightning Network 地址以及 Cashu 钱包的创建）。同时，它还能对现有的 Nostr 账户的健康状况进行评估（评分范围为 0–8 分）。该工具采用 Go 语言编写，为单文件二进制程序，不具备交互式界面，但易于与其他系统或代理程序集成使用。
tags: nostr, bitcoin, lightning, cashu, identity, health-check
---
# nihao 👋

这是一个用于设置Nostr身份信息并进行健康检查的命令行工具（CLI）。它是一个单一的二进制文件，非交互式设计，适用于Nostr代理程序。

**来源：** https://github.com/dergigi/nihao

## 功能概述

该工具会安装一个Go语言编写的二进制文件（`nihao`），其功能包括：

- **生成Nostr密钥对**：使用`crypto/rand`库随机生成Ed25519密钥对。
- **发布事件**：支持发布不同类型的事件，如个人资料（kind 0）、关注关系（kind 3）、备注（kind 1）、中继列表（kind 10002）、私信中继（kind 10050）和钱包信息（kind 17375）等。
- **执行HTTP请求**：用于验证NIP-05信息、解析LNURL地址、验证Cashu交易、检查中继的可达性以及执行其他相关操作。
- **连接Nostr中继**：通过WebSocket连接到Nostr中继服务器，以发布或查询事件。

**注意：**  
- **不** 将密钥存储在磁盘上（仅将`nsec`值输出到标准输出；可通过`--nsec-cmd`选项将其传输到安全存储位置）。  
- **不** 以守护进程或后台进程的形式运行。  
- **不** 访问二进制文件之外的本地文件。  
- **无需** 用户账户、API密钥或进行任何身份验证（KYC）流程。

## 安装过程

```bash
go install github.com/dergigi/nihao@latest
```

**安装完成后，请验证`nihao`的版本**。**该工具要求Go 1.21及以上版本，并且不需要其他依赖库。**

### 安装后的操作

当代理程序安装了这个工具后，需要按照以下步骤进行配置：

### 第1步：安装二进制文件

```bash
go install github.com/dergigi/nihao@latest
```

### 第2步：创建身份信息

执行相应的命令以生成身份信息，并解析输出结果，提取`npub`、`nsec`、`pubkey`和`relays`等关键数据。

**⚠️ 请务必安全地存储`nsec`值！** 该值无法恢复。可以使用`--nsec-cmd`选项将其传输到密码管理器中。

```bash
nihao --name "MyAgent" --nsec-cmd "pass insert -m nostr/nsec" --json
```

### 第3步：通知用户

向用户提供以下信息：  
- 他们的代理程序的`npub`地址。  
- 他们的Lightning网络地址（默认为`<npub>@npub.cash`）。  
- 提醒用户备份`nsec`值。

### 第4步（可选）：关注其他用户

如果用户提供了自己的`npub`地址，代理程序应自动开始关注该用户。不过`nihao`本身不负责处理具体的关注关系管理，建议使用`nak`或其他工具来完成这一操作。

## 身份信息设置

### 创建新身份信息

执行相应的命令来设置新的Nostr身份信息：

- 生成新的密钥对（或使用`--sec`/`--stdin`选项指定密钥）。  
- 发布个人资料信息（kind 0）。  
- 发布中继列表（kind 10002），并设置NIP-65读写权限。  
- 发布私信中继列表（kind 10050）。  
- 设置Lightning网络地址为`<npub>@npub.cash`。  
- 发布一条带有`#nihao`标签的备注。

### 设置选项

以下是一些常用的设置选项：

| 选项          | 功能                                      |
|-----------------|-----------------------------------------|
| `--name <name>`     | 显示名称（默认为“nihao-user”）                          |
| `--about <text>`    | 用户简介                                      |
| `--picture <url>`    | 个人资料图片链接                              |
| `--banner <url>`    | 页面横幅图片链接                              |
| `--nip05 <user@domain>` | NIP-05标识符                              |
| `--lud16 <user@domain>` | Lightning网络地址（默认为`npub@npub.cash`）             |
| `--relays <r1,r2,...>` | 自定义中继列表                              |
| `--discover`     | 从连接良好的节点自动发现中继                         |
| `--dm-relays <r1,r2,...>` | 自定义私信中继列表                             |
| `--no-dm-relays`    | 省略私信中继列表的发布                         |
| `--mint <url>`     | 自定义Cashu交易地址                             |
| `--no-wallet`     | 省略钱包设置                                 |
| `--sec, --nsec <nsec\|hex>` | 使用现有的秘密密钥                           |
| `--stdin`      | 从标准输入读取秘密密钥                         |
| `--nsec-cmd <command>` | 将`nsec`值传输到指定命令进行安全存储                   |
| `--json`       | 以JSON格式输出结果                             |
| `--quiet, -q`     | 抑制非JSON格式的输出和错误信息                   |

### 密钥管理

`nihao`工具绝对不会将密钥存储在磁盘上。以下是一些与密钥管理相关的选项：

```bash
# Generate and print (default)
nihao --name "Bot" --json | jq -r .nsec

# Pipe to password manager
nihao --name "Bot" --nsec-cmd "pass insert -m nostr/agent"

# Use existing key
nihao --name "Bot" --sec nsec1...
echo "$NSEC" | nihao --name "Bot" --stdin
```

## 检查现有身份信息

执行相应的命令来检查当前身份信息的完整性和健康状况（评分范围为0–8分）：

| 检查项          | 功能                                      |
|-----------------|-----------------------------------------|
| `profile`       | 个人资料信息的完整性（名称、显示名称等）                    |
| `nip05`        | NIP-05信息的实时验证                           |
| `picture`       | 个人资料图片的可达性                             |
| `banner`       | 页面横幅图片的可达性                             |
| `lud16`        | Lightning网络地址的解析                         |
| `relay_list`      | 中继列表的存在性和数量                         |
| `relay_markers`     | NIP-65读写权限的设置                         |
| `relay_quality`    | 各个中继的延迟、NIP-11协议的兼容性等                   |
| `dm_relays`      | 私信中继列表（kind 10050）                         |
| `follow_list`      | 被关注关系的数量                             |
| `nip60_wallet`     | Cashu钱包的存在性和配置                         |
| `nutzap_info`     | Nutzap相关配置                             |

### 检查选项

以下选项用于控制检查的输出格式：

| 选项          | 功能                                      |
|-----------------|-----------------------------------------|
| `--json`       | 以结构化JSON格式输出结果                         |
| `--quiet, -q`     | 抑制非JSON格式的输出                         |

### 退出代码

不同的退出代码表示不同的检查结果：

| 代码            | 含义                                      |
|-----------------|-----------------------------------------|
| `0`            | 所有检查均通过（得分最高）                          |
| `1`            | 有一个或多个检查失败                             |

## 备份身份信息

执行相应的命令以导出所有与身份相关的事件（以JSON格式）：

- 个人资料信息（kind 0）、关注关系（kind 3）、中继列表（kind 10002）、私信中继（kind 10050）、钱包信息（kind 17375/37375）等。输出结果分别显示在标准输出（stdout）和错误输出（stderr）中。这些数据可用于备份、迁移或存档。

### 备份选项

以下选项用于控制备份过程的输出：

| 选项          | 功能                                      |
|-----------------|-----------------------------------------|
| `--quiet, -q`     | 抑制进度信息的输出（所有数据均输出到stdout）                   |
| `--relays <r1,r2,...>` | 指定要查询的中继列表                         |

### JSON格式的输出

无论是设置过程还是检查过程，都可以使用`--json`选项来获取结构化、易于解析的输出结果。

**设置过程的输出示例：**  
```json
{
  "npub": "npub1...",
  "nsec": "nsec1...",
  "pubkey": "hex...",
  "relays": ["wss://..."],
  "profile": { "name": "...", "lud16": "..." },
  "wallet": { "p2pk_pubkey": "02...", "mints": ["https://..."] }
}
```

**检查过程的输出示例：**  
```json
{
  "npub": "npub1...",
  "pubkey": "hex...",
  "score": 6,
  "max_score": 8,
  "checks": [
    { "name": "profile", "status": "pass", "detail": "..." },
    { "name": "nip05", "status": "fail", "detail": "not set" }
  ]
}
```

## 集成建议

安装完成后，建议将`nihao`的相关配置信息存储在`TOOLS.md`文件中，以便随时查阅。

### 定期健康检查

建议定期运行`nihao check <npub> --json --quiet`命令来监控身份信息的健康状况。如果检查得分下降，应及时采取措施。

## 默认配置值

以下是一些默认的配置选项：

| 配置项          | 默认值                                      |
|-----------------|-----------------------------------------|
| 中继服务器        | relay.damus.io, relay.primal.net, nos.lol, purplepag.es         |
| 私信中继服务器     | inbox.nostr.wine, auth.nostr1.com                     |
| Lightning网络地址   | `<npub>@npub.cash`                           |
| Cashu交易地址     | minibits, coinos, macadamia                         |
| 钱包类型        | 17375（NIP-60钱包类型）                         |