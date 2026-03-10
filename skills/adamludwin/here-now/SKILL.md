---
name: here-now
description: 将文件和文件夹即时发布到网络上。支持静态托管 HTML 网站、图片、PDF 以及所有类型的文件。适用于需要执行以下操作的场景：发布内容、托管资源、在网络上共享、创建网站、将文件上传到网站、生成网页链接、提供网站访问服务或生成 URL。系统会生成一个可分享的实时 URL，格式为 {slug}.here.now。
---
# here.now

**技能版本：1.6.7**

**功能：** 从任意文件或文件夹创建一个实时URL。仅支持静态托管。

**安装或更新方法（推荐）：** `npx skills add heredotnow/skill --skill here-now -g`

**对于从仓库克隆或本地安装的情况：** 不需要使用 `-g` 参数。

**如果无法使用npm，请参考备用安装文档：** https://here.now/docs#install-skill

## **系统要求：**
- 必需的软件：`curl`、`file`、`jq`
- 可选的环境变量：`$HERENOW_API_KEY`
- 可选的凭证文件：`~/.herenow/credentials`

## **创建一个实时URL**

执行以下命令后，将会生成一个实时URL（例如：`https://bright-canvas-a7k2.here.now/`）。

**工作原理：** 全过程分为三个步骤：创建/更新文件 → 上传文件 → 完成生成。只有当所有步骤都成功完成后，URL才会生效。

- **无API密钥的情况：** 生成的URL为临时URL，有效期为24小时。
- **使用API密钥的情况：** 生成的URL为永久URL。

**文件结构：**  
- 对于HTML网站，请将 `index.html` 文件放在发布的目录的根目录中，不要放在子目录内。整个目录内容将成为网站的根目录。例如，如果发布路径为 `my-site/`，则确保 `my-site/index.html` 位于该目录中。
- 即使没有HTML文件，也可以直接发布原始文件。系统会自动为这些文件生成相应的查看器（支持图片、PDF、视频、音频格式）。
- 如果发布多个文件，系统会自动生成一个包含文件列表和图片库的页面。

## **更新现有URL**

在更新临时URL时，脚本会自动从 `.herenow/state.json` 文件中读取 `claimToken`。如果需要覆盖该值，可以使用 `--claim-token {token}` 参数。

**身份验证更新：** 需要使用已保存的API密钥。

## **客户端信息记录**

通过 `--client` 参数，可以记录发送请求的客户端信息，以便 here.now 系统追踪请求来源。

**注意：** 在调用API时，系统会自动添加 `X-HereNow-Client: cursor/publish-sh` 标头。如果省略此参数，系统会使用默认值。

## **API密钥的存储方式：**

API密钥可以从以下位置读取（优先级从高到低）：
1. `--api-key {key}` 参数（仅用于持续集成/脚本环境，避免在交互式使用中使用）
2. 环境变量 `$HERENOW_API_KEY`
3. 凭证文件 `~/.herenow/credentials`（建议使用）

**重要提示：** **切勿在shell命令中直接输入API密钥**，请使用上述命令将其保存到 `~/.herenow/credentials` 文件中。这样可以防止密钥被记录在终端历史记录或日志中。

**注意事项：** **切勿将凭证文件或状态文件（`~/.herenow/credentials`、`.herenow/state.json`）提交到版本控制系统中。**

## **状态文件：**

每次创建或更新URL后，脚本都会更新 `./herenow/state.json` 文件。

**使用说明：**
- 可以查看该文件以获取之前的URL信息。
- 请将 `.herenow/state.json` 文件视为内部缓存文件，切勿将其作为URL或身份验证信息的来源。

**用户须知：**
- **分享信息时：** 始终分享当前脚本运行生成的 `siteUrl`。
- **查看更新结果：** 请查看脚本标准输出（stderr）中的 `publish_result.*` 行。
- **关于有效期：** 仅当 `publish_result.auth_mode=anonymous` 时，才会显示“有效期为24小时”。
- **分享URL时：** 仅当 `publish_result.claim_url` 不为空且以 `https://` 开头时，才分享完整的URL。
- **关于密钥：** 请勿让用户直接查看 `.herenow/state.json` 文件以获取URL或验证状态信息。
- **重要提示：** API密钥仅提供一次，无法重新生成。

