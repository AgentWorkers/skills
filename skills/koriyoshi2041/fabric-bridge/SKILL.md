---
name: fabric-bridge
description: "运行 Fabric AI 模式以进行文本转换、分析和内容创作。当用户请求使用 Fabric 模式、提取有价值的信息、分析声明、改进写作内容、使用 Fabric 进行总结，或提到 “fabric” CLI 时，请使用该功能。Fabric 支持 242 种以上的模式，可用于内容分析、写作改进、代码审查、威胁建模以及结构化数据提取等任务。"
homepage: https://github.com/danielmiessler/fabric
metadata: {"clawdbot":{"emoji":"🧶","requires":{"bins":["fabric-ai"]},"install":[{"id":"brew","kind":"brew","formula":"fabric-ai","bins":["fabric-ai"],"label":"Install Fabric AI (brew)"}]}}
---

# Fabric Bridge

您可以通过 `fabric-ai` CLI 来运行 Fabric AI 模式。每个模式都是针对特定任务设计的可重用系统提示。

> 请参阅 `references/popular-patterns.md`，以获取按类别分类的高质量模式列表。

## 重要说明

- 命令是 **`fabric-ai`**，而不是 `fabric`。
- 首次设置时：运行 `fabric-ai -S` 以配置 API 密钥。
- 如果模式列表为空：运行 `fabric-ai -U` 以更新模式。
- 对于大多数调用，建议使用 `-s`（流式输出）以避免长时间等待。

## 核心命令

### 基本用法

```bash
echo "input text" | fabric-ai -p <pattern>
```

### 流式输出（推荐）

```bash
echo "input text" | fabric-ai -p <pattern> -s
```

### 处理 YouTube 视频

```bash
fabric-ai -y "https://youtube.com/watch?v=..." -p extract_wisdom -s
```

### 处理网页

```bash
fabric-ai -u "https://example.com/article" -p summarize -s
```

### 指定模型

```bash
echo "input" | fabric-ai -p <pattern> -m gpt-4o
```

### 中文输出

```bash
echo "input" | fabric-ai -p <pattern> -g zh -s
```

### 链式调用模式（将输出传递给下一个模式）

```bash
echo "input" | fabric-ai -p extract_wisdom | fabric-ai -p summarize
```

### 推理策略（需要预先设置）

```bash
echo "input" | fabric-ai -p <pattern> --strategy cot -s
```

### 处理图像（多模态）

```bash
echo "describe this image" | fabric-ai -p <pattern> -a /path/to/image.png -s
```

### 使用上下文信息

```bash
echo "input" | fabric-ai -p <pattern> -C my_context -s
```

### 会话连续性

```bash
echo "input" | fabric-ai -p <pattern> --session my_session -s
```

### 将输出保存到文件

```bash
echo "input" | fabric-ai -p extract_wisdom -o output.md
```

### 将输出复制到剪贴板

```bash
echo "input" | fabric-ai -p extract_wisdom -c
```

### 干运行（预览，不调用 API）

```bash
fabric-ai -p <pattern> --dry-run
```

### 列出所有可用模式

```bash
fabric-ai -l
```

## 模板变量

模式中可以包含 `{{variable}}` 占位符。使用 `-v` 传递值：

```bash
# Single variable
echo "input" | fabric-ai -p <pattern> -v="#role:expert"

# Multiple variables
echo "input" | fabric-ai -p <pattern> -v="#role:expert" -v="#points:30"
```

## 自定义模式

您可以在 `~/.config/fabric/patterns/<name>/system.md` 文件中创建自定义模式。

每个模式目录都包含一个 `system.md` 文件，其中包含了该模式的系统提示。

## 提供文件内容

```bash
cat file.txt | fabric-ai -p <pattern> -s
cat file1.md file2.md | fabric-ai -p <pattern> -s
```

## 提示

- 建议使用 `-s`（流式输出）进行交互式操作——输出会逐步显示。
- 通过链式调用模式来实现多步骤处理（例如：提取 → 总结 → 翻译）。
- 如果用户需要中文输出，请使用 `-g zh`。
- 使用 `-o file.md` 将输出保存到文件，使用 `-c` 将输出复制到剪贴板。
- 使用 `--dry-run` 来查看在调用 API 之前将要发送的数据。
- 定期运行 `fabric-ai -U` 以获取新的社区模式。