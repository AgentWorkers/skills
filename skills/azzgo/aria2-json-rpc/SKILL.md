---
name: aria2-json-rpc
description: 通过 JSON-RPC 2.0 与 aria2 下载管理器进行交互。可以使用自然语言命令来管理下载任务、查询下载状态以及控制下载过程。适用于 aria2 的使用、下载任务的管理或种子文件（torrent）的操作场景。
license: MIT
compatibility: Requires Python 3.6+. WebSocket support requires websockets package (pip install websockets) and Python version must match dependency requirements.
metadata:
  author: ISON
  version: "1.1.0"
---

## 该技能的功能

该技能允许您通过自然语言命令来控制 aria2 下载管理器：
- 下载文件（支持 HTTP/HTTPS/FTP/Magnet/Torrent/Metalink 协议）
- 监控下载进度和状态
- 控制下载操作（暂停、恢复、删除下载）
- 管理批量下载任务（暂停所有下载、恢复所有下载）
- 查看下载统计信息并配置相关选项

## 使用方法（针对 AI 代理）

**⚠️ 重要提示：** **切勿手动构造 JSON-RPC 请求！**  
**✅ 请始终使用 `scripts/` 目录中的 Python 脚本。**  
**⚠️ 请使用 `python3` 命令，而非 `python`（尤其是在 macOS 系统上，因为 `python` 可能不存在）**

### 工作流程（必须遵循）

**步骤 1：检查配置状态**

在执行任何 aria2 命令之前，务必先检查配置是否已准备好：
```bash
python3 scripts/config_loader.py test
```

- 如果配置成功：继续执行用户的命令。
- 如果配置失败：引导用户初始化配置（参见步骤 2）。

**步骤 2：初始化配置（如需要）**

如果连接测试失败，引导用户设置配置：
```bash
# Recommended: User config (survives skill updates)
python3 scripts/config_loader.py init --user

# Alternative: Local config (project-specific)
python3 scripts/config_loader.py init --local
```

然后指导用户使用他们的 aria2 服务器信息编辑生成的配置文件。

**步骤 3：执行用户命令**

配置完成后，执行用户请求的 aria2 操作。

### 示例工作流程

**用户：** “下载 http://example.com/file.zip”

**您执行：**
```bash
# 1. Check configuration
python3 scripts/config_loader.py test
```

如果测试通过：
```bash
# 2. Execute download command
python3 scripts/rpc_client.py aria2.addUri '["http://example.com/file.zip"]'
```

**您回复：** “✓ 下载已开始！GID: 2089b05ecca3d829”

如果测试失败：
```
Configuration not ready. Please initialize:
1. Run: python3 scripts/config_loader.py init --user
2. Edit ~/.config/aria2-skill/config.json with your aria2 server details
3. Run: python3 scripts/config_loader.py test (to verify)
```

## 文档结构

**有关详细的执行说明，请参阅：**
- **[references/execution-guide.md](references/execution-guide.md)** - 为 AI 代理提供的完整指南，内容包括：
  - 命令映射表（用户意图 → 脚本调用）
  - 参数格式规则
  - 逐步示例
  - 常见错误及避免方法
  - 响应格式指南

**有关 aria2 方法的详细信息，请参阅：**
- **[references/aria2-methods.md](references/aria2-methods.md)** - aria2 RPC 方法的详细文档

## 常用命令快速参考

| 用户意图 | 命令示例 |
|-------------|----------------|
| 下载文件 | `python3 scripts/rpc_client.py aria2.addUri '["http://example.com/file.zip"]'` |
| 检查状态 | `python3 scripts/rpc_client.py aria2.tellStatus <GID>` |
| 列出正在下载的文件 | `python3 scripts/rpc_client.py aria2.tellActive` |
| 列出已暂停的下载任务 | `python3 scripts/rpc_client.py aria2.tellStopped 0 100` |
| 暂停下载 | `python3 scripts/rpc_client.py aria2.pause <GID>` |
| 恢复下载 | `python3 scripts/rpc_client.py aria2.unpause <GID>` |
| 查看统计信息 | `python3 scripts/rpc_client.py aria2.getGlobalStat` |
| 查看版本信息 | `python3 scripts/rpc_client.py aria2.Version` |
| 清除下载结果 | `python3 scripts/rpc_client.py aria2.purgeDownloadResult` |

有关更多详细信息和使用方法，请参阅 [execution-guide.md](references/execution-guide.md)。

## 可用的脚本

- `scripts/rpc_client.py` - 主要的 RPC 调用接口脚本
- `scripts/examples/list-downloads.py` - 格式化的下载列表脚本
- `scripts/examples/pause-all.py` - 暂停所有下载的脚本
- `scripts/examples/add-torrent.py` - 添加 torrent 下载的脚本
- `scripts/examples/monitor-downloads.py` - 实时监控下载状态的脚本
- `scripts/examples/set-options.py` - 修改配置选项的脚本

## 配置设置

脚本会自动从多个来源加载配置，优先级如下（从高到低）：

### 配置优先级

1. **环境变量**（最高优先级，用于临时覆盖）：
   - `ARIA2_RPC_HOST`、`ARIA2_RPC_PORT`、`ARIA2_RPC_PATH` 等
   - 适用于 CI/CD 流程、临时配置修改和测试场景
   **注意**：仅用于参考。代理应使用配置文件进行配置。

