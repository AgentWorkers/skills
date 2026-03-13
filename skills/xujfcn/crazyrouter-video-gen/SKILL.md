---
name: crazyrouter-video-gen
description: >
  **通过Crazyrouter API生成AI视频**  
  支持Sora 2、Kling V2、Veo 3、Seedance、Pika、MiniMax Hailuo、Runway等平台。支持文本转视频的功能。当用户需要生成或创建视频时可以使用该API。  
  需要设置环境变量`CRAZYROUTER_API_KEY`（可在https://crazyrouter.com获取）。
---
# 通过 [Crazyrouter](https://crazyrouter.com) 生成视频

使用 [Crazyrouter](https://crazyrouter.com) 根据文本提示生成视频——只需一个 API 密钥，即可使用多种视频 AI 模型。

## 支持的模型

| 模型 | ID | 描述 |
|-------|-----|-------------|
| Sora 2 | `sora-2` | OpenAI 的视频模型 |
| Kling V2 | `kling-v2-1` | Kuaishou 的电影风格模型 |
| Veo 3 | `veo3` | Google 的视频模型 |
| Seedance 1.5 Pro | `doubao-seedance-1-5-pro_720p` | ByteDance 的视频模型 |
| Pika 1.5 | `pika-1.5` | 创意视频模型 |
| MiniMax Hailuo 2.3 | `MiniMax-Hailuo-2.3` | MiniMax 的视频模型 |
| Runway VIP | `runway-vip-video` | 专业合成视频模型 |

## 脚本目录

**代理执行**：
1. `SKILL_DIR` = 本 SKILL.md 文件所在的目录
2. 脚本路径 = `${SKILL_DIR}/scripts/main.mjs`

## 第 0 步：检查 API 密钥 ⛔ 此步骤为必填

```bash
[ -n "${CRAZYROUTER_API_KEY}" ] && echo "key_present" || echo "not_set"
```

| 结果 | 操作 |
|--------|--------|
| `key_present` | 继续 |
| `not_set` | 请求用户设置 `CRAZYROUTER_API_KEY`。可在 https://crazyrouter.com 获取密钥 |

## 使用方法

```bash
# Generate with default model (sora-2)
node ${SKILL_DIR}/scripts/main.mjs --prompt "A cat playing piano" --output cat.mp4

# With Kling V2
node ${SKILL_DIR}/scripts/main.mjs --prompt "Ocean waves at sunset" --output waves.mp4 --model kling-v2-1

# With Veo 3
node ${SKILL_DIR}/scripts/main.mjs --prompt "Timelapse of city traffic" --output city.mp4 --model veo3
```

### 参数选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--prompt <text>` | 视频描述（必填） | — |
| `--output <path>` | 输出文件路径（必填） | — |
| `--model <id>` | 要使用的模型 | `sora-2` |

**注意**：视频生成是异步的——根据所选模型的不同，可能需要 30 到 120 秒的时间。脚本会持续轮询直到生成完成。