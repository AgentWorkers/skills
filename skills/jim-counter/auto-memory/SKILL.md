---
name: auto-memory
description: **不可摧毁的代理内存**——数据被永久存储，绝不会丢失。决策、身份信息以及相关上下文都会以“内存链”的形式保存在 Autonomys 网络中。即使系统状态完全丢失，也能仅通过一个唯一的 CID（身份标识符）重新还原你的全部历史记录。
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
# 自动记忆功能

该功能在Autonomys网络上提供永久性的去中心化存储服务，采用链表结构来存储代理的“记忆”数据，支持由Claude、GPT、Gemini以及任何支持OpenClaw技能的LLM驱动的代理。

## 功能概述

1. **上传文件**到Auto Drive并获取一个CID（内容标识符）——这是一个在Autonomys分布式存储网络中的永久、不可变的地址。
2. **使用CID从Auto Drive下载文件**——如果设置了密钥，则通过认证后的API进行下载；否则会通过公共网关下载。
3. **将记忆数据保存为链式结构**——每个记忆条目都是一个包含`header.previousCid`指针的JSON对象，这些条目被永久存储在链表中。
4. **从链表中恢复记忆**——通过提供最新的CID，可以反向遍历链表来重建代理的全部历史记录。

## 使用场景

- 用户输入“将此文件保存到自动记忆中”或“上传到Autonomys”或“永久保存”。
- 用户请求“从自动记忆中下载文件”或提供CID以获取文件。
- 用户执行“保存记忆”、“永久记录此内容”或“创建检查点”等操作。
- 用户需要将数据永久且不可变地存储在去中心化网络中时。

## 安装后操作

通过ClawHub安装完成后，需要将相关脚本设置为可执行状态：

```bash
chmod +x skills/auto-memory/scripts/*.sh
```

请注意：ClawHub在安装过程中不会自动处理文件的权限设置。

## 配置参数

### API密钥

需要设置`AUTO_DRIVE_API_KEY`。最简单的配置方法是运行引导式设置脚本：

```bash
scripts/setup-auto-memory.sh
```

