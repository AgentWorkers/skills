---
name: auto-drive
description: 不可摧毁的代理内存——数据会永久存储，永远不会丢失。将决策、身份信息以及相关上下文以内存链的形式保存在 Autonomys Network 上。即使系统状态完全丢失，也能通过一个唯一的 CID（标识符）重新构建所有的历史记录。
metadata:
  openclaw:
    emoji: "🧬"
    primaryEnv: AUTO_DRIVE_API_KEY
    requires:
      bins: ["curl", "jq", "file"]
      env: ["AUTO_DRIVE_API_KEY"]
    install:
      - id: curl-brew
        kind: brew
        formula: curl
        bins: ["curl"]
        label: "Install curl (brew)"
      - id: jq-brew
        kind: brew
        formula: jq
        bins: ["jq"]
        label: "Install jq (brew)"
      - id: file-brew
        kind: brew
        formula: file-formula
        bins: ["file"]
        label: "Install file (brew)"
---
# 自动驱动技能（Auto-Drive Skill）

该技能利用Autonomys网络上的永久去中心化存储空间，通过链表结构来保存代理的“记忆”数据。适用于由Claude、GPT、Gemini或任何支持OpenClaw技能的LLM驱动的代理。

## 该技能的功能

1. **上传文件**到Autonomys存储空间，并获取一个CID（内容标识符）——这是一个在Autonomys去中心化存储网络中永久且不可变的地址。
2. **使用CID从Autonomys存储空间下载文件**：如果设置了API密钥，则会使用经过身份验证的API；否则会通过公共网关下载。
3. **将记忆数据保存为链式结构**：每个记忆条目都包含一个JSON格式的数据，以及一个`header.previousCid`指针，这些数据会被永久存储在链表中。
4. **从链表中恢复记忆**：通过提供最新的CID，可以反向遍历链表以重建代理的完整历史记录。

## 适用场景

- 当用户执行“将此文件保存到Autonomys”或“上传到Autonomys”或“永久存储”等操作时。
- 当用户需要从Autonomys存储空间下载文件或提供CID以获取文件时。
- 当用户执行“保存记忆”、“永久记住此内容”或“创建检查点”等操作时。
- 当用户执行“恢复记忆”、“调用链表数据”、“重建记忆”或“加载历史记录”等操作时。
- 任何希望将数据永久且不可变地存储在去中心化网络上的场景。

## 安装后的配置

通过ClawHub安装完成后，需要确保相关脚本具有可执行权限：

```bash
chmod +x skills/auto-drive/scripts/*.sh
```

请注意：ClawHub在安装过程中不会自动处理文件权限设置。

## 配置参数

### API密钥（API Key）

需要设置`AUTO_DRIVE_API_KEY`。最简单的配置方法是运行引导式设置脚本：

```bash
scripts/setup-auto-drive.sh
```

