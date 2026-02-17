---
name: screen-narrator
description: 使用 Gemini Vision 和 ElevenLabs 的语音功能，实现对你 macOS 屏幕活动的实时解说。
homepage: https://github.com/buddyh/narrator
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "requires": {
          "bins": ["python3", "tmux", "peekaboo"],
          "env": ["GEMINI_API_KEY", "ELEVENLABS_API_KEY"]
        },
      },
  }
---
# 屏幕叙述器（Screen Narrator）

此技能与上游的 `narrator` 仓库实现相关联。

它支持 Gemini-vision 的多种叙述风格（体育、自然、恐怖、黑色电影、真人秀、ASMR、摔跤等），以及 ElevenLabs 的文本到语音（TTS）技术。同时，还提供了可选的双声道叙述功能，并可通过 JSON 文件实现实时控制。

## 官方安装方式

请使用以下仓库进行安装：

```bash
cd /Users/buddy/narrator
/Users/buddy/narrator/.venv/bin/python -m narrator sports --help
```

## 设置步骤

```bash
cd /Users/buddy/narrator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**所需环境：**
- `GEMINI_API_KEY`
- `ELEVENLABS_API_KEY`
- 可选：`ELEVENLABS_VOICE_ID`

## 运行时控制命令

**在 tmux 会话中启动实时叙述（推荐方式）：**

```bash
tmux new-session -d -s narrator "cd /Users/buddy/narrator && /Users/buddy/narrator/.venv/bin/python -m narrator sports --control-file /tmp/narrator-ctl.json --status-file /tmp/narrator-status.json"
```

**设置定时器：**

```bash
tmux new-session -d -s narrator "cd /Users/buddy/narrator && /Users/buddy/narrator/.venv/bin/python -m narrator wrestling --time 5m --control-file /tmp/narrator-ctl.json --status-file /tmp/narrator-status.json"
```

**动态切换叙述风格：**

```bash
echo '{"command": "style", "value": "horror"}' > /tmp/narrator-ctl.json
```

**设置禁用粗话的功能：**

```bash
echo '{"command": "profanity", "value": "low"}' > /tmp/narrator-ctl.json
```

**暂停/恢复叙述：**

```bash
echo '{"command": "pause"}' > /tmp/narrator-ctl.json
echo '{"command": "resume"}' > /tmp/narrator-ctl.json
```

**停止叙述：**

```bash
tmux kill-session -t narrator
```

**检查当前状态：**

```bash
cat /tmp/narrator-status.json
```

## 注意事项：**
- 仅适用于 macOS 系统（支持屏幕截图和 TTS/音频功能）。
- 该 OpenClaw 技能封装与 `/Users/buddy/narrator` 的实现保持一致，以避免文档描述与实际运行效果之间的差异。