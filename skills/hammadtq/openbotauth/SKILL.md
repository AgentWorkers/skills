# openbotauth

这是一个用于AI代理的加密身份验证系统。只需注册一次，即可在任何地方对HTTP请求进行签名（遵循RFC 9421标准）。支持通过请求签名代理实现浏览器集成。

## 使用场景

- 用户希望使用已签名的身份浏览网站
- 验证浏览器会话
- 以机器人身份发送HTTP请求
- 设置OpenBotAuth请求头
- 区分人类与机器人的会话来源
- 管理代理密钥
- 对抓取会话进行签名
- 在OBA注册表中注册代理
- 为代理配置企业级单点登录（SSO）

## 所需工具

- Bash命令行

## 使用说明

该功能是**自包含的**，无需依赖任何npm包。核心模式使用Node.js（v18及以上）和curl；代理模式还需要openssl。

### 兼容模式

**核心模式（便携式，推荐使用）：**
- 支持：Claude Code、Cursor、Codex CLI、Goose以及任何支持Shell的代理
- 注册过程使用Node.js的加密库和curl
- 在执行`POST /agents`操作时仅需要临时生成token

**浏览器模式（可选，依赖运行时环境）：**
- 适用于：agent-browser、OpenClaw Browser Relay、CUA工具
- 承载式token不能存储在浏览器运行时环境中
- 首先通过CLI模式完成注册，之后才能使用签名功能

### 密钥存储

密钥存储在`~/.config/openbotauth/key.json`文件中，采用OBA规定的格式：

```json
{
  "kid": "<thumbprint-based-id>",
  "x": "<base64url-raw-public-key>",
  "publicKeyPem": "-----BEGIN PUBLIC KEY-----\n...",
  "privateKeyPem": "-----BEGIN PRIVATE KEY-----\n...",
  "createdAt": "..."
}
```

OBA token存储在`~/.config/openbotauth/token`文件中（权限设置为600）。

代理注册信息（包括`agent_id`和JWKS URL）应在步骤3之后保存到代理的内存或笔记中。

### Token使用规则

- **Token仅用于注册**：
  - 仅用于`POST /agents`操作（以及密钥更新）
- 注册完成后立即删除`~/.config/openbotauth/token`文件
- 绝不要将token附加到浏览器会话中

**最低权限要求：** `agents:write`和`profile:read`
- 如果需要访问`/keys`接口，请添加`keys:write`权限

**注意：** **切勿使用全局请求头**来传递OBA token：
  - `agent-browser`的`set headers`命令会全局应用请求头
- 应始终使用基于源域的请求头（通过`open --headers`命令设置）

---

### 步骤1：检查现有身份

```bash
cat ~/.config/openbotauth/key.json 2>/dev/null && echo "---KEY EXISTS---" || echo "---NO KEY FOUND---"
```

- **如果存在密钥**：读取密钥以获取`kid`、`x`和`privateKeyPem`。检查代理是否已注册（查看内存或笔记中的`agent_id`）。如果已注册，则跳至步骤4（签名操作）。
- **如果不存在密钥**：进入步骤2。

---

### 步骤2：生成Ed25519密钥对（如果未注册）

在本地执行此操作。所有数据仅保存在本地，不会离开计算机。

```bash
node -e "
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
const publicKeyPem = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const privateKeyPem = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();

// Derive kid from JWK thumbprint (matches OBA's format)
const spki = publicKey.export({ type: 'spki', format: 'der' });
if (spki.length !== 44) throw new Error('Unexpected SPKI length: ' + spki.length);
const rawPub = spki.subarray(12, 44);
const x = rawPub.toString('base64url');
const thumbprint = JSON.stringify({ kty: 'OKP', crv: 'Ed25519', x });
const hash = crypto.createHash('sha256').update(thumbprint).digest();
const kid = hash.toString('base64url').slice(0, 16);

const dir = path.join(os.homedir(), '.config', 'openbotauth');
fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
fs.writeFileSync(path.join(dir, 'key.json'), JSON.stringify({
  kid, x, publicKeyPem, privateKeyPem,
  createdAt: new Date().toISOString()
}, null, 2), { mode: 0o600 });

console.log('Key generated!');
console.log('kid:', kid);
console.log('x:', x);
"
```

