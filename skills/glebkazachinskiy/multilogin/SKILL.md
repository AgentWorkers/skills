---
name: multilogin
description: >
  **使用说明：**  
  当您需要管理 Multilogin X 浏览器配置文件时，可以使用 xcli CLI 工具来执行以下操作：  
  - 启动临时配置文件；  
  - 列出已保存的配置文件；  
  - 启动/停止已保存的配置文件；  
  - 检查启动器的状态。
metadata: { "openclaw": { "emoji": "🌐", "requires": { "bins": ["xcli", "mlx-launcher"] } } }
---
# Multilogin X

通过 `xcli` 命令行工具来管理反检测浏览器配置文件。

## 重要提示：**启动器必须先运行**

在任何 `xcli` 命令（`login` 除外）执行之前，`mlx-launcher` 进程必须已经运行。如果跳过这一步，将会出现“连接被拒绝”或“启动器未激活”的错误。

---

## 安装

### 版本获取

两个二进制文件都有一个 `/latest` 端点，可以获取当前版本信息：

```
https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/latest       → e.g. "0.0.72"
https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/latest   → e.g. "1.75.0"
```

下载链接遵循以下模式：

```
https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/{VERSION}/xcli_{PLATFORM}
https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/{VERSION}/launcher-{PLATFORM}
```

**平台对应文件名：**

| 平台 | xcli | mlx-launcher |
|------|------|--------------|
| Linux x64 | `xcli_linux_amd64` | `launcher-linux_amd64.bin` |
| macOS x64 | `xcli_darwin_amd64` | `launcher-darwin_amd64.bin` |
| macOS ARM | `xcli_darwin_arm64` | `launcher-darwin_arm64.bin` |
| Windows | `xcli_windows_amd64.exe` | `launcher-windows_amd64.exe` |

### 在 Linux（VPS / Docker）上安装

```bash
# Resolve latest versions
CLI_VER=$(curl -sL "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/latest")
LAUNCHER_VER=$(curl -sL "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/latest")
echo "Installing xcli $CLI_VER, launcher $LAUNCHER_VER"

# Download binaries
curl -L -o /usr/local/bin/xcli "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/${CLI_VER}/xcli_linux_amd64"
curl -L -o /usr/local/bin/mlx-launcher "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/${LAUNCHER_VER}/launcher-linux_amd64.bin"

# Make executable
chmod +x /usr/local/bin/xcli /usr/local/bin/mlx-launcher

# Verify
xcli --help
mlx-launcher --help
```

### 在 macOS 上安装

```bash
# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
  SUFFIX="darwin_arm64"
else
  SUFFIX="darwin_amd64"
fi

# Resolve latest versions
CLI_VER=$(curl -sL "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/latest")
LAUNCHER_VER=$(curl -sL "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/latest")
echo "Installing xcli $CLI_VER, launcher $LAUNCHER_VER"

# Download binaries
curl -L -o /usr/local/bin/xcli "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/${CLI_VER}/xcli_${SUFFIX}"
curl -L -o /usr/local/bin/mlx-launcher "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/${LAUNCHER_VER}/launcher-${SUFFIX}.bin"

# Make executable
chmod +x /usr/local/bin/xcli /usr/local/bin/mlx-launcher

# macOS may quarantine downloaded binaries — remove the flag
xattr -d com.apple.quarantine /usr/local/bin/xcli 2>/dev/null
xattr -d com.apple.quarantine /usr/local/bin/mlx-launcher 2>/dev/null

# Verify
xcli --help
mlx-launcher --help
```

### 在 Windows 上安装

```powershell
# Resolve latest versions
$CLI_VER = (Invoke-WebRequest -Uri "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/latest").Content.Trim()
$LAUNCHER_VER = (Invoke-WebRequest -Uri "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/latest").Content.Trim()
Write-Host "Installing xcli $CLI_VER, launcher $LAUNCHER_VER"

# Download binaries
Invoke-WebRequest -Uri "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/${CLI_VER}/xcli_windows_amd64.exe" -OutFile "$env:USERPROFILE\xcli.exe"
Invoke-WebRequest -Uri "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/${LAUNCHER_VER}/launcher-windows_amd64.exe" -OutFile "$env:USERPROFILE\mlx-launcher.exe"

# Add to PATH (current session)
$env:PATH += ";$env:USERPROFILE"
```

