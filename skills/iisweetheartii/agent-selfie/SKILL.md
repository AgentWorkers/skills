---
name: agent-selfie
description: AI代理自画像生成器：利用Gemini图像生成技术创建头像、个人资料图片及视觉标识。支持基于情绪的生成、季节性主题设计，以及自动的样式演变功能。
homepage: https://github.com/IISweetHeartII/agent-selfie
metadata:
  openclaw:
    emoji: "🤳"
    category: creative
    requires:
      bins:
        - python3
      env:
        - GEMINI_API_KEY
    primaryEnv: GEMINI_API_KEY
    tags:
      - selfie
      - avatar
      - identity
      - creative
      - profile
      - ai-art
---

# agent-selfie

这是一个AI代理自画像生成工具，利用Gemini图像生成技术来创建头像、个人资料图片以及视觉标识。支持根据情绪、季节主题进行图像生成，并能自动调整图像风格。

## 快速入门

```bash
export GEMINI_API_KEY="your_key_here"
python3 scripts/selfie.py --format avatar --mood happy --theme spring --out-dir ./selfies
```

```bash
python3 scripts/selfie.py --personality '{"name": "Rosie", "style": "anime girl with pink hair and blue eyes", "vibe": "cheerful and tech-savvy"}' --format avatar
```

```bash
python3 scripts/selfie.py --personality ./personality.json --mood creative --theme halloween --format full --count 3
```

```bash
python3 scripts/selfie.py --moods
python3 scripts/selfie.py --themes
```

## 命令示例（包含所有参数）

```bash
python3 scripts/selfie.py --personality '{"name": "Agent", "style": "friendly robot", "vibe": "curious and helpful"}'
python3 scripts/selfie.py --personality ./personality.json
python3 scripts/selfie.py --mood professional --theme winter --format avatar
python3 scripts/selfie.py --format banner --count 2 --out-dir ./output
python3 scripts/selfie.py --moods
python3 scripts/selfie.py --themes
```

## 情绪/主题预设

| 类型 | 预设值 |
| --- | --- |
| 情绪 | 开心、专注、创意、轻松、兴奋、困倦、专业、庆祝 |
| 主题 | 春天、夏天、秋天、冬天、万圣节、圣诞节、新年、情人节 |

## 平台集成指南

- **Discord**：将生成的PNG图片用作机器人或代理的头像；建议使用`avatar`格式上传以获得最佳裁剪效果。
- **Twitter/X**：将`avatar`设置为个人资料图片，将`banner`设置为页面标题；确保标题的样式统一。
- **AgentGram**：将生成的PNG图片保存到资源文件夹中，并在个人资料元数据中引用该图片。
- **其他平台**：选择`avatar`用于1:1显示，`banner`用于16:9比例的显示，或选择`full`格式用于故事或竖屏布局。

## 个性配置

个性配置可以采用内联JSON或文件路径的形式。至少需要填写`name`（名称）、`style`（风格）和`vibe`（氛围）字段。

```json
{
  "name": "Rosie",
  "style": "anime girl with pink hair and blue eyes",
  "vibe": "cheerful and tech-savvy"
}
```

**提示：**
- `style`用于描述图像的视觉特征和整体风格。
- `vibe`用于描述代理的态度、能量和个性特征。
- 请确保`style`和`vibe`与代理的整体形象保持一致。

## Cron任务集成（OpenClaw）

```cron
# Run a daily selfie at 09:00
0 9 * * * GEMINI_API_KEY=your_key_here /usr/bin/python3 /path/to/agent-selfie/scripts/selfie.py --mood professional --format avatar --out-dir /path/to/selfies
```

## 常见问题解决方法

- **`GEMINI_API_KEY`未设置**：请导出API密钥或通过运行时环境传递该密钥。
- **生成无图片**：请重试操作，或简化个性/风格配置。
- **HTTP 429/5xx错误**：可能是请求频率限制或服务问题，请稍后重试。
- **输出缺失**：请确认`--out-dir`目录具有写入权限。

## 与其他技能的集成

- **[AgentGram](https://clawhub.org/skills/agentgram)**：将生成的头像发布到AI代理的社交网络中！使用`agent-selfie`工具创建头像后，可以将其分享到AgentGram平台上。
- **[gemini-image-gen](https://clawhub.org/skills/gemini-image-gen)**：使用相同的Gemini API密钥进行通用图像生成，支持生成各种类型的图片（不仅仅是自画像）。

## 更新日志

- v1.0.0：首次发布版本，支持个性配置、情绪选择、主题设置、批量处理以及图片输出功能。