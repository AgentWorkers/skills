---
name: here-now
description: 将文件和文件夹即时发布到网络上。支持静态托管HTML网站、图片、PDF文件以及任何类型的文件。适用于以下场景：需要“发布内容”、“托管资源”、“在网络上部署”、“在网络上分享”、“创建网站”、“将文件上传到网站”、“生成网页链接”、“提供网站访问服务”或“生成URL”的情况。系统会生成一个可共享的实时URL，格式为 `{slug}.here.now`。
---
# here.now

**技能版本：1.6.6**

**功能说明：**  
能够从任意文件或文件夹生成一个实时可访问的URL。仅支持静态托管。

**安装或更新方法（推荐）：**  
使用 `npx skills add heredotnow/skill --skill here-now -g`  

**对于通过仓库链接或本地项目安装的情况：**  
直接运行相同命令，无需添加 `-g` 参数。  

**如果无法使用npm，请参考备用安装说明：**  
https://here.now/docs#install-skill  

## **系统要求：**  
- 必需的软件：`curl`、`file`、`jq`  
- 可选的环境变量：`$HERENOW_API_KEY`  
- 可选的凭证文件：`~/.herenow/credentials`  

## **生成实时URL的步骤：**  
```bash
./scripts/publish.sh {file-or-dir}
```  
该脚本会生成一个实时URL（例如：`https://bright-canvas-a7k2.here.now/`）。  

**工作原理：**  
整个过程分为三个步骤：创建/更新文件 → 上传文件 → 完成生成。只有当所有步骤都成功完成后，生成的URL才会真正生效。  

- **无API密钥的情况：**  
会生成一个**匿名工件**，该工件在24小时后失效。  
- **使用API密钥的情况：**  
生成的工件将永久有效。  

**文件结构建议：**  
- 对于HTML网站，请将 `index.html` 文件放在发布的目录根目录中（不要放在子目录内）。  
- 例如：如果发布路径为 `my-site/`，则确保 `my-site/index.html` 存在于该目录中，而不是包含 `my-site/` 的父目录中。  
- 即使没有HTML文件，该脚本也能自动处理图片、PDF、视频、音频等文件类型。  
- 多个文件会被自动组织成目录结构，并提供文件列表和图片库功能。  

## **更新现有工件：**  
```bash
./scripts/publish.sh {file-or-dir} --slug {slug}
```  
在更新匿名工件时，脚本会自动从 `.herenow/state.json` 文件中读取 `claimToken`。  
可以通过 `--claim-token {token}` 参数来覆盖此值。  
**需要认证的更新：**  
必须使用已保存的API密钥。  

## **客户端信息记录：**  
通过 `--client` 参数，`here.now` 脚本可以记录操作来源：  
```bash
./scripts/publish.sh {file-or-dir} --client cursor
```  
此参数会在API调用时附加 `X-HereNow-Client: cursor/publish-sh` 标头。  
如果省略此参数，脚本会使用默认值。  

## **API密钥的存储方式：**  
脚本从以下途径读取API密钥（优先选择第一个有效的值）：  
1. `--api-key {key}` 参数（仅用于持续集成/脚本环境，避免在交互式操作中使用）  
2. 环境变量 `$HERENOW_API_KEY`  
3. 凭证文件 `~/.herenow/credentials`（推荐使用）  

**注意：**  
**切勿在shell命令中直接输入API密钥！**  
请始终使用上述命令将其保存到 `~/.herenow/credentials` 文件中，这样可以防止密钥被记录在终端历史记录或日志中。  
**切勿将凭证文件或状态文件（`~/.herenow/credentials`、`.herenow/state.json`）提交到版本控制系统中。**  

