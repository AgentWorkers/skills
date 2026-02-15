# Feishu 消息技能

这是一个用于 Feishu 消息操作的统一工具包，为常见任务提供了一个统一的 CLI 入口点。

## 使用方法

通过 `index.js` 使用统一的 CLI：
```bash
node skills/feishu-message/index.js <command> [options]
```

## 命令

### 1. 获取消息 (`get`)
通过 ID 获取消息内容。支持对合并后的消息进行递归获取。
```bash
node skills/feishu-message/index.js get <message_id> [--raw] [--recursive]
```
示例：
```bash
node skills/feishu-message/index.js get om_12345 --recursive
```

### 2. 发送音频 (`send-audio`)
以语音气泡的形式发送音频文件。
```bash
node skills/feishu-message/index.js send-audio --target <id> --file <path> [--duration <ms>]
```
- `--target`: 用户 OpenID (`ou_`) 或 ChatID (`oc_`)。
- `--file`: 音频文件的路径（mp3/wav 等）。
- `--duration`: （可选）持续时间（以毫秒为单位）。

### 3. 创建群聊 (`create-chat`)
创建一个包含指定用户的群聊。
```bash
node skills/feishu-message/index.js create-chat --name "Project Alpha" --users "ou_1" "ou_2" --desc "Description"
```

### 4. 列出置顶消息 (`list-pins`)
列出聊天中的置顶消息。
```bash
node skills/feishu-message/index.js list-pins <chat_id>
```

## 旧版脚本
为了保持向后兼容性，仍然提供了独立的脚本：
- `get.js`
- `send-audio.js`
- `create-chat.js`
- `list Pins_v2.js`

## 依赖项
- axios
- form-data
- music-metadata
- commander