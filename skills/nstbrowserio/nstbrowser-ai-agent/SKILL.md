---
name: nstbrowser-ai-agent
description: >
  这是一个用于AI代理的浏览器自动化命令行工具（CLI），集成了NSTbrowser功能。当用户需要执行高级的浏览器指纹识别、浏览器配置文件管理、代理设置、批量操作多个浏览器配置文件，或者针对大型数据集进行基于光标的分页处理时，可以使用该工具。该工具支持以下命令：  
  - `use NST profile`：使用指定的NST配置文件  
  - `configure proxy for profile`：为指定配置文件配置代理设置  
  - `manage browser profiles`：管理所有浏览器配置文件  
  - `batch update profiles`：批量更新所有浏览器配置文件  
  - `start multiple browsers`：同时启动多个浏览器  
  - `list profiles with pagination`：以分页方式列出所有浏览器配置文件  
  - 以及任何需要利用NSTbrowser反检测功能的操作。
allowed-tools: Bash(npx nstbrowser-ai-agent:*), Bash(nstbrowser-ai-agent:*)
---
# 使用 nstbrowser-ai-agent 进行浏览器自动化

## 概述

本技能允许 AI 代理通过 nstbrowser-ai-agent CLI 和 Nstbrowser 的集成来控制浏览器。Nstbrowser 提供了高级的浏览器指纹识别、配置文件管理和反检测功能，以支持专业的浏览器自动化任务。

**该工具需要 Nstbrowser 服务才能正常运行。** 所有的浏览器操作都是通过 Nstbrowser 的配置文件来执行的，这些配置文件提供了以下功能：
- 高级的浏览器指纹识别和反检测机制
- 支持持久会话的配置文件管理
- 每个配置文件都可以设置代理
- 可以对多个配置文件进行批量操作
- 支持对配置文件进行标签和分组管理

## 先决条件

在使用此工具之前，请确保满足以下条件：

### 1. 安装 Nstbrowser 客户端

必须在您的系统上安装并运行 Nstbrowser 客户端。

- 从以下链接下载：https://www.nstbrowser.io/
- 安装客户端应用程序
- 启动 Nstbrowser 客户端

### 2. Nstbrowser 服务正在运行

Nstbrowser 的 API 服务必须能够被访问：

- 默认端点：`http://127.0.0.1:8848`
- 使用 CLI 验证服务是否正在运行：
  ```bash
  nstbrowser-ai-agent profile list
  ```
- 预期响应：配置文件列表或空列表

### 3. 配置 API 密钥

从 Nstbrowser 控制面板获取您的 API 密钥并进行配置：

**方法 1：配置文件（推荐）**
```bash
nstbrowser-ai-agent config set key YOUR_API_KEY
```

**方法 2：环境变量**

在您的 shell 配置文件中设置 NST_API_KEY 环境变量。

### 4. 安装 nstbrowser-ai-agent CLI

安装 nstbrowser-ai-agent CLI：
```bash
# Using npx (no installation required)
npx nstbrowser-ai-agent --help

# Or install globally
npm install -g nstbrowser-ai-agent
```

### 5. 验证安装

测试您的设置：

```bash
# Check CLI version
nstbrowser-ai-agent --version

# List profiles (verifies API connection)
nstbrowser-ai-agent profile list
```

如果您看到了配置文件列表或空列表，说明环境配置正确。

## 快速入门

通过以下示例，您可以在 5 分钟内开始使用该工具：

### 选项 1：使用临时浏览器（最快）

适用于快速测试或一次性任务：

```bash
# 1. Start temporary browser
nstbrowser-ai-agent browser start-once

# 2. Open a website
nstbrowser-ai-agent open https://example.com

# 3. Take a snapshot
nstbrowser-ai-agent snapshot -i

# 4. Close browser (auto-cleanup)
nstbrowser-ai-agent close
```

**注意：** 临时浏览器不会保存会话状态，并且在使用后会自动清除。

### 选项 2：使用配置文件（推荐用于持久会话）

适用于需要保存会话、cookie 或登录状态的任务：