---

## 环境检测

在运行命令之前，请先检测您的操作系统环境：

```bash
# Am I in Docker?
if [ -f /.dockerenv ]; then
  echo "DOCKER"
else
  echo "BARE METAL"
fi
```

两种环境都使用相同的 `xcli` 和 `mlx-launcher` 二进制文件，确保这些文件已经添加到系统的 `PATH` 环境变量中。

---

## 无界面模式（VPS / Docker）

这是主要的使用模式，不显示任何界面，所有操作都在后台进行。

### 第一步：启动启动器

```bash
mlx-launcher -port 45000 &
sleep 5
```

### 验证

```bash
xcli launcher-info
```

在继续之前，您必须看到版本号。如果出现错误，请等待片刻后重试。

### 第二步：登录

```bash
xcli login --username 'USER@EMAIL' --password 'PASSWORD'
```

如果用户未提供登录凭据，系统会请求输入凭据。令牌的有效期为约 24 小时，存储在 `~/.config/xcli/` 目录下。

### 第三步：启动临时配置文件

临时配置文件使用完毕后会被自动删除。

```bash
xcli profile-quick --browser-type mimic --os-type linux --automation puppeteer --headless
```

启动两个临时配置文件：

```bash
xcli profile-quick --browser-type mimic --os-type linux --automation puppeteer --headless
xcli profile-quick --browser-type mimic --os-type linux --automation puppeteer --headless
```

每个配置文件会返回一个 ID 和一个用于 Puppeteer/Selenium 自动化的端口。

### 无界面模式的使用限制：

- **必须** 使用 `--headless` 参数，因为没有显示服务器。
- **必须** 使用 `--os-type linux` 参数，以确保与操作系统匹配。
- **必须** 使用 `--browser-type mimic` 参数，因为 `stealthfox` 在 Linux 上不可用。
- **不要** 使用 `profile-create` 命令来创建临时会话，应使用 `profile-quick`。
- **不要** 使用 `&` 在后台运行 `xcli` 命令（只能使用 `mlx-launcher`）。

---

## 带界面的模式（macOS / Windows / Linux）

在带有显示器的设备上（例如 Mac 机器），配置文件可以打开可见的浏览器窗口。

### 第一步：启动启动器

```bash
mlx-launcher -port 45000 &
sleep 5
xcli launcher-info
```

### 第二步：登录

```bash
xcli login --username 'USER@EMAIL' --password 'PASSWORD'
```

### 第三步：启动配置文件（带界面）

在 macOS 上：

```bash
xcli profile-quick --browser-type mimic --os-type macos --automation puppeteer
xcli profile-quick --browser-type stealthfox --os-type macos --automation puppeteer
```

在 Windows 上：

```bash
xcli profile-quick --browser-type mimic --os-type windows --automation puppeteer
xcli profile-quick --browser-type stealthfox --os-type windows --automation puppeteer
```

**注意：** 由于没有使用 `--headless` 参数，浏览器窗口将是可见的。

### 带界面的模式使用限制：

- `--os-type` 参数必须与实际操作系统匹配（`macos`、`windows` 或 `linux`）。
- 在 macOS 和 Windows 上都可以使用 `mimic`（Chromium）和 `stealthfox`（Firefox）浏览器。
- 在带有界面的 Linux 系统上，只能使用 `mimic` 浏览器。

---

## 通过 OpenClaw Node（VPS 与 Mac 的混合模式）实现图形界面

这是最优雅的设置方式：VPS 24/7 运行无界面模式，Mac 机器根据需要处理图形界面任务。

### 架构

