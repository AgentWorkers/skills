# SocialRails

通过 SocialRails API，您可以轻松管理社交媒体账号：安排帖子发布、查看分析数据、生成 AI 生成的内容，以及列出已连接的社交媒体账户。

## 设置

1. 从 [SocialRails 控制台](https://socialrails.com/dashboard/settings) 获取 API 密钥（需要 Creator 计划或更高级别的订阅）。
2. 安装该技能：
   ```bash
   openclaw install socialrails
   ```
3. 配置您的 API 密钥：
   ```bash
   openclaw config socialrails apiKey sr_live_your_key_here
   ```

## 命令

| 命令 | 描述 | 必需参数 |
|---------|-------------|---------------------|
| `schedule-post` | 安排社交媒体帖子的发布 | `content`（帖子内容），`platform`（平台） |
| `show-analytics` | 查看帖子分析数据 | — |
| `generate-caption` | 生成 AI 生成的内容 | `prompt`（提示语） |
| `list-posts` | 列出已安排的或已发布的帖子 | — |
| `list-accounts` | 列出已连接的社交媒体账户 | — |

## 支持的平台

Twitter、LinkedIn、Facebook、Instagram、TikTok、Bluesky、Pinterest、Threads、YouTube

## 示例

```text
> 安排下周一上午 9 点发布一条关于我们产品发布的推文。
> 查看过去 30 天的帖子分析数据。
> 为我们的新办公室照片生成一条 Instagram 说明文字。
> 列出我已安排的帖子。
> 我连接了哪些社交媒体账户？
```

## 配置

配置信息存储在 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "socialrails": {
      "apiKey": "sr_live_your_key_here",
      "baseUrl": "https://socialrails.com/api/v1"
    }
  }
}
```

## API 密钥权限范围

每个命令都需要相应的 API 密钥权限范围：

- `read`：list-posts（列出帖子）、show-analytics（查看分析数据）、list-accounts（列出账户）
- `write`：schedule-post（安排帖子发布）
- `ai`：generate-caption（生成 AI 生成的内容）

如需完全访问所有功能，请创建一个包含这三个权限范围的 API 密钥。

## 链接

- [API 文档](https://socialrails.com/documentation/api-overview)
- [OpenClaw 设置指南](https://socialrails.com/documentation/openclaw-setup)
- [SocialRails 控制台](https://socialrails.com/dashboard)