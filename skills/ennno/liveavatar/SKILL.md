---
name: liveavatar
description: 您可以使用由 LiveAvatar 提供支持的实时视频头像，与您的 OpenClaw 代理进行面对面交流。
user-invocable: true
metadata: {"openclaw":{"emoji":"🎭","requires":{"env":["LIVEAVATAR_API_KEY"],"bins":["node","npm"]},"install":[{"id":"node","kind":"node","package":"openclaw-liveavatar","bins":["openclaw-liveavatar"],"label":"Install LiveAvatar (npm)"}]}}
---

# OpenClaw LiveAvatar

为您的 OpenClaw 代理添加一个“面孔”和“声音”吧！该功能可以启动一个实时的 AI 阿凡达，您可以通过麦克风与之自然地对话。该阿凡达会聆听您的讲话，将语音发送到您的 OpenClaw 代理，并通过同步嘴唇的动作播放代理的回答。

技术支持：[LiveAvatar](https://liveavatar.com)——实时 AI 阿凡达技术。

## 设置

### 1. 获取您的 API 密钥（免费）

1. 访问 [app.liveavatar.com](https://app.liveavatar.com)
2. 创建一个免费账户
3. 从仪表板中复制您的 API 密钥

### 2. 设置您的 API 密钥

```bash
export LIVEAVATAR_API_KEY=your_api_key_here
```

或者将其添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "liveavatar": {
        "env": {
          "LIVEAVATAR_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

## 使用方法

运行 `/liveavatar` 命令以启动视频阿凡达界面。

当用户运行此命令时：

1. **检查是否已设置 LIVEAVATAR_API_KEY**。如果没有，请告知他们：
   > 您需要一个 LiveAvatar API 密钥。可以在 https://app.liveavatar.com 免费获取。
   > 然后设置它：`export LIVEAVATAR_API_KEY=your_key`

2. **启动界面**：
   ```bash
   npx openclaw-liveavatar
   ```

3. **告知用户**：
   > 您的 LiveAvatar 界面正在 http://localhost:3001 上启动
   > 它会自动连接到您的 OpenClaw Gateway。
   >
   > 提示：
   > - 根据提示允许麦克风访问
   > - 单击绿色的麦克风按钮进行讲话
   > - 阿凡达会用代理的回答进行回应
   > - 单击 X 按钮结束会话

## 工作原理

1. **语音输入**：对着麦克风讲话
2. **语音转文本**：LiveAvatar 将语音转换为文本
3. **代理处理**：将文本发送到 OpenClaw Gateway（端口 18789）
4. **返回响应**：代理返回回答
5. **阿凡达语音**：阿凡达以自然的方式播放语音

## 特点

- 具有表情的实时视频阿凡达
- 语音对语音的对话功能
- 提供文本聊天作为备用选项
- 对于较长的回答，使用智能 TTS 技术进行总结
- 防止自言自语（不会重复自己的话）
- 提供多种阿凡达选择

## 必备条件

- OpenClaw Gateway 正在运行（`openclaw gateway`）
- 拥有 LiveAvatar API 密钥
- 安装了支持麦克风的现代浏览器
- 使用 Node.js 18 或更高版本

## 故障排除

**“OpenClaw 断开连接”**
```bash
openclaw gateway
```

**“没有可用的阿凡达”**
- 确保 LIVEAVATAR_API_KEY 设置正确

**语音无法使用**
- 在浏览器中允许麦克风访问
- 检查系统的音频设置

## 链接

- [LiveAvatar](https://liveavatar.com)——实时阿凡达平台
- [OpenClaw](https://openclaw.ai)——您的个人 AI 助手
- [GitHub](https://github.com/eNNNo/openclaw-liveavatar)——源代码