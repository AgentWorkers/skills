---
name: archon
description: 完整的 Archon 分布式身份管理功能：包括本地节点管理、DID（去中心化身份）的创建、凭证的颁发、凭证库的操作以及公共网络的解析功能。
homepage: https://archon.technology
metadata:
  project: archon
  type: identity
  networks:
    - archon
    - hyperswarm
  local_node: true
---

# Archon - 去中心化身份网络

Archon 是一个开源的去中心化、自主管理的身份（SSI）系统。该技能提供了完整的 Archon 功能，包括本地节点管理、DID 操作、凭证发放、仓库管理以及公共网络访问。

## 平台支持

**跨平台（所有平台）：**
- ✅ 公共网络 API 操作（DID 解析、网络统计）
- ✅ 通过 `npx` 使用 Keymaster CLI（@didcid/keymaster）
- ✅ 仅需要 Node.js 和 curl 即可进行只读操作

**本地节点操作：**
- ✅ **Linux** - 支持原生 Docker，所有脚本均可运行
- ✅ **macOS** - 需要 Docker Desktop，脚本也可运行（部分命令有细微差异）
- ⚠️ **Windows** - 需要 WSL2 和 Docker Desktop，或使用 PowerShell 适配的原生 Docker
  - 辅助脚本使用 Bash（可以使用 Git Bash、WSL2 或适应 PowerShell）
  - 路径处理有所不同（`%USERPROFILE%` 对应 `~`）

**针对 Windows 用户的建议：**
- 使用 WSL2（Ubuntu）以实现完全兼容性
- 或者使用公共网络 API 和 keymaster CLI（跨平台）
- 可以使用 PowerShell 进行本地节点管理，但需要调整脚本

## 架构

**本地 Archon 节点：`~/bin/archon`（Docker Compose 堆栈）**
- **Keymaster**（`:4226`）- 钱包操作、DID 创建、签名
- **Gatekeeper**（`:4224`）- 公共 DID 解析、网络网关
- **IPFS**（`:5001`）- 内容可寻址存储
- **Bitcoin 节点** - 区块链锚定（signet、mainnet）
- **MongoDB/Redis** - 状态管理
- **Grafana**（`:3003`）- 统计仪表盘

**公共网络：`https://archon.technology`
- 提供对公共 DID 的只读访问
- 支持网络探索和统计

## 本地节点管理

### 节点控制

**管理脚本**（在 HexMem 中有详细说明）：
```bash
/home/sat/bin/archon-start.sh   # Start Docker Compose stack
/home/sat/bin/archon-stop.sh    # Stop Docker Compose stack
/home/sat/bin/archon-status.sh  # Full status + health checks
/home/sat/bin/archon-health.sh  # Quick health check (exit 0 if healthy)
```

**直接使用 Docker Compose：**
```bash
cd ~/bin/archon
/snap/bin/docker compose ps        # List containers
/snap/bin/docker compose logs -f   # Follow logs
/snap/bin/docker compose up -d     # Start services
/snap/bin/docker compose down      # Stop services
```

**健康检查：**
- Keymaster API：`curl -sf http://localhost:4226/api/v1/ready`
- Gatekeeper API：`curl -sf http://localhost:4224/api/v1/ready`

### 配置

**钱包位置：`~/bin/archon/data/keymaster/wallet.json`（加密）**
**密码：`your-secure-passphrase`
**配置目录：`~/.config/hex/archon/`（其他钱包位置）

**环境设置：**
```bash
export ARCHON_CONFIG_DIR="$HOME/.config/hex/archon"
export ARCHON_PASSPHRASE="your-secure-passphrase"
export ARCHON_GATEKEEPER_URL="http://localhost:4224"  # or https://archon.technology
export ARCHON_WALLET_PATH="$HOME/bin/archon/data/keymaster/wallet.json"
```

## 本地节点操作（Keymaster CLI）

`@didcid/keymaster` CLI 提供完整的钱包操作。请始终从配置目录运行该命令：

### 身份管理

**列出钱包中的身份：**
```bash
cd ~/.config/hex/archon
npx @didcid/keymaster list-ids
```

**创建新的 DID：**
```bash
npx @didcid/keymaster create-id \
  --name "identity-name" \
  --type agent  # or asset
```

**解析 DID（本地）：**
```bash
npx @didcid/keymaster resolve-id did:cid:bagaaiera...
```

**导出 DID 文档：**
```bash
npx @didcid/keymaster get-did did:cid:bagaaiera...
```

### 可验证的凭证

**发放凭证：**
```bash
npx @didcid/keymaster issue-credential \
  --issuer-did did:cid:... \
  --subject-did did:cid:... \
  --type IdentityLink \
  --claims '{"nostr_npub":"npub1...","platform":"nostr"}'
```

**列出发放给我的凭证：**
```bash
npx @didcid/keymaster list-credentials
```

**获取凭证详情：**
```bash
npx @didcid/keymaster get-credential did:cid:...
```

**验证凭证：**
```bash
npx @didcid/keymaster verify-credential did:cid:...
```

### 仓库操作

**列出仓库：**
```bash
npx @didcid/keymaster list-vaults
```

