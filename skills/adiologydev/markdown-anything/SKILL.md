---
name: markdown-anything
description: 使用 Markdown Anything API，可以将 PDF、DOCX、XLSX、PPTX、图片、音频以及 25 种以上的其他文件格式转换为格式规范的 Markdown 文本。
homepage: https://markdownanything.com
metadata:
  clawdbot:
    emoji: "📝"
    requires:
      env: ["MDA_API_TOKEN"]
    primaryEnv: "MDA_API_TOKEN"
    files: ["scripts/*"]
---
# Markdown Anything

使用 [Markdown Anything](https://markdownanything.com) API 将文件转换为格式清晰、结构良好的 Markdown 文本。支持 PDF、DOCX、XLSX、PPTX、图片、音频以及 25 种以上的其他格式。

## 设置

将您的 API 令牌设置为环境变量。您可以在 [Markdown Anything 工作空间](https://markdownanything.com/workspaces) 的 **设置 > API 令牌** 中获取该令牌。

```
MDA_API_TOKEN=mda_your_token_here
```

## 使用场景

当用户需要执行以下操作时，可以使用 `mda-convert` 工具：
- 将文件转换为 Markdown 格式
- 从 PDF、文档、图片或音频文件中提取文本
- 将文档转换为 Markdown 格式，以便在提示或工作流程中使用

## 工具

### mda-convert

该工具用于将文件转换为 Markdown 格式。运行 `scripts/convert.sh`，并将文件路径作为第一个参数传递。

**参数：**
- `$1` — 需要转换的文件路径

**可选的环境变量：**
- `MDA_ENHANCED.AI=true` — 对扫描的文档、图片和音频使用增强型 AI 处理（需要额外费用）
- `MDA_INCLUDE_METADATA=true` — 在响应中包含文档元数据
- `MDA_OPTIMIZE_TOKENS=true` — 优化输出内容，以提高 LLM 令牌的使用效率

**示例：**
```
scripts/convert.sh /path/to/document.pdf
```

该工具会将转换后的 Markdown 内容输出到标准输出（stdout）。

### mda-credits

查看您的剩余信用额度。运行 `scripts/credits.sh`（不带任何参数）即可。

**示例：**
```
scripts/credits.sh
```

## 安全性与隐私

- 文件会被发送到 `https://markdownanything.com/api/v1/convert` 进行处理
- 您的 API 令牌会通过 `Authorization` 头部字段传递
- 除了转换结果外，不会在本地存储任何数据
- 有关数据处理的详细信息，请参阅 [Markdown Anything 隐私政策](https://markdownanything.com/privacy)