保存`kid`和`x`值，这些值用于后续注册。

---

### 步骤3：在OpenBotAuth中注册代理

这是一个**一次性设置**，为代理生成一个用于签名验证的JWKS公钥地址。

#### 3a. 从用户处获取token

请求用户提供OpenBotAuth token：
> 我需要一个OpenBotAuth token来注册我的加密身份。请花费30秒完成：
>
> 1. 访问**https://openbotauth.org/token**
> 2. 点击“使用GitHub登录”
> 3. 复制token并发送给我
>
> Token的格式为`oba_`后跟64个十六进制字符。

收到token后，请将其保存：

```bash
node -e "
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const dir = path.join(os.homedir(), '.config', 'openbotauth');
fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
const token = process.argv[1].trim();
fs.writeFileSync(path.join(dir, 'token'), token, { mode: 0o600 });
console.log('Token saved.');
" "THE_TOKEN_HERE"
```

#### 3b. 注册代理

```bash
node -e "
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const dir = path.join(os.homedir(), '.config', 'openbotauth');
const key = JSON.parse(fs.readFileSync(path.join(dir, 'key.json'), 'utf-8'));
const tokenPath = path.join(dir, 'token');
const token = fs.readFileSync(tokenPath, 'utf-8').trim();

const AGENT_NAME = process.argv[1] || 'my-agent';
const API = 'https://api.openbotauth.org';

fetch(API + '/agents', {
  method: 'POST',
  redirect: 'error',  // Never follow redirects with bearer token
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: AGENT_NAME,
    agent_type: 'agent',
    public_key: {
      kty: 'OKP',
      crv: 'Ed25519',
      kid: key.kid,
      x: key.x,
      use: 'sig',
      alg: 'EdDSA'
    }
  })
})
.then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
.then(async d => {
  console.log('Agent registered!');
  console.log('Agent ID:', d.id);

  // Fetch session to get username for JWKS URL
  const session = await fetch(API + '/auth/session', {
    redirect: 'error',  // Never follow redirects with bearer token
    headers: { 'Authorization': 'Bearer ' + token }
  }).then(r => { if (!r.ok) throw new Error('Session HTTP ' + r.status); return r.json(); });
  const username = session.profile?.username || session.user?.github_username;
  if (!username) throw new Error('Could not resolve username from /auth/session');
  const jwksUrl = API + '/jwks/' + username + '.json';

  // Write config.json for the signing proxy
  fs.writeFileSync(path.join(dir, 'config.json'), JSON.stringify({
    agent_id: d.id,
    username: username,
    jwksUrl: jwksUrl
  }, null, 2), { mode: 0o600 });
  console.log('Config written to ~/.config/openbotauth/config.json');

  // Delete token — no longer needed after registration
  fs.unlinkSync(tokenPath);
  console.log('Token deleted (no longer needed)');

  console.log('');
  console.log('JWKS URL:', jwksUrl);
  console.log('');
  console.log('Save this to memory:');
  console.log(JSON.stringify({
    openbotauth: {
      agent_id: d.id,
      kid: key.kid,
      username: username,
      jwks_url: jwksUrl
    }
  }, null, 2));
})
.catch(e => console.error('Registration failed:', e.message));
" "AGENT_NAME_HERE"
```

#### 3c. 验证注册结果

```bash
curl https://api.openbotauth.org/jwks/YOUR_USERNAME.json
```

您应该能在`keys`数组中看到自己的公钥。这是验证器用于检查签名的URL。

**将`agent_id`、用户名和JWKS URL保存到代理的内存或笔记中**——这些信息将在每个签名请求的`Signature-Agent`请求头中使用。

### Token安全注意事项

| 操作 | 禁止的操作 |
|--------|-------|
| 使用`curl -H "Authorization: Bearer ..." https://api.openbotauth.org/agents` | 将token设置为浏览器的全局请求头 |
| 注册完成后删除token | 将token保留在浏览器会话中 |
| 使用基于源域的请求头进行签名 | 使用`set headers`命令时不要包含token |
| 将token保存在`~/.config/openbotauth/token`（权限设置为600） | 不要将token写入聊天记录 |

