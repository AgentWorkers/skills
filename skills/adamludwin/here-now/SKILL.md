---
name: here-now
description: 将文件和文件夹即时发布到网络上。适用于需要执行“发布此内容”、“托管此内容”、“部署此内容”、“在网络上分享此内容”、“创建网站”或“将此内容上传到在线平台”的场景。发布后，会生成一个实时可访问的URL，格式为 {slug}.here.now。
---
# here.now

**技能版本：1.6.4**

**功能说明：**  
将任何文件或文件夹发布到网页，并获取相应的实时URL。仅支持静态托管。

**安装或更新方法（推荐）：**  
`npx skills add heredotnow/skill --skill here-now -g`  

**针对仓库绑定或本地项目的安装方式：**  
直接运行相同命令，无需添加`-g`参数。  

**如果npm不可用，请参阅备用安装文档：**  
https://here.now/docs#install-skill  

## **系统要求：**  
- 必需的软件：`curl`、`file`、`jq`  
- 可选的环境变量：`$HERENOW_API_KEY`  
- 可选的凭据文件：`~/.herenow/credentials`  

## **发布文件：**  
```bash
./scripts/publish.sh {file-or-dir}
```  
脚本会输出文件的实时URL（例如：`https://bright-canvas-a7k2.here.now/`）。  

**工作流程：**  
发布过程分为三个步骤：创建/更新文件 → 上传文件 → 完成发布。只有当上传成功后，发布才会生效。  

- **匿名发布：**  
若未使用API密钥，发布内容将在24小时后失效。  
- **使用API密钥：**  
使用保存的API密钥后，发布内容将永久有效。  

**文件结构提示：**  
- 对于HTML网站，请将`index.html`文件放在发布的目录根目录中（不要放在子目录内）。该目录的内容将成为网站的根目录。  
- 例如：要发布`my-site/`，请确保`my-site/index.html`文件存在于该目录中。  

**文件类型支持：**  
- 单个文件：会自动生成丰富的查看器（支持图片、PDF、视频、音频格式）。  
- 多个文件：会自动生成包含文件列表和图片库的页面。  

## **更新已发布的文件：**  
```bash
./scripts/publish.sh {file-or-dir} --slug {slug}
```  
在更新匿名发布的内容时，脚本会自动从`.herenow/state.json`文件中读取`claimToken`。  
可通过`--claim-token {token}`参数覆盖该值。  
**注意：** 使用API密钥进行更新时需要提供有效的API密钥。  

## **客户端信息记录：**  
通过`--client`参数，`here.now`可以记录发布操作的来源（例如：`cursor`）。  
**说明：**  
此参数会在API调用时附加`X-HereNow-Client: cursor/publish-sh`头部信息。  
如果省略该参数，脚本会使用默认值。  

## **API密钥的存储方式：**  
脚本从以下途径读取API密钥（优先选择第一个匹配的来源）：  
1. `--api-key {key}`参数（仅用于持续集成/脚本环境，避免在交互式操作中使用）  
2. 环境变量`$HERENOW_API_KEY`  
3. 凭据文件`~/.herenow/credentials`（建议使用）  

**密钥安全提示：**  
**严禁** 直接在shell命令中输入API密钥。请务必使用上述命令将其保存到`~/.herenow/credentials`文件中，以防止密钥被记录在终端历史记录或日志中。  
**注意：** 切勿将凭据文件或状态文件（`~/.herenow/credentials`、`.herenow/state.json`）提交到版本控制系统中。  

## **状态文件更新：**  
每次发布后，脚本会更新工作目录下的`.herenow/state.json`文件：  
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
发布前可查看该文件以获取之前的发布信息。  
请将`.herenow/state.json`文件视为内部缓存文件，切勿将其作为URL或身份验证信息的来源。  

**用户须知：**  
- 请始终分享当前脚本运行生成的`siteUrl`。  
- 请查看脚本标准输出（stderr）中的`publish_result.*`行。  
- 仅当`publish_result.auth_mode=anonymous`时，才显示“24小时后失效”的提示。  
- 仅当`publish_result.claim_url`非空且以`https://`开头时，才提供完整的URL。  
- 严禁让用户直接查看`.herenow/state.json`文件以获取URL或验证状态信息。  
**重要提示：** API密钥仅发放一次，无法重新获取。  

## **使用限制：**  
| 功能        | 匿名发布          | 认证发布                |
| -------------- | ------------------ | ---------------------------- |
| 文件大小上限    | 250 MB             | 5 GB                         |
| 失效时间      | 24小时           | 永久有效（或自定义过期时间）    |
| 发布频率    | 每IP每小时5次       | 每账户每小时60次           |
| 是否需要账户    | 不需要                 | 需要账户（请在here.now获取API密钥）    |

## **获取API密钥：**  
**从匿名发布升级为永久发布的方法：**  
1. 请求用户提供电子邮件地址。  
2. 调用注册接口发送登录链接。  
**操作步骤：**  
```bash
curl -sS https://here.now/api/auth/login \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```  
3. 告知用户：“请查看收件箱中的登录链接，点击后从控制面板复制API密钥。”  
4. 用户提供密钥后，请将其保存到`~/.herenow/credentials`文件中。  
**注意：** 请确保密钥保存在正确的位置。  

## **脚本选项：**  
| 参数                | 说明                                      |
| ---------------------- | -------------------------------------------- |
| `--slug {slug}`        | 更新现有发布内容，而非创建新链接          |
| `--claim-token {token}` | 覆盖匿名发布的claimToken                |
| `--title {text}`       | 查看器标题（非网站发布的文件适用）            |
| `--description {text}` | 查看器描述                              |
| `--ttl {seconds}`      | 设置过期时间（仅限认证发布）                    |
| `--client {name}`      | 记录发布来源的代理名称（例如：`cursor`）            |
| `--base-url {url}`     | API基础URL（默认：`https://here.now`）           |
| `--allow-nonherenow-base-url` | 允许将内容发布到非默认的URL          |
| `--api-key {key}`      | API密钥（建议使用凭据文件存储）                |

## **扩展功能：**  
有关删除、元数据修改、内容查询等操作，请参阅[references/REFERENCE.md]。  
**完整文档：**  
https://here.now/docs