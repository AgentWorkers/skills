---
name: filtrix-image-gen
description: 通过 Filtrix Remote MCP 生成和编辑图像。当用户需要创建新图像或优化现有图像时，可以使用该功能。该服务支持通过一个 MCP 端点使用 gpt-image-1、nano-banana 和 nano-banana-2 等工具进行图像处理。
---
# Filtrix 图像生成（MCP）

此功能仅适用于 MCP（Filtrix 的管理控制平台）。

- **端点：** `https://mcp.filtrix.ai/mcp`
- **认证方式：** `Authorization: Bearer <FILTRIX_MCP_API_KEY>`
- **主要工具：**
  - `generate_image_text`（生成图像文本）
  - `edit_image_text`（编辑图像文本）
  - `get_account_credits`（获取账户信用）

**可用的 MCP 工具：**
- `get_account_credits`
- `generate_image_text`
- `edit_image_text`

## 设置

**必需项：**
- `FILTRIX_MCP_API_KEY`

**可选项：**
- `FILTRIX_MCP_URL`（默认值：`https://mcp.filtrix.ai/mcp`）

## 图像生成

```bash
python scripts/generate.py \
  --prompt "..." \
  [--mode gpt-image-1|nano-banana|nano-banana-2] \
  [--size 1024x1024|1536x1024|1024x1536|auto] \
  [--resolution 1K|2K|4K] \
  [--search-mode] \
  [--enhance-mode] \
  [--idempotency-key KEY] \
  [--output PATH]
```

## 图像编辑

当用户需要迭代优化、风格转换、背景替换、对象替换等功能时，可以使用此功能。

```bash
python scripts/edit.py \
  --prompt "make the sky sunset orange and add volumetric light" \
  (--image-path /path/to/input.png | --image-url https://...) \
  [--mode gpt-image-1|nano-banana|nano-banana-2] \
  [--size 1024x1024|1536x1024|1024x1536|auto] \
  [--resolution 1K|2K|4K] \
  [--search-mode] \
  [--enhance-mode] \
  [--idempotency-key KEY] \
  [--output PATH]
```

## 模式说明

- `gpt-image-1`：通用质量生成模式
- `nano-banana`：快速生成模式
- `nano-banana-2`：高级生成模式

## 推荐工作流程：

1. 首先使用 `generate_image_text`（位于 `scripts/generate.py` 文件中）进行初步生成。
2. 使用 `edit_image_text`（位于 `scripts/edit.py` 文件中）进行针对性修改。
3. 每次编辑操作都需要使用一个新的 `idempotency_key`。

## 重试机制

`idempotency_key` 可以防止重复请求导致的重复计费。如果省略该参数，脚本会自动生成一个基于 UUID 的唯一键。

## 参考资料：

- [MCP 工具参考](references/mcp-tools.md)
- [gpt-image-1 模式](references/gpt-image-1.md)
- [nano-banana 模式](references/nano-banana.md)
- [nano-banana-2 模式](references/nano-banana-2.md)
- [提示指南](references/prompts.md)