---
name: vk
description: "管理 VK.com（Vkontakte）社区：发布内容（文本、图片、视频）并处理用户消息。可通过 VK API 实现社区管理的自动化。"
---

# VK社区管理

此技能允许您使用VK API来管理VK社区。

## 必备条件
- VK访问令牌（Access Token）。**重要提示：**请使用**用户令牌（User Token）以获得完整权限（如删除帖子、上传图片等）。详情请参阅[references/api.md](references/api.md)。
- Node.js开发环境。

## 核心工作流程

### 1. 在社区墙上发布内容
要在社区墙上发布内容：
1. 如果有媒体文件，请先上传它们：
   - `node scripts/vk_cli.js upload-photo $TOKEN $GROUP_ID "./image.jpg"`
2. 使用获取到的附件ID，通过`post`命令发布内容：
   - `node scripts/vk_cli.js post $TOKEN -$GROUP_ID "帖子内容" $ATTACH_ID`

### 2. 处理用户消息
要回复用户消息：
1. 使用`get-messages`命令获取消息历史记录。
2. 使用`message`命令发送回复。

### 3. 实时监控（长轮询，Long Poll）
要即时接收和处理消息：
1. 确保在您的群组设置中启用了**长轮询API**（管理 → API交互 → 长轮询API）。
2. 使用`poll`命令：
   - `node scripts/vk_cli.js poll $TOKEN $GROUP_ID 1`（其中`1`表示自动标记消息为已读）。

**注意：**此技能在使用具有`messages,wall,groups,offline`权限的用户令牌时效果最佳。请使用[VK Host](https://vkhost.github.io/)获取永久令牌。

## 高级功能
有关设置长轮询和特定API方法的详细信息，请参阅[references/api.md](references/api.md)。