# Dropbox Manager Skill

通过MCP服务器和CLI管理Dropbox文件。该功能采用Swift原生实现，基于SwiftyDropbox SDK，并支持OAuth 2.0的PKCE认证机制以及安全的Keychain令牌存储。

## 设置

### 先决条件

```bash
# Clone and build Dropbook
git clone https://github.com/RyanLisse/Dropbook.git
cd Dropbook
make build
```

### 认证

#### 选项1：使用Keychain进行OAuth登录（推荐）

使用带有安全Keychain存储功能的交互式OAuth流程：

```bash
export DROPBOX_APP_KEY="your_dropbox_app_key"
export DROPBOX_APP_SECRET="your_dropbox_app_secret"
make login
# or: swift run dropbook login
```

此过程将：
1. 生成PKCE代码验证器和挑战码（SHA256格式，符合RFC 7636标准）
2. 打开一个包含状态参数的授权URL（具有CSRF保护机制）
3. 提示用户粘贴授权码
4. 将代码兑换为访问令牌和刷新令牌
5. **将令牌保存到macOS的Keychain中**（采用硬件加密方式）
6. 如果Keychain不可用，会回退到`~/.dropbook/auth.json`文件中存储令牌
7. 启用令牌的自动刷新功能

**安全特性（符合RFC 9700标准）：**
- 使用PKCE和S256挑战码机制
- 通过状态参数实现CSRF保护
- 令牌存储采用`kSecAttrAccessibleWhenUnlocked`属性
- 使用CryptoKit进行加密操作

#### 选项2：使用环境变量（旧版本）

```bash
export DROPBOX_APP_KEY="your_dropbox_app_key"
export DROPBOX_APP_SECRET="your_dropbox_app_secret"
export DROPBOX_ACCESS_TOKEN="your_dropbox_access_token"
```

**注意**：手动生成的令牌不支持自动刷新。在生产环境中请使用OAuth登录方式。

### 登出

从Keychain和文件存储中清除所有保存的令牌：

```bash
make logout
# or: swift run dropbook logout
```

## MCP服务器（推荐）

启动MCP服务器：

```bash
make mcp
# or: ./.build/debug/dropbook mcp
```

### MCP工具

| 工具 | 描述 |
|------|-------------|
| `list_directory` | 列出Dropbox目录中的文件和文件夹 |
| `search` | 按名称或内容搜索文件 |
| `upload` | 将文件上传到Dropbox |
| `download` | 从Dropbox下载文件 |
| `delete` | 删除文件或文件夹（文件会被移至回收站） |
| `get_account_info` | 获取账户名称和电子邮件 |
| `read_file` | 读取文本文件的内容 |

#### list_directory

列出Dropbox目录中的文件和文件夹。

**参数：**
- `path`（字符串，可选）：目录路径。默认值："/"

**响应：**
```json
{
  "files": [
    {"type": "file", "name": "doc.pdf", "path": "/Docs/doc.pdf", "size": 1024},
    {"type": "folder", "name": "Projects", "path": "/Projects"}
  ]
}
```

#### search

按名称或内容搜索文件。

**参数：**
- `query`（字符串，必填）：搜索关键字
- `path`（字符串，可选）：搜索范围路径。默认值："/"

**响应：**
```json
{
  "count": 2,
  "results": [
    {"matchType": "filename", "metadata": {"name": "report.pdf", "path": "/Docs/report.pdf"}}
  ]
}
```

#### upload

将文件上传到Dropbox。

**参数：**
- `localPath`（字符串，必填）：本地文件的绝对路径
- `remotePath`（字符串，必填）：Dropbox中的目标路径
- `overwrite`（布尔值，可选）：如果目标文件存在则覆盖。默认值：false

**响应：**
```json
{
  "uploaded": true,
  "name": "file.txt",
  "path": "/Uploads/file.txt",
  "size": 5000
}
```

#### download

从Dropbox下载文件。

