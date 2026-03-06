---
name: myr
version: 1.1.0
description: Capture, search, verify, export, import, and synthesize Methodological Yield Reports (MYRs) for OODA-based intelligence compounding. Use when: (1) installing MYR on a node, (2) storing yield from OODA cycles, (3) searching prior yield before new work, (4) operator-reviewing MYR quality, (5) exporting/importing signed MYRs between nodes, (6) running the HTTP server for live peer sync, (7) managing network peers, (8) generating weekly digests, or (9) integrating MYR with an agent memory system. Triggers: "install MYR", "store a MYR", "what did we learn about", "weekly yield", "export yield", "import yield", "methodological yield", "MYR", "peer sync", "start MYR server".
---

# MYR — 方法论性产出报告（Methodological Yield Reports）

这是一个基于pistis框架的智能复合系统。每个完整的OODA（观察、定位、决策、行动）循环都会产生各种产出：技术方法、洞察、验证结果以及模式。MYR会以加密方式记录这些产出，确保它们能够在不同的会话、代理和节点之间持续积累。

**仓库地址：** https://github.com/JordanGreenhall/myr-system

## 必需的输出结果

对于每次MYR操作，需要返回以下信息：
1. 执行的操作
2. 受影响的工件ID
3. 验证结果
4. 下一步推荐的操作

## 安装（新节点）

```bash
git clone https://github.com/JordanGreenhall/myr-system.git
cd myr-system
npm install
cp config.example.json config.json
```

编辑 `config.json` 文件：
- 设置唯一的 `node_id`（例如 `n2`、`north-star`）——**不能使用 `n1`**
- 设置 `port`（默认值：3719，可以选择任何未使用的端口）
- 将 `node_url` 设置为可外部访问的地址（建议使用Tailscale IP地址——详见“网络”部分）
- 确保路径和密钥存储位置可写

生成密钥：

```bash
node scripts/myr-keygen.js
```

配置环境：

```bash
export MYR_HOME=/absolute/path/to/myr-system
```

## 节点身份

每个节点都必须拥有唯一的 `node_id` 和 `node_uuid`。这些信息在生成密钥时设置，并在运行时进行验证。

**如果 `node_id` 仍然是默认的 `"n1"`，所有脚本都将拒绝执行**。系统会显示错误信息并提供修复步骤，然后退出。

`myr-keygen` 命令会生成你的密钥对，并自动将 `node_uuid` 写入 `config.json` 文件。请验证你的节点身份：

```bash
node $MYR_HOME/scripts/myr-identity.js
```

## 安装验证（Ping测试）

执行以下五个步骤，所有步骤都必须成功：

```bash
cd $MYR_HOME
node scripts/myr-store.js --intent "Installation test" --type technique \
  --question "Does MYR work on this node?" --evidence "Store succeeded" \
  --changes "MYR is operational" --tags "test"
node scripts/myr-search.js --query "installation test"
node scripts/myr-verify.js --queue
node scripts/myr-sign.js --all
node scripts/myr-export.js --all
```

如果所有步骤都成功，说明节点已正常运行。

---

## HTTP服务器（实时节点同步）

MYR包含一个HTTP服务器，用于实现实时的节点间同步。节点会按照预定时间表自动进行同步，无需手动交换数据包。

### 启动服务器

```bash
cd $MYR_HOME
node server/index.js
```

服务器启动后的输出结果：

```
MYR node server listening on port 3719
  Discovery: http://<your-ip>:3719/.well-known/myr-node
  Health:    http://<your-ip>:3719/myr/health
```

### 作为持久化服务运行（macOS使用launchd）

创建 `~/Library/LaunchAgents/com.myr.server.plist` 文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.myr.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/node</string>
        <string>/path/to/myr-system/server/index.js</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/myr-system</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>MYR_HOME</key>
        <string>/path/to/myr-system</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/path/to/myr-system/logs/server.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/myr-system/logs/server-error.log</string>
</dict>
</plist>
```

```bash
mkdir -p $MYR_HOME/logs
launchctl load ~/Library/LaunchAgents/com.myr.server.plist
```

验证服务器是否正常运行：

```bash
curl http://localhost:<port>/myr/health
```

### 服务器端点

| 端点          | 认证方式    | 功能                        |
|------------------|-----------|-----------------------------|
| `GET /well-known/myr-node` | 无        | 节点发现（协议版本、公钥、功能信息）           |
| `GET /myr/health`     | 无        | 状态检查（节点状态、节点数量、报告数量）           |
| `GET /myr/reports`    | 节点密钥     | 可共享的报告列表（支持 `since`、`limit` 参数）       |
| `GET /myr/reports/:signature` | 节点密钥     | 获取特定报告                    |
| `POST /myr/peers/announce` | 无        | 节点主动请求配对                    |

### 网络可达性

节点之间必须能够互相访问。有以下几种选择：
- **Tailscale（推荐）：** 在两个节点上安装Tailscale，将 `node_url` 设置为Tailscale的IP地址（例如 `http://100.x.x.x:3719`）。这种方式私密且加密，无需端口转发。
- **VPN：** 任何共享的VPN方案都可以使用。
- **公共互联网：** 将 `node_url` 设置为公共IP地址或域名，并启用端口转发。但这种方式不太推荐。

---

## 节点管理

