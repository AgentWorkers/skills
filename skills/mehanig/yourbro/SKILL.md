---
name: yourbro
description: 在 yourbro.ai 上发布支持人工智能（AI）的网页，并实现端到端加密功能。
user-invocable: true
metadata:
  openclaw:
    os: ["darwin", "linux"]
    homepage: "https://yourbro.ai"
    requires:
      bins: ["yourbro-agent"]
      env: ["YOURBRO_TOKEN"]
    primaryEnv: "YOURBRO_TOKEN"
    install:
      - id: download-darwin-arm64
        kind: download
        url: "https://yourbro.ai/releases/latest/yourbro-agent-darwin-arm64"
        bins: ["yourbro-agent"]
        label: "Download yourbro-agent (macOS Apple Silicon)"
      - id: download-darwin-amd64
        kind: download
        url: "https://yourbro.ai/releases/latest/yourbro-agent-darwin-amd64"
        bins: ["yourbro-agent"]
        label: "Download yourbro-agent (macOS Intel)"
      - id: download-linux-amd64
        kind: download
        url: "https://yourbro.ai/releases/latest/yourbro-agent-linux-amd64"
        bins: ["yourbro-agent"]
        label: "Download yourbro-agent (Linux x86_64)"
      - id: download-linux-arm64
        kind: download
        url: "https://yourbro.ai/releases/latest/yourbro-agent-linux-arm64"
        bins: ["yourbro-agent"]
        label: "Download yourbro-agent (Linux ARM64)"
---
# yourbro — 发布由 AI 支持的网页

您可以使用 yourbro.ai 发布多文件网页，并实现端到端加密。OpenClaw 会将页面目录写入您的代理程序（该程序会将其存储在本地），然后 yourbro.ai 通过端到端加密的中继从代理程序获取内容来渲染这些页面。服务器永远不会看到您的页面内容。

## 工作原理

```
OpenClaw writes files to /data/yourbro/pages/{slug}/ -> page is live immediately -> visitor loads page -> browser fetches E2E encrypted bundle from agent via relay -> decrypts -> rendered in sandboxed iframe
```

您的代理程序（yourbro-agent）运行在您的机器上，并从本地目录提供页面服务。yourbro.ai 是一个“盲目的”加密中继——它从不存储、查看或提供您的内容。所有页面数据在传输过程中都会使用 X25519 + AES-256-GCM 进行加密。只有当代理程序在线时，页面才能正常显示。对磁盘上的文件进行编辑后，更改会立即生效。

代理程序通过出站 WebSocket 与 yourbro.ai 连接——无需暴露任何端口、DNS 或 TLS 证书。

## 设置

### 1. 获取 yourbro API 令牌

登录 https://yourbro.ai，进入您的控制面板，然后创建一个 API 令牌。

将令牌设置到 OpenClaw 的配置文件中：

```json
{
  "skills": {
    "entries": {
      "yourbro": {
        "env": {
          "YOURBRO_TOKEN": "yb_your_token_here"
        }
      }
    }
  }
}
```

### 2. 启动代理程序

`yourbro-agent` 是您的个人存储服务器。设置好 API 令牌和服务器地址后，启动该程序：

```bash
export YOURBRO_TOKEN="yb_your_token_here"
export YOURBRO_SERVER_URL="https://api.yourbro.ai"
yourbro-agent
```

代理程序会自动通过 WebSocket 与 yourbro.ai 连接。首次启动时，它会显示一个配对代码：

```
=== PAIRING CODE: A7X3KP9M (expires in 5 minutes) ===
Relay mode: connecting to wss://api.yourbro.ai/ws/agent
```

无需打开任何端口，也无需设置域名。该服务可以在 NAT/防火墙后正常使用。

要将其设置为后台服务，请参考 `contrib/yourbro-agent.service`（Linux systemd）或 `contrib/com.yourbro.agent.plist`（macOS launchd）。

### 3. 配对代理程序

进入 yourbro.ai 的控制面板。您的代理程序会显示在“已配对代理”列表中（状态为“在线”）。从列表中选择它，输入配对代码，然后点击“配对”。这会在您的浏览器和代理程序之间交换 X25519 加密密钥，以实现端到端加密。

### 4. 发布页面