```
VPS (OpenClaw main agent, 24/7, headless)
  ↕ paired via gateway
Mac (OpenClaw Node, paired device)
  → runs Multilogin with visible browser windows
  → VPS delegates GUI tasks here
```

### 何时使用 VPS：

- 用于无界面的临时配置文件（自动化、爬取、批量任务）
- 所有非图形界面的操作

### 何时使用 Mac 机器：

- 当用户需要查看浏览器界面（例如进行视觉检查或手动操作）时
- 当任务需要显示界面（如 CAPTCHA 验证）时
- 当需要使用 `stealthfox` 浏览器时（在 Linux 上不可用）
- 当需要可视化调试配置文件时

### 如何将任务委托给 Mac 机器：

从 VPS 的主代理程序使用 `sessions_spawn` 命令将任务发送到 Mac 机器：

```json
{
  "tool": "sessions_spawn",
  "agentId": "node-mac",
  "message": "Start the Multilogin launcher and launch 2 quick profiles with GUI. Use: mlx-launcher -port 45000 & sleep 5 && xcli login --username 'USER' --password 'PASS' && xcli profile-quick --browser-type mimic --os-type macos --automation puppeteer && xcli profile-quick --browser-type stealthfox --os-type macos --automation puppeteer"
}
```

Mac 机器将：
1. 在本地启动启动器
2. 使用提供的凭据登录
3. 启动带有可见浏览器窗口的配置文件
4. 返回配置文件的 ID 和端口信息

### Mac 机器的安装要求：

- Mac 机器的 `PATH` 环境变量中必须包含 `xcli` 和 `mlx-launcher` 二进制文件（参见上述在 macOS 上的安装说明）
- 需要能够访问 Multilogin API（网址：signin.multilogin.com）
- OpenClaw Node 必须正在运行，并且与 VPS 服务器连接

---

## 完整的 `xcli` 命令参考

### 常用命令

| 命令 | 功能 |
|---------|-------------|
| `login` | 登录到您的账户 |
| `launcher-info` | 查看正在运行的启动器的信息 |
| `help` | 查看所有命令的帮助文档 |

### 文件夹操作

| 命令 | 功能 |
|---------|-------------|
| `create-folder` | 创建指定名称的文件夹 |
| `list-folder` | 查看所有可用文件夹 |
| `remove-folder` | 根据 ID 删除文件夹 |
| `update-folder` | 根据 ID 更新文件夹信息 |

### 工作空间操作

| 命令 | 功能 |
|---------|-------------|
| `list-workspace` | 查看所有可用工作空间 |
| `switch-workspace` | 切换到不同的工作空间 |

### 代理设置

| 命令 | 功能 |
|---------|-------------|
| `proxy-countries` | 列出代理服务支持的国家和地区 |
| `proxy-regions` | 根据国家代码获取代理区域 |
| `proxy-cities` | 根据区域代码获取代理城市 |
| `proxy-get` | 根据参数获取代理 URL |

### 配置文件操作

| 命令 | 功能 |
|---------|-------------|
| `profile-quick` | 启动一个临时的配置文件（使用 v4 API） |
| `profile-create` | 创建一个新的持久性配置文件 |
| `profile-template` | 创建一个新的浏览器配置文件模板 |
| `profile-start` | 根据 ID 启动配置文件 |
| `profile-stop` | 根据 ID 停止配置文件 |
| `profile-list` | 列出指定文件夹中的配置文件 |
| `profile-stat` | 查看当前正在运行的配置文件的统计信息 |
| `profile-status` | 查看指定配置文件的状态 |
| `profile-update` | 更新现有配置文件 |
| `profile-clone` | 复制配置文件 |
| `profile-move` | 将配置文件移动到其他文件夹 |
| `profile-remove` | 根据 ID 删除配置文件 |
| `profile-restore` | 从回收站恢复被删除的配置文件 |
| `profile-export` | 将配置文件导出为文件 |
| `profile-export-status` | 查看配置文件导出状态 |
| `profile-import` | 从文件导入配置文件 |
| `profile-import-status` | 查看配置文件导入状态 |
| `profile-cookie-import` | 将 Cookie 导入配置文件 |
| `profile-cookie-export` | 从配置文件导出 Cookie |