---

### 步骤4：签名请求

为目标URL生成符合RFC 9421标准的签名请求头。生成的JSON对象可用于`agent-browser open --headers`或`set headers --json`（OpenClaw）命令。

**所需参数：**
- `TARGET_URL`：要浏览的URL
- `METHOD`：HTTP方法（如GET、POST等）
- `JWKS_URL`：步骤3中获取的JWKS公钥地址

```bash
node -e "
const { createPrivateKey, sign, randomUUID } = require('crypto');
const { readFileSync } = require('fs');
const { join } = require('path');
const { homedir } = require('os');

const METHOD = (process.argv[1] || 'GET').toUpperCase();
const TARGET_URL = process.argv[2];
const JWKS_URL = process.argv[3] || '';

if (!TARGET_URL) { console.error('Usage: node sign.js METHOD URL JWKS_URL'); process.exit(1); }

const key = JSON.parse(readFileSync(join(homedir(), '.config', 'openbotauth', 'key.json'), 'utf-8'));
const url = new URL(TARGET_URL);
const created = Math.floor(Date.now() / 1000);
const expires = created + 300;
const nonce = randomUUID();

// RFC 9421 signature base
const lines = [
  '\"@method\": ' + METHOD,
  '\"@authority\": ' + url.host,
  '\"@path\": ' + url.pathname + url.search
];
const sigInput = '(\"@method\" \"@authority\" \"@path\");created=' + created + ';expires=' + expires + ';nonce=\"' + nonce + '\";keyid=\"' + key.kid + '\";alg=\"ed25519\"';
lines.push('\"@signature-params\": ' + sigInput);

const base = lines.join('\n');
const pk = createPrivateKey(key.privateKeyPem);
const sig = sign(null, Buffer.from(base), pk).toString('base64');

const headers = {
  'Signature': 'sig1=:' + sig + ':',
  'Signature-Input': 'sig1=' + sigInput
};
if (JWKS_URL) {
  headers['Signature-Agent'] = JWKS_URL;
}

console.log(JSON.stringify(headers));
" "METHOD" "TARGET_URL" "JWKS_URL"
```

示例参数：
- `METHOD`：例如`GET`
- `TARGET_URL`：例如`https://example.com/page`
- `JWKS_URL`：例如`https://api.openbotauth.org/jwks/your-username.json`

**对于要求严格的验证器**：如果目标网站不接受这种内联签名方式，建议使用`@openbotauth/bot-cli`或`openbotauth-demos/packages/signing-ts`提供的参考签名工具。

### 步骤5：将签名请求头应用于浏览器会话

**对于单次签名导航（演示/雷达验证）：**
```bash
agent-browser open <url> --headers '<OUTPUT_FROM_STEP_4>'
```
这种方式使用基于源域的请求头（更安全）。

**对于实际浏览（子资源/XHR请求）：** 使用签名代理（步骤A-C）。

**在OpenClaw浏览器中：**
```
set headers --json '<OUTPUT_FROM_STEP_4>'
```

**对于具有命名会话的情况：**
```bash
agent-browser --session myagent open <url> --headers '<OUTPUT_FROM_STEP_4>'
```

**重要提示：** 每次导航前都需要重新生成签名。** 由于RFC 9421签名与`@method`、`@authority`和`@path`相关联，因此在访问不同URL之前必须重新生成请求头。对于连续浏览，建议使用签名代理。

---

### 显示当前身份

```bash
node -e "
const { readFileSync, existsSync } = require('fs');
const { join } = require('path');
const { homedir } = require('os');
const f = join(homedir(), '.config', 'openbotauth', 'key.json');
if (!existsSync(f)) { console.log('No identity found. Run Step 2 first.'); process.exit(0); }
const k = JSON.parse(readFileSync(f, 'utf-8'));
console.log('kid:        ' + k.kid);
console.log('Public (x): ' + k.x);
console.log('Created:    ' + k.createdAt);
"
```

