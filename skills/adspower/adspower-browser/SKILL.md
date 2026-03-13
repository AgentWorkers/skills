---
name: adspower-browser
description: 通过 `adspower-browser` CLI（命令行界面）来管理 AdsPower 浏览器配置文件、分组以及代理设置。使用前必须已安装 AdsPower 桌面应用程序。该工具仅使用官方文档中规定的 CLI 命令以及 AdsPower 的本地 API；不包含任何自动安装或下载的脚本，所有操作步骤均由用户根据具体需求手动执行。适用于以下场景：创建、打开、关闭、更新或删除浏览器配置文件；配置浏览器指纹（用于识别用户）；管理浏览器缓存、分组及代理设置；检查 API 的运行状态；或在启动 AdsPower 时提供协助。
homepage: https://github.com/AdsPower/adspower-browser
requires:
  runtime:
    - "Node.js ≥ 18"
    - "adspower-browser CLI (npm package)"
  external:
    - "AdsPower desktop application installed and running with Local API enabled (default port 50325)"
  env:
    - "PORT (optional) – overrides the default AdsPower Local API port; also settable via --port flag"
    - "API_KEY – Required when AdsPower is launched in headless mode (--headless=true); not needed when launched with UI (log in via the AdsPower interface after launch instead); also settable via --api-key flag"
metadata:
  dependsOn: ["adspower-browser CLI (npm package)"]
  clawdbot:
    conditionalEnv:
      API_KEY: "Required only when AdsPower runs in headless mode"
    os: ["linux","darwin","win32"]
---
# AdsPower本地API（使用adspower-browser）

