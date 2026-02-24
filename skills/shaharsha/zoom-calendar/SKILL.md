---
name: zoom-calendar
description: >
  **创建 Zoom 会议并将其添加到 Google 日历事件中（包含相应的会议数据，如图标、视频设置、备注等）**  
  此功能适用于在创建日历事件时使用 Zoom，或将 Zoom 会议添加到现有日历事件中，以及任何涉及 Zoom 与 Google 日历集成的场景。  
  **使用要求：**  
  - 需要 Zoom 服务器到服务器的 OAuth 凭据；  
  - 需要 Google 日历（gog）的授权。
metadata: {"clawdbot":{"emoji":"📹","version":"1.0.0","author":"Leo 🦁","tags":["zoom","calendar","google-calendar","meetings","video-conference","scheduling"],"requires":{"env":["GOG_KEYRING_PASSWORD","GOG_ACCOUNT"],"credentials":[".credentials/zoom.json"]}}}
allowed-tools: [exec]
---
# Zoom + Google Calendar 📹

通过 API 创建 Zoom 会议，并将其关联到 Google 日历事件——这一过程与 Zoom for Google Workspace 插件用户界面中的操作完全相同。

## 快速使用方法

```bash
bash skills/zoom-calendar/scripts/zoom_meeting.sh <event_id> "Meeting Title" "2026-03-01T11:50:00" 60
```

**参数：**
| 参数 | 说明 | 示例 |
|-------|-------------|---------|
| `event_id` | Google 日历事件 ID | `dgth9d45bb93a0q7ohfnckq88k` |
| `topic` | 会议主题 | `"团队会议"` |
| `start_time` | ISO 格式的时间（不包含时区，默认为耶路撒冷时间） | `"2026-03-01T11:50:00"` |
| `duration` | 会议时长（以分钟为单位，可选，默认为 60 分钟） | `45` |

**输出：** 参与链接、会议 ID、密码以及自动关联到 Google 日历的事件信息。

## 典型工作流程：

1. 使用 `gog calendar create` 命令创建日历事件。
2. 使用事件 ID 运行 `zoom_meeting.sh` 脚本。
3. 完成后，会议数据（包括图标、视频链接和备注）会自动添加到日历中。

## 重要规则：

| 规则 | 详细说明 |
|------|--------|
| **iconUri** | 必须使用脚本中指定的 URL——这是 Zoom 官方市场提供的图标链接。 |
| **entryPoints** | 仅支持 `video` 类型——不支持电话或 SIP 方式。 |
| **`passcode`** | 注意：这里使用的是 `passcode`，而非 `pin`。字段名称非常重要。 |
| **`meetingCode`** | 也需要包含会议 ID。 |
| **notes** | 使用 `<br />` 来分隔文本行（不要使用 `\n`）。 |
| **description** | 保持该字段为空——避免重复显示会议信息。 |
| **location** | 保持该字段为空——Zoom 会议的详细信息会通过 `conferenceData` 属性显示。 |
| **默认设置** | 除非特别要求，否则不要手动添加 Zoom 相关信息。 |

## 认证设置：

### Zoom（服务器到服务器的 OAuth）：

认证凭据：`.credentials/zoom.json`
```json
{"account_id": "...", "client_id": "...", "client_secret": "..."}
```

在 Zoom 官方市场（marketplace.zoom.us）中创建账户，然后选择 “开发”（Develop） > “服务器到服务器的 OAuth”（Server-to-Server OAuth）设置。所需权限：`meeting:write:admin` 和 `meeting:read:admin`。

### Google 日历：

使用 `gog` CLI 进行认证。脚本会自动处理令牌的生成和更新。需要设置环境变量 `GOG_KEYRING_PASSWORD` 和 `GOG_ACCOUNT`。