---

### 企业级单点登录（SSO）集成——开发计划

> **现状：** 尚未实现。这是未来的开发方向。

对于使用Okta、WorkOS或Descope的组织，OBA将支持将代理密钥与您的IdP（身份提供者）颁发的企业主体关联。OBA**不会替代**您的IdP目录——它只是为您已管理的身份添加可验证的代理密钥和审计记录。

**预计流程：**
1. 通过IdP（SAML/OIDC）进行身份验证
2. 将代理的公钥与相应的企业主体关联
3. 代理的签名将包含企业的身份信息

这会补充（而非替代）IdP原生提供的代理功能——让您获得可移植的密钥和Web验证机制。

---

### 签名请求头参考

每个签名请求都会生成以下符合RFC 9421标准的请求头：

| 请求头 | 用途 |
|--------|---------|
| `Signature` | 签名结果（base64编码的Ed25519签名） |
| `Signature-Input` | 包含签名涉及的组件（`@method @authority @path`）、签名时间、过期时间、密钥ID、加密算法等信息 |
| `Signature-Agent` | 用于解析公钥的JWKS URL（来自OBA注册表） |

`Signature-Input`包含了验证器所需的所有信息：哪些组件被签名、签名时间、签名者（密钥ID）以及签名有效期。

### 在OpenClaw中的会话关联

在OpenClaw环境中运行时，您可以将会话密钥包含在签名数据中或作为自定义参数，以便将签名与原始聊天记录关联起来：

```
agent:main:main                              # Main chat session
agent:main:discord:channel:123456789         # Discord channel
agent:main:subagent:<uuid>                   # Spawned sub-agent
```

这样可以帮助发布者判断请求是来自主代理还是子代理。

---

### 子代理身份（第二阶段——待开发）

子代理的密钥生成（基于父代理密钥的HKDF算法）已规划中，但目前尚未实现安全可靠的方案。目前，子代理应：
1. 生成自己的独立密钥对（步骤2）
2. 分别在OBA中注册（步骤3）
3. 父代理可以选择发布一个签名证明，将子代理的`kid`与其关联

相关的委托/证明协议正在设计中。

### 通过代理实现请求级签名（推荐用于实际浏览）

RFC 9421签名是**针对每个请求**生成的——它们与特定的方法、权限和路径相关联。步骤4-5仅适用于首次页面加载。对于子资源、XHR请求和重定向，使用签名代理会更加可靠。

**OpenClaw浏览器中的实现：**
```
set headers --json '<OUTPUT_FROM_STEP_4>'
```

**对于具有命名会话的情况：**
```bash
agent-browser --session myagent open <url> --headers '<OUTPUT_FROM_STEP_4>'
```

**重要提示：** 每次导航前都需要重新生成签名。** 由于RFC 9421签名依赖于`@method`、`@authority`和`@path`，因此在访问不同URL之前必须重新生成请求头。对于持续浏览，建议使用签名代理。

---

### 显示当前身份

```bash
node -e "
const { readFileSync, existsSync } = require('fs');
const { join } = require('path');
const { homedir } = require('os');
const f = join(homedir(), '.config', 'openbotauth', 'key.json');
if (!existsSync(f)) { console.log('No identity found. Run Step 2 first.'); process.exit(0); }
const k = JSON.parse(readFileSync(f, 'utf-8'));
console.log('kid:        ' + k.kid);
console.log('Public (x): ' + k.x);
console.log('Created:    ' + k.createdAt);
"
```

---

### 企业级单点登录（SSO）集成——开发计划

> **现状：** 尚未实现。这是未来的开发方向。

对于使用Okta、WorkOS或Descope的组织，OBA将支持将代理密钥与您的IdP颁发的企业主体关联。OBA**不会替代**您的IdP目录——它只是为您已管理的身份添加可验证的代理密钥和审计记录。

**预计流程：**
1. 通过IdP（SAML/OIDC）进行身份验证
2. 将代理的公钥与企业主体关联
3. 代理的签名将包含企业的身份信息

这会补充（而非替代）IdP原生提供的代理功能——让您获得可移植的密钥和Web验证机制。

