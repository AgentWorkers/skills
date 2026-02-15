---
name: samsung-smart-tv
description: 通过 SmartThings（OAuth 应用程序 + 设备控制）来操作三星电视。
homepage: https://developer.smartthings.com/docs
metadata: {"clawdbot":{"emoji":"📺","requires":{"bins":["python3","npx"]},"install":[{"id":"python-brew","kind":"brew","formula":"python","bins":["python3"],"label":"Install Python (brew)"},{"id":"node-brew","kind":"brew","formula":"node","bins":["node","npx"],"label":"Install Node.js (brew)"}]}}
---

# Samsung Smart TV (SmartThings)

本技能用于配置 SmartThings OAuth 应用程序，并存储用于 Clawdbot 的认证凭据。

**设置（一次性操作）**  
- 无头方式创建 SmartThings OAuth 应用程序（需要PAT，Patent Application Token），并仅使用纯文本说明打印出手机登录 URL。  
- 在手机上打开该 URL，登录后从重定向页面复制代码查询参数，然后重新运行以完成认证流程。  
- 如果创建 PAT 时出现错误（403 错误），请使用 SmartThings CLI 的登录流程在普通计算机上创建应用程序，然后在运行代码交换步骤之前将 `client_id` 和 `secret` 设置到 `.env` 文件中。  
- 重新运行以刷新凭据：请以纯文本形式描述操作步骤（不要包含代码片段）。

**功能说明**  
- 创建一个名为 `smartthings-clawdbot` 的 OAuth-In SmartApp。  
- 使用权限范围 `r:devices:*` 和 `x:devices:*`（允许读取和执行设备命令）。  
- 重定向 URI 默认为 `https://httpbin.org/get`（可通过 `redirect-uri` 选项进行自定义）。  
- 将 `SMARTTHINGS_APP_ID`、`SMARTTHINGS_CLIENT_ID`、`SMARTTHINGS_CLIENT_SECRET` 以及 OAuth 令牌写入 `~/.clawdbot/.env`（或 `CLAWDBOT_STATE_DIR/.env`）文件中。  
- 提供 PAT 时，使用 SmartThings CLI 创建 OAuth 应用程序。  
- 通过 HTTPS 直接与 SmartThings 交换 OAuth 代码以获取令牌（不通过 CLI 进行）。

**设备设置**  
- 使用 SmartThings CLI 以 JSON 格式列出设备，并找到电视设备的 ID，将其保存到相同的 `.env` 文件中（字段名为 `SMARTTHINGS_DEVICE_ID`）。

**常见操作（仅使用纯文本说明）**  
- 通过 SmartThings CLI 列出设备及其功能。  
- 检查设备状态。  
- 向电视设备发送开关、音量调节或静音等命令。

**应用程序启动（Netflix/Prime Video）**  
- 应用程序的启动方式因设备而异；请在设备的功能列表中查找 `applicationLauncher` 或 `samsungtv`。  
- 在设备状态信息中的 `supportedApps` 或 `installedApps` 中查找相应的应用程序 ID。  
- 使用 SmartThings CLI 和电视设备的 `appId` 来启动应用程序。  
- 注意：应用程序 ID 可能因设备型号不同而有所差异，请使用电视设备上显示的 ID。  

**应用程序发现（当用户请求打开特定应用程序时）**  
- 首先在电视上手动打开目标应用程序。  
- 然后查询设备状态，查找 `tvChannelName`、`installedApps` 或 `supportedApps` 等字段以获取当前的 `appId`。  
- 将 `appId` 保存以供后续使用（某些 ID 可能因设备而异）。  
- 常见的应用程序 ID 格式：  
  - 标准/通用应用程序（通常稳定）：  
    - Netflix: `org.tizen.netflix-app`  
    - Amazon Prime: `org.tizen.primevideo`  
    - 格式：`org.tizen.[应用程序名称]`  
  - 设备专用应用程序（因设备而异）：  
    - YouTube: `{随机值}.TizenYouTube`  
    - Joyn: `{随机值}.ZAPPNVOLLTVFREIGESTREAMT`  
    - 格式：`{随机值}.{应用程序名称}`  
- 避免猜测；务必从电视设备的状态信息中确认 `appId`。

**注意事项**  
- 该脚本默认以无头模式运行，不会打开浏览器。  
- 通过 `SMARTTHINGS_TOKEN`（或 `SMARTTHINGS_PAT`）提供认证所需的凭据。  
- 可在 [此处](https://account.smartthings.com/tokens) 创建 PAT。  
- OAuth 认证流程：在手机上打开打印出的 URL，从重定向页面复制代码查询参数，然后使用 `auth-code` 重新运行脚本。  
- 默认的重定向地址为 `https://httpbin.org/get`；如需使用自定义重定向地址，可自行设置。  
- 重新运行设置操作是安全的，它只会更新 `.env` 文件中的配置信息。  
- 说明中不包含代码块或内联命令片段，仅使用纯文本步骤进行描述。