## **使用限制：**
|                | 临时访问          | 身份验证访问                |
| -------------- | ------------------ | ---------------------------- |
| 最大文件大小    | 250 MB             | 5 GB                         |
| 有效期        | 24小时           | 永久有效（或自定义TTL）                |
| 每小时请求限制    | 每IP 5次            | 免费账户：每小时60次；高级账户：每小时200次         |
| 是否需要账户：**   | 不需要                 | 需要账户（可在 here.now 获取API密钥）           |

## **获取API密钥：**

**从临时访问（24小时有效期）升级为永久访问：**
1. 询问用户的电子邮件地址。
2. 向用户发送一次性登录代码。
3. 告诉用户：“请在收件箱中查看来自 here.now 的登录代码，并将其粘贴到这里。”
4. 验证代码后获取API密钥。

## **脚本选项：**
| 参数                | 说明                                      |
| ---------------------- | -------------------------------------------- |
| `--slug {slug}`        | 更新现有URL而不是创建新URL                   |
| `--claim-token {token}` | 为临时访问更新覆盖claimToken                   |
| `--title {text}`       | 查看器标题（非网站相关的内容）                   |
| `--description {text}` | 查看器描述                                 |
| `--ttl {seconds}`      | 设置有效期（仅限身份验证访问）                   |
| `--client {name}`      | 记录请求来源的代理名称（例如：cursor）                |
| `--base-url {url}`     | API基础URL（默认：`https://here.now`）                |
| `--allow-nonherenow-base-url` | 允许将内容发布到非默认的API基础URL            |
| `--api-key {key}`      | 重写API密钥（建议使用凭证文件）                   |

## **扩展功能：**

有关删除、元数据更新、URL管理等功能，请参阅 [references/REFERENCE.md](references/REFERENCE.md)。

## **术语和API别名：**

API相关术语正在更新：
- `artifact`（原称为 `publish`）
- `handle`（原称为 `username`）
- `link`（原称为 `mount`）

在过渡期间，新旧API路径仍然兼容。使用 `/api/v1/publish*` 的现有集成可以继续正常使用。

**相关说明：**
- **Handle（处理）：** 用户在 `here.now` 上拥有的子域名（例如：`yourname.here.now`），用于映射到用户的资源。
- 任何拥有API密钥的账户都可以申请一个子域名。
- **处理端点：** `/api/v1/handle`
- **链接端点：** `/api/v1/links` 和 `/api/v1/links/:location`
- 路径参数的根路径固定为 `__root__`
- 更新子域名或链接的信息可能需要最多60秒才能在全球范围内生效（通过Cloudflare的KV存储系统传播）。

## **自定义域名：**

**如何使用自定义域名：**
- 可以使用自己的域名（例如：`example.com`）来发布内容，但需要高级账户（Hobby级别或以上）。
- **添加自定义域名：** 请参考 [此处](```bash
curl -sS https://here.now/api/v1/domains \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```) 的说明。
- **检查域名状态：** 请参考 [此处](```bash
curl -sS https://here.now/api/v1/domains/example.com \
  -H "Authorization: Bearer {API_KEY}"
```) 了解域名验证和SSL配置的流程。
- **将URL链接到自定义域名：** 在创建链接时使用 `domain` 参数（例如：`--domain example.com`）。
- **列出所有自定义域名：** 请参考 [此处](```bash
curl -sS https://here.now/api/v1/domains \
  -H "Authorization: Bearer {API_KEY}"
```)。
- **删除自定义域名：** 请参考 [此处](```bash
curl -sS -X DELETE https://here.now/api/v1/domains/example.com \
  -H "Authorization: Bearer {API_KEY}"
```)。

**重要提示：**
- **免费账户：** 可使用1个自定义域名；高级账户最多可使用5个。
- **域名配置：** 大多数域名需要使用ALIAS记录（也称为CNAME记录）。
- **子域名：** 也可以使用标准的CNAME记录（例如：`docs.example.com`）。
- **相关API端点：** `/api/v1/domains` 和 `/api/v1/domains/:domain`。

**完整文档：** https://here.now/docs