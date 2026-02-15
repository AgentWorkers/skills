# Feishu 文件操作技能

通过 Feishu API 管理文件的上传和下载。

## 先决条件

- 首先安装 `feishu-common`。
- 该技能依赖于 `../feishu-common/index.js` 来处理令牌和 API 认证。

## 命令

### 发送文件
将本地文件上传到聊天或用户。
```bash
node skills/feishu-file/send.js --target <chat_id_or_user_id> --file <local_path>
```

### 仅上传文件
上传文件并获取其 `file_key`（用于卡片或富文本格式）。
```bash
node skills/feishu-file/upload.js --file <local_path>
```

### 下载文件
从消息中下载文件资源。
```bash
node skills/feishu-file/download.js --message-id <msg_id> --file-key <file_key> --output <local_path>
```
**注意：** 机器人必须能够访问该消息（即该消息必须在当前聊天中）。对于他人发送的文件，需要 `im:resource:read` 权限。