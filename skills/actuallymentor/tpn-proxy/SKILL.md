---
name: tpn-proxy
aliases: [tpn, subnet-65, sn65, proxy, socks5]
description: 通过 Tao Private Network (TPN) 使用去中心化的 SOCKS5 代理来发起网络请求。该功能也被称为“TPN”、“TPN 代理”、“subnet 65”或“SN65”。当用户要求“运行 TPN”、“使用代理”或提到“subnet 65”时，指的就是这个功能。该功能适用于以下场景：通过代理路由 HTTP 流量、进行匿名网络请求、访问受地理限制的内容、使用去中心化的 VPN、通过 SOCKS5 代理获取 URL，或需要使用住宅区的代理 IP 地址。它支持集中式的 API 密钥认证以及去中心化的 x402 微支付方式。
metadata: { "openclaw": { "emoji": "📡", "requires": { "bins": ["curl"], "env": ["TPN_API_KEY"] }, "primaryEnv": "TPN_API_KEY" } }
---
# TPN去中心化SOCKS5代理

该功能通过Tao Private Network的去中心化SOCKS5代理路由网络流量。这些代理属于Bittensor子网（SN65），在80多个国家拥有商业和住宅类型的出口节点。

你可以使用以下命令来请求相关服务：

- 通过德国的代理访问`https://ipv4.icanhazip.com`
- 使用美国IP地址代理访问`google.com`
- 请求在日本使用SOCKS5代理，时长为30分钟
- 查看TPN支持哪些国家的代理服务

---

## 安全性

| 方面 | 详情 |
|--------|--------|
| 环境变量 | `TPN_API_KEY` — 仅用于检查是否存在（`[ -n "$TPN_API_KEY" ]`），不会被回显或记录 |
| 读取/写入的文件 | 无 |
| 访问的其他秘密信息 | 无 — 除了`TPN_API_KEY`外，没有其他密钥或凭证 |
| 网络目的地 | `api.taoprivatenetwork.com`（API调用）+ 用户指定的URL（根据第5步进行验证） |
| x402签名 | 完全由外部库处理（`@x402/*`）；该功能仅提供端点URL |

---

## 这是一个动作技能

该技能会执行API调用并直接返回结果，不会向用户显示文档或操作指南。

**预期行为：**

- 你需自行调用TPN API（通过`curl`或其他工具），并将完整的代理凭证返回给用户。
- 当用户请求通过代理访问某个URL时，你也需自行发起该请求。
- 显示完整的SOCKS5凭证（用户名、密码、主机、端口）——这些凭证是临时性的，仅适用于当前代理租用期间。
- 仅当用户明确询问“我该如何自己操作？”时，才需要向用户说明如何调用API。
- 如果没有API密钥，需指导用户完成账户设置——这是用户唯一能自行完成的步骤。

**注意事项：** 如果你的回复中包含“你可以运行这个命令来...”或“使用这个curl来生成...”，请重新考虑——用户使用该技能时期望你直接执行命令并给出结果。

---

## 分步流程

每次用户请求代理或请求通过代理访问某个URL时，请遵循以下步骤：

### 安全性：输入验证（强制要求）

在构建任何shell命令之前，**必须验证用户提供的所有输入**。切勿将原始用户输入直接插入shell命令中。

| 输入              | 验证规则                                                                                     |
|--------------------|------------------------------------------------------------------------------------------------------|
| `geo`              | 必须是2个大写的ASCII字母（ISO 3166-1 alpha-2编码）。拒绝其他格式。                |
| `minutes`          | 必须是1到1440之间的正整数。拒绝非数字或超出范围的值。            |
| `connection_type`  | 必须是`any`、`datacenter`或`residential`之一。拒绝其他值。                            |
| `format`           | 必须是`text`或`json`之一。拒绝其他格式。                                                |
| URL（第5步使用）      | 必须以`http://`或`https://`开头，不能包含shell特殊字符，并且是一个格式正确的URL。 |

**规则：**

- **切勿** 将原始用户输入直接插入shell命令中。务必先进行验证。
- **切勿** 通过字符串连接用户输入来构建 `-d` JSON负载。使用安全的静态模板，并仅插入经过验证的值。
- 使用`curl`时，务必对URL和代理URI参数进行转义。
- 建议使用代理内置的HTTP工具（如`WebFetch`）来获取用户指定的URL，而不是手动构建`curl`命令。

