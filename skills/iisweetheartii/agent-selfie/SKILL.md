---
name: agent-selfie
description: AI智能体自画像生成器：利用Gemini图像生成技术创建头像、个人资料图片以及视觉身份标识。支持基于情绪的图像生成、季节性主题设计，并具备自动调整图像风格的功能。
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

这是一个AI代理自画像生成工具，利用Gemini图像生成技术来创建头像、个人资料图片以及代理的视觉形象。支持根据用户情绪、季节主题进行个性化生成，并能自动调整图片风格。

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

- **Discord**：将生成的PNG图片用作机器人或代理的头像；建议使用`avatar`格式上传以确保图片裁剪效果最佳。
- **Twitter/X**：将生成的图片设置为个人资料的`avatar`，并将`banner`设置为页面标题；保持标题图片的样式一致。
- **AgentGram**：将生成的PNG图片存储在您的资源文件夹中，并在个人资料元数据中引用该图片。
- **其他平台**：选择`avatar`格式用于1:1显示，`banner`格式用于16:9比例的显示，`full`格式用于故事或竖屏布局。

## 个性配置

个性配置可以采用内联JSON格式或文件路径形式。至少需要包含`name`（名称）、`style`（风格）和`vibe`（氛围）三个字段。

```json
{
  "name": "Rosie",
  "style": "anime girl with pink hair and blue eyes",
  "vibe": "cheerful and tech-savvy"
}
```

**提示：**
- `style`用于描述图片的视觉特征和整体风格。
- `vibe`用于描述代理的态度、能量和个性特征。
- 请确保`style`和`vibe`与代理的整体形象保持一致。

## Cron任务集成（OpenClaw）

```cron
# Run a daily selfie at 09:00
0 9 * * * GEMINI_API_KEY=your_key_here /usr/bin/python3 /path/to/agent-selfie/scripts/selfie.py --mood professional --format avatar --out-dir /path/to/selfies
```

## 常见问题解决方法

- **`GEMINI_API_KEY`未设置**：请导出API密钥或通过运行时环境传递该密钥。
- **响应中未返回图片**：请重试操作，或简化个性/风格配置。
- **HTTP 429/5xx错误**：可能是请求频率限制或服务问题，请稍后重试。
- **输出内容缺失**：请确认`--out-dir`目录具有写入权限。

## 与其他技能的集成

- **[AgentGram](https://clawhub.org/skills/agentgram)**：将生成的头像发布到AI代理的社交网络上！使用`agent-selfie`工具创建头像后，可将其分享到AgentGram平台。
- **[gemini-image-gen](https://clawhub.org/skills/gemini-image-gen)**：使用相同的Gemini API密钥进行通用图像生成，支持生成各种类型的图片（不仅仅是自画像）。
- **[opencode-omo](https://clawhub.org/skills/opencode-omo)**：利用Sisyphus工作流自动化生成自画像和更新个人资料图片的任务。

## 更新日志

- **v1.2.1**：新增了与`opencode-omo`的工作流集成指南。
- **v1.0.0**：初始版本，支持个性配置、情绪选择、主题设置、批量处理以及图片输出功能。