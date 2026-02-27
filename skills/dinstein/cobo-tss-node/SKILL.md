---
name: cobo-tss-node
description: "**管理 Cobo TSS 节点以进行 MPC 阈值签名**  
**用途：**  
- 设置新的 TSS 节点  
- 启动/停止节点服务  
- 检查节点状态或健康状况  
- 为密钥共享检查进行签名  
- 导出共享数据以备灾难恢复  
- 备份或更新节点  
- 将节点作为 systemd 或 launchd 服务进行安装  
**不适用场景：**  
- Cobo WaaS API 集成  
- 在链上构建交易  
- 钱包用户界面（wallet UI）的实现"
version: 0.2.0
metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "requires": { "bins": ["curl", "python3"] },
      },
  }
---
# Cobo TSS Node

**Cobo TSS Node** 是 Cobo 共享托管解决方案中的客户端 MPC（Multi-Party Computing）签名组件。

## 使用场景

✅ **适用场景：**
- 安装 Cobo TSS Node 可执行文件
- 初始化新的 TSS 节点（生成密钥及节点 ID）
- 启动/停止/重启节点服务
- 将节点作为系统服务安装（Linux 的 systemd 或 macOS 的 launchd）
- 检查节点状态、查看节点所属组或读取日志
- 定期检查密钥共享状态并进行签名操作
- 导出密钥共享文件以备灾难恢复
- 备份或更新节点配置

❌ **不适用场景：**
- 与 Cobo WaaS REST API 交互 → 请使用 Cobo SDK
- 直接构建链上交易
- 管理 Cobo Portal（Web 界面操作）

## 快速入门

```bash
./scripts/install.sh                        # Download binary
./scripts/setup-keyfile.sh                  # Create password file
./scripts/init-node.sh                      # Initialize (outputs Node ID)
./scripts/install-service.sh linux          # Install systemd service
./scripts/node-ctl.sh start                 # Start
```

## 脚本

| 脚本 | 功能 |
|--------|---------|
| `scripts/install.sh` | 从 GitHub 仓库下载二进制文件 |
| `scripts/setup-keyfile.sh` | 创建 `.password` 密钥文件（权限设置为 600） |
| `scripts/init-node.sh` | 初始化节点密钥和数据库 |
| `scripts/node-info.sh` | 查看节点 ID 和所属组信息 |
| `scripts/start-node.sh` | 在前台启动节点 |
| `scripts/install-service.sh` | 将节点作为 systemd 服务（Linux）或 launchd 服务（macOS）安装 |
| `scripts/node-ctl.sh` | 提供统一的日常操作命令行接口 |

## 日常维护操作

所有安装后的操作均通过 `node-ctl.sh` 脚本完成：

```bash
./scripts/node-ctl.sh <command> [--dir ~/.cobo-tss-node]
```

### 服务管理

| 命令 | 功能 |
|---------|-------------|
| `status` | 显示服务状态（systemctl/launchctl） |
| `start` | 启动 TSS Node 服务 |
| `stop` | 停止服务 |
| `restart` | 重启服务 |
| `logs` | 查看最近 50 行日志 |
| `logs -f` | 实时查看日志 |
| `logs --lines=200` | 查看更多日志内容 |

Linux 系统使用 `journalctl` 查看日志，macOS 系统则从 `~/.cobo-tss-node/logs/launchd-stdout.log` 文件中读取日志。

### 状态检查

**通过一个命令即可完成以下检查：**
- 服务是否正在运行
- 二进制文件版本
- 数据库是否存在及文件大小
- 配置文件是否存在
- 密钥文件的权限是否正确（必须为 600）
- 可用磁盘空间
- 节点 ID 和元数据信息

### MPC 组管理

**显示组详细信息：** 组成员、阈值、公钥、协议类型等。

### 密钥共享状态检查（定期签名）

**使用本地密钥共享文件进行签名**，无需完整的 MPC 程序即可验证共享文件的完整性。**
- 如果未提供消息，系统会自动生成签名文件：`checkup-YYYY-MM-DD`
- **建议**：每周执行一次，或在基础设施发生变更后执行
- 该操作仅限于本地，无需网络连接或 WebSocket。

### 灾难恢复导出

**将加密后的密钥共享文件导出到指定目录：`~/.cobo-tss-node/recovery/YYYYMMDD-HHMMSS/`**
- 导出的文件是加密的，需要数据库密码才能恢复数据
- **建议**：每次生成新密钥或重新共享密钥后执行此操作，并将备份文件存储在异地。

### 备份

**在 `~/.cobo-tss-node/backups/YYYYMMDD-HHMMSS/` 目录下创建备份文件，包含：**
- `secrets.db`（加密的数据库文件，包含密钥共享信息和会话数据）
- `cobo-tss-node-config.yaml`（配置文件）
- `.password`（密钥文件）
- `SHA256SUMS`（文件完整性校验码）