2. **技能目录配置**（项目特定配置）：
   - 位置：`skills/aria2-json-rpc/config.json`
   - 适用于项目特定设置和本地测试
   ⚠️ **警告**：使用 `npx skills add` 更新技能时，此配置可能会丢失。

3. **用户配置目录**（全局默认配置，安全可靠） 🆕：
   - 位置：`~/.config/aria2-skill/config.json`
   - 适用于所有项目中的个人默认设置
   ✅ **安全**：在更新技能时配置不会丢失。

4. **默认配置**（localhost:6800）：
   - 适用于本地开发的默认配置

### 配置选项

- **host**：主机名或 IP 地址（默认：`localhost`）
- **port**：端口号（默认：`6800`）
- **path**：URL 路径（默认：`null`）；设置为 `/jsonrpc` 以使用标准 aria2，或设置为自定义路径以使用反向代理
- **secret**：RPC 密钥（默认：`null`）
- **secure**：是否使用 HTTPS（默认：`false`）
- **timeout**：请求超时时间（以毫秒为单位，默认：`30000`）

### 快速设置（针对 AI 代理）

**重要提示**：始终使用 Python 脚本进行配置管理，切勿直接使用 shell 命令。

**步骤 1：检查当前配置状态**
```bash
python3 scripts/config_loader.py show
```

**步骤 2：（如需要）初始化配置**

**用户配置（推荐使用，配置在更新后仍可保留）：**
```bash
python3 scripts/config_loader.py init --user
```

**项目特定配置：**
```bash
python3 scripts/config_loader.py init --local
```

**步骤 3：指导用户编辑配置文件**

初始化完成后，工具会显示配置文件的路径。指导用户使用他们的 aria2 服务器信息（主机名、端口号、密钥等）编辑配置文件。

**步骤 4：验证配置**
```bash
python3 scripts/config_loader.py test
```

**示例配置文件内容：**
```json
{
  "host": "localhost",
  "port": 6800,
  "secret": "your-secret-token",
  "secure": false,
  "timeout": 30000
}
```

### 配置管理（针对 AI 代理）

**可用于配置管理的 Python 脚本：**
```bash
# Check current configuration and source
python3 scripts/config_loader.py show

# Initialize user config (recommended - update-safe)
python3 scripts/config_loader.py init --user

# Initialize local config (project-specific)
python3 scripts/config_loader.py init --local

# Test connection to aria2 server
python3 scripts/config_loader.py test
```

**代理配置设置流程：**

1. **检查配置是否存在**：运行 `python3 scripts/config_loader.py show`
2. **如果配置缺失或无效**：引导用户运行 `python3 scripts/config_loader.py init --user`
3. **用户编辑配置**：告知用户配置文件的路径及所需字段（主机名、端口号、密钥等）
4. **验证配置**：运行 `python3 scripts/config_loader.py test`
5. **执行操作**：配置验证通过后，执行用户的 aria2 命令

### 高级配置

**反向代理设置：**

对于类似 `https://example.com:443/jsonrpc` 的反向代理设置，配置文件应包含以下内容：
```json
{
  "host": "example.com",
  "port": 443,
  "path": "/jsonrpc",
  "secret": "your-secret-token",
  "secure": true
}
```

**环境变量（仅供参考）：**

配置也可以通过环境变量进行覆盖：
- `ARIA2_RPC_HOST`：主机名
- `ARIA2_RPC_PORT`：端口号
- `ARIA2_RPC_PATH`：URL 路径
- `ARIA2_RPC_SECRET`：密钥
- `ARIA2_RPCSecure`：是否使用 HTTPS（`true` 或 `false`）

**注意**：建议使用 Python 脚本进行配置管理。环境变量的设置仅用于参考。

## 关键原则（针对 AI 代理）

1. **切勿** 手动构造 JSON-RPC 请求。
2. **始终** 通过 `python3` 使用 Bash 工具调用 Python 脚本。
3. **在执行命令前** **务必检查配置**：
   - 先运行 `python3 scripts/config_loader.py test`
   - 如果测试失败，引导用户完成配置初始化。
4. **切勿** 直接运行原始的 shell 命令（如 `mkdir`、`cat`、`export` 等）。
   - 使用 Python 脚本进行配置管理，例如 `config_loader.py init`、`config_loader.py show` 等。
5. **解析** 脚本输出并为用户提供格式化的结果。
6. **如有疑问**，请参考执行指南（execution-guide.md）。

## 支持的操作

### 下载管理
- 添加下载任务（支持 HTTP/FTP/Magnet/Torrent/Metalink 协议）
- 暂停/恢复下载（单个或全部）
- 删除下载任务
- 使用自定义选项添加下载任务

### 监控
- 检查下载状态
- 列出正在下载、等待或已暂停的下载任务
- 获取全局统计信息
- 实时监控下载进度

### 配置管理
- 获取/修改下载选项
- 获取/修改全局配置选项
- 查询 aria2 的版本信息
- 列出所有可用的方法

### 维护
- 清除下载结果
- 删除特定的下载任务

**需要帮助？**

- **执行详情**：[references/execution-guide.md](references/execution-guide.md)
- **方法参考**：[references/aria2-methods.md](references/aria2-methods.md)
- **故障排除**：[references/troubleshooting.md](references/troubleshooting.md)
- **aria2 官方文档**：https://aria2.github.io/