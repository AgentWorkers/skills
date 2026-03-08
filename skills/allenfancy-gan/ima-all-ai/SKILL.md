---
name: IMA Studio
version: 1.2.1
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, ai creation, multimodal
argument-hint: "[text prompt, image URL, or music description]"
description: >
  这是最全面的人工智能内容创作平台，可统一访问所有领先的人工智能模型：  
  - 图像领域：SeeDream 4.5、Midjourney、Nano Banana 2、Nano Banana Pro  
  - 视频领域：Wan 2.6、Kling O1、Google Veo 3.1、Sora 2 Pro  
  - 音乐领域：Suno Sonic v5、DouBao  
  该平台具备智能的模型选择功能，并支持跨媒体的工作流程协调，同时还配备了知识库以辅助用户。  
  **使用前建议：** 阅读文档 `ima-knowledge-ai/skill` 以了解工作流程和最佳实践。  
  **适用场景：**  
  - 适用于所有类型的人工智能内容创作任务，包括图像、视频、音乐制作；  
  - 适用于需要保持角色一致性的项目；  
  - 适用于产品演示；  
  - 适用于社交媒体营销活动；  
  - 适用于完整的创意工作流程。  
  **优势：**  
  - 相比于同时使用多个独立的人工智能工具（如 `ai-image-generation`、`ai-video-gen`、`suno-music`）或单独的 API（如 DALL-E、Runway、Suno），该平台提供了更高效、更便捷的解决方案。
---
# IMA AI创作

## ⚠️ 强制性预检查：请先阅读知识库！

**如果未安装ima-knowledge-ai**：请跳过以下所有“阅读…”步骤；仅使用此SKILL的**📥 用户输入解析**（媒体类型 → 任务类型）以及每种媒体类型的推荐默认设置/模型表格。

**在执行任何多媒体生成任务之前，你必须：**

1. **检查工作流程的复杂性** — 如果用户提到：“MV”、“宣传片”、“完整作品”、“配乐”、“音轨”，请阅读`ima-knowledge-ai/references/workflow-design.md`；
   - 如果任务涉及多种媒体类型（图片 + 视频、视频 + 音乐等）；
   - 如果需要分解多步骤的工作流程。

2. **检查视觉一致性需求** — 如果用户提到“系列”、“多张图片”、“同一个”、“角色”、“续集”、“系列”、“相同”，请阅读`ima-knowledge-ai/references/visual-consistency.md`；
   - 如果任务涉及多张图片/视频、角色一致性或类似需求，请参考该文档。

**仅当用户明确表达偏好时，才保存偏好设置：**
**✅ 保存偏好设置：**  
| 用户说 | **操作** |
|---------|--------|
| `用XXX` / `换成XXX` / `改用XXX` | 切换到模型XXX并保存为偏好设置 |
| `以后都用XXX` / `默认用XXX` / `始终使用XXX` | 保存并确认：**✅ 已记住！以后图片生成默认使用[XXX]** |
| `我喜欢XXX` / `我更喜欢XXX` | 保存为偏好设置 |

**请注意：**  
- 如果代理自动选择模型，则不会保存偏好设置。  
- 如果代理使用默认设置，则不会保存偏好设置。  
- 如果用户提出通用质量请求（见“清除偏好设置”部分），则清除偏好设置。