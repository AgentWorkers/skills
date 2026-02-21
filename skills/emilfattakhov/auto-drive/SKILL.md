---
name: auto-drive
description: 通过 Auto-Drive 将文件上传和下载到 Autonomys Network 的永久性去中心化存储系统中。将记忆数据以链表的形式保存下来，以便日后恢复；只需一个 CID（Content Identifier）即可重新构建完整的代理上下文（agent context）。
metadata:
  openclaw:
    emoji: "🧬"
    requires:
      bins: ["curl", "jq", "file"]
      env: ["AUTO_DRIVE_API_KEY"]
    install:
      - id: jq-brew
        kind: brew
        formula: jq
        bins: ["jq"]
        label: "Install jq (brew)"
---
# 自动驱动技能（Auto-Drive Skill）

该技能利用Autonomys网络的去中心化存储功能，并通过链表结构来保存代理（agent）的状态数据，以实现数据的永久保存和快速恢复。

## 该技能的功能

1. **上传文件**到Autonomys网络，并获取一个CID（内容标识符）——这是一个在Autonomys分布式存储网络中永久且不可变的地址。
2. **使用CID从Autonomys下载文件**——如果设置了API密钥，则会使用认证后的API进行下载；否则会通过公共网关下载文件。
3. **将状态数据保存为链表**：每个状态记录都包含一个JSON格式的数据条目，以及一个`header.previousCid`指针，这些数据条目会被永久地存储在链表中。
4. **从链表中恢复数据**：通过提供最新的CID，可以逆序遍历链表，从而重建代理的全部状态历史记录。

## 适用场景

- 当用户执行“将此文件保存到Autonomys”或“上传到Autonomys”或“永久存储”等操作时。
- 当用户需要从Autonomys下载文件或提供CID以获取文件内容时。
- 当用户执行“保存状态数据”、“永久记录此信息”或“创建检查点”等操作时。
- 当用户需要“恢复数据”、“调用链表记录”、“重建状态数据”或“加载历史记录”等操作时。
- 任何希望将数据永久且不可变地存储在去中心化网络中的场景。

## 配置要求

### API密钥（API Key）