**参数：**
- `remotePath`（字符串，必填）：Dropbox中的文件路径
- `localPath`（字符串，必填）：本地目标路径

**响应：**
```json
{
  "downloaded": true,
  "to": "/tmp/report.pdf"
}
```

#### delete

从Dropbox删除文件或文件夹（文件会被移至回收站）。

**参数：**
- `path`（字符串，必填）：要删除的文件或文件夹路径

**响应：**
```json
{
  "deleted": true,
  "path": "/Docs/old-file.pdf"
}
```

#### get_account_info

获取Dropbox账户信息。

**参数：** 无

**响应：**
```json
{
  "name": "Ryan Lisse",
  "email": "user@example.com"
}
```

#### read_file

从Dropbox读取并返回文本文件的内容。

**参数：**
- `path`（字符串，必填）：Dropbox中的文件路径

**响应：** 返回文件的文本内容。仅支持UTF-8编码的文本文件。

## CLI命令

```bash
# Authentication
make login                 # OAuth login with Keychain storage
make logout                # Clear stored tokens

# File operations
make list                  # List root directory
swift run dropbook list /path

# Search files
swift run dropbook search "query" [path]

# Upload file
swift run dropbook upload /local/path /remote/path [--overwrite]

# Download file
swift run dropbook download /remote/path /local/path

# Start MCP server
make mcp
```

## MCP客户端配置

### Claude代码（项目级）

项目中包含一个`.mcp.json`文件，用于配置MCP服务器：

```json
{
  "mcpServers": {
    "dropbox": {
      "command": "/path/to/Dropbook/.build/debug/dropbook",
      "args": ["mcp"],
      "env": {
        "DROPBOX_APP_KEY": "${DROPBOX_APP_KEY}",
        "DROPBOX_APP_SECRET": "${DROPBOX_APP_SECRET}"
      }
    }
  }
}
```

在Claude Code的settings.json配置文件中启用MCP服务器：

```json
{
  "enableAllProjectMcpServers": true
}
```

### Claude桌面应用

```json
{
  "mcpServers": {
    "dropbox": {
      "command": "/path/to/dropbook/.build/debug/dropbook",
      "args": ["mcp"],
      "env": {
        "DROPBOX_APP_KEY": "${DROPBOX_APP_KEY}",
        "DROPBOX_APP_SECRET": "${DROPBOX_APP_SECRET}"
      }
    }
  }
}
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `notConfigured` | 缺少环境变量 | 设置`DROPBOX_APP_KEY`和`DROPBOX_APP_SECRET` |
| `invalidArguments` | 缺少必需的参数 | 检查工具参数是否正确 |
| `notFound` | 路径不存在 | 使用`list_directory`命令验证路径 |
| `itemNotFound` | Keychain中找不到令牌 | 运行`make login`命令进行身份验证 |

## 架构

```
Dropbook/
├── Sources/
│   ├── DropbookCore/           # Business logic (actor-based)
│   │   ├── Auth/               # Keychain & file token storage
│   │   ├── Config/             # Configuration management
│   │   ├── Models/             # Domain models
│   │   └── Services/           # DropboxService actor
│   ├── DropbookCLI/            # CLI adapter
│   │   └── Commands/           # Login, logout, file commands
│   └── DropbookMCP/            # MCP server
├── dropbox-skill/              # Skill documentation
├── Makefile                    # Build automation
├── .mcp.json                   # MCP server configuration
└── Package.swift
```

## 使用rclone进行批量操作

对于大规模操作（如备份、同步或批量传输），可以使用[rclone](https://rclone.org/)——这是一个支持Dropbox功能的强大云同步工具。

### 安装rclone

```bash
brew install rclone
```

### 配置rclone以使用Dropbox

```bash
# Interactive setup (opens browser for OAuth)
rclone authorize dropbox