```bash
# 1. List available profiles
nstbrowser-ai-agent profile list

# 2. Create a new profile (if needed)
nstbrowser-ai-agent profile create my-profile

# 3. Open browser with profile (auto-starts if not running)
nstbrowser-ai-agent open https://example.com

# 4. Interact with page
nstbrowser-ai-agent snapshot -i
nstbrowser-ai-agent click @e1

# 5. Close browser (session saved to profile)
nstbrowser-ai-agent close
```

**预期输出：**
- 配置文件列表会显示您的配置文件及其名称和 ID
- 浏览器将以无头模式打开
- 快照会显示页面结构以及元素引用（如 @e1、@e2 等）
- 会话状态会在浏览器重启后仍然保持

## 核心概念

### 配置文件

**配置文件是 Nstbrowser 自动化的基础。** 每个配置文件都是一个独立的浏览器环境，其中存储了以下内容：
- **浏览器指纹**：Canvas、WebGL、字体、屏幕分辨率、时区
- **会话数据**：Cookie、localStorage、sessionStorage
- **登录状态**：跨会话保持的认证信息
- **代理设置**：每个配置文件都可以设置不同的代理
- **浏览器配置**：用户代理、平台、语言设置

**为什么使用配置文件？**
- 为不同的任务维护独立的身份
- 在多次自动化运行之间保持登录状态
- 在不同的网站之间隔离 Cookie 和数据
- 为不同的地区配置不同的代理

### 配置文件名称与 ID

所有与配置文件相关的命令都支持配置文件名称和 ID：

**配置文件名称：**
- 更易于用户理解，便于记忆
- 例如：`my-profile`、`test-account`、`production-bot`
- 适用于：交互式操作或需要描述性名称的脚本

**配置文件 ID：**
- 采用 UUID 格式，确保唯一性
- 例如：`86581051-fb0d-4c4a-b1e3-ebc1abd17174`
- 适用于：需要使用多个配置文件的脚本编写或确保精确匹配配置文件的情况

**UUID 格式的自动检测：**
- 系统会自动检测配置文件名称中的 UUID 格式
- 如果您向 `--profile` 参数提供了一个 UUID 格式的字符串，它将被视为配置文件 ID
- 这可以防止您误创建配置文件

**配置文件解析优先级：**
1. `--profile` 参数（配置文件名称或自动检测到的 UUID 格式的 ID）
2. 如果没有指定配置文件，则使用系统默认的浏览器

**配置文件解析逻辑：**
当您为浏览器操作指定一个配置文件时：
1. **检查已运行的浏览器** - 如果有浏览器正在运行，则使用该浏览器（如果有多个浏览器，则使用最早启动的）
2. **启动浏览器** - 如果指定的配置文件不存在，则启动该配置文件
3. **创建配置文件** - 如果配置文件名称不存在，则自动创建该配置文件
4. **错误** - 如果配置文件 ID 不存在，则返回错误
5. **使用默认浏览器** - 如果没有指定配置文件，则使用临时浏览器

**重要提示：** 如果多个配置文件具有相同的名称，将使用最早启动的浏览器。

### 持久会话

一旦使用配置文件启动了一个会话，该会话将“锁定”在该浏览器实例上。后续命令将自动使用相同的浏览器，而无需重复使用 `--profile` 参数。

```bash
# First command: link session to profile
nstbrowser-ai-agent --profile my-profile open https://example.com

# Subsequent commands: Stays in 'my-profile' automatically
nstbrowser-ai-agent snapshot -i
nstbrowser-ai-agent click @e1
nstbrowser-ai-agent fill @e2 "data"
```

这使得自动化脚本更加简洁，并减少了重复指定配置文件的需要。

### 元素引用

元素通过引用（如 @e1、@e2）来标识，这使得自动化比使用 CSS 选择器更加可靠。

```bash
# Get snapshot with refs
nstbrowser-ai-agent snapshot -i

# Output shows elements with refs:
# @e1 button "Submit"
# @e2 textbox "Email"
# @e3 textbox "Password"

# Use refs to interact
nstbrowser-ai-agent fill @e2 "user@example.com"
nstbrowser-ai-agent fill @e3 "password"
nstbrowser-ai-agent click @e1
```