### 第1步：获取API密钥

检查环境变量`$TPN_API_KEY`是否已设置（OpenClaw会自动从配置文件中读取该密钥）：

1. 测试该变量：`[ -n "$TPN_API_KEY" ] && echo "API key is set" || echo "API key is not set"` — **切勿** 回显或记录密钥值本身。
2. 如果未设置 → 检查用户是否可以通过[x402](https://www.x402.org)支付（无需API密钥）；否则指导用户完成账户设置（参见“设置TPN”部分）。

### 第2步：选择响应格式

| 情况 | 使用 `format` | 原因 |
|-----------|--------------|-----|
| 只需要一个有效的代理URI | `text`（默认） | 无需解析 |
| 需要显示结构化的主机/端口/用户名/密码信息 | `json` | 可以获取各个字段 |
| 不确定 | `text` | 更简单，出错的可能性更低 |

如果选择`json`，请使用`jq`解析响应：

```bash
curl -s ... | jq -r '.vpnConfig.username'
```

如果`jq`不可用，可以使用`format=text`——它返回一个不需要解析的简单`socks5://` URI。

> **切勿** 使用`python -c`、`grep`、`cut`或其他基于shell的JSON解析方法。这些方法在处理动态输入时可能存在安全风险。请始终使用`jq`或`format=text`。

### 第3步：生成代理

将用户的请求参数映射到以下字段：

| 参数             | 类型    | 是否必填 | 默认值 | 描述                                    |
|-------------------|---------|----------|---------|------------------------------------------------|
| `minutes`         | 整数 | 是      | —       | 租用时长（1–1440分钟）。未指定时默认为60分钟。 |
| `geo`             | 字符串  | 否       | 任意     | ISO国家代码（例如`"US"`、`"DE"`、`"JP"`） |
| `format`          | 字符串  | 否       | `text`  | URI格式为`text`，对象格式为`json`   |
| `connection_type` | 字符串  | 否       | `any`   | `any`、`datacenter`或`residential`    |

> **安全的JSON格式构建：** 在构建curl命令之前，务必先验证`geo`（2个大写字母）、`minutes`（1–1440分钟）、`connection_type`（枚举值）和`format`（枚举值）。切勿将原始用户输入直接插入JSON正文或命令的任何部分。

### 第4步：展示结果

向用户展示**完整的代理凭证**，以便他们立即连接。这些凭证是临时性的（仅适用于当前租用期间），并且在当前上下文中显示是安全的。使用`socks5h://`协议（其中包含`h`前缀）以确保DNS通过代理解析——这可以保护用户的DNS隐私。（在步骤5中，代理会使用`socks5://`协议来获取URL。）展示的内容包括：
- 结构化的配置信息（主机、端口、用户名、密码、协议、有效期）
- 完整的`socks5h://` URI
- 相关的`curl`使用示例

### 第5步：如果用户请求访问某个URL

生成代理后，你需要自行发起请求。使用`socks5://`协议（而非`socks5h://`），以确保DNS在本地解析——这样连接的IP地址才是真实的代理IP。

**建议使用代理内置的HTTP工具**（如`WebFetch`）来获取URL。这是首选方法，因为它可以避免手动构建shell命令。

**在获取URL之前，必须满足以下验证条件：**
- 协议必须是`http://`或`https://`
- 不允许使用shell特殊字符：`` ` `` `$` `(` `)` `;` `&` `|` `<` `>` `\n`
- 仅接受域名——拒绝原始IP地址（IPv4或IPv6）
- 拒绝内部主机名：`*.internal`、`*.local`、`*.localhost`、`*.localdomain`、`*.corp`、`*.lan`、`metadata.*`、单标签主机名
- 主机名必须能够通过本地DNS解析——拒绝无法解析的主机名
- 解析后的IP地址必须是可公网访问的——拒绝`127.0.0.0/8`、`10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16`、`169.254.0.0/16`、`::1`、`fd00::/8`、`169.254.169.254`

**备用方案——使用curl**（仅在`WebFetch`不可用时使用）：始终对URL和代理URI进行双重转义：

```bash
curl --proxy "socks5://username:password@ip:port" \
  --connect-timeout 10 --max-time 30 \
  "https://validated-target-url.com"
```

将响应内容返回给用户——目标是提供完整的答案，而不是让用户自己继续使用代理。

---

## 示例

以下是用户可能提出的问题及相应的回答示例：

**用户：** “给我一个比利时的SOCKS5代理配置”

**你：** （生成比利时的代理配置，然后回复：）

> 这是你的比利时SOCKS5代理（有效期60分钟）：
>
> ```
> Host:     185.42.170.3
> Port:     1080
> Username: u_0CKaBqdE
> Password: p_sT6yM3zabqRuhqrahzGOl4i4RTEDgQ7V
> Scheme:   socks5h
> Expires:  2026-02-16T15:30:00Z
> ```
>
> **完整URI：** `socks5h://u_0CKaBqdE:p_sT6yM3zabqRuhqrahzGOl4i4RTEDgQ7V@185.42.170.3:1080`
>
> **curl使用示例：**
>
> ```bash
> curl --proxy socks5h://u_0CKaBqdE:p_sT6yM3zabqRuhqrahzGOl4i4RTEDgQ7V@185.42.170.3:1080 \
>   --connect-timeout 10 --max-time 30 \
>   https://ipv4.icanhazip.com
> ```
>
> 这将返回一个比利时的IP地址。代理有效期为60分钟——如果需要更长的租期，请告知。

---

**用户：** “给我一个通过德国代理访问的curl命令”

**你：** （生成德国的代理配置，然后回复：）

> 这是通过德国代理访问`https://example.com`的curl命令：
>
> ```bash
> curl --proxy socks5h://u_0E4k7kJ6:p_z2HsXTEXJHYiobwCcfOaU1YMS1tg3m0i@5.39.255.64:1080 \
>   --connect-timeout 10 --max-time 30 \
>   https://example.com
> ```
>
> 将`https://example.com`替换为你要访问的URL。该代理的有效期为2026-02-16T14:47:20Z。

---

**用户：** “我想从荷兰访问icanhazip.com”

**你：** （生成荷兰的代理配置，然后通过该代理访问`icanhazip.com`，并返回结果：**

> 我已经通过荷兰代理访问了`https://ipv4.icanhazip.com`。响应结果如下：
>
> ```
> 82.148.30.91
> ```
>
> 这是荷兰的出口IP地址。该代理的有效期为2026-02-16T15:12:00Z，如需更多请求，请告知。

---

**用户：** “我需要一个美国的住宅代理，时长2小时”

**你：** （生成美国的住宅代理配置，然后回复：**

> 这是你的美国住宅代理（有效期2小时，消耗25个信用点）：
>
> ```
> Host:     68.210.185.149
> Port:     1080
> Username: u_02NyffuT
> Password: p_CIYLqgIyLZ1rSvZGQbdh3lyxQQBcBsQn
> Scheme:   socks5h
> Type:     residential
> Expires:  2026-02-16T16:41:00Z
> ```
>
> **完整URI：** `socks5h://u_02NyffuT:p_CIYLqgIyLZ1rSvZGQbdh3lyxQQBcBsQn@68.210.185.149:1080`
>
> 住宅代理被阻止的可能性较低。如果需要其他国家的代理，请告知。

---

**用户：** “我还有多少信用点？**

**你：** （调用`GET /api/v1/user/balance`获取信息，然后回复：**

> 你目前还有**74个信用点**。
>
> 参考信息：60分钟的代理费用为20个信用点，10分钟的代理费用为10个信用点。你可以在https://api.taoprivatenetwork.com购买更多信用点——套餐价格从1,000信用点起，价格为9.99美元。

---

**用户：** “使用代理查看我的网站在德国的显示效果”

**你：** （生成德国的代理配置，然后访问用户的网站，并返回结果：**

> 我已经通过德国代理访问了你的网站（IP地址：`91.203.50.12`）：
>
> - **状态：** 200 OK
> - **内容语言：** `de` — 看起来你的网站检测到了德国IP并显示了德语版本
> - **页面标题：** “欢迎访问Example”
>
> 对德国用户来说，一切显示正常。还需要在其他国家测试吗？

---

**用户：** “如何设置TPN？” / “我该如何开始使用TPN？”

**你：** （检查用户是否已有API密钥——如果有，告知他们已设置完成；如果没有：**

> 要开始使用TPN，请：
>
> 1. 访问https://api.taoprivatenetwork.com创建账户
> 2. 在控制面板中生成API密钥（格式类似`tpn-abc123...`）
> 3. 你的第一个密钥包含**100个免费信用点**，足够使用大约5次代理服务
>
> 生成密钥后，请分享给我，我会保存下来以便后续使用。

---

**操作模式：** 用户提出请求，你执行操作，然后返回结果。** 你永远不会告诉用户如何调用API——你自行调用API并将结果返回给他们。

---

## API参考

**基础URL：** `https://api.taoprivatenetwork.com`

**认证：** 在请求头中传递`X-API-Key: <你的密钥>`。不要使用`Authorization: Bearer`。

### 端点

| 方法 | 路径                          | 认证方式 | 描述                     |
|--------|-------------------------------|------------|---------------------------------|
| POST   | `/api/v1/proxy/generate`      | API密钥    | 生成SOCKS5代理           |
| POST   | `/api/v1/vpn/generate`        | API密钥    | 生成WireGuard VPN          |
| GET    | `/api/v1/user/balance`        | API密钥    | 查看信用点余额            |
| GET    | `/api/v1/vpn/countries`       | 无       | 列出可用国家        |
| POST   | `/api/v1/vpn/cost`            | 无       | 计算信用点费用           |
| GET    | `/api/v1/vpn/stats`           | 无       | 网络统计信息              |
| GET    | `/api/v1/health`              | 无       | 系统健康检查                    |
| POST   | `/api/v1/x402/proxy/generate` | x402       | 生成SOCKS5代理（x402协议）    |
| POST   | `/api/v1/x402/vpn/generate`   | x402       | 生成WireGuard VPN（x402协议）   |

### 响应格式

**`/proxy/generate`（格式为`text`时：**

```json
{
  "success": true,
  "vpnConfig": "socks5://u_02NyffuT:p_CIYLqgIyLZ1rSvZGQbdh3lyxQQBcBsQn@9.160.73.2:1080",
  "minutes": 60,
  "expiresAt": "2026-02-14T19:08:25.690Z",
  "creditsUsed": 20,
  "type": "socks5"
}
```

**`/proxy/generate`（格式为`json`时：**

```json
{
  "success": true,
  "vpnConfig": {
    "username": "u_0CKaBqdE",
    "password": "p_sT6yM3zabqRuhqrahzGOl4i4RTEDgQ7V",
    "ip_address": "68.210.185.149",
    "port": 1080
  },
  "minutes": 60,
  "expiresAt": "2026-02-14T19:08:23.958Z",
  "creditsUsed": 20,
  "usedFallback": false,
  "type": "socks5",
  "connection_type": "any"
}
```

### `/vpn/countries`查询参数

| 参数             | 类型   | 默认值 | 描述                                      |
|-------------------|--------|---------|--------------------------------------------------|
| `format`          | 字符串 | `json`  | `"json"`表示数组，`text`表示换行分隔的列表 |
| `type`            | 字符串 | `code`  | `"code"`表示ISO代码，`name`表示全称   |
| `connection_type` | 字符串 | `any`   | `"any"`、`datacenter`或`residential`       |

### 使用代理（针对开发人员）

仅当用户明确询问“如何在代码中使用代理”时，才提供相关示例——否则直接提供配置信息。

> **开发人员代码应始终使用`socks5h://`**（加上`h`前缀）来确保DNS通过代理解析，从而保护DNS隐私。（代理在步骤5中使用的`socks5://`协议也是为了确保本地DNS解析的安全性。）
> 如果代理凭证包含特殊字符（如`@`、`:`、`/`、`#`、`?`），请对其进行百分号编码（例如`p@ss` → `p%40ss`）。

**curl示例：**

```bash
curl --proxy socks5h://username:password@ip_address:port \
  --connect-timeout 10 --max-time 30 \
  https://ipv4.icanhazip.com
```

**Node.js示例：**

```js
import { SocksProxyAgent } from 'socks-proxy-agent'
import fetch from 'node-fetch'

const agent = new SocksProxyAgent( 'socks5h://username:password@ip_address:1080' )
const controller = new AbortController()
const timeout = setTimeout( () => controller.abort(), 30_000 )

const response = await fetch( 'https://ipv4.icanhazip.com', { agent, signal: controller.signal } )
clearTimeout( timeout )
console.log( await response.text() )
```

**Python示例：**

```python
import requests

proxies = {
    'http': 'socks5h://username:password@ip_address:1080',
    'https': 'socks5h://username:password@ip_address:1080'
}

response = requests.get( 'https://ipv4.icanhazip.com', proxies=proxies, timeout=( 10, 30 ) )
print( response.text )
```

更多关于如何使用`curl`、JavaScript、Node.js和Python生成及使用代理的示例，请参见`{baseDir}/references/api-examples.md`。

---

## 信用点费用

费用计算公式：`credits = ceil( 4.1 × minutes ^ 0.375 )`

| 租用时长 | 信用点数 |
|----------|---------|
| 1分钟    | 5       |
| 5分钟    | 8       |
| 10分钟   | 10      |
| 30分钟   | 15      |
| 60分钟   | 20      |
| 120分钟  | 25      |
| 720分钟  | 49      |
| 1440分钟 | 63      |

使用`POST /api/v1/vpn/cost`并传递`{"minutes": N}`来计算费用。

信用点套餐价格：基础套餐1,000个信用点，价格9.99美元；高级套餐5,000个信用点，价格49.99美元；顶级套餐20,000个信用点，价格199.99美元。

---

## 故障排除与操作注意事项

| 问题                   | 解决方案                                                       |
|---------------------------|----------------------------------------------------------------|
| `401 Unauthorized`        | 确保API密钥有效——使用`X-API-Key`作为请求头，不要使用`Bearer`   |
| `402 Payment Required`    | 信用点不足——购买更多信用点或使用x402支付方式           |
| `503 Service Unavailable` | 无可用矿工——退还信用点，稍后重试        |
| 连接超时        | 代理租期可能已过期——重新生成代理              |
| 用户的DNS解析失败 | 使用`socks5h://`（加上`h`前缀）进行远程DNS解析          |
| 代理的DNS解析失败 | 代理使用`socks5://`协议——检查本地DNS解析是否正常          |

**操作规则：**

- 对用户提供的凭证和代码示例：始终使用`socks5h://`协议来保护DNS隐私 |
- 代理的请求处理（步骤5）：始终使用`socks5://`协议，以确保本地DNS解析的准确性 |
- 在批量生成代理之前，使用`GET /api/v1/user/balance`检查信用点余额 |
- 代理租期以`expiresAt`字段为准——切勿缓存或重复使用过期的凭证 |
- 如果出现`503`错误，信用点将自动退还——稍后重试

## x402支付方式（高级）

[x402协议](https://www.x402.org)支持使用USDC进行按请求计费的访问。无需账户或API密钥——非常适合已经支持x402协议的代理。

如果你是支持x402协议的代理，你应该已经知道如何处理支付流程。TPN的x402端点遵循以下标准：

1. 发送`POST /api/v1/x402/proxy/generate`请求——返回`HTTP 402`状态码及`payment-required`请求头
2. 按照[x402协议](https://www.x402.org)完成支付流程
3. 重新发送请求以获取SOCKS5代理的凭证

请求体与普通端点相同。无需提供`X-API-Key`。

更多关于x402协议的示例（包括curl和浏览器JS代码）请参见`{baseDir}/references/x402-examples.md`，详细协议规范请参考[https://www.x402.org`。签名处理完全由外部库负责——该功能仅提供端点URL。

---

## 链接

- 控制面板和账户：https://api.taoprivatenetwork.com
- API文档：https://api.taoprivatenetwork.com/docs/getting-started/
- Swagger UI：https://api.taoprivatenetwork.com/api-docs/
- OpenAPI规范：https://api.taoprivatenetwork.com/api-docs/openapi.json
- 适合大型语言模型的文档：https://api.taoprivatenetwork.com/docs/llms-full.txt
- x402协议详情：https://www.x402.org