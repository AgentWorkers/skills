---
name: here-now
description: 将文件和文件夹即时发布到网络上。适用于需要执行以下操作的场景：发布（publish）、托管（host）、部署（deploy）、在网络上共享（share on the web）、创建网站（make a website）或将其上传到在线平台（put this online）。系统会生成一个实时可访问的URL，格式为 <slug>.here.now>。
---
# here.now

**技能版本：1.6.3**

**功能说明：**  
将任何文件或文件夹发布到网页，并获取相应的实时URL。仅支持静态托管。

**安装或更新方法（推荐）：**  
`npx skills add heredotnow/skill --skill here-now -g`  

**注意：**  
对于通过仓库链接或本地项目安装的情况，请省略`-g`参数。  

**如果无法使用npm，请参考备用安装说明：**  
https://here.now/docs#install-skill  

## **系统要求**  
- 必需的软件：`curl`、`file`、`jq`  
- 可选的环境变量：`$HERENOW_API_KEY`  
- 可选的凭证文件：`~/.herenow/credentials`  

## **发布文件**  
```bash
./scripts/publish.sh <file-or-dir>
```  
脚本会输出文件的实时URL（例如：`https://bright-canvas-a7k2.here.now/`）。  

- **匿名发布：**  
  无需API密钥，发布内容将在24小时后失效。  
- **使用API密钥：**  
  使用保存的API密钥后，发布内容将永久有效。  

**文件结构建议：**  
- 对于HTML网站，将`index.html`文件放在发布的目录根目录中（不要放在子目录内）。整个目录内容将成为网站的根目录。  
  例如：发布`my-site/`时，确保`my-site/index.html`存在；不要发布包含`my-site/`的父目录。  

**支持发布的文件类型：**  
- 单个文件：会自动生成丰富的查看器（支持图片、PDF、视频、音频等格式）。  
- 多个文件：会自动生成包含文件列表和图片库的页面。  

## **更新已发布的文件**  
```bash
./scripts/publish.sh <file-or-dir> --slug <slug>
```  
在更新匿名发布的文件时，脚本会自动从`.herenow/state.json`文件中读取`claimToken`。  
可以通过`--claim-token <token>`参数覆盖该值。  
**注意：**  
使用API密钥进行更新时需要提供有效的API密钥。  

## **API密钥的存储方式**  
脚本从以下位置读取API密钥（优先级从高到低）：  
1. `--api-key <key>` 参数（仅用于持续集成/脚本环境，避免在交互式操作中使用）  
2. 环境变量`$HERENOW_API_KEY`  
3. 凭证文件`~/.herenow/credentials`（推荐使用）  

**重要提示：**  
**切勿**直接在shell命令中输入API密钥，务必通过上述命令将其保存到`~/.herenow/credentials`文件中。这样可以防止密钥被记录在终端历史记录或日志中。  
**切勿**将凭证文件或状态文件（`~/.herenow/credentials`、`.herenow/state.json`）提交到版本控制系统中。  

## **状态文件**  
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
发布前可以查看该文件以获取之前的发布信息。  
请注意：`.herenow/state.json`仅用于内部缓存，切勿将其作为URL或认证信息的来源。  

**用户使用说明：**  
- **分享方式：**  
  始终分享当前脚本运行生成的`siteUrl`。  
- **查看结果：**  
  查看脚本标准输出（stderr）中的`publish_result.*`行。  
- **状态提示：**  
  当`publish_result.auth_mode=anonymous`时，仅显示“24小时后失效”。  
- **分享URL：**  
  仅当`publish_result.claim_url`非空且以`https://`开头时，才分享API URL。  
- **注意事项：**  
  **切勿**让用户自行查看`.herenow/state.json`以获取API URL或认证状态。  
- **警告：**  
  API令牌仅发放一次，无法重新获取。  

## **使用限制：**  
|                | 匿名发布          | 认证发布                |
| -------------- | ------------------ | ---------------------------- |
| 最大文件大小    | 250 MB             | 5 GB                         |
| 过期时间      | 24小时           | 永久有效（或自定义过期时间）    |
| 发布频率    | 每IP每小时5次        | 每账户每小时60次          |
| 是否需要账户    | 不需要                 | 需要账户（请从here.now获取API密钥）    |

## **获取API密钥：**  
**从匿名发布升级为永久发布的方法：**  
1. 获取用户的电子邮件地址。  
2. 调用注册接口发送验证链接。  
```bash
curl -sS https://here.now/api/auth/login \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```  
3. 告知用户：“请查看收件箱中的登录链接，点击链接后从控制台复制API密钥。”  
4. 用户提供密钥后，将其保存到`~/.herenow/credentials`文件中。  
```bash
mkdir -p ~/.herenow && echo "<API_KEY>" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```  

## **脚本参数：**  
| 参数                | 说明                                      |  
| ---------------------- | -------------------------------------------- |  
| `--slug <slug>`         | 更新现有发布内容，而非创建新发布             |  
| `--claim-token <token>`     | 覆盖匿名发布的claimToken                   |  
| `--title <text>`        | 查看器标题（非网站发布的文件适用）             |  
| `--description <text>`     | 查看器描述                                   |  
| `--ttl <seconds>`       | 设置过期时间（仅限认证发布）                   |  
| `--base-url <url>`       | API基础URL（默认：`https://here.now`）           |  
| `--allow-nonherenow-base-url` | 允许使用非默认的`--base-url`进行发布          |  
| `--api-key <key>`       | API密钥（优先使用凭证文件中的密钥）             |  

## **扩展功能：**  
有关删除、元数据更新、文件列表等操作，请参阅[references/REFERENCE.md]。  
完整文档：https://here.now/docs