**注意：** 对于现代 Web 框架（React、Vue、Angular），CSS 选择器可能比元素引用更可靠。

## 配置

### 配置文件（推荐）

将配置信息持久化存储在 `~/.nst-ai-agent/config.json` 文件中：

```bash
# Set API key (required)
nstbrowser-ai-agent config set key YOUR_API_KEY

# Optional: Set custom host
nstbrowser-ai-agent config set host api.example.com

# Optional: Set custom port
nstbrowser-ai-agent config set port 9000

# View all configuration
nstbrowser-ai-agent config show

# Get specific value
nstbrowser-ai-agent config get key
```

配置信息会在会话之间保持，并且优先于环境变量。

### 环境变量

配置文件的替代方案：

```bash
# Nstbrowser API credentials (required if not using config)
# Set NST_API_KEY in your environment

# Optional: Nstbrowser API endpoint
# Set NST_HOST and NST_PORT if using custom endpoint

# Optional: Specify profile for each command
# nstbrowser-ai-agent open https://example.com --profile "my-profile"
```

**优先级：** 配置文件 > 环境变量 > 默认值

## 常用命令

### 配置文件管理

**列出所有配置文件**
```bash
# List all profiles
nstbrowser-ai-agent profile list

# List with JSON output
nstbrowser-ai-agent profile list --json

# List with pagination (for large datasets)
nstbrowser-ai-agent profile list-cursor --page-size 50
```

**显示配置文件详情**
```bash
# Show by name or ID
nstbrowser-ai-agent profile show my-profile --json
nstbrowser-ai-agent profile show 86581051-fb0d-4c4a-b1e3-ebc1abd17174 --json
```

**创建配置文件**
```bash
nstbrowser-ai-agent profile create my-profile \
  --proxy-host proxy.example.com \
  --proxy-port 8080 \
  --proxy-type http \
  --platform Windows
```

**删除配置文件**
```bash
# Delete single profile
nstbrowser-ai-agent profile delete <profile-name-or-id>

# Delete multiple profiles
nstbrowser-ai-agent profile delete id-1 id-2 id-3
```

### 浏览器控制

**启动浏览器**
```bash
# Start with profile name
nstbrowser-ai-agent browser start my-profile

# Start with profile ID
nstbrowser-ai-agent browser start 86581051-fb0d-4c4a-b1e3-ebc1abd17174

# Start temporary browser
nstbrowser-ai-agent browser start-once

# Start temporary browser
nstbrowser-ai-agent browser start-once
```

**停止浏览器**
```bash
# Stop specific browser
nstbrowser-ai-agent browser stop my-profile

# Stop all browsers
nstbrowser-ai-agent browser stop-all
```

**列出正在运行的浏览器**
```bash
nstbrowser-ai-agent browser list
```

### 页面导航

**打开 URL**
```bash
# Auto-launches browser if not running
nstbrowser-ai-agent open https://example.com
```

**导航**
```bash
nstbrowser-ai-agent back
nstbrowser-ai-agent forward
nstbrowser-ai-agent reload
```

### 页面检查

**获取快照**
```bash
# Accessibility snapshot with refs (best for AI)
nstbrowser-ai-agent snapshot -i

# Compact snapshot
nstbrowser-ai-agent snapshot -c

# Custom depth
nstbrowser-ai-agent snapshot -d 3
```

**获取页面信息**
```bash
nstbrowser-ai-agent get title
nstbrowser-ai-agent get url
```

**截图**
```bash
nstbrowser-ai-agent screenshot output.png

# Annotated screenshot with element labels
nstbrowser-ai-agent screenshot --annotate output.png
```

### 元素交互

**点击**
```bash
# Click by ref
nstbrowser-ai-agent click @e1

# Click by CSS selector
nstbrowser-ai-agent click 'button[type="submit"]'
```