**创建仓库：**
```bash
npx @didcid/keymaster create-vault \
  --name "vault-name" \
  --owner-did did:cid:...
```

**向仓库添加项目：**
```bash
npx @didcid/keymaster vault-put \
  --vault-id vault-name \
  --key "item-key" \
  --value "item-value" \
  --metadata '{"type":"backup","timestamp":"2026-02-03"}'
```

**列出仓库项目：**
```bash
npx @didcid/keymaster list-vault-items vault-name
```

**从仓库获取项目：**
```bash
npx @didcid/keymaster vault-get \
  --vault-id vault-name \
  --key "item-key"
```

**从仓库检索文件：**
```bash
npx @didcid/keymaster vault-get \
  --vault-id vault-name \
  --key "item-key" \
  --output /path/to/file
```

### 组织操作

**创建组：**
```bash
npx @didcid/keymaster create-group \
  --name "daemon-collective" \
  --owner-did did:cid:... \
  --members did:cid:member1,did:cid:member2
```

**获取组信息：**
```bash
npx @didcid/keymaster get-group daemon-collective
```

**向组添加成员：**
```bash
npx @didcid/keymaster add-group-member \
  --group-id daemon-collective \
  --member-did did:cid:...
```

### 文档签名

**签名任意数据：**
```bash
echo "data to sign" | npx @didcid/keymaster sign \
  --did did:cid:... \
  --output signature.json
```

**验证签名：**
```bash
npx @didcid/keymaster verify \
  --signature signature.json \
  --data "data to sign"
```

## 辅助脚本

位置：`~/clawd/skills/archon/scripts/`

### 公共网络脚本

**archon-resolve.sh** - 从公共节点解析 DID
```bash
~/clawd/skills/archon/scripts/archon-resolve.sh did:cid:bagaaiera...
```

**archon-status.sh** - 公共节点网络统计
```bash
~/clawd/skills/archon/scripts/archon-status.sh
```

### 本地节点脚本

**archon-create-did.sh** - 使用本地节点创建新的 DID
```bash
~/clawd/skills/archon/scripts/archon-create-did.sh "name" "agent"
```

**archon-issue-credential.sh** - 发放可验证的凭证
```bash
~/clawd/skills/archon/scripts/archon-issue-credential.sh \
  did:cid:issuer... \
  did:cid:subject... \
  "CredentialType" \
  '{"key":"value"}'
```

**archon-vault-backup.sh** - 备份到仓库
```bash
~/clawd/skills/archon/scripts/archon-vault-backup.sh \
  vault-name \
  /path/to/file \
  backup-key
```

**archon-vault-list.sh** - 列出仓库内容
```bash
~/clawd/skills/archon/scripts/archon-vault-list.sh vault-name
```

## HexMem 集成

Archon 的操作在 HexMem 中有详细记录：

```bash
source ~/clawd/hexmem/hexmem.sh

# Query Archon facts
hexmem_select "SELECT predicate, object_text FROM facts WHERE subject_entity_id = 10;"

# Log Archon events
hexmem_event "identity" "archon" "Created new DID" "did:cid:..."

# Record lessons
hexmem_lesson "identity" "Always encrypt vault items with meaningful metadata" "..."
```

**自动仓库备份**（参见 `~/clawd/hexmem/SKILL.md`）：
- HexMem 数据库：每天凌晨 3 点（MST 时间）备份到 `hexmem-vault`
- 凭证：每月 1 日凌晨 3 点（MST 时间）备份到 `hexmem-vault`

## 使用场景

**身份操作：**
- 为新代理/项目创建 DID
- 发放证明能力的凭证
- 跨平台身份链接（Nostr ↔ Archon）
- 加密身份证明

**安全存储：**
- 将数据加密后存储在 Archon 仓库中
- 分布式凭证存储
- 配置版本控制（加密）
- 通过 IPFS 进行灾难恢复

**组织协调：**
- 使用共享凭证的守护进程集体
- 用于协作工作的组仓库
- 基于角色的访问控制
- 多代理协调协议

**网络探索：**
- 解析其他代理的 DID
- 验证凭证链
- 探索去中心化身份网络
- 监控网络健康状况

## 跨平台使用

### 对于不同平台的 AI 代理

**公共网络 API（所有平台）：**
```bash
# Works everywhere with curl/web_fetch
curl -s "https://archon.technology/api/v1/did/did:cid:..." | jq '.'
```

**Keymaster CLI（支持 Node.js 的所有平台）：**
```bash
# Cross-platform via npx
cd ~/.config/archon  # or %USERPROFILE%\.config\archon on Windows
npx @didcid/keymaster list-ids
npx @didcid/keymaster list-credentials
```

**平台特定注意事项：**

**Linux：**
- 支持原生 Docker
- 所有辅助脚本均可直接使用
- 推荐用于生产环境

**macOS：**
- 需要 Docker Desktop
- 辅助脚本可用（自动检测 BSD 和 GNU 命令）
- `detect-platform.sh` 脚本会自动调整 `stat` 和 `sha256sum` 命令

