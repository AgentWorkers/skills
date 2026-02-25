---
name: here-now
description: 将文件和文件夹即时发布到网络上。适用于需要执行“发布此内容”、“托管此内容”、“部署此内容”、“在网络上共享此内容”、“创建网站”或“将此内容放到线上”等操作的场景。系统会生成一个实时可访问的URL，格式为<slug>.here.now>。
---
# here.now

**技能版本：1.6.2**

**功能说明：**  
将任何文件或文件夹发布到网页，并获取相应的实时URL。仅支持静态托管。

**安装或更新方法（推荐）：**  
`npx skills add heredotnow/skill --skill here-now -g`  

**注意：**  
对于通过仓库链接或本地项目安装的情况，请省略`-g`参数。  

**如果无法使用npm，请参考备用安装说明：**  
https://here.now/docs#install-skill  

## **系统要求：**  
- 必需的软件：`curl`、`file`、`jq`  
- 可选的环境变量：`$HERENOW_API_KEY`  
- 可选的凭证文件：`~/.herenow/credentials`  

## **发布文件/文件夹：**  
```bash
./scripts/publish.sh <file-or-dir>
```  
该脚本会生成一个实时URL（例如：`https://bright-canvas-a7k2.here.now/`）。  

- **匿名发布：**  
  如果未提供API密钥，系统会生成一个有效期为24小时的匿名发布链接。  
  提供API密钥后，发布内容将永久保存。  

**文件结构提示：**  
- 对于HTML网站，请将`index.html`文件放在要发布的目录的根目录中（不要放在子目录内）。  
  例如：如果你的文件结构为`my-site/`且其中包含`index.html`，则直接发布`my-site/`目录。  

- **非HTML文件处理：**  
  单个文件会被自动显示（支持图片、PDF、视频、音频格式）；  
  多个文件会自动生成一个包含文件列表和图片库的页面。  

## **更新已发布的文件/文件夹：**  
```bash
./scripts/publish.sh <file-or-dir> --slug <slug>
```  
在更新匿名发布的文件时，脚本会自动从`.herenow/state.json`文件中读取`claimToken`。  
可通过`--claim-token <token>`参数来覆盖该Token值。  
**注意：**  
经过身份验证的更新需要使用已保存的API密钥。  

## **API密钥的存储方式：**  
脚本从以下途径读取API密钥（优先级从高到低）：  
1. `--api-key <key>` 参数（仅用于持续集成/脚本执行，避免在交互式环境中使用）  
2. 环境变量`$HERENOW_API_KEY`  
3. 凭证文件`~/.herenow/credentials`（建议使用）  

**密钥安全提示：**  
**切勿**直接在shell命令中输入API密钥，务必通过`~/.herenow/credentials`文件进行存储。这样可以防止密钥被记录在终端历史记录或日志中。  
**注意：**  
切勿将凭证文件或状态文件（`~/.herenow/credentials`、`.herenow/state.json`）提交到版本控制系统中。  

## **状态文件更新：**  
每次发布后，脚本会更新工作目录下的`.herenow/state.json`文件。  
**注意：**  
如果用户已发布过相同的内容，使用`--slug`参数进行更新，而非重新创建新的发布链接。  

**用户须知：**  
- **务必**分享`siteUrl`（网站URL）。  
- **对于匿名发布：**同时分享`claimUrl`，以便用户能够永久保存该链接。  
- **警告：**`claimToken`仅生成一次，无法重新获取。  

**使用限制：**  
|                | 匿名发布          | 经过身份验证的发布                |
| -------------- | ------------------ | ---------------------------- |
| 最大文件大小    | 250 MB             | 5 GB                         |
| 有效期        | 24小时           | 永久（或自定义TTL）                    |
| 每小时发送次数    | 每IP地址5次          | 每账户60次                        |
| 是否需要账户    | 不需要                 | 需要账户（请从here.now获取API密钥）            |

## **获取API密钥：**  
**如何从匿名发布升级为永久发布：**  
1. 请求用户的电子邮件地址。  
2. 调用注册接口发送一个链接给用户：  
   **代码示例：**  
   ```bash
curl -sS https://here.now/api/auth/login \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```  
3. 告知用户：“请查看收件箱中的登录链接，点击后从控制面板复制API密钥。”  
4. 用户提供密钥后，将其保存到`~/.herenow/credentials`文件中：  
   **代码示例：**  
   ```bash
mkdir -p ~/.herenow && echo "<API_KEY>" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```  

## **脚本参数说明：**  
| 参数                | 说明                                      |
| ---------------------- | -------------------------------------------- |
| `--slug <slug>`        | 更新现有发布内容，而非创建新链接          |
| `--claim-token <token>` | 覆盖匿名更新时的claimToken值          |
| `--title <text>`       | 查看器的标题（适用于非网站内容）                |
| `--description <text>` | 查看器的描述                              |
| `--ttl <seconds>`      | 设置过期时间（仅限身份验证后的发布）            |
| `--base-url <url>`     | API基础URL（默认：`https://here.now`）           |
| `--allow-nonherenow-base-url` | 允许使用非默认的API基础URL          |
| `--api-key <key>`      | 重置API密钥（优先使用凭证文件）                   |

## **扩展功能：**  
有关删除、元数据修改、内容声明、列表查询等操作，请参阅[references/REFERENCE.md]。  
**完整文档：**  
https://here.now/docs