**填写输入**
```bash
# Fill by ref
nstbrowser-ai-agent fill @e2 "text"

# Fill by CSS selector
nstbrowser-ai-agent fill 'input[name="email"]' "user@example.com"
```

**输入文本**
```bash
nstbrowser-ai-agent type @e3 "text"
```

**获取元素文本**
```bash
nstbrowser-ai-agent get text @e4
nstbrowser-ai-agent get text '.product-price'
```

### 等待命令

**等待元素出现**
```bash
nstbrowser-ai-agent wait 'button.submit'
```

**等待指定时间**
```bash
# Wait 3 seconds
nstbrowser-ai-agent wait 3000
```

**等待页面加载完成**
```bash
nstbrowser-ai-agent wait --load networkidle
```

### JavaScript 执行

**执行 JavaScript**
```bash
nstbrowser-ai-agent eval "document.title"
nstbrowser-ai-agent eval "document.querySelectorAll('a').length"

# Execute from stdin
echo "document.body.innerHTML" | nstbrowser-ai-agent eval --stdin
```

### 代理管理

**显示代理设置**
```bash
nstbrowser-ai-agent profile proxy show my-profile --json
```

**更新代理设置**
```bash
nstbrowser-ai-agent profile proxy update my-profile \
  --host proxy.example.com \
  --port 8080 \
  --type http \
  --username proxyuser \
  --password proxypass
```

**重置代理设置**
```bash
nstbrowser-ai-agent profile proxy reset <profile-name-or-id>
```

**批量更新代理设置**
```bash
# Batch update
nstbrowser-ai-agent profile proxy batch-update id-1 id-2 id-3 \
  --host proxy.example.com \
  --port 8080 \
  --type http

# Batch reset
nstbrowser-ai-agent profile proxy batch-reset id-1 id-2 id-3
```

## 工作流程示例

### 模式 1：基于配置文件的自动化

**用例：** 自动化需要持久登录会话或 Cookie 的任务。

```bash
# 1. List profiles to verify connection
nstbrowser-ai-agent profile list

# 2. Set profile by name
nstbrowser-ai-agent config set profile my-profile

# 3. List profiles to find target
nstbrowser-ai-agent profile list

# 4. Open browser with profile (auto-starts if not running)
nstbrowser-ai-agent open https://example.com --profile "my-profile"
nstbrowser-ai-agent open https://example.com

# 6. Get snapshot
nstbrowser-ai-agent snapshot -i

# 7. Interact with page
nstbrowser-ai-agent click @e1
nstbrowser-ai-agent fill @e2 "data"

# 8. Close (session saved to profile)
nstbrowser-ai-agent close
```

### 模式 2：批量管理配置文件

**用例：** 高效管理多个配置文件（更新代理设置、添加标签、组织配置文件）。

```bash
# Get multiple profile IDs
PROFILE_IDS=$(nstbrowser-ai-agent profile list --json | jq -r '.data.profiles[0:3] | map(.profileId) | join(" ")')

# Batch update proxy
nstbrowser-ai-agent profile proxy batch-update $PROFILE_IDS \
  --host proxy.example.com \
  --port 8080 \
  --type http

# Batch add tags
nstbrowser-ai-agent profile tags batch-create $PROFILE_IDS \
  automated:blue batch-updated:green

# Batch move to group
GROUP_ID=$(nstbrowser-ai-agent profile groups list --json | jq -r '.data.groups[0].groupId')
nstbrowser-ai-agent profile groups batch-change $GROUP_ID $PROFILE_IDS
```

### 模式 3：登录和抓取数据

**用例：** 登录到网站，导航到数据页面并提取信息。

```bash
# 1. Open login page
nstbrowser-ai-agent --profile my-profile open https://site.com/login

# 2. Wait for page to load
nstbrowser-ai-agent wait --load networkidle

# 3. Fill and submit using CSS selectors
nstbrowser-ai-agent fill 'input[placeholder="Email"]' "user@example.com"
nstbrowser-ai-agent fill 'input[type="password"]' "userpassword"
nstbrowser-ai-agent click 'button[type="submit"]'

# 4. Wait for navigation
nstbrowser-ai-agent wait --load networkidle

# 5. Navigate to target page
nstbrowser-ai-agent open https://site.com/data

# 6. Extract data
nstbrowser-ai-agent snapshot -i > data.txt
nstbrowser-ai-agent eval "document.querySelector('.info')?.textContent"

# 7. Close (session saved to profile)
nstbrowser-ai-agent close
```

