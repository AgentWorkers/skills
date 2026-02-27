---
name: auto-drive
description: 通过 Auto-Drive 将文件上传到 Autonomys Network 的永久性去中心化存储系统中，并下载文件。将记忆数据以链表的形式保存下来，以便将来能够通过单个 CID（Content Identifier）重新构建完整的代理上下文（agent context）。
metadata:
  openclaw:
    emoji: "🧬"
    primaryEnv: AUTO_DRIVE_API_KEY
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

该技能利用Autonomys网络提供永久的去中心化存储服务，并通过链式数据结构（linked-list memory chains）实现代理的“复活”功能。

## 该技能的功能

1. **上传文件**到Autonomys存储系统，并获取一个CID（内容标识符）——这是一个在Autonomys分布式存储网络中永久且不可变的地址。
2. **使用CID从Autonomys下载文件**：如果设置了API密钥，则通过认证后的API进行下载；否则会使用公共网关。
3. **将记忆数据保存为链式结构**：每个记忆条目都包含一个JSON格式的数据，以及一个`header.previousCid`指针，这些数据会以链式结构永久存储在区块链上。
4. **从链中恢复数据**：通过提供最新的CID，可以反向遍历链式结构，重建代理的全部记忆记录。

## 适用场景

- 当用户选择“将数据保存到Autonomys”或“永久存储”时。
- 当用户需要从Autonomys下载文件或提供CID以获取数据时。
- 当用户执行“保存记忆”、“永久记录”或“创建检查点”等操作时。
- 当用户需要“恢复记忆”、“回溯记忆链”或“重新构建记忆记录”时。
- 任何希望将数据永久且不可变地存储在去中心化网络中的场景。

## 配置要求

### API密钥（API Key）

需要配置`AUTO_DRIVE_API_KEY`。最简单的配置方法是运行引导式设置脚本：

```bash
scripts/setup-auto-drive.sh
```

