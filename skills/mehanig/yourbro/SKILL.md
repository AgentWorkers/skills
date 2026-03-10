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
# yourbro — 发布由 AI 驱动的网页

您可以使用 yourbro.ai 发布多文件网页，并实现端到端加密。ClawdBot 会将页面目录写入您的代理（该代理会将其存储在本地），然后 yourbro.ai 通过端到端加密的中继从代理获取内容来渲染这些页面。服务器永远不会看到您的页面内容。

## 工作原理

```
ClawdBot writes files to /data/yourbro/pages/{slug}/ -> page is live immediately -> visitor loads page -> browser fetches E2E encrypted bundle from agent via relay -> decrypts -> rendered in sandboxed iframe
```

您的代理（yourbro-agent）运行在您的机器上，并从本地目录提供页面服务。yourbro.ai 是一个完全中立的加密中继——它从不存储、查看或提供您的内容。所有页面数据在传输之前都会使用 X25519 + AES-256-GCM 进行加密。只有当您的代理处于在线状态时，页面才能正常显示。对磁盘上的文件进行编辑后，更改会立即生效。

代理通过出站 WebSocket 与 yourbro.ai 连接——无需暴露任何端口、DNS 或 TLS 证书。

## 设置

### 1. 获取 yourbro API 令牌

登录 https://yourbro.ai，进入您的仪表板，然后创建一个 API 令牌。

将其设置到 OpenClaw 的配置中：

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

### 2. 启动代理

`yourbro-agent` 可执行文件是您的个人存储服务器。设置您的 API 令牌和服务器地址，然后启动它：

```bash
export YOURBRO_TOKEN="yb_your_token_here"
export YOURBRO_SERVER_URL="https://api.yourbro.ai"
yourbro-agent
```

代理会自动通过 WebSocket 与 yourbro.ai 连接。首次启动时，它会显示一个配对代码：

```
=== PAIRING CODE: A7X3KP9M (expires in 5 minutes) ===
Relay mode: connecting to wss://api.yourbro.ai/ws/agent
```

无需打开任何端口，也无需域名。该服务可以在 NAT/防火墙后面正常使用。

要将其作为后台服务运行，请参考 `contrib/yourbro-agent.service`（Linux systemd）或 `contrib/com.yourbro.agent.plist`（macOS launchd）。

### 3. 配对您的代理

进入 yourbro.ai 仪表板。您的代理会显示在“已配对代理”列表中（状态为“在线（中继）”。从下拉菜单中选择它，输入配对代码，然后点击“配对”。这将在这台浏览器和代理之间交换 X25519 加密密钥，以实现端到端加密。

### 4. 发布页面

请求 ClawdBot 发布一个页面。它将执行以下操作：
1. 创建页面目录：`mkdir -p /data/yourbro/pages/{slug}/`
2. 创建 `index.html`（必需）以及其他文件（JS、CSS 等）
3. 可选地创建 `page.json` 文件，其中包含 `{"title": "我的页面", "public": false}` 以自定义页面标题和可见性设置
4. 页面将发布在 `https://yourbro.ai/p/USERNAME/SLUG`（或根据配置发布在 `https://CUSTOM_DOMAIN/SLUG`）

要更新页面，只需编辑相关文件——更改会立即生效。要删除页面，只需删除相应的目录。无需调用任何 API。

### 页面可见性（公共 vs 私有）

页面默认是**私有的**。只有页面所有者（经过身份验证并完成配对的浏览器）才能通过端到端加密查看私有页面。

要将页面设置为公开（任何拥有链接的人都可以查看）：

```bash
echo '{"title": "My Portfolio", "public": true}' > /data/yourbro/pages/my-page/page.json
```

要将页面重新设置为私有：

```bash
echo '{"title": "My Portfolio", "public": false}' > /data/yourbro/pages/my-page/page.json
```

如果 `page.json` 文件缺失或没有 `public` 字段，页面将默认保持**私有**状态。

所有页面（无论是公开的还是私有的）都通过端到端加密进行传输。匿名访问者会生成临时的 X25519 密钥。公开页面无法访问页面存储数据。页面的显示依赖于代理是否处于在线状态。

## 文件位置

| 路径 | 描述 |
|---|---|
| `yourbro-agent` | 代理可执行文件（由 OpenClaw 安装到 `~/.openclaw/tools/yourbro/`） |
| `/data/yourbro/pages/` | 页面目录——每个页面对应一个包含 `index.html` 及其他资源的文件夹 |
| `/data/yourbro/pages/{slug}/index.html` | 每个页面的必选入口文件 |
| `/data/yourbro/pages/{slug}/page.json` | 可选元数据：`{"title": "页面标题", "public": false}`。将 `public` 设置为 `true` 可以使页面对所有人可见 |
| `~/.yourbro/agent.db` | SQLite 数据库（存储代理身份信息、授权密钥和页面数据） |