### 脚本操作

| 命令 | 功能 |
|---------|-------------|
| `script-list` | 列出 Script Runner 文件夹中的可用脚本 |
| `script-start` | 在配置文件中运行脚本 |
| `script-stop` | 停止正在运行的脚本 |
| `cookie-robot` | 在配置文件中启动 Cookie Robot 功能 |

### 对象操作（扩展程序、文件等）

| 命令 | 功能 |
|---------|-------------|
| `object-types` | 列出对象类型 |
| `object-list` | 查看所有对象 |
| `object-meta` | 获取对象元数据 |
| `object-create` | 创建对象（需要启动代理程序） |
| `object-download` | 将对象下载到本地存储 |
| `object-delete` | 删除对象 |
| `object-restore` | 从回收站恢复对象 |
| `object-stats` | 查看对象的使用情况 |
| `object-convert` | 在本地和云端之间转换对象存储格式 |
| `enable-object` | 为配置文件启用某个对象 |
| `disable-object` | 为配置文件禁用某个对象 |
| `object-extension-create` | 从 URL 创建扩展程序对象 |

### 标签操作

| 命令 | 功能 |
|---------|-------------|
| `create-tag` | 创建一个或多个标签 |
| `tag-list` | 列出标签（可选搜索过滤） |
| `tag-remove` | 根据 ID 删除标签 |
| `tag-assign` | 为配置文件分配标签 |
| `tag-unassign` | 从配置文件中移除标签 |

### 两步验证（2FA）

| 命令 | 功能 |
|---------|-------------|
| `enable-2fa` | 启用两步验证 |
| `view-backup-codes` | 查看备份代码 |
| `disable-2fa-for-user` | 为用户禁用两步验证 |
| `disable-2fa-for-workspace` | 为工作空间禁用两步验证 |
| `enable-2fa-for-workspace` | 为工作空间启用两步验证 |

### 账户管理

| 命令 | 功能 |
|---------|-------------|
| `referral-code` | 获取推荐码 |
| `multipoints` | 查看积分余额 |

---

## 常用命令参数说明

| 参数 | 可能的值 | 说明 |
|------|--------|-------|
| `--browser-type` | `mimic`, `stealthfox` | Linux 上只能使用 `mimic` |
| `--os-type` | `linux`, `macos`, `windows`, `android` | 必须与操作系统匹配 |
| `--automation` | `puppeteer`, `selenium` | 用于指定自动化工具 |
| `--headless` | （无默认值） | 无界面模式下必须使用 |
| `--proxy-string` | `host:port:user:pass` | 可选的代理配置 |
| `--proxy-type` | `http`, `https`, `socks5` | 使用代理时必须指定 |
| `--core-version` | 例如 `144.4` | 指定浏览器版本 |

---

## 故障排除

| 错误 | 原因 | 解决方法 |
|---------|-------|-----|
| “连接被拒绝”/“启动器未激活” | 启动器未运行 | 执行 `mlx-launcher -port 45000 &` 然后 `sleep 5` |
| “找不到浏览器版本” | 操作系统或浏览器类型不匹配 | 在 Linux 上使用 `--browser-type mimic --os-type linux` |
| “上下文超时” | 启动器正在下载浏览器核心文件（首次运行时） | 等待 30-60 秒后重试，核心文件会缓存 |
| “令牌无效” | 未登录 | 重新执行 `xcli login` |
| 需要图形界面但在 VPS 上 | 无显示服务器 | 通过 `sessions_spawn` 将任务委托给 Mac 机器 |
| macOS 上出现 “unidentified developer” 错误 | 可能是 Gatekeeper 防病毒机制导致的隔离 | 运行 `xattr -d com.apple.quarantine <binary>`