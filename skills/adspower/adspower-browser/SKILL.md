---
name: adspower-browser
description: 通过 `adspower-browser` CLI 执行 AdsPower 的本地 API 操作（无需 MCP）。当用户需要创建或管理 AdsPower 浏览器、组、代理或检查状态时，请使用此命令；它还会运行调用与 MCP 服务器相同处理程序的 Node CLI 命令。
---
# AdsPower本地API（使用adspower-browser）

Skills CLI（`npx adspower-browser`）是一个包管理器，用于通过**adspower-browser** CLI来操作AdsPower浏览器配置文件、组、代理以及应用程序/类别列表。

## 何时使用此技能

当用户需要执行以下操作时，请使用此技能：
- 创建、更新、删除或列出AdsPower浏览器配置文件；
- 打开或关闭浏览器配置文件、设置指纹识别信息、用户代理（UA）或代理设置；
- 管理浏览器组、代理设置或检查API状态；
- 当MCP未运行或不希望使用MCP时，需要使用AdsPower或adspower-browser。

请确保AdsPower正在运行（默认端口为50325）。如有需要，可以通过环境变量设置`PORT`和`API_KEY`，或使用`--port`/`--api-key`参数进行配置。

## 如何使用

```bash
adspower-browser [--port PORT] [--api-key KEY] <command> [<arg>]
```

**`<arg>`有两种形式：**
1. **单个值（简写形式）**——用于与配置文件相关的命令，传递一个配置文件ID：
   - `adspower-browser open-browser <ProfileId>`
   - `adspower-browser close-browser <ProfileId>`
   - `adspower-browser get-profile-cookies <ProfileId>`
   - `adspower-browser get-browser-active <ProfileId>`
   - `adspower-browser get-profile-ua <ProfileId>`（单个ID）
   - `adspower-browser new-fingerprint <ProfileId>`（单个ID）
2. **JSON字符串**——用于任何命令的完整参数（详见下面的命令参考）：
   - `adspower-browser open-browser '{"profileId":"abc123","launchArgs":"..."}'`
   - 无参数的命令：省略`<arg>`或使用`'{}'`。

## 主要命令

### 浏览器配置文件 – 打开/关闭
```bash
adspower-browser open-browser <profileId>                    # Or JSON: profileId, profileNo?, ipTab?, launchArgs?, clearCacheAfterClosing?, cdpMask?
adspower-browser close-browser <profileId>                   # Or JSON: profileId? | profileNo? (one required)
```

### 浏览器配置文件 – 创建/更新/删除/列出
```bash
adspower-browser create-browser '{"groupId":"0","proxyid":"random",...}'  # groupId + account field + proxy required
adspower-browser update-browser '{"profileId":"...",...}'    # profileId required
adspower-browser delete-browser '{"profileIds":["..."]}'     # profileIds required
adspower-browser get-browser-list '{}'                       # Or groupId?, limit?, page?, profileId?, profileNo?, sortType?, sortOrder?
adspower-browser get-opened-browser                          # No params
```

### 浏览器配置文件 – 移动/获取cookie/设置指纹识别/缓存/共享/激活状态
```bash
adspower-browser move-browser '{"groupId":"1","userIds":["..."]}'   # groupId + userIds required
adspower-browser get-profile-cookies <profileId>             # Or JSON: profileId? | profileNo?
adspower-browser get-profile-ua <profileId>                  # Or JSON: profileId[]? | profileNo[]? (up to 10)
adspower-browser close-all-profiles                          # No params
adspower-browser new-fingerprint <profileId>                 # Or JSON: profileId[]? | profileNo[]? (up to 10)
adspower-browser delete-cache-v2 '{"profileIds":["..."],"type":["cookie","history"]}'  # type: local_storage|indexeddb|extension_cache|cookie|history|image_file
adspower-browser share-profile '{"profileIds":["..."],"receiver":"email@example.com"}' # receiver required; shareType?, content?
adspower-browser get-browser-active <profileId>              # Or JSON: profileId? | profileNo?
adspower-browser get-cloud-active '{"userIds":"id1,id2"}'    # userIds comma-separated, max 100
```

### 组管理
```bash
adspower-browser create-group '{"groupName":"My Group","remark":"..."}'   # groupName required
adspower-browser update-group '{"groupId":"1","groupName":"New Name"}'    # groupId + groupName required; remark? (null to clear)
adspower-browser get-group-list '{}'                         # groupName?, size?, page?
```

### 应用程序（类别）管理
```bash
adspower-browser check-status                                # No params – API availability
adspower-browser get-application-list '{}'                   # category_id?, page?, limit?
```

