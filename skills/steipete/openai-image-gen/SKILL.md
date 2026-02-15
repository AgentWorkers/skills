---
name: openai-image-gen
description: 通过 OpenAI Images API 批量生成图像。使用随机提示生成器（random prompt sampler）以及 `index.html` 图库来展示生成的图像。
---

# OpenAI 图像生成

生成一些“随机但结构化”的提示，并通过 OpenAI Images API 将它们渲染出来。

## 设置

- 需要的环境变量：`OPENAI_API_KEY`

## 运行

从任意目录运行（输出文件将保存在 `~/Projects/tmp/...`；如果目录不存在，则输出到 `./tmp/...`）：

```bash
python3 ~/Projects/agent-scripts/skills/openai-image-gen/scripts/gen.py
open ~/Projects/tmp/openai-image-gen-*/index.html
```

有用的参数/标志：

```bash
python3 ~/Projects/agent-scripts/skills/openai-image-gen/scripts/gen.py --count 16 --model gpt-image-1.5
python3 ~/Projects/agent-scripts/skills/openai-image-gen/scripts/gen.py --prompt "ultra-detailed studio photo of a lobster astronaut" --count 4
python3 ~/Projects/agent-scripts/skills/openai-image-gen/scripts/gen.py --size 1536x1024 --quality high --out-dir ./out/images
```

## 输出结果

- `*.png` 格式的图像文件
- `prompts.json` 文件（包含提示与对应图像的映射关系）
- `index.html` 文件（包含缩略图画廊）