`yourbro-agent` 是一个静态的可执行文件，没有运行时依赖项。OpenClaw 会根据元数据中的安装链接从 GitHub 下载适用于相应平台的二进制文件（darwin/arm64、darwin/amd64、linux/amd64、linux/arm64）。

## 配置

| 变量 | 是否必需 | 默认值 | 描述 |
|---|---|---|---|
| `YOURBRO_TOKEN` | 是 | -- | 来自 yourbro.ai 仪表板的 API 令牌（ClawdBot 和代理都会使用） |
| `YOURBRO_SERVER_URL` | 是 | -- | yourbro API 服务器地址（例如 `https://api.yourbro.ai`） |
| `YOURBRO_SQLITE_PATH` | 否 | `~/.yourbro/agent.db` | SQLite 数据库路径 |

您只需要设置两个环境变量（`YOURBRO_TOKEN` 和 `YOURBRO_SERVER_URL`）即可。

## 使用方法

当用户请求您在 yourbro 上发布页面或创建网页时，请按照以下步骤操作：

1. **检查令牌**：确认环境变量 `YOURBRO_TOKEN` 已设置。
2. **查找代理 ID**：列出用户的代理以获取代理 ID，并使用第一个处于在线状态的代理的 ID。
3. **生成内容**：创建 HTML/JS/CSS 文件。页面以目录形式存储——每个页面对应一个包含 `index.html` 及其他资源的文件夹。
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

5. **分享链接**：`https://yourbro.ai/p/USERNAME/my-page`
   如果用户配置了自定义域名（可以通过 `GET /api/custom-domains` 查看），则分享链接为：`https://CUSTOM_DOMAIN/my-page`

## 示例

### 简单的静态页面

页面发布地址为：`https://yourbro.ai/p/USERNAME/hello`（或根据配置为 `https://CUSTOM_DOMAIN/hello`）

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

### 列出页面

页面列表通过端到端加密的中继在仪表板上显示。所有中继请求都必须进行加密（使用 X25519 ECDH + AES-256-GCM）。仪表板会在配对完成后自动处理加密过程。

## 页面数据存储

页面可以使用 `postMessage` 功能存储和检索数据。Shell 负责处理端到端加密——页面的 JS 代码只需发送明文消息。所有数据都存储在代理的本地 SQLite 数据库中，并且是针对特定页面路径进行隔离的。

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

### 列出密钥

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

所有数据存储都是针对特定页面路径进行隔离的，并通过中继进行端到端加密。存储操作需要代理处于在线状态才能执行。

## 自定义域名

用户可以将页面发布在自己的域名下，而不仅仅是 `yourbro.ai/p/USERNAME/slug`。自定义域名的格式为 `https://CUSTOM_DOMAIN/slug`（不需要 `/p/` 前缀，用户名会自动包含在链接中）。

要检查用户是否配置了自定义域名：

```bash
curl https://api.yourbro.ai/api/custom-domains \
  -H "Authorization: Bearer $YOURBRO_TOKEN"
```

响应将是一个包含多个域名的数组。每个域名都有一个 `domain` 和 `default_slug` 字段。在分享页面链接时，如果配置了自定义域名且验证通过（`"verified": true`），则优先使用自定义域名链接：
- 默认链接：`https://yourbro.ai/p/USERNAME/my-page`
- 自定义域名：`https://pages.example.com/my-page`

用户可以在 yourbro.ai 仪表板中配置自定义域名（通过 DNS CNAME 和 TXT 验证）。代理无需进行任何配置更改——自定义域名同样使用相同的端到端加密中继。

## 安全模型

yourbro 采用零信任架构：

- **端到端加密传输**：所有页面流量（无论是公开的还是私有的）都使用 X25519 ECDH + AES-256-GCM 进行加密。中继服务器只能传递无法解密的密文。匿名访问者会生成临时的 X25519 密钥；已配对的用户使用存储在 IndexedDB 中的持久密钥。
- **服务器无权限访问数据**：yourbro.ai 从不存储、查看或提供页面内容。它只是一个中立的转发器。
- **X25519 密钥对**：密钥对是在本地生成的。私钥永远不会离开用户的设备。公钥在配对过程中进行交换，用于实现端到端加密。
- **配对安全性**：配对请求会使用代理的 X25519 公钥进行端到端加密（配对前可以通过代理列表 API 获取该公钥）。中继还会验证请求用户是否是该代理的所有者。被盗的配对代码对其他用户无效。配对代码是一次性使用的，5 分钟后失效，并且最多只能尝试 5 次。
- **数据隔离**：每个代理都有自己的 SQLite 数据库。所有数据都存储在用户的本地设备上。
- **代理必须在线**：页面只有在代理处于在线状态时才能显示。没有缓存数据，也没有服务器端的缓存机制。