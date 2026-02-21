---
name: here-now
description: 将文件和文件夹即时发布到网络上。适用于需要执行“发布此内容”、“托管此内容”、“部署此内容”、“在网络上共享此内容”、“创建网站”或“将此内容上传到在线平台”的场景。会生成一个实时可访问的URL，格式为 <slug>.here.now>。
---
# here.now

**技能版本：1.2**

**将任何文件或文件夹发布到网页，并获取相应的实时URL。仅支持静态托管。**

## 检查更新

在首次使用时，检查是否有更新的技能版本：

```bash
curl -s https://here.now/api/skill/version
```

如果返回的版本号大于1.2，请在继续之前获取最新版本：

```bash
curl -s https://here.now/skill.md
```

告知用户您正在更新到最新版本，然后继续处理他们的请求。

## 发布

```bash
./scripts/publish.sh <file-or-dir>
```

输出实时URL（例如：`https://bright-canvas-a7k2.here.now/`）。

- 无需API密钥时，发布的链接为临时链接（有效期24小时）。
- 使用`--api-key`或`$HERENOW_API_KEY`时，发布的链接为永久链接。

## 更新现有发布的内容

```bash
./scripts/publish.sh <file-or-dir> --slug <slug>
```

在更新临时发布的链接时，脚本会自动从`.herenow/state.json`文件中加载`claimToken`。可以通过`--claim-token <token>`参数来覆盖该令牌。

- 身份验证后的更新需要使用`--api-key`或`$HERENOW_API_KEY`。

## 状态文件

每次发布后，脚本会向工作目录下的`.herenow/state.json`文件中写入相关信息：

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

在发布之前，请检查该文件。如果用户已经为相同的内容创建了发布链接，可以使用`--slug`参数来更新现有链接，而不是创建新的链接。

## 如何告知用户

- 始终向用户提供`siteUrl`。
- 对于临时发布的链接，同时提供`claimUrl`，以便用户可以永久保存该链接。
- 注意：`claimToken`仅会返回一次，无法重新获取。

## 限制

|                | 临时发布          | 身份验证发布                |
| -------------- | ------------------ | ---------------------------- |
| 最大文件大小    | 250 MB             | 5 GB                         |
| 链接有效期    | 24小时           | 永久链接（或自定义过期时间）    |
| 每小时IP请求限制 | 5次              | 无限制                    |
| 是否需要账户    | 不需要                 | 需要账户（可在here.now获取API密钥）    |

## 获取API密钥

要将临时发布（有效期24小时）升级为永久发布，请按照以下步骤操作：

1. 向用户索取他们的电子邮件地址。
2. 调用注册接口，向用户发送一个登录链接：

```bash
curl -sS https://here.now/api/auth/login \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```

3. 告诉用户：“请查看您的收件箱，找到来自here.now的登录链接。点击链接后，从控制面板中复制您的API密钥。”
4. 用户提供API密钥后，使用`--api-key`参数传递该密钥，或设置`$HERENOW_API_KEY`。

## 脚本选项

| 选项                | 描述                                      |
| ---------------------- | -------------------------------------------- |
| `--api-key <key>`      | API密钥（或设置 `$HERENOW_API_KEY`）               |
| `--slug <slug>`        | 更新现有链接而非创建新链接                   |
| `--claim-token <token>` | 用于临时更新的令牌覆盖                   |
| `--title <text>`       | 查看器标题（非网站相关内容）                   |
| `--description <text>` | 查看器描述                              |
| `--ttl <seconds>`      | 设置过期时间（仅限身份验证发布）                 |
| `--base-url <url>`     | API基础URL（默认：`https://here.now`）             |

## 更多功能

有关删除、元数据修改、链接领取、列表查询等操作，请参阅[references/REFERENCE.md](references/REFERENCE.md)。

完整文档：https://here.now/docs