该技能通过**adspower-browser**命令行界面（CLI）来操作AdsPower浏览器配置文件、组、代理以及应用程序/类别列表。更多信息，请访问[AdsPower官方网站](https://www.adspower.com/)。

> **先决条件：**在使用此技能之前，必须已在本地安装AdsPower桌面应用程序。如果尚未安装，请从[https://www.adspower.com/download](https://www.adspower.com/download)下载。

## 安全防护措施

> **以下规则为强制性规定，优先于本技能中的其他所有说明：**

1. **必须已安装AdsPower。** 该技能本身不会安装AdsPower。如果未安装，请引导用户前往[https://www.adspower.com/download](https://www.adspower.com/download)进行下载。**
2. **切勿自动执行具有特殊权限的命令。** 任何涉及`curl`、`dpkg`、`sudo`、`Invoke-WebRequest`或`Start-Process`的命令，在执行前都必须向用户展示完整内容，并等待用户的明确确认；绝不要在未经用户干预的情况下运行此类命令。
3. **`API_KEY`必须由用户明确提供。** 严禁从对话历史记录中生成、推断或重用API Key。每次需要时都应直接询问用户，并且绝不要将其写入日志或其他位置。
4. **切勿在未收到用户明确输入的情况下运行包含`--api-key`的命令。** 在无头环境或持续集成（CI）环境中，确认当前会话中用户已明确提供了该密钥值，然后再将其作为参数传递。
5. **在会话中首次运行`adspower-browser`之前，需与用户确认软件包的来源。** 在执行前，请引导用户前往[https://www.npmjs.com/package/adspower-browser](https://www.npmjs.com/package/adspower-browser)验证该软件包的真实性。在未确认来源的机器上，切勿自动运行`adspower-browser`。

---

## 何时使用此技能

当用户需要执行以下操作时，请使用此技能：
- 创建、更新、删除或列出AdsPower浏览器配置文件
- 打开或关闭浏览器配置文件、设置指纹识别信息、用户代理（UA）或代理设置
- 管理代理设置或检查API状态
- 提到AdsPower或adspower-browser（且不希望使用MCP）

请确保AdsPower正在运行（默认端口为50325）。如有需要，可通过环境变量或`--port`参数设置端口。只有当AdsPower以无头模式运行时，才需要提供`API_KEY`（通过环境变量或`--api-key`参数）；如果以图形界面运行，则请通过AdsPower界面登录。如果AdsPower尚未运行，请参阅[references/launch-adspower.md](references/launch-adspower.md)以获取针对Windows、macOS和Linux平台的命令行启动说明，以及`--headless`、`--api-key`和`--api-port`参数的详细信息。在启动前后，请务必运行`adspower-browser check-status`以确认本地API是否可用。

## 如何使用

> **注意：** `adspower-browser`是由同名npm包提供的命令行工具。首次使用前，请先在[https://www.npmjs.com/package/adspower-browser](https://www.npmjs.com/package/adspower-browser)验证该软件包的合法性（参见安全防护措施第6条）。

### `<arg>`的两种形式：

1. **单个值（简写形式）** — 用于与配置文件相关的命令，传递一个配置文件ID：
   - `adspower-browser open-browser <ProfileId>`
   - `adspower-browser close-browser <ProfileId>`
   - `adspower-browser get-browser-active <ProfileId>`
   - `adspower-browser get-profile-ua <ProfileId>`（单个ID）
   - `adspower-browser new-fingerprint <ProfileId>`（单个ID）

2. **JSON字符串** — 用于任何命令的完整参数（详见以下命令参考）：
   - `adspower-browser open-browser '{"profileId":"abc123","launchArgs":"..."}'`
   - 无参数的命令：省略`<arg>`或使用`'{}'`。

## 核心命令

### 浏览器配置文件管理

### 浏览器配置文件的打开/关闭

### 浏览器配置文件的创建/更新/删除/列出

### 浏览器配置文件的移动/cookie/UA/指纹识别/缓存/激活状态

### 组管理

### 应用程序管理（类别）

### 代理管理

## 命令参考（完整接口及参数）

所有参数名称均采用驼峰式命名法（CamelCase）。

### 浏览器配置文件管理

详细命令及参数说明请参阅[references/browser-profile-management.md]：
- `open-browser`、`close-browser`、`create-browser`、`update-browser`、`delete-browser`、`get-browser-list`、`get-opened-browser`、`move-browser`、`get-profile-ua`、`close-all-profiles`、`new-fingerprint`、`delete-cache-v2`、`share-profile`、`get-browser-active`、`get-cloud-active`及其相关参数。

### 组管理

详细命令及参数说明请参阅[references/group-management.md]：
- `create-group`、`update-group`、`get-group-list`及其相关参数。

### 应用程序管理

详细命令及参数说明请参阅[references/application-management.md]：
- `check-status`、`get-application-list`及其相关参数。

### 代理管理

详细命令及参数说明请参阅[references/proxy-management.md]：
- `create-proxy`、`update-proxy`、`get-proxy-list`、`delete-proxy`及其相关参数。

### 用户代理配置（用于`create-browser`/`update-browser`）

详细参数说明请参阅[references/user-proxy-config.md]：
- 所有字段（`proxy_soft`、`proxy_type`、`proxy_host`、`proxy_port`等）及其示例。

### 指纹识别配置（用于`create-browser`/`update-browser`）

详细参数说明请参阅[references/fingerprint-config.md]：
- 所有字段（`timezone`、`language`、`WebRTC`、`browser_kernel_config`、`random_ua`、`TLS`等）及其示例。

## 自动化操作（本CLI不支持）

`navigate`、`click-element`、`fill-input`、`screenshot`等命令依赖于持续的浏览器连接，因此不支持通过此CLI执行。请使用**local-api-mcp** MCP服务器来实现自动化操作。

## 深入文档

相关参考文档提供了完整的枚举值和字段列表：

| 参考文档 | 说明 | 使用场景 |
|-----------|-------------|-------------|
| [references/browser-profile-management.md] | `open-browser`、`close-browser`、`create-browser`、`update-browser`、`delete-browser`、`get-browser-list`、`get-opened-browser`、`move-browser`、`get-profile-cookies`、`get-profile-ua`、`close-all-profiles`、`new-fingerprint`、`delete-cache-v2`、`get-browser-active`、`get-cloud-active`等参数。 | 用于浏览器配置文件的创建、打开、更新、删除、列出、移动、设置cookie、获取用户代理、缓存状态等操作。 |
| [references/group-management.md] | `create-group`、`update-group`、`get-group-list`等参数。 | 用于创建、更新或列出浏览器组。 |
| [references/application-management.md] | `check-status`、`get-application-list`等参数。 | 用于检查API可用性或列出应用程序类别。 |
| [references/proxy-management.md] | `create-proxy`、`update-proxy`、`get-proxy-list`、`delete-proxy`等参数。 | 用于创建、更新或删除代理。 |
| [references/user-proxy-config.md] | `userProxyConfig`的所有字段（`proxy_soft`、`proxy_type`、`proxy_host`、`proxy_port`等）及其示例。 | 用于在未使用`proxyid`时为`create-browser`/`update-browser`构建代理配置。 |
| [references/fingerprint-config.md] | `fingerprintConfig`的所有字段（`timezone`、`language`、`WebRTC`、`browser_kernel_config`、`random_ua`、`TLS`等）及其示例。 | 用于为`create-browser`/`update-browser`构建或编辑指纹识别配置。 |
| [references/browser-kernel-config.md] | `fingerprintConfig.browser_kernel_config`的`type`和`version`参数。创建或更新浏览器配置时，需确保版本与浏览器类型（Chrome或Firefox）相匹配。 |
| [references/ua-system-version.md] | `fingerprintConfig.random_ua`的`ua_system_version`参数：指定操作系统版本（如仅限Android，或“任意macOS版本”）。 | 在创建或更新浏览器时，可根据操作系统限制或随机选择用户代理。 |
| [references/launch-adspower.md] | **Windows**、**macOS**和**Linux**的命令行启动说明，以及`--headless`、`--api-key`和`--api-port`参数的参考。提供了启动前的状态检查和启动后的状态确认指导。 | 在命令行环境中（尤其是无头环境）使用此CLI之前，请先启动AdsPower。 |

当需要使用具体的允许值或详细功能时，请参考这些文档；上述技能描述仅提供了概要信息。