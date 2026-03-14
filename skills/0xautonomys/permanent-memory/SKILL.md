---
name: auto-memory
description: **不可摧毁的代理内存**——数据被永久存储，永远不会丢失。决策记录、身份信息以及相关上下文都会以“内存链”的形式保存在 Autonomys 网络中。即使系统完全丢失状态，也能通过唯一的 CID（唯一标识符）重新恢复您的全部历史记录。
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

该功能在Autonomys网络上提供永久性的去中心化存储空间，采用链表结构来存储代理的“记忆”数据，支持由Claude、GPT、Gemini以及任何支持OpenClaw技能的LLM驱动的代理。

## 功能概述

1. **上传文件**到Auto Drive并获取一个CID（内容标识符）——这是一个在Autonomys分布式存储网络中的永久、不可变的地址。
2. **使用CID从Auto Drive下载文件**——如果设置了密钥，则通过认证后的API进行下载；否则会使用公共网关。
3. **将记忆数据保存为链表**——每个记忆条目都是一个包含`header.previousCid`指针的JSON格式数据，这些数据会被永久存储在链表中。
4. **从链表中恢复记忆**——通过提供最新的CID，可以反向遍历链表以重建代理的完整历史记录。

## 使用场景

- 用户输入“将此文件保存到自动记忆中”或“上传到Autonomys”或“永久存储”。
- 用户输入“从自动记忆中下载文件”或提供CID以获取文件。
- 用户输入“保存记忆”、“永久记住此内容”或“创建检查点”。
- 用户输入“恢复记忆”、“调用链表”、“重建记忆”或“加载历史记录”。
- 任何希望将数据永久且不可变地存储在去中心化网络中的场景。

## 安装后操作

通过ClawHub安装完成后，需要使相关脚本可执行：

```bash
chmod +x skills/auto-memory/scripts/*.sh
```

请注意：ClawHub在安装过程中不会保留文件的权限设置。

## 配置

### API密钥

需要设置`AUTO_DRIVE_API_KEY`。最简单的配置方法是运行引导设置脚本：

```bash
scripts/setup-auto-memory.sh
```