---

### 签名请求头参考

每个签名请求都会生成以下符合RFC 9421标准的请求头：

| 请求头 | 用途 |
|--------|---------|
| `Signature` | 签名结果 |
| `Signature-Input` | 包含签名涉及的组件、签名时间、签名者（密钥ID）和签名有效期 |
| `Signature-Agent` | 用于解析公钥的JWKS URL |

`Signature-Input`包含了验证器所需的所有信息：哪些组件被签名、签名时间、签名者以及签名有效期。

### 在OpenClaw中的会话关联

在OpenClaw环境中运行时，您可以将会话密钥包含在签名数据中或作为自定义参数，以便将签名与原始聊天记录关联起来：

```
agent:main:main                              # Main chat session
agent:main:discord:channel:123456789         # Discord channel
agent:main:subagent:<uuid>                   # Spawned sub-agent
```

这样可以帮助发布者判断请求是来自主代理还是子代理。

---

### 子代理身份（第二阶段——待开发）

子代理的密钥生成（基于父代理密钥的HKDF算法）已规划中，但目前尚未实现安全可靠的方案。目前，子代理应：
1. 生成自己的独立密钥对（步骤2）
2. 分别在OBA中注册（步骤3）
3. 父代理可以选择发布一个签名证明，将子代理的`kid`与其关联

相关的委托/证明协议正在设计中。

### 通过代理实现请求级签名（推荐用于实际浏览）

RFC 9421签名是**针对每个请求**生成的——它们与特定的方法、权限和路径相关联。步骤4-5仅适用于首次页面加载。对于子资源、XHR请求和重定向，使用签名代理会更加可靠。

**解决方案：** 启动一个本地签名代理。该代理会拦截所有HTTP/HTTPS请求，并自动添加新的签名。无需外部包，仅使用Node.js内置功能和openssl。

#### 步骤A：将代理配置到临时文件