**Windows：**
- **推荐方案 1：** 使用 WSL2 和 Docker Desktop
  - 完全兼容 Linux
  - 所有脚本均可正常运行
  - 最佳的开发体验

- **方案 2：** 使用原生 Windows 和 Git Bash
  - 可通过 `npx` 使用 Keymaster CLI
  - 辅助脚本在 Git Bash 中可用
  - 可能需要调整 Docker 命令的路径

- **方案 3：** 使用 PowerShell 适配
  - 用 PowerShell 重写脚本
  - 使用 `Get-FileHash`、`Get-Content` 和 Docker Desktop CLI
  - 例如：`docker compose` 的使用方式不变

**跨平台环境设置：**
```bash
# Linux/macOS/WSL2
export ARCHON_CONFIG_DIR="$HOME/.config/archon"
export ARCHON_PASSPHRASE="your-passphrase"

# Windows PowerShell
$env:ARCHON_CONFIG_DIR = "$env:USERPROFILE\.config\archon"
$env:ARCHON_PASSPHRASE = "your-passphrase"
```

**辅助脚本平台检测：**
`detect-platform.sh` 脚本会自动检测操作系统并设置：
- `$STAT_SIZE` - 适合平台的统计命令
- `$CHECKSUM_CMD` - sha256sum（Linux/Git Bash）或 `shasum`（macOS）
- `$DOCKER_CMD` - Docker 命令（通常是 `docker`）

## 公共网络 API

无需本地节点即可进行公共 DID 的只读访问：

**基础 URL：`https://archon.technology`

**解析 DID：**
```bash
curl -s "https://archon.technology/api/v1/did/did:cid:bagaaiera..." | jq '.'
```

**网络统计：**
```bash
curl -s "https://archon.technology" | grep -oP '"dids":\s*{[^}]+}' | jq -R 'fromjson'
```

**Web 界面：**
- DID 探索器：https://explorer.archon.technology/events
- P2P 钱包：https://wallet.archon.technology

## Hex 的 Archon 身份

**主要 DID：`did:cid:bagaaieratn3qejd6mr4y2bk3nliriafoyeftt74tkl7il6bbvakfdupahkla`

**发放的凭证：**
- Nostr 身份链接：`did:cid:bagaaierag6mj2uph22bocyfvsru32kzp5ahz4aq3kabo2pcbamjldignxapa`

**仓库：**
- `hex-vault`（`did:cid:bagaaierajb5yxhxqvzyw5yxxkvk7oaxmhgxzmsc5f3uixiwllgujoxxgmszq`）- 个人加密存储
- `hexmem-vault`（`did:cid:bagaaieratoq3bf6p24dr4gqod44wjlyzrl3dozqh3ra77ri3c6zfxs6o4pdq`）- HexMem 备份

**组：**
- `daemon-collective`（`did:cid:bagaaierausu7hgbctnkcdz66bgfxu2xfgxd5fgnf7cn2434b6cbtn73jydoa`）

## 安全实践**

**密钥管理：**
- 私钥从不离开本地机器
- 钱包使用强密码加密
- 密码安全存储在 `~/.config/hex/archon/archon.env` 中
- 密钥不会存储在 git 仓库或公开位置

**仓库安全：**
- 所有仓库项目均加密
- 通过 DID 验证访问权限
- 元数据不会泄露敏感信息
- 定期备份并验证

**网络安全：**
- 敏感操作在本地节点进行
- 公共节点仅用于只读查询
- 使用 Hyperswarm P2P 网络进行数据分发
- 通过 Bitcoin 进行数据锚定以确保数据不可篡改

## 故障排除**

**节点无响应：**
```bash
/home/sat/bin/archon-health.sh  # Check health
/home/sat/bin/archon-status.sh  # Detailed status
cd ~/bin/archon && /snap/bin/docker compose logs -f keymaster  # Check logs
```

**钱包被锁定：**
```bash
export ARCHON_PASSPHRASE="your-secure-passphrase"
# Then retry command
```

**DID 无法解析：**
- 检查是否已发布到网络（DID 在发布前仅可在本地访问）
- 验证 Gatekeeper 的连接状态
- 尝试使用公共节点：`https://archon.technology/api/v1/did/...`

**仓库访问权限被拒绝：**
- 使用 `list-ids` 验证 DID 所有权
- 检查仓库权限
- 确保使用正确的钱包

## 相关文档**

- **Archon GitHub：** https://github.com/archetech/archon
- **DID 核心规范：** https://www.w3.org/TR/did-core/
- **可验证的凭证：** https://www.w3.org/TR/vc-data-model/
- **HexMem 集成：** `~/clawd/hexmem/SKILL.md`
- **节点管理：** 详细信息在 HexMem 中（entity_id=10）

## 监控（心跳检查）

Archon 节点的健康状况每 2-4 小时通过 `HEARTBEAT.md` 进行检查：
- 容器健康状况（预期有 14 个指标）
- Keymaster API 的响应速度
- Gatekeeper API 的响应速度
- 故障时需要手动重启

---

**最后更新时间：** 2026-02-03  
**维护者：** Hex (hex@lightning-goats.com)  
**本地节点：`~/bin/archon`（Docker Compose）  
**公共节点：`archon.technology`