## 错误处理

### 常见错误（按出现频率排序）

#### 1. “需要 NST_API_KEY”

**原因：** API 密钥未配置。

**解决方法：**
```bash
# Method 1: Config file (recommended)
nstbrowser-ai-agent config set key YOUR_API_KEY

# Method 2: Set environment variable in your shell
```

**验证：**
```bash
nstbrowser-ai-agent config get key
```

#### 2. “无法连接到 Nstbrowser”

**原因：** Nstbrowser 服务未运行或端点错误。

**解决方法：**
1. 检查 NST 代理是否正在运行：
   ```bash
   nstbrowser-ai-agent nst status
   ```
2. 确保 Nstbrowser 客户端正在运行
3. 如果使用了自定义主机/端口，请进行相应的配置：
   ```bash
   nstbrowser-ai-agent config set host YOUR_HOST
   nstbrowser-ai-agent config set port YOUR_PORT
   ```

**验证：**
```bash
# Should show "NST agent is running and responsive"
nstbrowser-ai-agent nst status

# Should return list of profiles
nstbrowser-ai-agent profile list
```

#### 3. “找不到配置文件”

**原因：** 指定的配置文件不存在。

**解决方法：**
1. 列出可用的配置文件：
   ```bash
   nstbrowser-ai-agent profile list
   ```
2. 创建新的配置文件：
   ```bash
   nstbrowser-ai-agent profile create my-profile
   ```
3. 或者使用临时浏览器：
   ```bash
   nstbrowser-ai-agent browser start-once
   ```

**验证：**
```bash
# Should show your profile
nstbrowser-ai-agent profile show my-profile
```

#### 4. “元素未找到”或“操作超时”

**原因：** 元素引用失效或页面结构发生变化。

**解决方法：**
1. 获取最新的页面快照：
   ```bash
   nstbrowser-ai-agent snapshot -i
   ```
2. 使用 CSS 选择器代替元素引用：
   ```bash
   # Instead of: nstbrowser-ai-agent click @e1
   # Use: nstbrowser-ai-agent click 'button[type="submit"]'
   ```
3. 检查页面元素：
   ```bash
   nstbrowser-ai-agent eval "Array.from(document.querySelectorAll('input')).map(el => ({type: el.type, placeholder: el.placeholder}))"
   ```

**验证：**
```bash
# Element should be visible
nstbrowser-ai-agent is visible 'button[type="submit"]'
```

### 元素引用系统的限制

元素引用系统（如 @e1、@e2 等）在现代 Web 框架（Vue.js、React、Angular）中可能无法可靠地工作，因为这些框架的 DOM 会动态更新。

**解决方法：** 使用 CSS 选择器：
```bash
# 1. Inspect page elements
nstbrowser-ai-agent eval "Array.from(document.querySelectorAll('input')).map(el => ({type: el.type, placeholder: el.placeholder}))"

# 2. Use CSS selectors directly
nstbrowser-ai-agent fill 'input[placeholder="Email"]' "user@example.com"
nstbrowser-ai-agent fill 'input[type="password"]' "password"
nstbrowser-ai-agent click 'button[type="submit"]'
```

## 命令参考

### 配置文件相关命令
- `profile list` - 列出所有配置文件
- `profile list-cursor` - 带有分页功能的配置文件列表
- `profile show <名称或 ID>` - 显示配置文件详情
- `profile create <名称>` - 创建新的配置文件
- `profile delete <名称或 ID> [名称或 ID...]` - 删除配置文件
- `profile groups list` - 列出所有配置文件组
- `profile groups change <组 ID> <配置文件名称或 ID> [...]` - 将配置文件移动到指定组
- `profile groups batch-change <组 ID> <ID> [...]` - 批量更改配置文件所属组
- `profile cache clear <ID> [ID] [ID...]` - 清除配置文件缓存
- `profile cookies clear <ID> [ID] [ID...]` - 清除配置文件中的 Cookie