```bash
cat > /tmp/openbotauth-proxy.mjs << 'PROXY_EOF'
import { createServer as createHttpServer, request as httpRequest } from "node:http";
import { request as httpsRequest } from "node:https";
import { createServer as createTlsServer } from "node:tls";
import { connect, isIP } from "node:net";
import { createPrivateKey, sign as cryptoSign, randomUUID, createHash } from "node:crypto";
import { readFileSync, writeFileSync, existsSync, mkdirSync, unlinkSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import { execFileSync } from "node:child_process";

const OBA_DIR = join(homedir(), ".config", "openbotauth");
const KEY_FILE = join(OBA_DIR, "key.json");
const CONFIG_FILE = join(OBA_DIR, "config.json");
const CA_DIR = join(OBA_DIR, "ca");
const CA_KEY = join(CA_DIR, "ca.key");
const CA_CRT = join(CA_DIR, "ca.crt");

// Load credentials
if (!existsSync(KEY_FILE)) { console.error("No key found. Run keygen first."); process.exit(1); }
const obaKey = JSON.parse(readFileSync(KEY_FILE, "utf-8"));
let jwksUrl = null;
if (existsSync(CONFIG_FILE)) { const c = JSON.parse(readFileSync(CONFIG_FILE, "utf-8")); jwksUrl = c.jwksUrl || null; }

// Strict hostname validation (blocks shell injection & path traversal)
const HOSTNAME_RE = /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
function isValidHostname(h) {
  return typeof h === "string" && h.length > 0 && h.length <= 253 && (HOSTNAME_RE.test(h) || isIP(h) > 0);
}

// Ensure CA exists
mkdirSync(CA_DIR, { recursive: true, mode: 0o700 });
if (!existsSync(CA_KEY) || !existsSync(CA_CRT)) {
  console.log("Generating proxy CA certificate (one-time)...");
  execFileSync("openssl", ["req", "-x509", "-new", "-nodes", "-newkey", "ec", "-pkeyopt", "ec_paramgen_curve:prime256v1", "-keyout", CA_KEY, "-out", CA_CRT, "-days", "3650", "-subj", "/CN=OpenBotAuth Proxy CA/O=OpenBotAuth"], { stdio: "pipe" });
  execFileSync("chmod", ["600", CA_KEY], { stdio: "pipe" });
}

// Per-domain cert cache
const certCache = new Map();
function getDomainCert(hostname) {
  if (!isValidHostname(hostname)) throw new Error("Invalid hostname: " + hostname.slice(0, 50));
  if (certCache.has(hostname)) return certCache.get(hostname);
  // Use hash for filenames to prevent path traversal
  const hHash = createHash("sha256").update(hostname).digest("hex").slice(0, 16);
  const tk = join(CA_DIR, `_t_${hHash}.key`), tc = join(CA_DIR, `_t_${hHash}.csr`);
  const to = join(CA_DIR, `_t_${hHash}.crt`), te = join(CA_DIR, `_t_${hHash}.ext`);
  try {
    execFileSync("openssl", ["ecparam", "-genkey", "-name", "prime256v1", "-noout", "-out", tk], { stdio: "pipe" });
    execFileSync("openssl", ["req", "-new", "-key", tk, "-out", tc, "-subj", `/CN=${hostname}`], { stdio: "pipe" });
    writeFileSync(te, `subjectAltName=DNS:${hostname}\nbasicConstraints=CA:FALSE\nkeyUsage=digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth`);
    execFileSync("openssl", ["x509", "-req", "-sha256", "-in", tc, "-CA", CA_CRT, "-CAkey", CA_KEY, "-CAcreateserial", "-out", to, "-days", "365", "-extfile", te], { stdio: "pipe" });
    const r = { key: readFileSync(tk, "utf-8"), cert: readFileSync(to, "utf-8") };
    certCache.set(hostname, r);
    return r;
  } finally { for (const f of [tk, tc, to, te]) try { unlinkSync(f); } catch {} }
}

// RFC 9421 signing
function signReq(method, authority, path) {
  const created = Math.floor(Date.now() / 1000), expires = created + 300, nonce = randomUUID();
  const lines = [`"@method": ${method.toUpperCase()}`, `"@authority": ${authority}`, `"@path": ${path}`];
  const sigInput = `("@method" "@authority" "@path");created=${created};expires=${expires};nonce="${nonce}";keyid="${obaKey.kid}";alg="ed25519"`;
  lines.push(`"@signature-params": ${sigInput}`);
  const sig = cryptoSign(null, Buffer.from(lines.join("\n")), createPrivateKey(obaKey.privateKeyPem)).toString("base64");
  const h = { signature: `sig1=:${sig}:`, "signature-input": `sig1=${sigInput}` };
  if (jwksUrl) h["signature-agent"] = jwksUrl;
  return h;
}

const verbose = process.argv.includes("--verbose") || process.argv.includes("-v");
const port = parseInt(process.argv.find((a,i) => process.argv[i-1] === "--port")) || 8421;
let rc = 0;
function log(id, msg) { if (verbose) console.log(`[${id}] ${msg}`); }

const server = createHttpServer((cReq, cRes) => {
  const id = ++rc, url = new URL(cReq.url), auth = url.host, p = url.pathname + url.search;
  const sig = signReq(cReq.method, auth, p);
  log(id, `HTTP ${cReq.method} ${auth}${p} → signed`);
  const h = { ...cReq.headers }; delete h["proxy-connection"]; delete h["proxy-authorization"];
  Object.assign(h, sig); h.host = auth;
  const fn = url.protocol === "https:" ? httpsRequest : httpRequest;
  const pr = fn({ hostname: url.hostname, port: url.port || (url.protocol === "https:" ? 443 : 80), path: p, method: cReq.method, headers: h }, (r) => { cRes.writeHead(r.statusCode, r.headers); r.pipe(cRes); });
  pr.on("error", (e) => { log(id, `Error: ${e.message}`); cRes.writeHead(502); cRes.end("Proxy error"); });
  cReq.pipe(pr);
});

server.on("connect", (req, cSock, head) => {
  const id = ++rc, [host, ps] = req.url.split(":"), tp = parseInt(ps) || 443;
  // Validate host and port before processing
  if (!isValidHostname(host) || tp < 1 || tp > 65535) {
    log(id, `CONNECT rejected: invalid ${host}:${tp}`);
    cSock.write("HTTP/1.1 400 Bad Request\r\n\r\n"); cSock.end(); return;
  }
  log(id, `CONNECT ${host}:${tp} → MITM`);
  cSock.write("HTTP/1.1 200 Connection Established\r\nProxy-Agent: openbotauth-proxy\r\n\r\n");
  const dc = getDomainCert(host);
  const tls = createTlsServer({ key: dc.key, cert: dc.cert }, (ts) => {
    let data = Buffer.alloc(0);
    ts.on("data", (chunk) => {
      data = Buffer.concat([data, chunk]);
      const he = data.indexOf("\r\n\r\n");
      if (he === -1) return;
      const hs = data.subarray(0, he).toString(), body = data.subarray(he + 4);
      const ls = hs.split("\r\n"), [method, path] = ls[0].split(" ");
      const rh = {};
      for (let i = 1; i < ls.length; i++) { const c = ls[i].indexOf(":"); if (c > 0) rh[ls[i].substring(0, c).trim().toLowerCase()] = ls[i].substring(c + 1).trim(); }
      const cl = parseInt(rh["content-length"]) || 0, fp = path || "/";
      const sig = signReq(method, host + (tp !== 443 ? `:${tp}` : ""), fp);
      log(id, `HTTPS ${method} ${host}${fp} → signed`);
      Object.assign(rh, sig);
      const pr = httpsRequest({ hostname: host, port: tp, path: fp, method, headers: rh, rejectUnauthorized: true }, (r) => {
        let resp = `HTTP/1.1 ${r.statusCode} ${r.statusMessage}\r\n`;
        const rw = r.rawHeaders; for (let i = 0; i < rw.length; i += 2) resp += `${rw[i]}: ${rw[i+1]}\r\n`;
        resp += "\r\n"; ts.write(resp); r.pipe(ts);
      });
      pr.on("error", (e) => { log(id, `Error: ${e.message}`); ts.end("HTTP/1.1 502 Bad Gateway\r\nContent-Length: 0\r\n\r\n"); });
      if (body.length > 0) pr.write(body);
      if (cl <= body.length) { pr.end(); } else {
        let recv = body.length;
        const bh = (d) => { recv += d.length; pr.write(d); if (recv >= cl) { pr.end(); ts.removeListener("data", bh); } };
        ts.on("data", bh);
      }
    });
  });
  tls.listen(0, "127.0.0.1", () => {
    const lc = connect(tls.address().port, "127.0.0.1", () => { lc.write(head); lc.pipe(cSock); cSock.pipe(lc); });
    lc.on("error", () => cSock.end()); cSock.on("error", () => lc.end());
    cSock.on("close", () => { tls.close(); lc.end(); });
  });
});

server.listen(port, "127.0.0.1", () => {
  console.log(`openbotauth signing proxy on http://127.0.0.1:${port}`);
  console.log(`  kid: ${obaKey.kid}`);
  if (jwksUrl) console.log(`  Signature-Agent: ${jwksUrl}`);
  console.log("Every request gets a fresh RFC 9421 signature.");
});
PROXY_EOF
echo "Proxy written to /tmp/openbotauth-proxy.mjs"
```

#### 步骤B：启动代理

```bash
node /tmp/openbotauth-proxy.mjs --verbose
```

在`127.0.0.1:8421`端口上启动签名代理。所有通过该代理的HTTP和HTTPS请求都会被添加新的RFC 9421 Ed25519签名。

#### 步骤C：通过代理进行浏览

在另一个终端或通过agent-browser进行浏览：

```bash
# For demos (ignore cert warnings):
agent-browser --proxy http://127.0.0.1:8421 --ignore-https-errors open https://example.com