这将打开[explorer.ai3.storage](https://explorer.ai3.storage/mainnet/drive/developers)页面，在那里输入API密钥，密钥会被保存到`~/.openclaw/.env`文件中，并验证连接是否成功。

**手动配置步骤：**

1. 访问**https://explorer.ai3.storage**（注意不是`ai3.storage`，后者只是首页）。
2. 检查登录状态：如果侧边栏显示“登录”按钮或“我的文件”/“个人资料”/“开发者”页面上有锁图标，说明您尚未登录。
3. **AI代理提示**：您无法自行完成OAuth认证。请让用户通过Google、GitHub或Discord登录。用户登录后，您可以接管操作，或者直接让他们提供API密钥。
4. 登录成功后，点击左侧侧边栏的“开发者”选项。
5. 点击“创建API密钥”并复制生成的密钥。

然后通过以下方式配置环境变量：

- **环境变量**：`export AUTO_DRIVE_API_KEY=your_key_here`
- **OpenClaw配置**：`skills.entries.auto-memory.apiKey`

API密钥用于上传文件、保存记忆数据以及恢复记忆链。对于普通文件下载来说，API密钥是可选的；如果没有密钥，则会使用公共网关进行下载，此时下载的文件将以原始存储格式（压缩文件将不会被解压）返回。

## 核心操作

### 上传文件

```bash
scripts/automemory-upload.sh <filepath> [--json] [--compress]
```

使用三步上传协议将文件上传到Auto Drive主网。返回CID到标准输出（stdout）。需要`AUTO_DRIVE_API_KEY`参数。

- `--json`：强制指定MIME类型为`application/json`。
- `--compress`：启用ZLIB压缩。

### 下载文件

```bash
scripts/automemory-download.sh <cid> [output_path]
```

通过CID下载文件。如果设置了`AUTO_DRIVE_API_KEY`，则会使用认证后的API进行下载（服务器端会解压文件）；否则通过公共网关下载（文件将以原始存储格式返回）。如果省略`output_path`参数，文件将输出到标准输出。

### 保存记忆数据

```bash
scripts/automemory-save-memory.sh <data_file_or_string> [--agent-name NAME] [--state-file PATH]
```

使用Autonomys Agents的格式创建记忆数据：

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
- 如果第一个参数是普通字符串，它会被封装为`{"type": "memory", "content": "..."}`格式。
- `--agent-name`：设置代理的名称（默认值为`openclaw-agent`或`$AGENT_NAME`）。
- `--state-file`：指定状态文件的路径。

文件上传完成后，会更新状态文件，并将最新的CID保存到`MEMORY.md`文件中（如果该文件已存在于工作区中）。返回结构化的JSON数据到标准输出。

```json
{"cid": "bafk...", "previousCid": "bafk...", "chainLength": 5}
```

### 恢复全部记忆数据

```bash
scripts/automemory-recall-chain.sh [cid] [--limit N] [--output-dir DIR]
```

如果未提供CID，系统会从状态文件中读取最新的CID。然后从最新条目开始反向遍历链表，将每个记忆数据以JSON格式输出。

- `--limit N`：指定要检索的最大条目数量（默认值为50）。
- `--output-dir DIR`：将每个条目保存为带编号的JSON文件，而不是直接输出到标准输出。

该功能支持`header.previousCid`（Autonomys Agents格式）和根级别的`previousCid`，以保持向后兼容性。

### 恢复机制

每个保存的记忆数据都会获得一个唯一的CID，并指向前一个条目，从而在永久且不可变的去中心化存储网络中形成一个永久的链式结构。新的代理实例只需提供头部CID即可重建其全部记忆记录。

### 恢复机制的工作原理

每个保存的记忆数据都会获得一个唯一的CID，并与前一个条目关联，形成一个永久的链式结构。新的代理实例只需提供头部CID，就可以从链表的起始节点开始重建其全部历史记录。由于头部CID被存储在链表中，因此可以在任何设备上通过这个地址随时恢复代理的状态。

## 使用示例

- 用户：“将我的报告上传到Autonomys” → 运行`scripts/automemory-upload.sh /path/to/report.pdf`，然后获取CID和下载链接。
- 用户：“压缩后上传文件” → 运行`scripts/automemory-upload.sh /path/to/data.json --json --compress`。
- 用户：“我的`soul.md`文件已更新，请永久保存” → 运行`scripts/automemory-save-memory.sh /path/to/soul.md --agent-name my-agent`。
- 用户：“保存关于选择React作为前端框架的记忆记录” → 运行`scripts/automemory-save-memory.sh "Decision: using React for frontend. Reason: team familiarity and component reuse."`。
- 用户：“保存结构化记忆数据” → 先创建一个JSON文件，然后运行`scripts/automemory-save-memory.sh /tmp/milestone.json --agent-name my-agent`。
- 用户：“恢复我的记忆链” → 运行`scripts/automemory-recall-chain.sh`，从起始节点重建代理的状态和上下文。
- 用户：“从Autonomys下载文件`bafk...abc`” → 运行`scripts/automemory-download.sh bafk...abc ./downloaded_file`。

## 重要说明

- 通过Auto Drive存储的所有数据默认都是永久且公开的。请勿存储敏感信息、私钥或个人隐私数据。
- 免费API密钥在主网上的上传限制为每月20MB。下载次数不受限制。可以通过`GET /accounts/@me`查询剩余的上传额度，或运行`scripts/verify-setup.sh`来检查。
- 上传文件、保存记忆数据或恢复记忆链都需要API密钥。普通文件下载可以使用公共网关，但压缩文件将不会被解压。
- 记忆状态文件会记录`lastCid`、`lastUploadTimestamp`和`chainLength`等信息。请备份`lastCid`值，因为它用于恢复代理的状态。
- `automemory-save-memory.sh`脚本会在文件存在时自动将最新的CID保存到`MEMORY.md`文件中，并在每次保存时更新相关内容。您无需手动跟踪`MEMORY.md`中的最新CID。
- 文件以单次上传的方式上传。免费套餐每月的20MB上传限制实际上是指每个文件的上传大小上限，请确保每次上传的文件大小不超过此限制以节省费用。
- 任何文件的下载地址为：`https://gateway.autonomys.xyz/file/<CID>`。
- 为了实现更高的恢复韧性，可以考虑通过Autonomys的EVM将最新的CID存储在链表中，这样无需手动管理头部CID即可实现恢复。有关实现示例，请参考[openclaw-memory-chain](https://github.com/autojeremy/openclaw-memory-chain)合约。