### 代理相关命令
- `profile proxy show <名称或 ID>` - 显示代理设置
- `profile proxy update <名称或 ID>` - 更新代理设置
- `profile proxy reset <ID> [ID] [ID...]` - 重置代理设置
- `profile proxy batch-update <ID> [ID] [ID...]` - 批量更新代理设置
- `profile proxy batch-reset <ID> [ID] [ID...]` - 批量重置代理设置

### 标签相关命令
- `profile tags list` - 列出所有标签
- `profile tags create <ID> <标签>` - 向配置文件添加标签
- `profile tags update <ID> <标签:颜色> [...]` - 更新配置文件中的标签
- `profile tags clear <ID> [ID] [ID...]` - 清除配置文件中的标签
- `profile tags batch-create <ID> [ID] [ID...] <标签:颜色>` - 批量创建标签
- `profile tags batch-update <ID> [ID] [ID...] <标签:颜色>` - 批量更新标签
- `profile tags batch-clear <ID> [ID] [ID...]` - 批量清除标签

### 浏览器相关命令
- `browser list` - 列出正在运行的浏览器
- `browser start <名称或 ID>` - 使用指定配置文件启动浏览器
- `browser start-once` - 启动临时浏览器
- `browser stop <名称或 ID>` - 停止浏览器
- `browser stop-all` - 停止所有浏览器
- `browser pages <名称或 ID>` - 获取浏览器页面列表
- `browser debugger <名称或 ID>` - 获取浏览器的调试器 URL
- `browser cdp-url <名称或 ID>` - 获取浏览器的 CDP WebSocket URL
- `browser cdp-url-once` - 为临时浏览器获取 CDP URL
- `browser connect <名称或 ID>` - 连接到浏览器并获取 CDP URL
- `browser connect-once` - 连接到临时浏览器并获取 CDP URL

### 导航相关命令
- `open <URL>` - 导航到指定 URL
- `back` - 向后导航
- `forward` - 向前导航
- `reload` - 重新加载页面

### 页面检查相关命令
- `snapshot [-i] [-c] [-d <深度>]` - 获取页面快照
- `get title` - 获取页面标题
- `get url` - 获取当前 URL
- `get text <元素选择器>` - 获取元素文本
- `screenshot [路径]` - 截取页面截图
- `is visible <元素选择器>` - 检查元素是否可见

### 交互相关命令
- `click <元素选择器>` - 点击元素
- `fill <元素选择器> <文本>` - 向元素中输入文本
- `type <元素选择器> <文本>` - 在元素中输入文本
- `press <按键>` - 按下指定按键
- `wait <元素选择器|毫秒>` - 等待元素出现或指定时间

### 实用工具命令
- `eval <JavaScript>` - 执行 JavaScript 代码
- `close` - 关闭浏览器
- `session list` - 列出所有活动的会话
- `update check` - 检查是否有可用的更新
- `nst status` - 检查 NST 代理是否正在运行
- `config set <键> <值>` - 设置配置值
- `config get <键>` - 获取配置值
- `config show` - 显示所有配置信息

## JSON 输出

所有命令都支持 `--json` 参数，以便输出结果以机器可读的 JSON 格式显示：

```bash
nstbrowser-ai-agent profile list --json
nstbrowser-ai-agent snapshot -i --json
nstbrowser-ai-agent get text @e1 --json
```

## 最佳实践