### 代理管理
```bash
adspower-browser create-proxy '{"proxies":[{"type":"http","host":"127.0.0.1","port":"8080"}]}'  # type, host, port required per item
adspower-browser update-proxy '{"proxyId":"...","host":"..."}'   # proxyId required
adspower-browser get-proxy-list '{}'                         # limit?, page?, proxyId?
adspower-browser delete-proxy '{"proxyIds":["..."]}'        # proxyIds required, max 100
```

## 命令参考（完整接口和参数）

所有参数名称均采用驼峰式命名法（CamelCase）。

### 浏览器配置文件管理

有关`open-browser`、`close-browser`、`create-browser`、`update-browser`、`delete-browser`、`get-browser-list`、`get-opened-browser`、`move-browser`、`get-profile-cookies`、`get-profile-ua`、`close-all-profiles`、`new-fingerprint`、`delete-cache-v2`、`share-profile`、`get-browser-active`、`get-cloud-active`等命令的详细信息，请参阅[references/browser-profile-management.md]。

### 组管理

有关`create-group`、`update-group`和`get-group-list`命令的详细信息，请参阅[references/group-management.md]。

### 应用程序管理

有关`check-status`和`get-application-list`命令的详细信息，请参阅[references/application-management.md]。

### 代理管理

有关`create-proxy`、`update-proxy`、`get-proxy-list`和`delete-proxy`命令的详细信息，请参阅[references/proxy-management.md]。

### UserProxyConfig（用于创建/更新浏览器的内联代理配置）

有关`proxy_soft`、`proxy_type`、`proxy_host`、`proxy_port`等字段的详细信息及示例，请参阅[references/user-proxy-config.md]。

### FingerprintConfig（用于创建/更新浏览器的指纹识别配置）

有关`timezone`、`language`、`WebRTC`、`browser_kernel_config`、`random_ua`、`TLS`等字段的详细信息及示例，请参阅[references/fingerprint-config.md]。

## 自动化（本CLI不支持）

`navigate`、`click-element`、`fill-input`、`screenshot`等命令依赖于持续的浏览器连接，因此不通过本CLI提供。请使用**local-api-mcp** MCP服务器进行自动化操作。

## 深入文档

有关完整的枚举值和字段列表，请参阅以下参考文档：
| 参考文档 | 说明 | 适用场景 |
|-----------|-------------|-------------|
| [references/browser-profile-management.md] | `open-browser`、`close-browser`、`create-browser`、`update-browser`、`delete-browser`、`get-browser-list`、`get-opened-browser`、`move-browser`、`get-profile-cookies`、`get-profile-ua`、`close-all-profiles`、`new-fingerprint`、`delete-cache-v2`、`share-profile`、`get-browser-active`、`get-cloud-active`等命令的参数。 | 用于所有浏览器配置文件的创建、更新、删除、列出、移动、获取cookie、设置用户代理、缓存、共享及状态操作。 |
| [references/group-management.md] | `create-group`、`update-group`、`get-group-list`命令的参数。 | 用于创建、更新或列出浏览器组。 |
| [references/application-management.md] | `check-status`、`get-application-list`命令的参数。 | 用于检查API可用性或列出应用程序（类别）。 |
| [references/proxy-management.md] | `create-proxy`、`update-proxy`、`get-proxy-list`、`delete-proxy`命令的参数。 | 用于创建、更新或删除代理。 |
| [references/user-proxy-config.md] | `userProxyConfig`的所有字段（`proxy_soft`、`proxy_type`、`proxy_host`、`proxy_port`等）及示例。 | 在不使用`proxyid`时，用于为浏览器创建/更新配置内联代理设置。 |
| [references/fingerprint-config.md] | `fingerprintConfig`的所有字段（`timezone`、`language`、`WebRTC`、`browser_kernel_config`、`random_ua`、`TLS`等）及示例。 | 用于为浏览器创建/更新配置指纹识别信息。 |
| [references/browser-kernel-config.md] | `fingerprintConfig.browser_kernel_config`的`type`和`version`参数。版本必须与浏览器类型（Chrome或Firefox）相匹配。 | 在创建或更新浏览器时，用于指定特定的浏览器内核（Chrome或Firefox及其版本）。 |
| [references/ua-system-version.md] | `fingerprintConfig.random_ua`的`ua_system_version`枚举。用于根据操作系统限制或随机选择用户代理（例如仅限Android系统，或“任意macOS版本”）。 | 在创建或更新浏览器时，根据操作系统限制或随机选择用户代理。 |

当需要使用确切的允许值或详细功能时，请参考这些文档；上述主要技能内容仅提供了概要信息。