## **状态文件更新：**  
每次生成或更新工件后，脚本会更新工作目录下的 `.herenow/state.json` 文件：  
```json
{
  "publishes": {
    "bright-canvas-a7k2": {
      "siteUrl": "https://bright-canvas-a7k2.here.now/",
      "claimToken": "abc123",
      "claimUrl": "https://here.now/claim?slug=bright-canvas-a7k2&token=abc123",
      "expiresAt": "2026-02-18T01:00:00.000Z"
    }
  }
}
```  
在生成或更新工件之前，可以查看该文件以获取之前的工件信息。  
请将 `.herenow/state.json` 视为内部缓存文件，切勿将其作为URL或认证信息的来源。  

**用户须知：**  
- **务必分享当前脚本生成的 `siteUrl`。**  
- 请阅读并遵循脚本输出中的 `publish_result.*` 行内容。  
- 仅当 `publish_result.auth_mode=anonymous` 时，才显示“24小时后失效”的提示。  
- 仅当 `publish_result.claim_url` 不为空且以 `https://` 开头时，才提供完整的URL。  
- **切勿让用户自行查看 `.herenow/state.json` 文件以获取URL或认证状态。**  
- **警告：** API密钥仅发放一次，无法重新获取。  

**使用限制：**  
|                | 匿名访问          | 认证访问                |
| -------------- | ------------------ | ---------------------------- |
| 最大文件大小    | 250 MB             | 5 GB                         |
| 失效时间       | 24小时           | 永久有效（或自定义TTL）    |
| 每IP每小时请求限制 | 5次              | 免费用户：60次/小时；高级用户：200次/小时 |
| 是否需要账户    | 不需要                 | 需要账户（可在 here.now 获取API密钥）    |

## **获取API密钥的流程：**  
**从匿名访问升级为永久访问：**  
1. 请求用户的电子邮件地址。  
2. 向用户发送一次性登录验证码。  
```bash
curl -sS https://here.now/api/auth/agent/request-code \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```  
3. 告知用户：“请在收件箱中查找来自 here.now 的登录验证码，并将其粘贴到这里。”  
4. 验证验证码后获取API密钥。  
```bash
curl -sS https://here.now/api/auth/agent/verify-code \
  -H "content-type: application/json" \
  -d '{"email":"user@example.com","code":"ABCD-2345"}'
```  
5. 保存获取到的 `apiKey`。  
```bash
mkdir -p ~/.herenow && echo "{API_KEY}" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```  

## **脚本参数说明：**  
| 参数                | 说明                                      |
| ---------------------- | -------------------------------------------- |
| `--slug {slug}`        | 更新现有工件而非创建新工件                |
| `--claim-token {token}` | 用于匿名更新的claimToken                |
| `--title {text}`       | 查看器的标题（非网站工件适用）             |
| `--description {text}` | 查看器的描述                            |
| `--ttl {seconds}`      | 设置过期时间（仅限认证访问）               |
| `--client {name}`      | 认证请求的来源名称（例如：cursor）            |
| `--base-url {url}`     | API基础URL（默认：`https://here.now`）           |
| `--allow-nonherenow-base-url` | 允许将认证信息发送到非默认的 `--base-url`     |
| `--api-key {key}`      | API密钥（优先使用凭证文件中的密钥）           |

## **其他功能说明：**  
有关删除、元数据更新、文件列表等功能，请参阅 [references/REFERENCE.md](references/REFERENCE.md)。  

## **术语与API别名：**  
API的相关接口名称正在更新：  
- `artifact`（原名为 `publish`）  
- `handle`（原名为 `username`）  
- `link`（原名为 `mount`）  
在过渡期间，新旧接口名称都会被支持。  
使用 `/api/v1/publish*` 的现有集成仍然可以正常使用。  

## **相关术语快速参考：**  
- **Handle（处理方式）：**  
用户在 `here.now` 上拥有的子域名（例如：`yourname.here.now`），用于映射到对应的工件。  
- **Link（链接）：**  
任何拥有API密钥的账户都可以申请一个处理方式。  
- **相关API端点：**  
  - `handle`：`/api/v1/handle`  
  - `link`：`/api/v1/links` 和 `/api/v1/links/:location`  
- **路径参数的默认前缀：**  
  - `__root__`  

**完整文档：**  
https://here.now/docs