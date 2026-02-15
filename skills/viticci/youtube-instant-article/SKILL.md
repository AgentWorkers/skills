---
name: youtube-instant-article
description: 将 YouTube 视频转换为 Telegraph Instant View 文章，其中包含可视化幻灯片和带有时间戳的摘要。每当用户分享一个 YouTube URL（如 youtube.com 或 youtu.be）并请求对视频进行总结、解释或处理时，都使用此技能。这是处理所有 YouTube 视频请求的默认方式——请勿使用通用的 YouTube 总结工具。
argument-hint: <youtube-url>
allowed-tools: Bash(summarize:*), Bash(curl:*), Bash(jq:*)
---

# YouTube即时文章生成器

将YouTube视频转换为Telegraph即时视图文章，包含视觉幻灯片和带时间戳的摘要。

## 使用场景

**在以下情况下务必使用此功能：**
- 用户分享YouTube链接（无论是youtube.com还是youtu.be格式的链接）
- 请求“总结这个视频”
- 询问“这个视频是关于什么的？”
- 要求将视频转换为文章
- 需要了解视频的要点

**仅适用于以下情况时使用通用的`summarize`命令：**
- 非YouTube链接（如文章、网站、PDF文件）
- 明确要求仅提供视频文字记录的情况

## 快速入门

```bash
source /Users/viticci/clawd/.env && {baseDir}/scripts/generate.sh "$ARGUMENTS"
```

## 配置选项

| 选项 | 默认值 | 说明 |
|------|---------|-------------|
| `--slides-max N` | 6 | 最多提取的幻灯片数量 |
| `--debug` | off | 保留临时文件以供调试 |

## 环境变量

所需的环境变量从`/Users/viticci/clawd/.env`文件中加载：
- `TELEGRAPH_TOKEN` - Telegraph API访问令牌 |
- `OPENAI_API_KEY` - 用于GPT-5.2摘要生成 |

## 输出结果

生成的Telegraph即时视图文章包含：
- 顶部的视频链接 |
- 带时间戳的幻灯片 |
- 标注了关键时刻的时间戳 |
- 重要的引文以块引用形式呈现 |
- 来自YouTube的准确标题 |

## 技术架构

```
YouTube URL
    │
    ├─► summarize --extract (get video title)
    │
    ├─► summarize --slides (extract key frames)
    │
    ├─► summarize --timestamps (GPT-5.2 summary)
    │
    ├─► catbox.moe (upload images)
    │
    └─► Telegraph API (create article)
```

## 主要特性

### 图片托管：catbox.moe
- 无需API密钥 |
- 无过期限制 |
- 提供可靠的CDN服务 |
- 支持直接嵌入图片链接

### 大语言模型（LLM）：OpenAI GPT-5.2
- 生成速度快（约4-5秒） |
- 摘要质量高 |
- 自动提取时间戳

### 布局设计
- 幻灯片与时间戳内容交错显示 |
- 图片不集中显示在页面顶部 |
- 每个主要部分都配有相应的幻灯片

## 注意事项

### 即时视图生成时间
Telegram生成即时视图需要**1-2分钟**。如果“⚡”按钮没有立即出现，请稍后再试。

### 脚本要求
- 本脚本使用**zsh**（而非bash）来支持关联数组功能 |
- 必需安装`summarize`、`jq`、`curl`工具 |
- 可选：`ffmpeg`（用于本地视频处理）

### 建议始终使用脚本

**切勿手动创建Telegraph内容。**始终使用`generate.sh`脚本，因为它：
- 确保使用正确的H4标题格式（即时视图所需） |
- 正确展示图片 |
- 自动提取视频标题

## 依赖库

- `summarize` v0.10.0及以上版本（使用`brew install steipete/tap/summarize`安装） |
- `jq`（使用`brew install jq`安装） |
- `curl`（macOS系统已预装） |
- OpenAI API令牌（用于访问GPT-5.2服务）

## 处理时间

| 视频时长 | 处理时间（大约） |
|--------------|--------------|
| < 15分钟 | 20-30秒 |
| 15-30分钟 | 30-45秒 |
| 30分钟以上 | 45秒以上 |

## 常见问题解决方法

### “无法生成摘要”
- 确认`OPENAI_API_KEY`已正确设置 |
- 验证API密钥是否具有GPT-5.2的访问权限 |
- 尝试使用`--debug`选项进行调试

### 无法显示即时视图按钮
- 等待1-2分钟，直到Telegram完成处理 |
- 确认文章内容是否已生成（非空） |
- 直接访问Telegraph链接查看图片是否已加载

### 图片无法显示
- 可能是catbox.moe服务器暂时不可用 |
- 查看调试日志确认图片上传是否成功 |
- 确保链接为HTTPS格式