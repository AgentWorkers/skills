---
name: volcengine-ai-image-generation
description: Volcengine AI服务中的图像生成工作流程：适用于用户需要将文本转换为图像、调整图像样式、优化生成参数或进行故障排查的场景。
---

# volcengine-ai-image-generation

该工具能够根据明确的提示结构和参数控制生成并迭代图像。

## 执行流程

1. 确认所使用的模型/端点以及输出的图像要求（尺寸、数量、风格等）。
2. 将用户输入的提示信息转换为标准的格式，包括主题、风格、场景、光照效果和相机设置等参数。
3. 设置图像生成参数并发送请求。
4. 返回包含生成图像的链接或文件，同时附上相应的提示信息和参数设置。

## 提示信息结构

- 主题（Subject）
- 构图方式（Composition）
- 风格（Style）
- 光照效果（Lighting）
- 图像质量要求（Quality Constraints）

## 参考资料

- `references/sources.md`