# Save the token output to config
mkdir -p ~/.config/rclone
cat > ~/.config/rclone/rclone.conf << 'EOF'
[dropbox]
type = dropbox
token = {"access_token":"...paste token here..."}
EOF
```

### 将文件备份到网络驱动器或Time Capsule

```bash
# Full backup with progress
rclone copy dropbox: /Volumes/TimeCapsule/Dropbox-Backup \
    --progress \
    --transfers 4 \
    --checkers 8 \
    --retries 10 \
    --log-file /tmp/dropbox-backup.log

# Sync (mirror - deletes files not in source)
rclone sync dropbox: /Volumes/Backup/Dropbox --progress

# Check what would be copied (dry run)
rclone copy dropbox: /Volumes/Backup --dry-run
```

### 常用的rclone命令

```bash
# List remote contents
rclone lsd dropbox:              # List directories
rclone ls dropbox:               # List all files
rclone size dropbox:             # Calculate total size

# Copy operations
rclone copy dropbox:folder /local/path    # Download folder
rclone copy /local/path dropbox:folder    # Upload folder

# Sync (bidirectional)
rclone bisync dropbox: /local/path --resync

# Mount as filesystem (macOS - requires macFUSE)
rclone mount dropbox: /mnt/dropbox --vfs-cache-mode full
```

### rclone的可靠性相关选项

| 选项 | 描述 |
|------|-------------|
| `--progress` | 显示实时传输进度 |
| `--transfers 4` | 并行传输的任务数量 |
| `--checkers 8` | 并行检查的任务数量 |
| `--retries 10` | 重试失败的操作次数 |
| `--low-level-retries 20` | 重试底层错误 |
| `--log-file path` | 将日志写入指定文件 |
| `--dry-run` | 显示即将执行的操作 |
| `--checksum` | 使用校验和进行数据验证 |

### 速率限制

Dropbox对API请求有严格的速率限制。如果遇到`too_many_requests`错误：

```bash
# Use bandwidth limiting
rclone copy dropbox: /backup --bwlimit 1M

# Or add delays between operations
rclone copy dropbox: /backup --tpslimit 2
```

rclone会通过指数级退避策略自动处理速率限制问题。

## 最佳实践

1. **使用OAuth登录**：采用安全的Keychain存储方式，并启用令牌自动刷新功能。
2. **使用MCP进行程序化访问**：更可靠。
3. **使用rclone进行批量操作**：适用于备份和大规模数据传输。
4. **先验证路径**：在执行操作前使用`list_directory`命令确认路径是否存在。
5. **优雅地处理错误**：检查响应中的错误信息。
6. **遵守速率限制**：在批量操作之间添加适当的延迟。
7. **使用绝对路径**：进行文件操作时始终提供完整的路径。

## 安全性措施

- **Keychain存储**：令牌采用硬件加密方式存储。
- **PKCE**：通过代码交换机制防止授权码被截获。
- **状态参数**：提供CSRF保护。
- **令牌自动刷新**：在令牌过期前自动更新。
- **CryptoKit**：使用现代的Swift加密库。

## 所需依赖库

- **SwiftyDropbox**（v10.2.4及以上版本）：官方的Dropbox Swift SDK
- **MCP (swift-sdk)**：用于模型上下文管理的SDK
- **CryptoKit**：Apple提供的加密框架
- **rclone**（可选）：用于批量操作和备份（使用`brew install rclone`安装）

## 相关资源

- [Dropbook GitHub仓库](https://github.com/RyanLisse/Dropbook)
- [CLAUDE.md](../CLAUDE.md)：完整的项目文档
- [Dropbox API文档](https://www.dropbox.com/developers/documentation)
- [rclone官方文档](https://rclone.org/dropbox/)：关于rclone的使用说明
- [RFC 7636 - PKCE协议](https://datatracker.ietf.org/doc/html/rfc7636)
- [RFC 9700 - OAuth 2.0安全最佳实践](https://datatracker.ietf.org/doc/html/rfc9700)