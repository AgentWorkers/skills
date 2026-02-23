---
name: here-now
description: 将文件和文件夹即时发布到网络上。当需要执行“发布此内容”、“托管此内容”、“部署此内容”、“在网络上共享此内容”、“创建网站”或“将此内容放到线上”等操作时，请使用该功能。系统会生成一个实时可访问的URL，格式为 `<slug>.here.now`。
---
# here.now

**技能版本：1.6**

**功能说明：**  
可以将任何文件或文件夹发布到网页，并获取一个实时生效的URL。仅支持静态托管。

**安装/更新方法：**  
`curl -fsSL https://here.now/install.sh | bash`

## 发布文件/文件夹  
```bash
./scripts/publish.sh <file-or-dir>
```  
该脚本会将文件/文件夹发布到指定的URL，并返回该URL（例如：`https://bright-canvas-a7k2.here.now/`）。  
- **匿名发布：** 无需API密钥，发布内容将在24小时后自动失效。  
- **授权发布：** 使用保存的API密钥后，发布内容将永久有效。  
**注意：** 发布的文件应放置在目录的根目录中（而不是子目录内）。例如，如果要发布`my-site/`，请确保`my-site/index.html`存在于该目录中。

## 更新已发布的文件/文件夹  
```bash
./scripts/publish.sh <file-or-dir> --slug <slug>
```  
在更新匿名发布的文件时，脚本会自动从`.herenow/state.json`文件中读取`claimToken`。可以通过`--claim-token <token>`参数来覆盖该Token。  
**授权更新：** 需要使用已保存的API密钥。

## API密钥的存储方式**  
脚本从以下位置读取API密钥（优先级依次为：  
1. `--api-key <key>` 参数（仅用于持续集成/脚本执行，避免在交互式环境中使用）  
2. 环境变量`$HERENOW_API_KEY`  
3. 文件`~/.herenow/credentials`（推荐用于自动化脚本）  

**如何存储API密钥？**  
请将API密钥写入`~/.herenow/credentials`文件中：  
```bash
mkdir -p ~/.herenow && echo "<API_KEY>" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```  
**重要提示：** **切勿在shell命令中直接输入API密钥**，务必通过上述命令将其保存到该文件中，以防止密钥被记录在终端历史记录或日志中。

## 状态文件（.herenow/state.json）**  
每次发布后，脚本会更新`./herenow/state.json`文件。  
**注意：** 如果用户已发布过相同的内容，使用`--slug`参数进行更新，而不是重新创建新的URL。

**用户须知：**  
- 请务必告知用户`siteUrl`（网站URL）。  
- 对于匿名发布，还需提供`claimUrl`，以便用户能够永久保存该URL。  
- **警告：** `claimToken`仅会生成一次，无法重新获取。

**使用限制：**  
|                | 匿名发布          | 授权发布                |
| -------------- | ------------------ | ---------------------------- |
| 最大文件大小    | 250 MB             | 5 GB                         |
| 失效时间      | 24小时           | 永久有效（或自定义过期时间）            |
| 发布频率    | 每IP每小时5次        | 每账户每小时60次                |
| 是否需要账户    | 无需                 | 需要账户（可在here.now获取API密钥）         |

## 获取API密钥的方法：**  
要将匿名发布升级为永久发布，请：  
1. 获取用户的电子邮件地址。  
2. 调用注册接口，向用户发送一个链接：  
```bash
curl -sS https://here.now/api/auth/login \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```  
3. 告知用户：“请查看您的收件箱，找到来自here.now的登录链接。点击链接后，从控制面板中复制API密钥。”  
4. 用户提供API密钥后，将其保存到`~/.herenow/credentials`文件中：  
```bash
mkdir -p ~/.herenow && echo "<API_KEY>" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```  

## 脚本参数说明：**  
| 参数                | 说明                                      |  
| ---------------------- | -------------------------------------------- |  
| `--slug <slug>`        | 使用指定 slug 更新现有发布内容             |  
| `--claim-token <token>` | 覆盖匿名发布的 claimToken                   |  
| `--title <text>`       | 查看器标题（非网站内容的发布）                   |  
| `--description <text>` | 查看器描述                              |  
| `--ttl <seconds>`      | 设置过期时间（仅限授权发布）                   |  
| `--base-url <url>`     | API基础URL（默认：`https://here.now`）                |  
| `--api-key <key>`      | API密钥（优先使用文件中的密钥）                   |

**更多功能：**  
有关删除、元数据修改、内容声明、列表查询等操作，请参阅[references/REFERENCE.md]。  
完整文档：https://here.now/docs