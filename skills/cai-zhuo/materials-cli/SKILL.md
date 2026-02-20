---
name: materials-cli
description: 使用 `declare-render` 和 AI 技术，将 JSON 模式渲染为图像，并根据提示生成新的 JSON 模式。
version: 1.0.5
metadata:
  openclaw:
    requires:
      env:
        - OPENAI_API_KEY
      bins:
        - node
    primaryEnv: OPENAI_API_KEY
---# Materials CLI

当用户需要将 JSON 模式渲染为图像（PNG/JPG 格式）、验证渲染数据模式，或根据自然语言提示生成模式并随后进行渲染时，可以使用此工具。

## 命令

- **render** — 将 JSON 模式文件渲染为图像。
- **generate** — 使用 AI（OpenAI）根据用户提供的提示生成模式，然后将其渲染为图像。
- **validate** — 根据声明的渲染数据模式验证 JSON 模式。

## 使用场景

- 用户请求将 JSON 模式渲染为图像。
- 用户希望根据描述生成图像，或根据提示创建模式并对其进行渲染。
- 用户需要验证 JSON 文件是否符合渲染数据模式的要求。

## 使用方法

通过 Node.js 运行该工具（可以在项目内部直接运行，或通过 `npm install -g materials-cli` 全局安装后使用）：

```bash
materials render <schema-path> [options]
materials generate "<prompt>" [options]
materials validate <schema-path> [options]
```

### Render（渲染）

- `materials render schema.json -o output.png`
- 选项：`-s, --schema <path>`（指定 JSON 模式文件路径），`-o, --output <path>`（指定输出图像文件路径，默认为 `./output.png`），`-f, --format <png|jpg>`（指定输出图像格式），`-w, --width`（指定图像宽度），`-h, --height`（指定图像高度），`--output-schema <path>`（指定 JSON 模式文件路径），`-i, --interactive`（交互式模式）。

### Generate（生成）

- `materials generate "A red circle with text Hello" -o out.png`
- 选项：`-o, --output`（指定输出图像文件路径），`-f, --format`（指定输出图像格式），`-w, --width`（指定图像宽度），`-h, --height`（指定图像高度），`--output-schema`（指定 JSON 模式文件路径），`--model`（指定使用的 AI 模型，如 `OPENAI`），`--api-key`（指定 OpenAI API 密钥），`--base-url`（指定 OpenAI API 的基础 URL），`--interactive`（交互式模式）。
- 如果未通过命令行参数提供这些选项，系统会使用默认值 `OPENAI_API_KEY`、`OPENAI_MODEL` 和 `OPENAI_BASE_URL`。

### Validate（验证）

- `materials validate schema.json`
- 选项：`-s, --schema <path>`（指定 JSON 模式文件路径），`-i, --interactive`（交互式模式）。

## CLI 帮助文档

```
Usage: materials <command> [options]

Commands:
  render <schema>     Render a JSON schema file to an image
  generate <prompt>   Use AI to generate a schema, then render
  validate <schema>   Validate a schema against the render data schema

Examples:
  materials render schema.json -o output.png
  materials generate "A red circle with text Hello"
  materials validate schema.json
```

## 模式格式

JSON 模式遵循 `declare-render` 格式：根节点包含 `id`、`width`、`height` 和 `layers` 等属性。层类型包括 `text`（文本）、`image`（图像）、`container`（容器）等。在渲染之前，可以使用 `materials validate <file>` 命令检查 JSON 模式的有效性。