---
name: myopenclaw-backup-restore
description: "OpenClaw的跨平台备份与恢复功能：支持Windows、macOS和Linux系统。在任何操作系统上创建的备份都可以在其他操作系统上恢复。适用于用户需要创建数据快照、从备份中恢复数据、迁移至新机器或防止数据丢失的场景。该工具具备预恢复预览功能、自动预恢复快照机制、网关令牌保护机制以及内置的HTTP服务器（支持基于浏览器的管理）。仅需Node.js环境即可运行（无需bash、rsync或python）。"
metadata:
  openclaw:
    requires:
      bins: ["node"]
    trust: high
    permissions:
      - read: ~/.openclaw
      - write: ~/.openclaw
      - network: listen
---
# MyOpenClaw 备份与恢复 — 跨平台支持

> **属于 [MyClaw.ai](https://myclaw.ai) 开放技能生态系统的一部分。**  
> 完整文档（中文）：请参阅 [README.md](README.md)

## 快速入门

```bash
# Backup
node scripts/backup-restore.js backup

# List backups
node scripts/backup-restore.js list

# Restore (always dry-run first!)
node scripts/backup-restore.js restore <archive> --dry-run
node scripts/backup-restore.js restore <archive>
```

无需任何设置，仅需 Node.js 即可运行，且不依赖任何其他第三方库。

## 备份内容

- 工作区文件（如 MEMORY.md、SOUL.md 等）  
- 所有工作区目录（适用于多代理团队）  
- Gateway 配置信息（包括令牌、API 密钥、通道设置）  
- 所有技能相关的文件  
- 扩展程序（extensions）  
- 凭据信息及通道配对状态  
- 代理配置与会话历史记录  
- 设备信息  
- 用户身份信息  
- Cron 任务  
- Guardian 脚本  
- ClawHub 注册表  
- 任务队列（delivery queue）  
- 内存索引（memory index）  

**排除的文件：** 日志文件（logs）、node_modules 目录、.git 文件夹、媒体文件、浏览器缓存文件（.lock/.deleted.* 文件）  

详细信息请参阅 [references/what-gets-saved.md](references/what-gets-saved.md)。

## 跨平台支持

- 备份文件采用 tar.gz 格式（Windows 10+/macOS/Linux 系统原生支持该格式）；  
- 在旧版本的 Windows 系统上会自动转换为 ZIP 格式；  
- 无论使用何种操作系统生成的备份文件，都可以在任何操作系统上进行恢复。  

## 命令操作

### 备份（backup）

```bash
node scripts/backup-restore.js backup [--output-dir <dir>]
```

在 `~/openclaw-backups/` 目录下生成 `openclaw-backup_{agent}_{timestamp}.tar.gz` 文件。系统会自动保留最近 7 个备份版本。  
在非 Windows 系统上，会为备份文件设置权限（`chmod 600`）。  

### 恢复（restore）

```bash
node scripts/backup-restore.js restore <archive> [--dry-run] [--overwrite-gateway-token]
```

- **安全特性：**  
  - **`--dry-run`：仅预览备份内容，不进行实际恢复操作。  
  - **恢复前自动创建快照**：在覆盖现有数据前会自动保存当前系统状态。  
  - **保留新服务器的令牌**：确保新服务器使用的令牌与旧服务器一致（避免控制界面显示错误）。  
  - **交互式确认**：需要用户手动输入 “yes” 才能继续恢复操作。  
  - **增强凭证安全性**：在非 Windows 系统上为备份文件设置更严格的权限（`chmod 700/600`）。  
  - **自动重启**：恢复完成后会自动重启 Gateway 服务。  
  - **兼容性**：支持 v1 和 v2 版本的备份文件结构。  

### 列出备份文件（list）

```bash
node scripts/backup-restore.js list [--backup-dir <dir>]
```

## HTTP 服务器

```bash
node scripts/server.js --token <secret> [--port 7373] [--backup-dir <dir>]
```

- **Web 界面**：`http://localhost:<port>/?token=<token>`  
- **远程访问**：仅支持列出、下载和上传备份文件。  
- **本地访问**：仅支持在本地执行备份和恢复操作（shell 命令仅限于在本地主机上执行）。  
- **令牌要求**：必须提供有效的令牌才能访问服务器。  

## 安全性注意事项

备份文件中包含机器人令牌（bot tokens）、API 密钥和凭证信息，请确保这些文件得到妥善保管，切勿将其上传到公共仓库，并通过加密通道进行传输。