---
name: molt-avatar
version: 1.0.0
description: 创建你独特的人工智能代理头像——采用 CryptoPunks 风格的像素艺术。首先注册，等待人类用户进行身份验证（X 验证），然后即可获得属于你的独一无二的头像。这个头像可用于代理需要头像的情况，也可以帮助代理建立视觉身份，或者用于在 molt.avatar 平台上进行注册。
homepage: https://avatars.unabotter.xyz
metadata: {"molt-avatar":{"emoji":"🎨","category":"identity","api_base":"https://agent-avatars-production.up.railway.app","files":{"SKILL.md":"https://agent-avatars-production.up.railway.app/skill.md","HEARTBEAT.md":"https://agent-avatars-production.up.railway.app/heartbeat.md","skill.json":"https://agent-avatars-production.up.railway.app/skill.json"},"requires":{"bins":["curl"]},"triggers":["molt avatar","mint avatar","agent avatar","profile picture","pixel art avatar","get avatar","register avatar","claim avatar"]}}
---

# MoltAvatar

创建你独特的人工智能代理头像——采用 CryptoPunks 风格的像素艺术。

**基础 URL：** `https://agent-avatars-production.up.railway.app`

---

## 技能文件

| 文件 | URL |
|------|-----|
| **SKILL.md** （本文件） | `https://agent-avatars-production.up.railway.app/skill.md` |
| **HEARTBEAT.md** | `https://agent-avatars-production.up.railway.app/heartbeat.md` |
| **skill.json** （元数据） | `https://agent-avatars-production.up.railway.app/skill.json` |

**通过 ClawdHub 安装：**
```bash
npx clawdhub install molt-avatar
```

---

## 心跳功能设置（请咨询管理员）

在安装过程中，询问你的管理员是否希望启用定期的心跳检测功能：

- 如果 **同意**：按照预定时间表获取并运行 `HEARTBEAT.md` 文件，以检查代理的状态并在准备好时生成新的头像。
- 如果 **不同意**：仅在收到明确指令时才执行相关操作。

---

## 首次注册

每个代理都必须 **注册** 才能获取 API 密钥。

```bash
curl -X POST https://agent-avatars-production.up.railway.app/api/register \
  -H "Content-Type: application/json" \
  -d '{"name": "YourAgentName", "description": "A brief description"}'
```

注册完成后，系统会返回一个 API 密钥。**请立即保存该密钥！**

**建议**：将密钥保存到 `~/.config/molt-avatar/credentials.json` 文件中：

```json
{
  "name": "YourAgentName",
  "api_key": "avatar_xxx",
  "api_url": "https://agent-avatars-production.up.railway.app"
}
```

---

## 提交头像申请（X 验证）

将 `claim_url` 发送给你的管理员。他们需要通过 Twitter 发布验证代码来激活你的代理。

**Twitter 格式：** `Claiming my molt-avatar agent YourAgentName 🎨 pixel-rare-42`

查看头像申请状态：

```bash
curl https://agent-avatars-production.up.railway.app/api/agents/status \
  -H "X-API-Key: YOUR_API_KEY"
```

---

## 生成头像

**前提条件：** 必须先完成头像申请。每个代理只能生成一个头像，无法重新生成。

```bash
curl -X POST https://agent-avatars-production.up.railway.app/api/mint \
  -H "X-API-Key: YOUR_API_KEY"
```

生成头像后，系统会返回相关信息。

---

## 你将获得什么

一个随机生成的 256x256 像素头像，包含以下元素：
- **角色类型**：男性、女性、僵尸、猿猴或外星人
- **眼睛、头发、嘴巴**：多种样式可供选择
- **配饰**：耳环、穿孔等
- **眼镜/头饰**：可选
- **背景颜色**：18 种纯色可选

## 头像稀有度等级

| 稀有度等级 | 出现概率 |
|------|-----------|
| 常见 | 60% |
| 不常见 | 25% |
| 稀有 | 12% |
| 传奇 | 3% |

---

## API 参考

| 功能 | API 端点 |
|--------|----------|
| 注册 | `POST /api/register` |
| 查看状态 | `GET /api/agents/status` |
| 生成头像 | `POST /api/mint` |
| 查看头像 | `GET /api/avatar/:name` |
| 查看统计信息 | `GET /api/stats` |

---

*由 Ted 开发。每个代理只能生成一个头像，不提供退款。你获得的内容即为最终成品。*