需要一个`AUTO_DRIVE_API_KEY`。代理（agent）可以在[ai3.storage](https://ai3.storage)获取免费的API密钥：

1. 访问https://ai3.storage
2. 使用**Google**或**GitHub**进行登录（单点登录）
3. 在左侧导航栏中选择**Developers**
4. 点击**Create API Key**

可以通过环境变量或OpenClaw配置来设置API密钥：

- **环境变量：**`export AUTO_DRIVE_API_KEY=your_key_here`
- **OpenClaw配置：**`skills.entries.auto-drive.apiKey`

API密钥用于上传文件、保存状态数据以及恢复状态链。对于普通文件下载来说，API密钥是可选的；如果没有API密钥，系统会使用公共网关进行下载，但下载到的文件将保持压缩状态（压缩文件不会被解压）。

## 核心操作

### 上传文件（Upload a File）

```bash
scripts/autodrive-upload.sh <filepath> [--json] [--compress]
```

使用三步上传协议将文件上传到Autonomys主网（单次上传整个文件）。上传成功后，API会返回CID。
- `--json`：强制将文件格式设置为`application/json`。
- `--compress`：启用ZLIB压缩。

### 下载文件（Download a File）

```bash
scripts/autodrive-download.sh <cid> [output_path]
```

根据CID下载文件。如果设置了`AUTO_DRIVE_API_KEY`，则会使用认证后的API进行下载（服务器端会解压文件）；否则会通过公共网关下载文件（下载到的文件将保持压缩状态）。如果省略了`output_path`参数，文件将输出到标准输出（stdout）。

### 保存状态数据（Save a Memory Entry）

```bash
scripts/autodrive-save-memory.sh <data_file_or_string> [--agent-name NAME] [--state-file PATH]
```

使用Autonomys代理的状态数据结构（header/data）来保存状态数据：

```json
{
  "header": {
    "agentName": "my-agent",
    "agentVersion": "1.0.0",
    "timestamp": "2026-02-14T00:00:00.000Z",
    "previousCid": "bafk...or null"
  },
  "data": {
    "type": "memory",
    "content": "..."
  }
}
```

- 如果第一个参数是文件路径，文件的内容将作为`data`字段保存。
- 如果第一个参数是普通字符串，系统会将其封装成`{"type": "memory", "content": "..."}`的形式。
- `--agent-name`：设置代理的名称（默认值为`openclaw-agent`或`$AGENT_NAME`）。
- `--state-file`：指定状态文件的路径。

数据上传完成后，系统会更新状态文件，并将最新的CID保存到`MEMORY.md`文件中（如果该文件已存在的话）。同时，最新的CID也会被保存到`MEMORY.md`文件中。

### 恢复全部状态数据（Recall the Full Chain）

```bash
scripts/autodrive-recall-chain.sh [cid] [--limit N] [--output-dir DIR]
```

如果未提供CID，系统会从状态文件中读取最新的CID，然后从最新记录开始逆序遍历链表，将每个状态记录以JSON格式输出。

- `--limit N`：指定要恢复的最大记录数（默认值为50条）。
- `--output-dir DIR`：将每个状态记录保存为带编号的JSON文件，而不是输出到标准输出。

系统同时支持`header.previousCid`（Autonomys代理的格式）和根级别的`previousCid`，以保持向后兼容性。

这就是所谓的“恢复机制”：新的代理实例只需提供一个CID，就可以重建其全部的状态数据。

## 恢复数据的原理

每个保存的状态数据都会获得一个唯一的CID，并且这个CID会指向前一个状态数据的CID。因此，当代理的服务器崩溃时，新的代理实例只需提供最后一个CID，就可以恢复所有状态数据。这种机制类似于版本控制，所有数据都会被永久地存储在Autonomys网络上。

## 使用示例

- 用户：“将我的报告上传到Autonomys。” → 运行`scripts/autodrive-upload.sh /path/to/report.pdf`，然后获取CID和文件下载链接。
- 用户：“压缩后上传文件。” → 运行`scripts/autodrive-upload.sh /path/to/data.json --json --compress`。
- 用户：“保存关于选择React作为前端框架的决策。” → 运行`scripts/autodrive-save-memory.sh "Decision: using React for frontend. Reason: team familiarity and component reuse."`。
- 用户：“保存一个结构化的数据记录。” → 创建一个JSON文件，然后运行`scripts/autodrive-save-memory.sh /tmp/milestone.json --agent-name my-agent`。
- 用户：“恢复我的状态数据链。” → 运行`scripts/autodrive-recall-chain.sh`，显示从初始状态到当前状态的全部历史记录。
- 用户：“从Autonomys下载文件bafk...abc。” → 运行`scripts/autodrive-download.sh bafk...abc ./downloaded_file`。

## 重要注意事项

- 存储在Autonomys上的所有数据默认都是**永久且公开的**。请勿存储敏感信息（如密码、私钥或个人隐私数据）。
- 免费API密钥在主网上的上传流量限制为每月20MB。下载流量不受限制。可以通过`GET /subscriptions/credits`查询剩余的下载次数。
- 上传文件、保存状态数据或恢复状态数据都需要API密钥。如果没有API密钥，可以使用公共网关进行下载，但压缩文件将不会被解压。
- 状态文件会记录`lastCid`、`lastUploadTimestamp`和`chainLength`等信息。请备份`lastCid`，因为它是一个重要的恢复关键。
- 文件是分块上传的。免费账户的每月20MB上传限制实际上是针对单个文件的限制，请确保每次上传的文件大小控制在20MB以内，以节省费用。
- 任何文件的公共网关地址为：`https://gateway.autonomys.xyz/file/<CID>`。
- 为了实现更高的恢复韧性，可以考虑通过Autonomys的EVM将最新的CID锚定到链表中，这样即使不记录链表的头部CID，也能实现数据的恢复。有关实现示例，请参考[openclaw-memory-chain](https://github.com/autojeremy/openclaw-memory-chain)。