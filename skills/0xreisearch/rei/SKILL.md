---
name: rei
description: 将 Rei Qwen3 Coder 设置为模型提供者。在配置 coder.reilabs.org、将 Rei 添加到 Clawdbot 时，或解决来自 Rei 端点的 403 错误时，请使用该设置。
---

# Rei Qwen3 Coder

Rei 提供了 Qwen3 Coder 功能，可通过 OpenAI 兼容的接口 `coder.reilabs.org` 进行使用。

## 通过脚本进行设置

```bash
./skills/rei/scripts/setup.sh YOUR_REI_API_KEY
```

此脚本会添加该服务提供者，将其加入模型允许列表，并重启代理服务器（gateway）。

## 通过代理进行设置

向您的代理发送指令：

> "使用 API 密钥 YOUR_KEY 设置 Rei"

代理会读取该指令并为您运行相应的设置脚本。

## 切换模型

**通过聊天界面：**
```
/model rei
/model opus
```

**通过脚本：**
```bash
./skills/rei/scripts/switch.sh rei
./skills/rei/scripts/switch.sh opus
```

**通过代理：**
> "切换到 Rei" 或 "切换回 Opus"

## 恢复设置

如果出现故障，可以恢复备份数据：

```bash
./skills/rei/scripts/revert.sh
```

## 手动设置

将以下配置添加到 `~/.clawdbot/clawdbot.json` 文件中：

```json
{
  "models": {
    "providers": {
      "rei": {
        "baseUrl": "https://coder.reilabs.org/v1",
        "apiKey": "YOUR_API_KEY",
        "api": "openai-completions",
        "headers": { "User-Agent": "Clawdbot/1.0" },
        "models": [{
          "id": "rei-qwen3-coder",
          "name": "Rei Qwen3 Coder",
          "contextWindow": 200000,
          "maxTokens": 8192
        }]
      }
    }
  },
  "agents": {
    "defaults": {
      "models": {
        "rei/rei-qwen3-coder": { "alias": "rei" }
      }
    }
  }
}
```

然后重启代理服务器：`clawdbot gateway restart`

## 故障排除

**403 错误：** 必须包含 `User-Agent: Clawdbot/1.0` 头部信息。设置脚本会自动添加该头部信息。如果您是手动配置的，请确保该头部信息存在。

**“模型不允许使用”：** 要切换到 Rei 模型，该模型必须被添加到 `agentsdefaults.models` 文件中。设置脚本会处理这一配置。对于手动设置，需要按照上述步骤添加相应的允许列表条目。