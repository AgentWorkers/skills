---
name: senseaudio-realtime-agent
description: Implement and debug SenseAudio realtime Agent lifecycle APIs: list agents, invoke session, query status, and leave session (`/v1/realtime/agents`, `/invoke`, `/status`, `/leave`). Use this whenever user asks to start or manage SenseAudio conversational agents, continue dialogues, or handle room/conv/token lifecycle errors.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio 实时代理

使用此技能实现 SenseAudio 代理的会话生命周期集成。

## 阅读前须知

- 请参考 `references/agent.md` 文件以获取更多信息。

## 工作流程

1. **发现代理**：
- 列出可用的代理，并选择所需的 `agent_id`。

2. **开始或继续对话**：
- 使用 `new_dialogue=true` 开始新会话。
- 使用 `new_dialogue=false` 和 `conv_id` 继续之前的对话。

3. **保存运行时凭据**：
- 将 `conv_id` 和 `room_id` 存储在应用程序的状态中（数据库或会话存储中），切勿将其保存在客户端代码或日志中。
- `/invoke` 方法返回的令牌具有时效性——请将其视为密码：不要记录在日志中，不要嵌入到 URL 中，并在通过 `/leave` 结束会话后丢弃这些令牌。
- 通过再次调用 `/invoke` 并使用相同的 `conv_id` 来更新令牌；切勿重复使用已过期的令牌。

4. **操作会话**：
- 根据需要查询房间状态。
- 完成会话后明确地退出会话。

5. **处理错误**：
- 区分配额限制/身份验证失败、代理未找到以及参数错误等情况。