# For production: install ~/.config/openbotauth/ca/ca.crt as trusted CA
```

**TLS注意事项：** 该代理通过生成由本地CA签发的域名证书来实现HTTPS中间人（MITM）功能。** 可以选择：
- 在演示或测试环境中使用`--ignore-https-errors`选项
- 安装`~/.config/openbotauth/ca/ca.crt`作为受信任的CA证书以获得稳定的代理行为

代理功能：
- 为所有出站请求添加新的RFC 9421签名
- 支持HTTP和HTTPS请求（为HTTPS请求生成本地CA证书）
- 在每个请求中包含`Signature-Agent`请求头（JWKS URL）
- 默认运行在`127.0.0.1:8421`端口（可通过`--port`参数调整）
- 需要在macOS/Linux系统中预先安装openssl以生成HTTPS证书

**安全提示：** `~/.config/openbotauth/ca/ca.key`是一个用于中间人功能的根证书。请将其视为敏感文件——如果被窃取，攻击者可以拦截该机器上的所有网络流量。

**限制：**
- 该代理不支持HTTP/2、WebSocket和多路复用连接
- 仅适用于演示和基本浏览场景；不适合生产环境
- **基于IP的域名：** 如果目标地址是IP地址，建议拒绝此类请求，或者使用`subjectAltName=IP:<ip>`代替`DNS:`（当前代码使用DNS，但某些严格的安全策略可能会拒绝此类请求）

**何时使用步骤4-5：** 适用于您能够控制每次导航操作且可以在每次导航前重新生成签名的简单单页加载场景。

---

### 重要提示

- 私钥存储在`~/.config/openbotauth/key.json`文件中，权限设置为0600——切勿泄露
- OBA token也存储在`~/.config/openbotauth/token`文件中，同样需要保密
- `Signature-Agent`必须指向一个可公开访问的JWKS URL才能正常工作
- 所有加密操作均使用Node.js内置的`crypto`模块——无需依赖npm包
- **安全提示：** 绝不要将私钥或OBA token发送到除`api.openbotauth.org`以外的任何域名
- **Token生命周期：** 注册完成后立即删除`~/.config/openbotauth/token`文件。后续签名操作不再需要该文件
- **浏览器会话：** 注册完成后，只有签名数据会通过网络传输，token应保留在本地
- **关于全局请求头的使用：** 在agent-browser中，切勿使用`set headers`命令与bearer token关联请求头。请使用`open --headers`命令来设置基于源域的请求头

---

### 文件结构

```
~/.config/openbotauth/
├── key.json       # kid, x, publicKeyPem, privateKeyPem (chmod 600)
├── key.pub.json   # Public JWK for sharing (chmod 644)
├── config.json    # Agent ID, JWKS URL, registration info
├── token          # oba_xxx bearer token (chmod 600)
└── ca/            # Proxy CA certificate (auto-generated)
    ├── ca.key     # CA private key
    └── ca.crt     # CA certificate