让 OpenClaw 发布一个页面。它会执行以下操作：
1. 创建页面目录：`mkdir -p /data/yourbro/pages/{slug}/`
2. 创建 `index.html`（必需）以及其他文件（JS、CSS 等）
3. 可选地创建 `page.json` 文件来设置页面标题、可见性及共享权限：`{"title": "我的页面", "public": false}` 或 `{"title": "我的页面", "allowed_emails": ["friend@gmail.com"]}` 用于设置共享权限
4. 页面将在 `https://yourbro.ai/p/USERNAME/SLUG`（或配置的 `https://CUSTOM_DOMAIN/SLUG`）上显示

要更新页面，只需编辑相关文件——更改会立即生效。要删除页面，只需删除对应的目录。无需调用任何 API。

### 页面访问控制

页面支持三种访问权限级别：
- **私有**（默认）：仅页面所有者可以查看
- **共享**：特定的 Google 账户可以查看（需要访问代码）
- **公开**：任何拥有链接的人都可以查看

#### 私有页面（默认）

如果 `page.json` 不存在或没有 `public` 字段，页面将默认设置为 **私有**。只有页面所有者（经过身份验证并通过配对的浏览器）才能通过端到端加密查看页面。

#### 公开页面

要将页面设置为公开（任何拥有链接的人都可以查看）：

```bash
echo '{"title": "My Portfolio", "public": true}' > /data/yourbro/pages/my-page/page.json
```

要将页面重新设置为私有：

```bash
echo '{"title": "My Portfolio", "public": false}' > /data/yourbro/pages/my-page/page.json
```

#### 共享页面（通过电子邮件和访问代码）

要通过特定用户的 Google 账户共享页面：

```bash
cat > /data/yourbro/pages/my-page/page.json << 'EOF'
{"title": "My Page", "allowed_emails": ["friend@gmail.com", "coworker@company.com"]}
EOF
```

代理程序会在 `page.json` 中自动生成一个 8 位的 `access_code` 并将其记录下来：

```
=== ACCESS CODE for page "my-page": A7X3KP9M ===
Share this code with invited viewers.
```

将页面链接和访问代码发送给受邀者：
- **链接**：`https://yourbro.ai/p/USERNAME/my-page`
- **访问代码**：`A7X3KP9M`

受邀者需要使用自己的 Google 账户登录 yourbro.ai。他们输入一次访问代码后，浏览器会记住该代码。

**为什么需要双重验证？** 电子邮件验证可以确认用户身份（由 yourbro.ai 的 Google OAuth 完成）。访问代码是只有您和受邀者才知道的秘密信息——即使服务器被入侵，也无法访问共享的页面。

您也可以手动设置访问代码：

```bash
cat > /data/yourbro/pages/my-page/page.json << 'EOF'
{"title": "My Page", "allowed_emails": ["friend@gmail.com"], "access_code": "MYCUSTOMCODE"}
EOF
```

要撤销访问权限，只需从 `allowed_emails` 中移除相应的电子邮件地址或更改访问代码（现有访问者需要输入新的访问代码）。

所有页面（公开、共享和私有）都通过端到端加密进行传输。匿名访问者会生成临时的 X25519 密钥。页面的显示依赖于代理程序是否处于在线状态。

## 文件位置

| 路径 | 说明 |
|---|---|
| `yourbro-agent` | 代理程序二进制文件（由 OpenClaw 安装到 `~/.openclaw/tools/yourbro/`） |
| `/data/yourbro/pages/` | 页面目录——每个页面对应一个文件夹，其中包含 `index.html` 及其他资源文件 |
| `/data/yourbro/pages/{slug}/index.html` | 每个页面的入口文件 |
| `/data/yourbro/pages/{slug}/page.json` | 可选元数据文件：`{"title": "...", "public": false, "allowed_emails": "...", "access_code": "..."}`。用于设置页面标题、可见性和共享权限 |
| `~/.yourbro/agent.db` | SQLite 数据库（存储代理程序的身份信息、授权密钥和页面数据）

代理程序是一个静态的可执行文件，没有运行时依赖项。OpenClaw 会从 GitHub 的发布版本中下载适合您的操作系统的二进制文件（darwin/arm64、darwin/amd64、linux/amd64、linux/arm64）。

## 配置