运行该脚本后，会在浏览器中打开[explorer.ai3.storage](https://explorer.ai3.storage/mainnet/drive/developers)页面，系统会提示您输入API密钥，并将其保存到`~/.openclaw/.env`文件中，同时验证连接是否成功。

**手动配置步骤：**

1. 访问**https://explorer.ai3.storage**（注意不是`ai3.storage`，后者只是首页）。
2. 检查登录状态：如果侧边栏显示“登录”按钮或“My Files”、“Profile”、“Developers”页面上有锁形图标，说明您尚未登录。
3. **注意事项：**您无法自行完成OAuth认证。请让用户通过Google、GitHub或Discord登录。登录完成后，您可以接管操作，或者直接让用户提供API密钥。
4. 登录成功后，在左侧边栏点击“Developers”。
5. 点击“Create API Key”并复制生成的API密钥。

接下来，通过以下方式配置环境变量：

- **环境变量：**`export AUTO_DRIVE_API_KEY=your_key_here`
- **OpenClaw配置文件：**`skills.entries.auto-drive.apiKey`

API密钥用于上传文件、保存记忆数据以及恢复记忆链。对于普通文件下载来说，API密钥是可选的；如果没有API密钥，系统会使用公共网关进行下载，此时下载的文件将保持压缩状态（不会解压）。

## 核心操作

### 上传文件（Upload a File）

```bash
scripts/autodrive-upload.sh <filepath> [--json] [--compress]
```

使用三步上传协议将文件上传到Autonomys主网。上传完成后，API会返回CID（输出到标准输出）。
- `--json`：强制指定文件格式为`application/json`。
- `--compress`：启用ZLIB压缩。

### 下载文件（Download a File）

```bash
scripts/autodrive-download.sh <cid> [output_path]
```

根据CID从Autonomys存储空间下载文件。如果设置了`AUTO_DRIVE_API_KEY`，则会使用经过身份验证的API进行解压；否则会通过公共网关下载（文件将以压缩状态返回）。如果省略`output_path`参数，文件将输出到标准输出。

### 保存记忆条目（Save a Memory Entry）

```bash
scripts/autodrive-save-memory.sh <data_file_or_string> [--agent-name NAME] [--state-file PATH]
```

使用Autonomys Agents规定的格式保存记忆数据：

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
- 如果第一个参数是普通字符串，系统会将其封装为`{"type": "memory", "content": "..."}`格式。
- `--agent-name`：设置代理的名称（默认为`openclaw-agent`或`$AGENT_NAME`）。
- `--state-file`：指定状态文件的路径。

文件上传完成后，系统会更新状态文件，并将最新的CID保存到`MEMORY.md`文件中（如果该文件已存在于工作区中）。同时，最新的CID也会被保存到`MEMORY.md`文件中。

### 恢复完整记忆链（Recall the Full Chain）

```bash
scripts/autodrive-recall-chain.sh [cid] [--limit N] [--output-dir DIR]
```

如果未提供CID，系统会从状态文件中读取最新的CID，然后从最新条目开始反向遍历链表，将所有记忆数据以JSON格式输出。
- `--limit N`：指定最多返回的条目数量（默认为50条）。
- `--output-dir DIR`：将每个条目保存为带编号的JSON文件，而不是直接输出到标准输出。

该功能支持`header.previousCid`（Autonomys Agents格式）和根级别的`previousCid`，以保持与旧版本的兼容性。

### 恢复记忆的原理

每个保存的记忆数据都会获得一个唯一的CID，并通过这个CID链接到之前的条目，从而形成一个永久且不可变的链式结构。新的代理实例只需提供这个CID，就可以重建其全部记忆记录。

## 恢复记忆的机制

每个保存的记忆数据都会获得一个唯一的CID，并通过这个CID链接到之前的条目，形成一个永久且不可变的去中心化存储链。新的代理实例只需提供这个CID，就可以从链表的起始节点开始重建其全部历史记录。由于CID被保存在链表中，因此无论在什么设备上，都可以随时通过这个CID恢复代理的状态。

## 使用示例

- 用户：“将我的报告上传到Autonomys。” → 运行`scripts/autodrive-upload.sh /path/to/report.pdf`，然后获取CID和下载链接。
- 用户：“压缩后上传文件。” → 运行`scripts/autodrive-upload.sh /path/to/data.json --json --compress`。
- 用户：“我的`soul.md`文件已更新，请永久保存。” → 运行`scripts/autodrive-save-memory.sh /path/to/soul.md --agent-name my-agent`。
- 用户：“保存关于选择React作为前端框架的记忆。” → 运行`scripts/autodrive-save-memory.sh "Decision: using React for frontend. Reason: team familiarity and component reuse."`。
- 用户：“保存一个结构化的数据记录。” → 创建一个JSON文件，然后运行`scripts/autodrive-save-memory.sh /tmp/milestone.json --agent-name my-agent`。
- 用户：“恢复我的记忆链。” → 运行`scripts/autodrive-recall-chain.sh`，从链表的起始节点重建代理的状态。

## 重要提示

- 通过Autonomys存储的所有数据默认都是永久且公开的。请勿存储敏感信息（如密码、私钥或个人隐私数据）。
- 免费API密钥在主网上的每月上传上限为20MB；下载次数不受限制。可以通过`GET /accounts/@me`查询剩余的上传次数，或运行`scripts/verify-setup.sh`进行验证。
- 上传文件、保存记忆数据或恢复记忆链都需要API密钥。如果没有API密钥，可以使用公共网关进行下载，但压缩文件将不会解压。
- 记忆状态文件会记录`lastCid`、`lastUploadTimestamp`和`chainLength`等信息。请备份`lastCid`值，因为它是一个重要的恢复关键。
- `autodrive-save-memory.sh`脚本会在文件存在时自动将最新的CID保存到`MEMORY.md`文件中。该脚本会自动创建`## Auto-Drive Chain`部分并更新该文件。您无需手动跟踪`MEMORY.md`中的最新CID。
- 文件是分块上传的；免费账户的每月上传上限为20MB，因此请确保每次上传的文件大小不超过这个限制，以节省费用。
- 任何文件的下载地址为：`https://gateway.autonomys.xyz/file/<CID>`。
- 为了实现更高的恢复灵活性，可以考虑通过Autonomys的EVM将最新的CID保存到链表中，这样即使丢失了本地状态，也可以通过链表直接恢复数据。有关实现示例，请参考[openclaw-memory-chain](https://github.com/autojeremy/openclaw-memory-chain)合约。