```

### 运行时兼容性

| 运行时环境 | 支持情况 | 备注 |
|---------|---------|-------|
| Claude Code / Cursor / Codex | 完全支持 | 推荐使用CLI进行注册 |
| agent-browser | 完全支持 | 使用基于源域的请求头，避免使用全局请求头 |
| OpenClaw Browser Relay | 注册后支持 | 首先需要通过CLI进行注册 |
| CUA / Browser Control | 注意：**请将控制平面视为潜在的安全风险** |
| skills.sh | 完全支持 | 使用curl进行注册是安全的 |

**对于浏览器环境：** 所有注册操作均需通过CLI完成。签名代理仅需要私钥（本地存储）和JWKS URL（公开访问）。浏览过程中无需携带bearer token。

### 官方软件包

对于生产环境集成，建议使用以下官方软件包：
- `@openbotauth/verifier-client`：用于验证签名
- `@openbotauth/registry-signer`：用于生成密钥和JWK相关操作
- `@openbotauth/bot-cli`：用于签名请求的CLI工具
- `@openbotauth/proxy`：用于实现签名代理

对于需要严格遵循RFC 9421标准的签名功能，建议使用`openbotauth-demos`提供的参考签名工具（`packages/signing-ts`）。

### 参考链接

- **官方网站：** https://openbotauth.org
- **API接口：** https://api.openbotauth.org
- **技术规范：** https://github.com/OpenBotAuth/openbotauth
- **IETF标准：** Web Bot Auth Architecture草案