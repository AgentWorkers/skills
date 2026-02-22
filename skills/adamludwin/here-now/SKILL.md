---
name: here-now
description: 将文件和文件夹即时发布到网页上。适用于需要执行“发布此内容”、“托管此内容”、“部署此内容”、“在网页上分享此内容”、“创建网站”或“将其放到线上”等操作的场景。会生成一个实时可访问的URL，格式为 `<slug>.here.now`。
---
# here.now

**技能版本：1.4**

将任何文件或文件夹发布到网页，并获取相应的实时URL。仅支持静态托管。

**检查技能更新：** `npx skills add heredotnow/skill --skill here-now`

## 发布文件/文件夹

```bash
./scripts/publish.sh <file-or-dir>
```

脚本会输出实时URL（例如：`https://bright-canvas-a7k2.here.now/`）。

- **匿名发布：** 无需API密钥，发布内容将在24小时后失效。
- **永久发布：** 使用保存的API密钥后，发布内容将永久有效。

## 更新已发布的文件/文件夹

```bash
./scripts/publish.sh <file-or-dir> --slug <slug>
```

在更新匿名发布的文件时，脚本会自动从`.herenow/state.json`文件中读取`claimToken`。如果需要覆盖该Token，可以使用`--claim-token <token>`参数。

**注意：** 经过身份验证的更新需要使用保存的API密钥。

## API密钥的存储

脚本从以下来源读取API密钥（优先选择第一个匹配的来源）：
1. `--api-key <key>` 参数（仅用于持续集成/脚本执行，避免在交互式环境中使用）
2. `$HERENOW_API_KEY` 环境变量
3. `~/.herenow/credentials` 文件（推荐用于代理服务器）

**重要提示：** **切勿** 直接在shell命令中输入API密钥，务必使用上述命令将其保存到`~/.herenow/credentials`文件中。这样可以防止密钥被记录在终端历史记录或日志中。

## 状态文件

每次发布后，脚本都会将相关信息写入工作目录下的`.herenow/state.json`文件。

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

在发布之前，请检查该文件。如果用户已经为相同的内容发布了文件，可以使用`--slug`参数进行更新，而不是创建新的发布记录。

## 如何告知用户：

- **务必** 共享`siteUrl`（网站URL）。
- 对于匿名发布，还需提供`claimUrl`，以便用户能够永久保存该发布内容。
- **警告：** `claimToken`仅会生成一次，无法重新获取。

## 使用限制：

|                | 匿名发布          | 经过身份验证的发布                |
| -------------- | ------------------ | ---------------------------- |
| 最大文件大小    | 250 MB             | 5 GB                         |
| 发布有效期    | 24小时           | 永久有效（或自定义过期时间）            |
| 发布频率限制 | 每IP每小时5次       | 每账户每小时60次                   |
| 是否需要账户   | 不需要             | 需要账户（在here.now获取API密钥）           |

## 获取API密钥

**将匿名发布升级为永久发布的方法：**

1. 请求用户提供他们的电子邮件地址。
2. 调用注册接口，向用户发送一个链接：
   ```bash
curl -sS https://here.now/api/auth/login \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```

3. 告知用户：“请查看您的收件箱，找到来自here.now的登录链接。点击链接后，从控制面板中复制您的API密钥。”
4. 用户提供API密钥后，将其保存到`~/.herenow/credentials`文件中：
   ```bash
mkdir -p ~/.herenow && echo "<API_KEY>" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```

## 脚本参数说明：

| 参数                | 说明                                      |
| ---------------------- | -------------------------------------------- |
| `--slug <slug>`        | 使用指定 slug 更新现有发布内容                   |
| `--claim-token <token>` | 为匿名更新覆盖 claimToken                        |
| `--title <text>`       | 查看者标题（非网站相关内容的标题）                |
| `--description <text>` | 查看者描述                                  |
| `--ttl <seconds>`      | 设置发布内容的过期时间（仅限经过身份验证的更新）         |
| `--base-url <url>`     | API的基础URL（默认：`https://here.now`）                 |
| `--api-key <key>`      | 重置API密钥（建议使用`~/.herenow/credentials`文件中的密钥）     |

## 更多功能说明：

关于删除、元数据修改、内容声明、列表查询等操作，请参阅[references/REFERENCE.md](references/REFERENCE.md)。

**完整文档：** https://here.now/docs