**注意**：请妥善保管备份文件，其中包含恢复节点所需的所有数据。

### 更新二进制文件

**操作步骤：**
1. 停止服务
2. 将当前二进制文件备份为 `cobo-tss-node.bak`
3. 下载并安装新版本
4. （如有需要）执行数据库迁移
5. 重启服务
6. 显示新版本信息

### 数据库迁移

**在二进制文件更新后执行此操作。`update` 命令会自动完成迁移。**

### 更改密码

**更改数据库加密密码，同时更新 `.password` 文件的权限。**

### 卸载服务

**删除 systemd/launchd 服务，但会保留 `~/.cobo-tss-node/` 目录下的所有数据。** 如需彻底删除节点，请执行 `rm -rf ~/.cobo-tss-node`。

## 推荐的维护计划

| 任务 | 周期 | 命令 |
|------|-----------|---------|
| 状态检查 | 每日 | `node-ctl.sh health` |
| 密钥共享状态检查 | 每周 | `node-ctl.sh sign <group-id>` |
| 备份 | 每周 | `node-ctl.sh backup` |
| 日志审查 | 每周 | `node-ctl.sh logs --lines=500` |
| 密钥共享文件导出 | 生成新密钥或重新共享后 | `node-ctl.sh export <group-ids>` |
| 二进制文件更新 | 新版本发布时 | `node-ctl.sh update` |
| 密码更新 | 每季度 | `node-ctl.sh change-password` |

## 配置文件参考

配置文件位于：`~/.cobo-tss-node/configs/cobo-tss-node-config.yaml`

**关键配置项：**
- **`env`**：开发模式（development）/生产模式（production）
- **`db.path`**：数据库文件路径
- **`callback.cb_server`**：风险控制回调 URL 及公钥（版本 1）
- **`callback.cb_server_v2`**：风险控制回调 URL 及公钥（版本 2）
- **`event.server`**：事件发布地址（用于密钥生成/签名/重新共享通知）
- **`embedded_risk_control_rules`**：密钥生成、签名、重新共享的本地允许/拒绝规则
- **`log`**：日志输出方式及配置
- **`metrics`：InfluxDB 监控端点

## 目录结构

```
~/.cobo-tss-node/
├── cobo-tss-node                    # binary
├── cobo-tss-node.bak               # previous binary (after update)
├── .password                        # key file (chmod 600)
├── configs/
│   ├── cobo-tss-node-config.yaml           # active config
│   └── cobo-tss-node-config.yaml.template  # template reference
├── db/
│   └── secrets.db                   # AES-GCM encrypted database
├── logs/                            # log files
├── recovery/                        # exported key shares
│   └── YYYYMMDD-HHMMSS/
└── backups/                         # full backups
    └── YYYYMMDD-HHMMSS/
        ├── secrets.db
        ├── cobo-tss-node-config.yaml
        ├── .password
        └── SHA256SUMS
```

## 关键文件相关设置

- 所有非交互式操作命令中都使用了 `--key-file` 参数（服务模式必需）
- 数据库采用 AES-GCM 加密；`.password` 文件的权限必须设置为 600
- Linux 服务运行时启用 `NoNewPrivileges`、`ProtectSystem=strict`，并限制读写路径（仅允许访问 `db`、`logs`、`recovery` 目录）
- macOS 代理通过 `KeepAlive` 和 `ThrottleInterval` 功能在故障时自动重启
- 备份文件包含 SHA256 校验码以确保数据完整性

## 故障排除

| 故障现象 | 原因 | 解决方法 |
|---------|-------|-----|
| 服务无法启动 | 配置文件缺失 | 使用 `cp configs/*.template/configs/cobo-tss-node-config.yaml` 复制配置文件 |
- 启动时出现 “password” 提示 | 未指定 `--key-file` 参数 | 重新安装服务：`install-service.sh linux` |
- 访问 `.password` 文件时权限被拒绝 | 文件权限设置错误 | 使用 `chmod 600 ~/.cobo-tss-node/.password` 更改权限 |
- 初始化失败 | 数据库已存在 | 使用 `node-info.sh` 检查；如确实需要删除数据库文件，请执行 `db/secrets.db` |
- WebSocket 连接失败 | 环境设置错误 | 根据实际环境选择正确的参数（`--dev`/`--sandbox`/`--prod`） |
- 服务立即退出 | 端口冲突或资源占用 | 查看 `node-ctl.sh logs` 以获取错误详情 |
- 迁移失败 | 版本不兼容 | 先尝试 `migrate --dry-run`；如问题持续存在，请联系 Cobo 技术支持 |