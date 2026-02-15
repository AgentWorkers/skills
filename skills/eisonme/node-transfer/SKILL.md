# node-transfer

这是一个用于在 OpenClaw 节点之间实现高速、高效文件传输的工具，它利用了 Node.js 的原生流（native streams）技术。

## 📋 目录结构

- [解决的问题](#problem-solved)
- [架构设计](#architecture)
- [系统要求](#requirements)
- [安装方法](#installation)
- [使用说明](#usage)
- [API 参考](#api-reference)
- [故障排除](#troubleshooting)

---

## 🎯 解决的问题

### 原始问题

在使用 OpenClaw 的标准 `nodes.invoke` 机制进行大文件传输时，我们遇到了以下关键问题：

| 问题 | 影响 |
|-------|--------|
| **Base64 编码开销** | 传输数据量增加 33%，传输速度变慢 |
| **内存耗尽（OOM）** | 将多 GB 大小的文件加载到内存中会导致进程崩溃 |
| **传输延迟** | JSON 序列化/反序列化过程会带来显著延迟 |
| **每次传输都需要重新部署脚本** | 每次文件传输后都需要重新部署相关脚本 |

### 解决方案

`node-transfer` 通过使用 Node.js 的原生 HTTP 流技术，解决了这些问题：

- ✅ **零内存开销**：文件直接从磁盘传输到网络，无需进行 Base64 编码 |
- ✅ **无 Base64 编码**：以原始二进制格式传输文件 |
- ✅ **传输速度快**：传输速度仅受网络带宽限制 |
- ✅ **一次安装，多次使用**：脚本在首次部署后会在节点上持久化保存 |

### 性能对比

| 测量指标 | Base64 传输 | node-transfer | 性能提升 |
|--------|----------------|---------------|-------------|
| 1GB 文件传输时间 | 约 15-30 分钟 | 约 8 秒 | **快 150 倍** |
| 内存使用量 | 超过 1GB | 小于 10MB | **减少 99%** |
| 首次传输的开销 | 无 | 约 30 秒（一次性安装） | - |
| 后续传输 | 约 15-30 分钟 | **<1 秒（检查）+ 约 8 秒（传输）** | **快 200 倍** |

---

## 🏗️ 架构设计

### 工作原理

```
┌──────────────┐     HTTP Stream      ┌──────────────┐
│  send.js     │ ◄──────────────────► │ receive.js   │
│  (Source)    │   (Token-protected)  │ (Destination)│
└──────────────┘                      └──────────────┘
       │                                     │
       ▼                                     ▼
┌──────────────┐                      ┌──────────────┐
│  Read Stream │                      │ Write Stream │
│  (fs.create  │                      │ (fs.create   │
│   ReadStream)│                      │  WriteStream)│
└──────────────┘                      └──────────────┘
       │                                     │
       ▼                                     ▼
┌──────────────┐                      ┌──────────────┐
│  File on     │                      │  File on     │
│  Disk        │                      │  Disk        │
└──────────────┘                      └──────────────┘
```

### 安全模型

1. **一次性令牌**：生成一个 256 位的随机加密令牌（64 个十六进制字符）。
2. **单次连接**：每个令牌仅允许进行一次下载。
3. **自动关闭**：传输完成后或连接断开时，服务器会自动关闭。
4. **令牌验证**：每个请求都必须包含正确的令牌。

### 数据流处理流程

1. **发送方（`send.js`）**：
   - 生成随机端口和安全令牌。
   - 在临时端口上启动 HTTP 服务器。
   - 直接将文件从磁盘流式传输到网络。
   - 传输完成后或超时（默认 5 分钟）后自动关闭。

2. **接收方（`receive.js`）**：
   - 使用令牌连接到发送方的 URL。
   - 将接收到的数据直接写入磁盘。
   - 报告传输进度、传输速度和完成状态。
   - 验证接收到的数据字节是否与预期大小一致。

---

## 📦 系统要求

- **Node.js**：版本 14.0.0 或更高。
- **网络**：节点之间需要支持 TCP 连接（任意端口 1024-65535）。
- **防火墙**：必须允许数据包的出站和入站传输（特别是临时端口）。
- **磁盘空间**：目标节点必须有足够的空间来存储接收到的文件。

---

## 🚀 安装方法

### “一次安装，多次使用”的机制

我们不再每次传输都重新部署脚本，而是将脚本部署到每个节点上，并在后续传输时进行快速版本检查。

### 方法 1：使用 `deploy.js`（推荐）

```bash
# Generate deployment script for a target node
node deploy.js E3V3

# This outputs a PowerShell script that you can execute via nodes.invoke()
```

### 方法 2：手动部署

在每个目标节点上创建相应的目录并复制文件：

```powershell
# Create directory
mkdir C:/openclaw/skills/node-transfer/scripts -Force

# Copy these files (ensure UTF-8 without BOM encoding):
# - send.js
# - receive.js
# - ensure-installed.js
# - version.js
```

### 方法 3：通过 OpenClaw 代理进行部署

```javascript
// 1. Check if already installed (< 100ms)
const check = await nodes.invoke({
    node: 'E3V3',
    command: ['node', 'C:/openclaw/skills/node-transfer/scripts/ensure-installed.js', 
              'C:/openclaw/skills/node-transfer/scripts']
});

const checkResult = JSON.parse(check.output);

if (!checkResult.installed) {
    // 2. Deploy if needed (one-time, ~30 seconds)
    // Use the deploy.js output or manually copy files
    console.log('Deploying node-transfer to E3V3...');
    // ... deployment code ...
}
```

---

## 💡 使用说明

### 基本传输流程

```javascript
const INSTALL_DIR = 'C:/openclaw/skills/node-transfer/scripts';
const SOURCE_NODE = 'E3V3';
const DEST_NODE = 'E3V3-Docker';

// Step 1: Check installation on both nodes (fast!)
const [sourceCheck, destCheck] = await Promise.all([
    nodes.invoke({
        node: SOURCE_NODE,
        command: ['node', `${INSTALL_DIR}/ensure-installed.js`, INSTALL_DIR]
    }),
    nodes.invoke({
        node: DEST_NODE,
        command: ['node', `${INSTALL_DIR}/ensure-installed.js`, INSTALL_DIR]
    })
]);

// Deploy if needed (usually only once per node ever)
// ... deployment code if not installed ...

// Step 2: Start sender on source node
const sendResult = await nodes.invoke({
    node: SOURCE_NODE,
    command: ['node', `${INSTALL_DIR}/send.js`, 'C:/data/large-file.zip']
});

const { url, token, fileSize, fileName } = JSON.parse(sendResult.output);

// Step 3: Start receiver on destination node
const receiveResult = await nodes.invoke({
    node: DEST_NODE,
    command: ['node', `${INSTALL_DIR}/receive.js`, url, token, '/incoming/file.zip']
});

const result = JSON.parse(receiveResult.output);
console.log(`Transferred ${result.bytesReceived} bytes in ${result.duration}s at ${result.speedMBps} MB/s`);
```

### 命令行使用方法

#### 发送方

```bash
node send.js /path/to/file.zip
```

输出：
```json
{
  "url": "http://192.168.1.10:54321/transfer",
  "token": "a1b2c3d4e5f6789...",
  "fileSize": 1073741824,
  "fileName": "file.zip",
  "sourceIp": "192.168.1.10",
  "port": 54321,
  "version": "1.0.0"
}
```

选项：
```bash
node send.js /path/to/file.zip --port 8080 --timeout 10
node send.js --help
node send.js --version
```

#### 接收方

```bash
node receive.js "http://192.168.1.10:54321/transfer" "token-here..." /path/to/save.zip
```

输出：
```json
{
  "success": true,
  "bytesReceived": 1073741824,
  "totalBytes": 1073741824,
  "duration": 8.42,
  "speedMBps": 121.5,
  "outputPath": "/path/to/save.zip"
}
```

选项：
```bash
node receive.js <url> <token> <output> --timeout 60 --no-progress
node receive.js --help
node receive.js --version
```

---

## 📚 API 参考

### `send.js`

用于启动 HTTP 服务器以流式传输文件。

**使用方法：** `node send.js <filePath> [options]`

**参数：**
- `filePath`（必填）：要传输的文件路径。

**选项：**
- `--port <n>`：指定端口（默认为随机生成的临时端口）。
- `--timeout <n>`：传输超时时间（默认为 5 分钟）。

**输出（JSON 格式）：**
| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `url` | string | 接收方需要连接的 HTTP URL |
| `token` | string | 安全令牌（64 个十六进制字符） |
| `fileSize` | number | 文件大小（字节） |
| `fileName` | string | 文件原始名称 |
| `sourceIp` | string | 发送方的 IP 地址 |
| `port` | number | 使用的 TCP 端口 |
| `version` | string | `send.js` 的版本信息 |

**退出码：**
- `0`：成功（传输完成或显示相关信息）。
- `1`：错误（错误详情见标准错误输出）。

**错误输出（JSON 格式）：**
```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable description"
}
```

错误代码：`FILE_NOT_FOUND`, `NOT_A_FILE`, `SERVER_ERROR`, `TIMEOUT`, `READ_ERROR`, `RESPONSE_ERROR`

---

### `receive.js`

用于连接到发送方并下载文件。

**使用方法：** `node receive.js <url> <token> <outputPath> [options]`

**参数：**
- `url`（必填）：来自 `send.js` 的输出 URL。
- `token`（必填）：来自 `send.js` 的安全令牌。
- `outputPath`（必填）：保存接收到的文件的路径。

**选项：**
- `--timeout <n>`：连接超时时间（秒）。
- `--no-progress`：禁用进度显示。

**输出（JSON 格式）：**
| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `success` | boolean | 成功时始终为 `true` |
| `bytesReceived` | number | 实际接收的字节数 |
| `totalBytes` | number | 预期文件大小（根据 `Content-Length`） |
| `duration` | number | 传输时间（秒） |
| `speedMBps` | number | 平均传输速度（MB/s） |
| `outputPath` | string | 文件的保存路径 |

**进度更新（当未使用 `--no-progress` 选项时）：**
```json
{
  "progress": true,
  "receivedBytes": 536870912,
  "totalBytes": 1073741824,
  "percent": 50,
  "speedMBps": 125.4
}
```

**退出码：**
- `0`：成功。
- `1`：错误（错误详情见标准错误输出）。

错误代码：`INVALID_ARGS`, `INVALID_URL`, `CONNECTION_ERROR`, `HTTP_ERROR`, `TIMEOUT`, `WRITE_ERROR`, `SIZE_MISMATCH`, `FILE_EXISTS`, `NO_DATA`

---

### `ensure-installed.js`

用于快速检查节点上是否已安装 `node-transfer`。

**使用方法：** `node ensure-installed.js <targetDir>`

**参数：**
- `targetDir`（必填）：需要检查的目录。

**输出（JSON 格式）：**

- 如果已安装：```json
{
  "installed": true,
  "version": "1.0.0",
  "message": "node-transfer is installed and up-to-date"
}
```
- 如果需要安装：```json
{
  "installed": false,
  "missing": ["send.js"],
  "mismatched": [],
  "currentVersion": null,
  "requiredVersion": "1.0.0",
  "action": "DEPLOY",
  "message": "Installation needed: 1 missing, 0 outdated"
}
```

**退出码：**
- `0`：已安装且版本最新。
- `1`：需要安装或更新。
- `2`：出现错误（例如目录无效等）。

### `deploy.js`

用于生成代理节点的部署脚本。

**使用方法：** `node deploy.js <nodeId> [targetDir]`

**输出（JSON 格式）：**
- `script`：用于部署文件的 PowerShell 脚本。
- `escapedScript`：适用于命令行的转义版本。
- `usage`：JavaScript 和命令行的使用示例。

---

## 🔧 故障排除

### “连接超时”

**原因**：网络连接问题或防火墙阻止了连接。

**解决方法：**
- 确保两个节点之间可以互相访问。
- 检查防火墙规则是否允许出站连接。
- 尝试使用 `--port` 参数指定特定端口。
- 增加 `--timeout` 参数来延长超时时间。

### “403 Forbidden: 无效或缺失的令牌”

**原因**：令牌不匹配或 URL 被篡改。

**解决方法：**
- 使用 `send.js` 输出的完整令牌。
- 不要修改 URL。
- 确保令牌未过期（发送方在 5 分钟后超时）。

### “409 Conflict: 传输已在进行中”

**原因**：使用相同的令牌尝试了多次连接。

**解决方法：**
- 每个发送方的 URL/令牌只能使用一次。
- 如果需要重试，请重新启动发送方。

### “FILE_NOT_FOUND” 或 “NOT_A_FILE”

**原因**：发送方的文件路径无效。

**解决方法：**
- 使用绝对路径。
- 确认文件存在。
- 检查文件权限。

### “SIZE_MISMATCH”

**原因**：传输过程中断或网络问题。

**解决方法：**
- 重新尝试传输。
- 检查网络稳定性。
- 如果文件传输不完整，系统会自动清理部分数据。

### 在使用 `ensure-installed.js` 时出现 “Hash mismatch” 错误**

**原因**：文件被修改或损坏。

**解决方法：**
- 使用 `deploy.js` 重新部署脚本。
- 确保文件在传输过程中未被修改。
- 检查文件编码（必须是 UTF-8 格式，且不含 BOM 字符）。

### 后续传输速度慢

**原因**：未使用 `ensure-installed.js` 进行安装检查。

**解决方法：**
- 必须先检查是否已安装（耗时 < 100 毫秒）。
- 仅在没有安装 `node-transfer` 的情况下才进行部署。
- 遵循 “一次安装，多次使用”的原则。

---

## 📄 相关文件

| 文件 | 用途 |
|------|---------|
| `send.js` | 向接收方传输文件的 HTTP 服务器 |
| `receive.js` | 从发送方下载文件的 HTTP 客户端 |
| `ensure-installed.js | 快速检查是否已安装及文件完整性 |
| `version.js` | 用于检测版本更新的版本信息 |
| `deploy.js` | 生成代理节点的部署脚本 |

---

## 🤝 贡献方式

有关如何将此功能集成到 OpenClaw 核心中的信息，请参阅 [CONTRIBUTING_PROPOSAL.md](./CONTRIBUTING_PROPOSAL.md)。

---

*专为 OpenClaw 设计：无需 Base64 编码，避免内存耗尽，无需等待。*