---
name: zai-tts
description: >
  使用 `uvx zai-tts` 命令通过 GLM-TTS 服务将文本转换为语音。适用于以下情况：  
  (1) 用户通过“tts”触发词或关键词请求音频/语音输出。  
  (2) 需要将内容以语音形式呈现（例如多任务处理、辅助学习、播客、驾驶、烹饪等场景）。  
  (3) 使用预先克隆好的语音资源进行语音合成。
homepage: https://github.com/aahl/zai-tts
metadata:
  {
    "openclaw":
      {
        "emoji": "🗣️",
        "requires": { "bins": ["uvx"], "env": ["ZAI_AUDIO_USERID", "ZAI_AUDIO_TOKEN"] },
        "primaryEnv": "ZAI_AUDIO_TOKEN",
        "install":
          [
            {
              "id": "userid",
              "kind": "input",
              "label": "User ID",
              "description": "Login `audio.z.ai` and executing `JSON.parse(localStorage['auth-storage']).state.user.userId` in the console via F12 Developer Tools",
              "secret": false,
              "envVar": "ZAI_AUDIO_USERID",
            },
            {
              "id": "token",
              "kind": "input",
              "label": "Auth Token",
              "description": "Login `audio.z.ai` and executing `JSON.parse(localStorage['auth-storage']).state.token` in the console via F12 Developer Tools",
              "secret": true,
              "envVar": "ZAI_AUDIO_TOKEN",
            },
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uvx"],
              "label": "Install uvx (brew)",
            },
            {
              "id": "uv-pip",
              "kind": "pip",
              "formula": "uv",
              "bins": ["uvx"],
              "label": "Install uvx (pip)",
            },
          ],
      },
  }
---
# Zai-TTS

使用 `uvx zai-tts` 命令，通过 GLM-TTS 服务生成高质量的语音文件。  
在使用此功能之前，您需要配置环境变量 `ZAI_AUDIO_USERID` 和 `ZAI_AUDIO_TOKEN`；这些变量可以通过登录 `audio.z.ai` 并在控制台（使用 F12 开发者工具）执行 `localStorage['auth-storage']` 来获取。

## 使用方法
```shell
uvx zai-tts -t "{msg}" -o {tempdir}/{filename}.wav
uvx zai-tts -f path/to/file.txt -o {tempdir}/{filename}.wav
```

## 更改语音速度和音量
```shell
uvx zai-tts -t "{msg}" -o {tempdir}/{filename}.wav --speed 1.5
uvx zai-tts -t "{msg}" -o {tempdir}/{filename}.wav --speed 1.5 --volume 2
```

## 更改语音类型
```shell
uvx zai-tts -t "{msg}" -o {tempdir}/{filename}.wav --voice system_002
```

## 可用的语音选项  
`system_001`：Lila——一种开朗、发音标准的女性声音  
`system_002`：Chloe——一种温柔、优雅、聪慧的女性声音  
`system_003`：Ethan——一种阳光开朗、发音标准的男性声音  

使用 shell 命令查看所有可用的语音：  
```shell
uvx zai-tts -l
```  
如果您想使用自定义语音，请先在 `audio.z.ai` 网站上完成语音克隆操作。