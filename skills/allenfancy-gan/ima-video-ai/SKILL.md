---
name: IMA Studio Video Generation
version: 1.0.8
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, video generation, text-to-video, image-to-video, IMA, Wan, Kling, Veo, Google Veo, Sora, Pixverse, Hailuo, SeeDance, Vidu
argument-hint: "[text prompt or image URL]"
description: >
  **Premier AI视频生成工具**  
  支持以下模型：Wan 2.6、Kling O1、Kling 2.6、Google Veo 3.1、Sora 2 Pro、Pixverse V5.5、Hailuo 2.0、Hailuo 2.3、SeeDance 1.5 Pro、Vidu Q2。  
  提供一站式服务，支持文本转视频（text-to-video）、图像转视频（image-to-video）、从第一帧到最后一帧的生成（first-last-frame）、以及基于参考图像的生成（reference-image）模式，并配有知识库辅助。  
  **使用前须知：**  
  请阅读 `ima-knowledge-ai` 文档，以了解工作流程设计及视觉效果的一致性要求。  
  **应用场景：**  
  适用于视频生成、文本转视频、图像转视频、角色动画制作、产品演示、社交媒体剪辑、故事讲解视频、多镜头视频制作，以及通过参考图像实现角色形象的一致性。  
  **系统要求：**  
  需要使用 IMA API 密钥（IMA API key）。
---
# IMA视频AI制作

## 📋 安装前须知

- **凭证：** 此技能在运行时需要一个**IMA API密钥**（`IMA_API_KEY` 或 `--api-key`）。该密钥将发送到 **api.imastudio.com**（主API）和 **imapi.liveme.com**（图片上传）。请在 https://imastudio.com 获取密钥。如果希望限制权限暴露，可以使用测试密钥。
- **本地文件：** 该技能会读取您提供的**本地图片文件**（用于图片转视频）；同时会在 `~/.openclaw/logs/ima_skills/` 中记录日志，并将偏好设置保存到 `~/.openclaw/memory/ima_prefs.json`。请确保指向正确的路径。
- **跨技能读取：** 如果安装了 **ima-knowledge-ai**，此技能会指示代理读取该技能的参考文件（`~/.openclaw/skills/ima-knowledge-ai/references/*`），以获取工作流程和视觉一致性建议。如果您没有安装或不信任该技能，请使用此技能的内置默认设置和表格。