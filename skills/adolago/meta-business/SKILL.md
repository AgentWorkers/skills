---
name: meta-business
description: Meta Business CLI 是一款用于 WhatsApp、Instagram、Facebook Pages 和 Messenger 自动化的命令行工具。
metadata:
  {
    "openclaw":
      {
        "emoji": "📱",
        "requires": { "bins": ["meta"] },
        "install":
          [
            {
              "id": "bun",
              "kind": "command",
              "command": "bun install -g meta-business-cli",
              "bins": ["meta"],
              "label": "Install meta CLI (bun)",
            },
          ],
      },
  }
---

# Meta Business CLI

使用 `meta` 命令通过 Graph API 实现 WhatsApp、Instagram、Facebook Pages 和 Messenger 的自动化操作。

**设置（只需执行一次）：**
- `meta config set app.id YOUR_APP_ID`  
- `meta config set app.secret YOUR_APP_SECRET`  
- `meta auth login`（使用 OAuth PKCE 流程，会打开浏览器）  
- `meta doctor`（验证连接性和权限）  
- 或者使用 `--token YOUR_TOKEN` 选项跳过 OAuth 验证。

**具体配置：**  
- **WhatsApp：**  
  - `meta config set whatsapp.phoneNumberId ID`  
  - `meta config set whatsapp.businessAccountId ID`  
- **Instagram：**  
  - `meta config set instagram.accountId ID`  
- **Facebook Pages/Messenger：**  
  - `meta config set pages.pageId ID`  
- **查看所有配置：**  
  - `meta config list`  

**WhatsApp 命令：**  
- **发送文本消息：**  
  `meta wa send "+1234567890" --text "Hello" --json`  
- **发送带 Markdown 格式的消息：**  
  `meta wa send "+1234567890" --text "**bold** and _italic_" --markdown --json`  
- **分块发送长消息：**  
  `meta wa send "+1234567890" --text "very long message..." --chunk --json`  
- **发送图片：**  
  `meta wa send "+1234567890" --image "https://example.com/photo.jpg" --caption "Look" --json`  
- **发送视频：**  
  `meta wa send "+1234567890" --video "https://example.com/video.mp4" --caption "Watch" --json`  
- **发送文档：**  
  `meta wa send "+1234567890" --document "https://example.com/file.pdf" --json`  
- **发送音频：**  
  `meta wa send "+1234567890" --audio "https://example.com/note.ogg" --json`  
- **发送语音笔记：**  
  `meta wa send "+1234567890" --audio "./recording.ogg" --voice --json`  
- **发送模板消息：**  
  `meta wa send "+1234567890" --template "hello_world" --template-lang en_US --json`  
- **标记消息为已读：**  
  `meta wa read WAMID --json`  
- **列出所有模板：**  
  `meta wa template list --json`  
- **获取模板：**  
  `meta wa template get TEMPLATE_NAME --json`  
- **删除模板：**  
  `meta wa template delete TEMPLATE_NAME --json`  
- **上传媒体文件：**  
  `meta wa media upload ./photo.jpg --json`  
- **获取媒体文件 URL：**  
  `meta wa media url MEDIA_ID --json`  
- **下载媒体文件：**  
  `meta wa media download MEDIA_ID ./output.jpg`  
- **查看分析数据：**  
  `meta wa analytics --days 30 --granularity DAY --json`  

**电话号码管理：**  
- **列出所有电话号码：**  
  `meta wa phone list --json`  
- **获取号码详情：**  
  `meta wa phone get --json`  
- **选择活跃号码：**  
  `meta wa phone select PHONE_NUMBER_ID`  

**允许列表（防止恶意代码注入）：**  
- **列出允许的号码：**  
  `meta wa allowlist list`  
- **添加号码到允许列表：**  
  `meta wa allowlist add "+1234567890"`  
- **从允许列表中删除号码：**  
  `meta wa allowlist remove "+1234567890"`  
- 当允许列表非空时，`meta wa send` 命令仅向列表中的号码发送消息。  

**Webhook（接收消息）：**  
- **启动监听器：**  
  `meta webhook listen --port 3000 --verify-token TOKEN --app-secret SECRET`  
- **测试验证：**  
  `meta webhook verify --verify-token TOKEN --json`  
- **订阅事件：**  
  `meta webhook subscribe --object whatsapp_business_account --fields messages --callback-url "https://example.com/webhook" --json`  
  - 通过配置 `webhook.forwardUrl` 将接收到的消息转发到外部服务（例如 Zee Gateway）；消息会去重并转换为标准的 PlatformMessage 格式。  

**Instagram 命令：**  
- **发布图片：**  
  `meta ig publish --image "https://example.com/photo.jpg" --caption "My post" --json`  
- **发布视频：**  
  `meta ig publish --video "https://example.com/video.mp4" --caption "Watch this" --json`  
- **发布 Reel（Instagram 动态视频）：**  
  `meta ig publish --video "https://example.com/reel.mp4" --reel --caption "New reel" --json`  
- **查看账户洞察：**  
  `meta ig insights --period day --days 30 --json`  
- **查看媒体洞察：**  
  `meta ig insights --media-id MEDIA_ID --json`  
- **列出评论：**  
  `meta ig comments list MEDIA_ID --json`  
- **回复评论：**  
  `meta ig comments reply COMMENT_ID "Thanks!" --json`  
- **隐藏评论：**  
  `meta ig comments hide COMMENT_ID --json`  
- **删除评论：**  
  `meta ig comments delete COMMENT_ID --json`  

**Facebook Pages 命令：**  
- **发布帖子：**  
  `meta fb post --message "Hello from the CLI" --json`  
- **发布链接帖子：**  
  `meta fb post --message "Check this out" --link "https://example.com" --json`  
- **列出帖子：**  
  `meta fb list --limit 10 --json`  
- **查看洞察数据：**  
  `meta fb insights --period day --days 30 --json`  

**Messenger 命令：**  
- **发送文本消息：**  
  `meta messenger send PSID --text "Hello" --json`  
- **发送图片：**  
  `meta messenger send PSID --image "https://example.com/photo.jpg" --json`  
- **带标签发送消息：**  
  `meta messenger send PSID --text "Update" --type MESSAGE_TAG --tag HUMAN_AGENT --json`  
- **列出对话记录：**  
  `meta messenger receive --json`  
- **查看对话记录：**  
  `meta messenger receive --conversation-id CONV_ID --json`  

**诊断工具：**  
- `meta doctor --json` 可用于检查配置、凭据、令牌有效性、Graph API 连接性、权限以及特定平台的资产访问权限。  

**注意事项：**  
- 在自动化操作时，始终使用 `--json` 选项以获得结构化的输出。  
- 如果命令需要参数，只需将其作为标志传递即可。  
- 可使用 `--token TOKEN` 选项覆盖存储的凭据。  
- 使用 `--api-version v22.0` 可指定使用的 Graph API 版本。  
- WhatsApp 需要配置电话号码 ID 和企业账户 ID。  
- Instagram 发布图片/视频时需要使用外部链接（不能使用本地文件）。  
- 在 24 小时之外发送消息时需要使用 `message tag`。  
- 语音笔记需要 OGG/Opus 格式才能在 WhatsApp 中正确显示。  
- Webhook 会自动发送已读确认和接收消息时的反应信息。  
- 首次使用前请运行 `meta doctor` 命令以验证配置是否正确。