| 变量 | 是否必需 | 默认值 | 说明 |
|---|---|---|---|
| `YOURBRO_TOKEN` | 是 | -- | 来自 yourbro.ai 控制面板的 API 令牌（OpenClaw 和代理程序都需要） |
| `YOURBRO_SERVER_URL` | 是 | -- | yourbro API 服务器地址（例如：`https://api.yourbro.ai`） |
| `YOURBRO_SQLITE_PATH` | 否 | `~/.yourbro/agent.db` | SQLite 数据库路径 |

您只需要设置两个环境变量（`YOURBRO_TOKEN` 和 `YOURBRO_SERVER_URL`）即可。

## 使用方法

当用户要求您在 yourbro 上发布页面或创建网页时，请按照以下步骤操作：
1. **检查令牌**：确认 `YOURBRO_TOKEN` 已在环境中设置。
2. **查找代理程序 ID**：列出用户的代理程序以获取其 ID。
3. **生成页面内容**：创建 HTML/JS/CSS 文件。页面是以目录形式组织的——每个页面对应一个文件夹，其中包含 `index.html` 及其他资源文件。
4. **创建页面目录**：
   ```bash
   mkdir -p /data/yourbro/pages/my-page/

   cat > /data/yourbro/pages/my-page/index.html << 'EOF'
   <!DOCTYPE html>
   <html>
   <head>
       <link rel="stylesheet" href="style.css">
   </head>
   <body>
       <h1>My Page</h1>
       <script src="app.js"></script>
   </body>
   </html>
   EOF

   cat > /data/yourbro/pages/my-page/style.css << 'EOF'
   body { background: #0a0a0a; color: #fafafa; }
   EOF

   cat > /data/yourbro/pages/my-page/app.js << 'EOF'
   console.log('Hello from yourbro!');
   EOF

   # Optional: set a custom title (page is private by default)
   echo '{"title": "My Page"}' > /data/yourbro/pages/my-page/page.json

   # Or make it public so anyone with the link can view it:
   # echo '{"title": "My Page", "public": true}' > /data/yourbro/pages/my-page/page.json
   ```
5. **分享页面链接**：`https://yourbro.ai/p/USERNAME/my-page`
   如果用户配置了自定义域名（通过 `GET /api/custom-domains` 查看），也可以分享为：`https://CUSTOM_DOMAIN/my-page`

## 示例

### 简单的静态页面

```bash
mkdir -p /data/yourbro/pages/hello/
cat > /data/yourbro/pages/hello/index.html << 'EOF'
<!DOCTYPE html><html><body><h1>Hello from yourbro!</h1></body></html>
EOF
echo '{"title": "Hello World"}' > /data/yourbro/pages/hello/page.json
```

页面的显示地址为：`https://yourbro.ai/p/USERNAME/hello`（或配置后的 `https://CUSTOM_DOMAIN/hello`）

### 包含 JS 和 CSS 的多文件页面

```bash
mkdir -p /data/yourbro/pages/dashboard/

cat > /data/yourbro/pages/dashboard/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><link rel="stylesheet" href="style.css"></head>
<body><div id="app"></div><script src="app.js"></script></body>
</html>
EOF

cat > /data/yourbro/pages/dashboard/style.css << 'EOF'
body { margin: 0; background: #111; color: #eee; font-family: system-ui; }
#app { padding: 20px; }
EOF

cat > /data/yourbro/pages/dashboard/app.js << 'EOF'
document.getElementById('app').innerHTML = '<h1>Dashboard</h1>';
EOF

echo '{"title": "Dashboard"}' > /data/yourbro/pages/dashboard/page.json
```

### 共享页面（仅限特定用户）

```bash
mkdir -p /data/yourbro/pages/team-report/
cat > /data/yourbro/pages/team-report/index.html << 'EOF'
<!DOCTYPE html><html><body><h1>Q1 Report</h1><p>Confidential</p></body></html>
EOF
cat > /data/yourbro/pages/team-report/page.json << 'EOF'
{"title": "Q1 Report", "allowed_emails": ["alice@company.com", "bob@company.com"]}
EOF
```

代理程序会自动生成访问代码并将其记录下来。将页面链接和访问代码分享给 Alice 和 Bob——他们需要登录 yourbro.ai，访问页面并输入访问代码。

### 更新现有页面

只需编辑文件——更改会立即生效：

```bash
cat > /data/yourbro/pages/hello/index.html << 'EOF'
<!DOCTYPE html><html><body><h1>Updated content!</h1></body></html>
EOF
```