1. **使用配置文件名称**：在大多数情况下，名称比 ID 更易于理解
2. **利用持久会话**：一旦浏览器启动，无需重复使用 `--profile` 参数
3. **使用批量操作**：对多个配置文件进行操作时效率更高
4. **使用分组和标签进行组织**：保持配置文件的整洁性
5. **对于现代应用程序，优先使用 CSS 选择器**：元素引用在某些框架中可能不可靠
6. **适当等待**：在导航后使用 `wait --load networkidle` 等待命令
7. **正确关闭浏览器**：始终关闭浏览器以保存会话状态
8. **处理错误**：检查命令输出并在需要时重试
9. **为每个配置文件配置代理**：根据地理位置或隐私需求配置代理
10. **定期更新**：定期运行 `nstbrowser-ai-agent update check` 命令以获取最新版本

## 更新

### 自动更新检查

CLI 每 24 小时自动检查一次更新，并在有新版本可用时通知您。

**禁用自动检查：**
```bash
# Set environment variable
NSTBROWSER_AI_AGENT_NO_UPDATE_CHECK=1
```

### 手动更新检查

```bash
# Check for updates
nstbrowser-ai-agent update check

# JSON output
nstbrowser-ai-agent update check --json
```

### 升级到最新版本

```bash
# If installed globally
npm install -g nstbrowser-ai-agent@latest

# If using npx
npx nstbrowser-ai-agent@latest

# If installed locally in project
npm install nstbrowser-ai-agent@latest
```

## 详细文档

有关更多详细信息，请参阅：

| 参考文档 | 使用场景 |
|-----------|-------------|
| [references/nst-api-reference.md](references/nst-api-reference.md) | 完整的 NST API 参考文档及所有命令说明 |
| [references/profile-management.md](references/profile-management.md) | 配置文件的创建、管理和生命周期 |
| [references/proxy-configuration.md](references/proxy-configuration.md) | 代理设置、测试和故障排除 |
| [references/batch-operations.md](references/batch-operations.md) | 高效地批量操作多个配置文件 |
| [references/troubleshooting.md](references/troubleshooting.md) | 常见问题及故障排除方法 |

## 可用的模板

| 模板 | 说明 |
|----------|-------------|
| [templates/profile-setup.sh](templates/profile-setup.sh) | 配置代理和标签的初始化模板 |
| [templates/batch-proxy-update.sh](templates/batch-proxy-update.sh) | 批量更新多个配置文件的代理设置 |
| [templates/automated-workflow.sh](templates/automated-workflow.sh) | 完整的自动化工作流程示例 |

```bash
./templates/profile-setup.sh my-profile --proxy-host proxy.com --proxy-port 8080
./templates/batch-proxy-update.sh "id1 id2 id3" --proxy-host proxy.com --proxy-port 8080
./templates/automated-workflow.sh my-profile https://example.com
```

## 注意事项

- **需要 Nstbrowser**：此工具仅与 Nstbrowser 服务配合使用
- **支持配置文件名称/ID**：所有命令都支持名称和 ID
- **自动启动**：如果配置文件未运行，浏览器会自动启动
- **名称解析**：配置文件名称会通过 API 自动转换为 ID
- **持久会话**：在同一会话中的命令之间会保持会话状态
- **配置文件由 Nstbrowser 管理**：配置文件由 Nstbrowser 客户端创建和存储
- **守护进程自动启动**：首次运行命令时启动守护进程，并在后续命令之间保持运行状态
- **会话持久化**：浏览器关闭时，会话状态会自动保存到配置文件中
- **临时浏览器**：使用 `browser start-once` 启动临时浏览器，这些浏览器不会保存会话状态

## CDP 集成

获取 Chrome 开发者工具协议（CDP）WebSocket URL 以连接外部工具：

```bash
# Get CDP URL for existing browser
nstbrowser-ai-agent browser cdp-url my-profile

# Get CDP URL for temporary browser
nstbrowser-ai-agent browser cdp-url-once

# Connect to browser and get CDP URL (starts if not running)
nstbrowser-ai-agent browser connect my-profile

# Connect to temporary browser and get CDP URL
nstbrowser-ai-agent browser connect-once
```

**使用场景：**
- 将 Puppeteer/Playwright 连接到 Nstbrowser 管理的浏览器
- 使用 Chrome 开发者工具进行调试
- 与基于 CDP 的自动化工具集成
- 使用外部工具监控浏览器活动