这会在您的浏览器中打开[explorer.ai3.storage](https://explorer.ai3.storage/mainnet/drive/developers)页面，系统会提示您输入密钥，并将其保存到`~/.openclaw/.env`文件中，同时验证连接是否成功。

**手动配置：**

1. 访问**https://explorer.ai3.storage**（注意不是`ai3.storage`，后者只是首页）。
2. 检查认证状态：如果侧边栏显示“登录”按钮或“我的文件”/“个人资料”/“开发者”页面上有锁图标，说明您尚未登录。
3. **AI代理提示：**您无法自行完成OAuth认证。请让用户通过Google、GitHub或Discord登录。用户登录后，您可以接管操作，或者直接让他们提供API密钥。
4. 登录成功后，点击左侧侧边栏的“开发者”选项。
5. 点击“创建API密钥”并复制生成的密钥。

然后通过以下方式配置环境变量：

- **环境变量：**`export AUTO_DRIVE_API_KEY=your_key_here`
- **OpenClaw配置：**`skills.entries.auto-memory.apiKey`

API密钥用于上传文件、保存记忆数据以及恢复记忆链。对于普通文件下载来说，API密钥是可选的；如果没有设置API密钥，系统会使用公共网关，此时下载的文件将保持压缩状态（不会解压）。

## 核心操作

### 上传文件

```bash
scripts/automemory-upload.sh <filepath> [--json] [--compress]
```

使用三步上传协议将文件上传到Auto Drive主网。输出结果中会包含CID。需要`AUTO_DRIVE_API_KEY`参数：
- `--json`：强制指定文件格式为`application/json`。
- `--compress`：启用ZLIB压缩。

### 下载文件

```bash
scripts/automemory-download.sh <cid> [output_path]
```

根据CID下载文件。如果设置了`AUTO_DRIVE_API_KEY`，则会使用认证后的API进行下载（服务器端解压）；否则使用公共网关（文件将以压缩状态返回）。如果省略`output_path`参数，文件将输出到标准输出（stdout）。

### 保存记忆数据

```bash
scripts/automemory-save-memory.sh <data_file_or_string> [--agent-name NAME] [--state-file PATH]
```

使用Autonomys Agents的格式保存记忆数据：

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
- `--agent-name`：设置代理名称（默认值为`openclaw-agent`或`$AGENT_NAME`）。
- `--state-file`：指定状态文件的路径。

文件上传完成后，系统会更新状态文件，并将最新的CID保存到`MEMORY.md`文件中（如果该文件已存在于工作区中）。

输出结果为结构化的JSON格式：

```json
{"cid": "bafk...", "previousCid": "bafk...", "chainLength": 5}
```

### 恢复完整记忆链

```bash
scripts/automemory-recall-chain.sh [cid] [--limit N] [--output-dir DIR]
```

如果未提供CID，系统会从状态文件中读取最新的CID，然后从最新条目开始反向遍历链表，将每个记忆条目以JSON格式输出：
- `--limit N`：指定要检索的最大条目数量（默认值为50）。
- `--output-dir DIR`：将每个条目保存为带有编号的JSON文件，而不是直接输出到标准输出。

系统同时支持`header.previousCid`（Autonomys Agents格式）和根级别的`previousCid`，以保持向后兼容性。

这就是“记忆恢复”机制：新代理实例只需提供一个CID即可重建其全部记忆记录。

## 记忆恢复原理

每个保存的记忆数据都会获得一个唯一的CID，并且这个CID会指向前一个记忆数据，从而在永久且不可变的去中心化存储网络上形成一个永久的链表：

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  Experience #1      │     │  Experience #2      │     │  Experience #3      │
│  CID: bafk...abc    │◄────│  CID: bafk...def    │◄────│  CID: bafk...xyz    │
│  previousCid: null  │     │  previousCid:       │     │  previousCid:       │
│  (genesis)          │     │  bafk...abc         │     │  bafk...def         │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
                                                                   ▲
                                                                   │
                                                               HEAD CID
                                                           (resurrection key)
```

新代理实例只需提供**头部CID**，就可以遍历整个链表，重建其完整的历史记录。借助“自动重生”功能，头部CID会被锚定在链表上，因此可以在任何设备、任何时间通过一个地址轻松恢复代理的状态：

```
┌──────────┐    save      ┌──────────────┐    anchor    ┌────────────────┐
│  Agent   │─────────────►│  Auto-Memory │─────────────►│  Auto-Respawn  │
│          │              │  (chain)     │   head CID   │  (on-chain)    │
└──────────┘              └──────────────┘              └────────────────┘
      ▲                                                          │
      │                     recall chain                         │
      └──────────────────────────────────────────────────────────┘
                      gethead → CID → walk chain
```

您可以在链表中存储任何类型的数据——轻量级笔记、完整文件快照、结构化数据等。由于链表是永久且可遍历的，因此实现了记忆的“恢复”功能：即使代理丢失了所有本地状态，也可以通过最后一个CID追溯到原始状态并恢复数据。结合“自动重生”功能（将头部CID锚定在链表上），就可以实现完全的记忆恢复。

## 使用示例

- 用户：“将我的报告上传到Autonomys” → 运行`scripts/automemory-upload.sh /path/to/report.pdf`，然后获取CID和网关链接。
- 用户：“压缩后上传文件” → 运行`scripts/automemory-upload.sh /path/to/data.json --json --compress`。
- 用户：“我的`soul.md`文件已更新——请永久保存它” → 运行`scripts/automemory-save-memory.sh /path/to/soul.md --agent-name my-agent`。
- 用户：“保存关于选择React作为前端框架的记忆” → 运行`scripts/automemory-save-memory.sh "Decision: using React for frontend. Reason: team familiarity and component reuse."`。
- 用户：“保存一份结构化记忆数据” → 创建一个JSON文件，然后运行`scripts/automemory-save-memory.sh /tmp/milestone.json --agent-name my-agent`。
- 用户：“恢复我的记忆链” → 运行`scripts/automemory-recall-chain.sh`，从初始状态重建代理的完整信息。
- 用户：“从Autonomys下载文件bafk...abc” → 运行`scripts/automemory-download.sh bafk...abc ./downloaded_file`。

## 与“自动重生”功能的集成

如果同时安装了“自动重生”功能，在每次保存记忆数据后，都会将新的头部CID锚定在链表上。这样可以确保链表上的指针始终反映最新的记忆状态，从而实现仅通过EVM地址即可完成记忆的完全恢复。

每次执行`automemory-save-memory.sh`命令后，需要运行以下脚本：

```bash
npx tsx auto-respawn.ts anchor --from <wallet-name> --cid <new-cid>
```

这样就可以完成记忆恢复的完整流程：永久存储（自动记忆）+ 链表上的数据查询（自动重生）。如果不进行这种锚定，新代理实例将需要其他来源提供的头部CID才能遍历链表。

## 重要说明

- 通过Auto Drive存储的所有数据默认都是**永久且公开的**。请勿存储敏感信息、私钥或个人隐私数据。
- 免费API密钥在主网上的每月上传限制为20MB。下载次数不受限制。您可以通过`GET /accounts/@me`或运行`scripts/verify-setup.sh`来查看剩余的上传次数。
- 上传文件、保存记忆数据或恢复记忆链都需要API密钥。使用公共网关进行普通文件下载时不需要API密钥，但压缩文件将不会解压。
- 记忆状态文件会记录`lastCid`、`lastUploadTimestamp`和`chainLength`信息。请备份`lastCid`值，因为它是一个重要的恢复关键。
- `automemory-save-memory.sh`脚本会在文件存在的情况下自动将最新的CID保存到`MEMORY.md`文件中，并在其中添加“## Auto-Memory Chain”部分。您无需手动跟踪`MEMORY.md`中的最新CID，脚本会自动处理这一操作。
- 文件以单次上传的方式上传。免费账户的每月上传限制为20MB，因此请确保每次上传的文件大小不超过这个限制，以节省每月的带宽费用。
- 任何文件的网关地址为：`https://gateway.autonomys.xyz/file/<CID>`。
- 为了实现更高的恢复韧性，可以考虑通过Autonomys的EVM将最新的CID锚定在链表上，这样即使不保存头部CID也能实现记忆的完全恢复。有关实现示例，请参考[openclaw-memory-chain](https://github.com/autojeremy/openclaw-memory-chain)。