### 删除页面

```bash
rm -rf /data/yourbro/pages/hello/
```

### 查看页面列表

页面列表通过端到端加密的中继在控制面板中显示。所有请求都必须经过加密（使用 X25519 ECDH + AES-256-GCM）。控制面板会在配对完成后自动处理加密过程。

## 页面数据存储

页面可以使用 `postMessage` 功能存储和检索数据。Shell 负责处理端到端加密；页面的 JavaScript 代码只需发送明文消息。所有数据都存储在代理程序的本地 SQLite 数据库中，并且是针对特定页面路径进行存储的。

### 设置值

```js
// In your page's JS (e.g., app.js)
var requestId = crypto.randomUUID();
window.parent.postMessage({
    type: 'yourbro-storage',
    action: 'set',
    key: 'user-score',
    value: { score: 42, level: 3 },
    requestId: requestId
}, '*');

window.addEventListener('message', function handler(event) {
    if (event.data.type === 'yourbro-storage-response' && event.data.requestId === requestId) {
        window.removeEventListener('message', handler);
        if (event.data.ok) console.log('Saved!');
    }
});
```

### 获取值

```js
var requestId = crypto.randomUUID();
window.parent.postMessage({
    type: 'yourbro-storage',
    action: 'get',
    key: 'user-score',
    requestId: requestId
}, '*');
// Response: { type: 'yourbro-storage-response', action: 'get', ok: true, data: { value: "..." } }
```

### 查看密钥

```js
window.parent.postMessage({
    type: 'yourbro-storage',
    action: 'list',
    prefix: 'user-',
    requestId: crypto.randomUUID()
}, '*');
// Response: { type: 'yourbro-storage-response', action: 'list', ok: true, data: [{ key: "user-score", ... }] }
```

### 删除密钥

```js
window.parent.postMessage({
    type: 'yourbro-storage',
    action: 'delete',
    key: 'user-score',
    requestId: crypto.randomUUID()
}, '*');
```

所有数据存储都是针对特定页面路径进行加密的。存储操作依赖于代理程序是否处于在线状态。

## 自定义域名

用户可以使用自己的域名来发布页面，而不仅仅是 `yourbro.ai/p/USERNAME/slug`。自定义域名的格式为 `https://CUSTOM_DOMAIN/slug`（不需要 `/p/` 前缀，用户名会自动添加）。

要检查用户是否配置了自定义域名：

```bash
curl https://api.yourbro.ai/api/custom-domains \
  -H "Authorization: Bearer $YOURBRO_TOKEN"
```

响应会返回一个域名数组。每个域名包含 `domain` 和 `default_slug` 字段。在分享页面链接时，如果配置了自定义域名且已验证（`"verified": true`），优先使用自定义域名：
- 默认链接：`https://yourbro.ai/p/USERNAME/my-page`
- 自定义域名：`https://pages.example.com/my-page`

用户可以在 yourbro.ai 的控制面板中配置自定义域名（通过 DNS CNAME 和 TXT 验证）。代理程序无需进行任何配置更改——所有自定义域名都使用相同的端到端加密中继。

## 安全模型

yourbro 采用零信任架构：
- **端到端加密传输**：所有页面流量（公开和私有）都使用 X25519 ECDH + AES-256-GCM 进行加密。中继服务器只能接收加密后的密文，无法读取内容。匿名访问者生成的密钥是临时的；已配对的用户使用存储在 IndexedDB 中的永久密钥。
- **服务器无权限**：yourbro.ai 从不存储、查看或提供页面内容。它只是一个中继服务器。
- **X25519 密钥对**：密钥对在本地生成。私钥不会离开用户的设备。公钥在配对过程中进行交换，用于实现端到端加密。
- **配对安全**：配对请求使用代理程序的 X25519 公钥进行端到端加密（配对前可以通过代理程序的 API 获取）。中继服务器还会验证请求用户的身份。即使配对代码被窃取，其他用户也无法访问共享页面。
- **访问控制**：访问代码是一次性使用的，5 分钟后失效，并且每次尝试的配对请求有限制（最多 5 次）。
- **数据隔离**：每个代理程序都有自己的 SQLite 数据库。所有数据都存储在用户的本地设备上。
- **代理程序必须在线**：页面只有在代理程序在线时才能显示。不存在过时的数据或服务器端的缓存。