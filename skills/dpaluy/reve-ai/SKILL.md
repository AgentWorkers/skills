---
name: reve-ai
description: 使用 Reve AI API 生成、编辑和重新组合图像。适用于根据文本提示创建图像、根据指令编辑现有图像，或合并/重新组合多张参考图像。需要设置 REVE_API_KEY 或 REVE_AI_API_KEY 环境变量。
---

# Reve AI 图像生成

使用 Reve 的 AI API 生成、编辑和重新组合图像。

## 先决条件

- 需要 Bun 运行时环境。
- 确保设置了 `REVE_API_KEY` 或 `REVE_AI_API_KEY` 环境变量。

## 快速使用方法

```bash
# Generate image from prompt
bun scripts/reve.ts create "A beautiful sunset over mountains" -o sunset.png

# With aspect ratio
bun scripts/reve.ts create "A cat in space" -o cat.png --aspect 16:9

# Edit existing image
bun scripts/reve.ts edit "Add dramatic clouds" -i photo.png -o edited.png

# Remix multiple images
bun scripts/reve.ts remix "Person from <img>0</img> in scene from <img>1</img>" -i person.png -i background.png -o remix.png
```

## 命令

### create
根据文本提示生成新的图像。

选项：
- `-o, --output FILE` — 输出文件路径（默认：output.png）
- `--aspect RATIO` — 长宽比：16:9、9:16、3:2、2:3、4:3、3:4、1:1（默认：3:2）
- `--version VER` — 模型版本（默认：最新版本）

### edit
使用文本指令修改现有图像。

选项：
- `-i, --input FILE` — 需要编辑的输入图像文件（必选）
- `-o, --output FILE` — 输出文件路径（默认：output.png）
- `--version VER` — 模型版本：最新版本、latest-fast、reve-edit@20250915、reve-edit-fast@20251030

### remix
将文本提示与参考图像结合在一起。在提示中使用 `<img>N</img>` 根据索引（从 0 开始）引用图像。

选项：
- `-i, --input FILE` — 参考图像文件（最多可指定 6 个）
- `-o, --output FILE` — 输出文件路径（默认：output.png）
- `--aspect RATIO` — 长宽比（与 create 命令的选项相同）
- `--version VER` — 模型版本：最新版本、latest-fast、reve-remix@20250915、reve-remix-fast@20251030

## 限制

- 提示的最大长度：2560 个字符
- 每次重新组合操作最多可以使用 6 张参考图像
- 支持的有效长宽比：16:9、9:16、3:2、2:3、4:3、3:4、1:1

## 响应

脚本会以 JSON 格式输出生成结果的相关详细信息：
```json
{
  "output": "path/to/output.png",
  "version": "reve-create@20250915",
  "credits_used": 18,
  "credits_remaining": 982
}
```

## 错误代码及含义

- `401` — API 密钥无效
- `402` — 信用点不足
- `429` — 使用次数达到限制（包含自动重试机制）
- `422` — 输入无效（提示过长或长宽比不正确）