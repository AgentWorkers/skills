---
name: lark-integration
description: 通过 Webhook 桥梁将 Lark（飞书）的消息功能与 OpenClaw 连接起来。支持双向传输文本消息、富文本消息（包含图片）以及图片消息。适用于将 Lark/飞书设置为消息通道、接收包含图片的消息、向 Lark 发送回复、读取 Lark 的文档/维基内容/表格数据，或解决 Lark 集成问题。该指南同时适用于 Lark International（larksuite.com）和 China Feishu（feishu.cn）版本。
---

# Lark 集成

将 Lark（Feishu）与 OpenClaw 连接起来，实现双向消息传递，并支持丰富的内容格式。

## 快速入门

```bash
# 1. Set credentials
echo "FEISHU_APP_ID=cli_xxx" >> ~/.openclaw/workspace/.env
mkdir -p ~/.openclaw/secrets
echo "your_app_secret" > ~/.openclaw/secrets/feishu_app_secret

# 2. Start bridge
cd skills/lark-integration/scripts
node bridge-webhook.mjs

# 3. Configure Lark webhook URL in developer console
# https://open.larksuite.com → Your App → Event Subscriptions
# URL: http://YOUR_SERVER_IP:3000/webhook
```

## 架构

```
Lark App ──webhook──► Bridge (port 3000) ──WebSocket──► OpenClaw Gateway
                           │                                   │
                           ◄────────── Reply ──────────────────┘
```

## 支持的消息类型

| 类型 | 方向 | 格式 |
|------|-----------|--------|
| `text` | 双向 | 纯文本 |
| `post` | → 接收 | 包含图片和链接的富文本 |
| `image` | → 接收 | 单张图片 |
| Reply | ← 发送 | 通过 feishu-card 技能发送的文本 |

## 平台检测

该插件会自动根据 URL 识别平台：
- `*.larksuite.com` → `https://open.larksuite.com`（国际版） |
- `*.feishu.cn` → `https://open.feishu.cn`（中国版） |

## 配置

### 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `FEISHU_APP_ID` | 是 | 来自 Lark 开发者控制台的 App ID |
| `FEISHU_APP_SECRET_PATH` | 否 | 密钥文件的路径（默认：`~/.openclaw/secrets/feishu_app_secret`） |
| `WEBHOOK_PORT` | 否 | Webhook 监听端口（默认：3000） |
| `FEISHU_THINKING_THRESHOLD_MS` | 否 | 消息显示“Thinking...”前的延迟时间（默认：2500 毫秒） |
| `FEISHU_ENCRYPT_KEY` | 否 | 如果 Lark 启用了加密功能，则需要此密钥 |
| `OPENCLAW_AGENT_ID` | 否 | 负责路由消息的代理（默认：main） |

### Lark 应用权限

在 Lark 开发者控制台的“权限与范围”（Permissions & Scopes）中启用以下权限：

**消息传递：**
- `im:message` - 发送和接收消息 |
- `im:message:send_as_bot` - 以机器人身份发送消息 |
- `im:resource` - 下载消息资源（图片）

**文档（可选）：**
- `docx:document:readonly` - 读取文档 |
- `wiki:wiki:readonly` - 读取 wiki 页面 |
- `sheets:spreadsheet:readonly` - 读取电子表格 |
- `bitable:bitable:readonly` - 读取 bitable 数据 |
- `drive:drive:readonly` - 访问驱动器文件 |

## 脚本

### bridge-webhook.mjs

主要的 Webhook 中间件。接收 Lark 事件，转发给 OpenClaw，并发送回复。

```bash
FEISHU_APP_ID=cli_xxx node scripts/bridge-webhook.mjs
```

### setup-service.mjs

将该脚本安装为 systemd 服务以实现自动启动：

```bash
node scripts/setup-service.mjs
# Creates /etc/systemd/system/lark-bridge.service
```

## 图片处理

消息中的图片会：
1. 从 `post` 内容或 `image` 消息类型中检测出来 |
2. 使用 `message_id` 和 `image_key` 通过 Lark API 下载 |
3. 转换为 base64 格式 |
4. 作为 `attachments` 参数发送给 OpenClaw Gateway |

```javascript
attachments: [{ mimeType: "image/png", content: "<base64>" }]
```

## 群组聊天行为

在群组聊天中，当以下情况发生时，该插件会作出响应：
- 机器人被@提及 |
- 消息以 `?` 或 `？` 结尾 |
- 消息包含触发词：help、please、why、how、what、帮、请、分析等 |
- 消息以机器人名称开头 |

否则，消息将被忽略以避免干扰。

## 读取文档

使用 `feishu-doc` 技能来读取 Lark 文档：

```bash
node skills/feishu-doc/index.js fetch "https://xxx.larksuite.com/docx/TOKEN"
```

支持的 URL 类型：
- `/docx/` - 新文档 |
- `/wiki/` - Wiki 页面（自动解析为底层文档） |
- `/sheets/` - 电子表格 |
- `/base/` - Bitable 数据（多维表格）

**权限说明：** 文档必须与机器人共享，或者机器人需要具有全租户范围的读取权限。

## 故障排除

### 读取文档时出现 “forBidden” 错误
- 文档未与机器人共享 → 将机器人添加为协作者 |
- 缺少所需权限 → 在控制台启用 `docx:document:readonly` |

### 未收到消息
- 检查 Webhook URL 是否可访问：`curl http://YOUR_IP:3000/health`
- 确认 Lark 控制台中的 Webhook 显示为 “Verified” |
- 查看中间件日志：`journalctl -u lark-bridge -f`

### 出现 “must be string” 错误
- 使用的是旧版本的中间件 → 升级版本，使用 `attachments` 参数来处理图片 |

### 图片未接收
- 缺少 `im:resource` 权限 → 在 Lark 控制台启用该权限 |
- 令牌过期 → 中间件会自动刷新，如卡住则重启中间件。

## 服务管理

```bash
# Check status
systemctl status lark-bridge

# View logs
journalctl -u lark-bridge -f

# Restart
systemctl restart lark-bridge
```

## 参考资料

- [Lark 开发者控制台](https://open.larksuite.com/)（国际版） |
- [Feishu 开发者控制台](https://open.feishu.cn/)（中国版） |
- 有关消息格式的详细信息，请参阅 `references/api-formats.md` |
- 有关逐步设置的说明，请参阅 `references/setup-guide.md`