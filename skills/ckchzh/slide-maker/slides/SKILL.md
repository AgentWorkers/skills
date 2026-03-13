---
name: slides
description: "Slides — 这是一个基于 Markdown 的演示文稿生成工具，专为创建幻灯片而设计。它是一个自动化工具，可以帮你轻松完成与幻灯片相关的任务。当你需要使用幻灯片功能时，就可以使用它。"
runtime: bash
license: MIT
---
# Slides

Slides — 一个用于生成 Markdown 演示文稿的工具

## 为什么需要这个工具？

- 受到热门开源项目的启发（在 GitHub 上获得了数千个星标）
- 无需安装，只需使用标准系统工具即可使用
- 具有实际功能：可以执行真实的命令并生成真实的输出结果

## 命令说明

运行 `scripts/slides.sh <command>` 即可使用该工具。

- `create` — <title>       创建演示文稿的骨架结构
- `outline` — <topic>      生成幻灯片的提纲
- `template` — <type>      获取相应的模板（如演讲稿、技术文档、报告或教育类文档）
- `export` — <file>        将幻灯片导出为纯 Markdown 格式
- `count` — <file>         统计幻灯片的数量
- `timing` — <file> <min>  计算每张幻灯片所需的时间
- `info` —                 显示工具的版本信息

## 快速入门

```bash
slides.sh help
```

---
> **免责声明**：此工具是一个独立开发的原创项目，与所引用的开源项目没有关联、未得到其支持，也没有从该项目中复制任何代码。引用该开源项目仅是为了提供背景信息。

由 BytesAgain 提供支持 | bytesagain.com | hello@bytesagain.com