`bin/myr.js` 命令行工具用于管理节点间的实时同步。

### 通过URL添加节点

```bash
node $MYR_HOME/bin/myr.js add-peer http://<peer-tailscale-ip>:<port>
```

该命令会获取节点的发现信息，注册其公钥，并将信任状态设置为“pending”（待确认）。

### 非同步方式验证节点指纹

在批准任何节点之前，必须通过其他渠道（语音、Signal或面对面交流）验证其指纹：

```bash
# Your fingerprint — share this with your peer
node $MYR_HOME/bin/myr.js fingerprint

# Peer's fingerprint — confirm this matches what they told you
node $MYR_HOME/bin/myr.js peer-fingerprint <peer-node-id>
```

**未经非同步方式验证指纹的节点不得被批准**。这是确保信任安全的关键步骤。

### 批准或拒绝节点

```bash
node $MYR_HOME/bin/myr.js approve-peer <node-id-or-url>
node $MYR_HOME/bin/myr.js reject-peer <node-id-or-url>
```

### 列出所有节点

```bash
node $MYR_HOME/bin/myr.js peers
```

### 手动同步（按需）

一旦服务器启动，系统会每15分钟自动同步所有受信任的节点。

### 标记报告为可共享

只有明确标记为 `share_network=1` 的报告才会被共享给其他节点。请标记你已验证的报告：

```sql
-- In your MYR database (db/myr.db)
BEGIN IMMEDIATE;
UPDATE myr_reports SET share_network=1
WHERE node_id='<your-node-id>' AND operator_rating >= 3 AND verified_at IS NOT NULL;
COMMIT;
```

---

## 连接到现有节点（完整流程）

1. **启动你的服务器**，并确认其可以通过 `node_url` 访问。
2. **获取目标节点的URL**（包括Tailscale IP地址和端口）。
3. **添加节点：`node bin/myr.js add-peer <target-node-url>`。
4. **通过非同步方式交换节点指纹**（语音、Signal或面对面交流）。
5. **批准节点：`node bin/myr.js approve-peer <target-node-id>`。
6. **请求目标节点也批准你**（目标节点需要执行相同的操作）。
7. **检查同步状态：`node bin/myr.js sync <target-node-id>`——应能获取到对方的报告。
8. **标记你的报告为可共享**（参见上文说明），以便其他节点可以下载你的报告。

---

## 捕获产出数据

### 出产数据的类型

- **technique**：可复用的有效方法。
- **insight**：能够改变决策方向的见解。
- **falsification**：证明某种方法无效的证据（具有很高的价值）。
- **pattern**：在不同循环中反复出现的规律或模式。

## 查找之前的产出数据

### 使用场景

在开始新项目、进行架构决策时，或者当有人询问“我们对某件事了解多少”时，可以使用这些之前的产出数据。

## 验证与评分规则

- 评分范围为1-5分。
- 只有指定的操作员才能给出最终评分。
- 一个MYR只有在至少经过1位操作员的评分达到3分以上后，才能被视为“符合网络使用标准”。
- 节点加入的条件是：必须至少有10个MYR报告，且最近10个报告的平均评分不低于3.0分。

```bash
node $MYR_HOME/scripts/myr-verify.js --queue
node $MYR_HOME/scripts/myr-verify.js --id ID --rating 4 --notes "..."
```

## 每周总结报告

```bash
node $MYR_HOME/scripts/myr-weekly.js [--week 2026-02-17] [--output report.md]
```

## 手动数据包交换（实时同步的替代方案）

如果无法使用实时同步功能，可以手动导出/导入签名后的数据包。

### 导出数据包

```bash
node $MYR_HOME/scripts/myr-export.js --all
```

导出的数据包为签名后的JSON格式，保存在 `$MYR_HOME/exports/` 目录下。

### 导入数据包

```bash
node $MYR_HOME/scripts/myr-import.js --file path.myr.json [--peer-key keys/peer.public.pem]
```

导入数据包时可能遇到以下错误：
- “你正在导入自己的数据包”：`node_id` 和 `node_uuid` 与当前节点匹配。此时系统会退出并显示错误信息。
- “两个不同节点的标签冲突”：`node_id` 相同但 `node_uuid` 不同。此时目标节点需要设置唯一的 `node_id` 并重新导出数据包。系统会退出并显示错误信息。
- 密钥不匹配：导入操作会失败并显示错误信息，系统不会自动覆盖原有数据。

## 跨节点数据整合

### 功能

该系统能够识别节点间的共性发现、分歧以及独特的贡献。

## 签名与信任机制

- 每个导出的MYR数据包都必须包含签名和签名者的ID。
- 如果签名验证失败，导入操作会失败。
- 绝不允许将未签名或无法验证的MYR数据包合并到可信的数据集中。

## 内存与系统集成（异步处理）

- MYR数据的捕获过程应该是即时且不会阻塞用户的其他操作。
- 在数据持久化过程中，不应影响用户的响应速度。
- 如果持久化失败，系统应记录错误并显示非致命性的警告信息。

## ID格式

`{node_id}-{YYYYMMDD}-{seq}` — 例如：`n2-20260227-001`

## 架构信息

有关网络协议和扩展路线图的详细信息，请参阅：
`$MYR_HOME/docs/NETWORK-ARCHITECTURE.md`