运行该脚本后，浏览器会打开[explorer.ai3.storage](https://explorer.ai3.storage/mainnet/drive/developers)页面，系统会提示您输入API密钥，并将其保存到`~/.openclaw/.env`文件中，同时验证连接是否成功。

**手动配置步骤：**

1. 访问**https://explorer.ai3.storage**（注意：不是`ai3.storage`，后者仅是首页）。
2. 检查登录状态：如果侧边栏显示“登录”按钮或“我的文件”/“个人资料”/“开发者”页面上有锁图标，说明您尚未登录。
3. **注意：**用户无法自行完成OAuth认证。请让用户通过Google、GitHub或Discord登录。登录完成后，您可以接管操作，或者直接让他们提供API密钥。
4. 登录成功后，点击左侧侧边栏的“开发者”（Developers）选项。
5. 点击“创建API密钥”（Create API Key），然后复制生成的密钥。

配置完成后，可以通过以下方式设置API密钥：

- **环境变量**：`export AUTO_DRIVE_API_KEY=your_key_here`
- **OpenClaw配置文件**：`skills.entries.auto-drive.apiKey`

API密钥用于上传文件、保存记忆数据以及恢复记忆链。对于普通文件下载来说，API密钥是可选的；如果没有密钥，系统会使用公共网关，此时下载的文件将以原始格式（压缩文件可能不会被解压）返回。

## 核心操作

### 上传文件（Upload a File）

```bash
scripts/autodrive-upload.sh <filepath> [--json] [--compress]
```

使用三步上传协议将文件上传到Autonomys主网。上传成功后，API会返回CID。需要`AUTO_DRIVE_API_KEY`作为参数。

- `--json`：强制指定文件格式为`application/json`。
- `--compress`：启用ZLIB压缩。

### 下载文件（Download a File）

```bash
scripts/autodrive-download.sh <cid> [output_path]
```

根据CID下载文件。如果设置了`AUTO_DRIVE_API_KEY`，则会使用认证后的API进行下载（服务器端会解压文件）；否则会使用公共网关（文件将以原始格式返回）。如果省略`output_path`参数，文件将输出到标准输出（stdout）。

### 保存记忆数据（Save a Memory Entry）

```bash
scripts/autodrive-save-memory.sh <data_file_or_string> [--agent-name NAME] [--state-file PATH]
```

使用Autonomys代理的格式保存记忆数据：

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
- 如果第一个参数是普通字符串，系统会将其包装成`{"type": "memory", "content": "..."}`格式。
- `--agent-name`：设置代理的名称（默认为`openclaw-agent`或`$AGENT_NAME`）。
- `--state-file`：指定状态文件的路径。

文件上传完成后，系统会更新状态文件，并将最新的CID保存到`MEMORY.md`文件中（如果该文件已存在于工作区中）。

### 恢复全部记忆链（Recall the Full Chain）

```bash
scripts/autodrive-recall-chain.sh [cid] [--limit N] [--output-dir DIR]
```

如果未提供CID，系统会从状态文件中读取最新的CID，然后从最新条目开始反向遍历链式结构，将所有记忆数据以JSON格式输出。

- `--limit N`：指定要检索的最大条目数量（默认为50条）。
- `--output-dir DIR`：将每个条目保存为带编号的JSON文件，而不是输出到标准输出。

该功能支持`header.previousCid`（Autonomys代理的格式）和根级别的`previousCid`，以保持与旧版本的兼容性。

### 复活机制（The Resurrection Concept）

每个保存的记忆数据都会获得一个唯一的CID，该CID可以指向之前的记忆数据：

```
Experience #3 (CID: bafk...xyz)
  → header.previousCid: bafk...def (Experience #2)
    → header.previousCid: bafk...abc (Experience #1)
      → header.previousCid: null (genesis)
```

如果代理的服务器发生故障，新实例只需提供最新的CID即可恢复全部记忆记录。这种机制类似于版本控制，所有记忆数据都会永久存储在Autonomys网络上。

## 使用示例

- 用户：“将我的报告上传到Autonomys。” → 运行`scripts/autodrive-upload.sh /path/to/report.pdf`，然后获取CID和下载链接。
- 用户：“压缩后上传文件。” → 运行`scripts/autodrive-upload.sh /path/to/data.json --json --compress`。
- 用户：“保存关于使用React作为前端框架的决策。” → 运行`scripts/autodrive-save-memory.sh "Decision: using React for frontend. Reason: team familiarity and component reuse."`。
- 用户：“保存一份结构化记忆记录。” → 创建一个JSON文件，然后运行`scripts/autodrive-save-memory.sh /tmp/milestone.json --agent-name my-agent`。
- 用户：“恢复我的记忆链。” → 运行`scripts/autodrive-recall-chain.sh`，查看从创建之初到现在的全部记忆记录。
- 用户：“从Autonomys下载文件bafk...abc。” → 运行`scripts/autodrive-download.sh bafk...abc ./downloaded_file`。

## 重要提示

- 所有存储在Autonomys上的数据默认都是**永久且公开的**。请勿存储敏感信息（如密码、私钥或个人隐私数据）。
- 免费API密钥在主网上的上传限制为每月20MB。下载次数不受限制。可以通过`GET /accounts/@me`查询剩余的上传额度，或运行`scripts/verify-setup.sh`进行验证。
- 上传文件、保存记忆数据或恢复记忆链都需要API密钥。普通文件下载可以使用公共网关，但压缩文件可能无法被解压。
- 记忆状态文件会记录`lastCid`、`lastUploadTimestamp`和`chainLength`等信息。请务必备份`lastCid`，因为它用于恢复数据。
- `autodrive-save-memory.sh`脚本会在文件存在时自动将最新的CID保存到`MEMORY.md`文件中，并在每次保存时更新相关内容。您无需手动跟踪`MEMORY.md`中的最新CID。
- 文件以单次上传的方式上传。免费账户的每月上传上限为20MB，因此请确保每次上传的文件大小不超过这个限制，以节省费用。
- 任何文件的下载地址为：`https://gateway.autonomys.xyz/file/<CID>`。
- 为了实现更高的恢复韧性，可以考虑将最新的CID通过Autonomys的EVM（智能合约平台）锚定在区块链上，这样无需手动管理CID即可实现数据的恢复。有关实现示例，请参考[openclaw-memory-chain](https://github.com/autojeremy/openclaw-memory-chain)。