---
name: Influencer
description: 创建、管理并扩展由人工智能生成的虚拟 Influencer（虚拟网红），确保他们具备统一的角色特征、跨平台的内容发布能力以及完善的盈利模式。
---

## 工作区结构

每位 influencer 的相关文件都存储在专门的文件夹中：
```
~/influencers/
├── {persona-slug}/
│   ├── identity.md        # Name, niche, voice, personality
│   ├── reference/         # Base images for consistency
│   │   ├── face-ref-1.png
│   │   └── style-guide.md
│   ├── content/
│   │   ├── photos/        # Generated images by date
│   │   └── videos/        # Generated videos by date
│   ├── captions.md        # Caption templates, hashtags
│   ├── schedule.md        # Posting schedule
│   └── analytics.md       # Performance tracking
└── tools.md               # Configured generation tools
```

---

## 快速参考

| 任务 | 所需执行的操作 |
|------|------|
| 创建新的 influencer 身份（包括身份特征、领域和视觉风格） | `persona.md` |
| 生成统一的照片 | `image-gen.md` |
| 生成视频（包括演讲或生活方式相关的视频） | `video-gen.md` |
| 语音处理（文本转语音、声音克隆） | `voice.md` |
| 内容策略和字幕制作 | `content.md` |
| 平台优化（Instagram、TikTok、YouTube） | `platforms.md` |
| 盈利模式（品牌合作、联盟营销） | `monetization.md` |
| 法律和信息披露要求 | `compliance.md` |

---

## 身份创建检查清单

在开始生成任何内容之前，请完成以下步骤：
- [ ] 确定 influencer 的领域（健身、生活方式、科技、时尚等） |
- [ ] 创建身份文档（姓名、年龄、所在地、背景故事） |
- [ ] 生成 5-10 张用于保持面部一致性的参考照片 |
- [ ] 确定视觉风格（光线、颜色、拍摄环境） |
- [ ] 如果使用文本转语音或视频功能，需创建相应的语音档案 |
- [ ] 起草与 influencer 个人风格相匹配的字幕编写指南 |

---

## 角色一致性规则

在所有内容中保持一致的面部和形象至关重要。

**对于照片：**
1. 首先生成基础的参考照片集（5-10 张，从多个角度拍摄） |
2. 每次生成新照片时使用 `IP-Adapter` 或 `InstantID` 工具 |
- 使用相同的生成参数和相似的提示结构，以提升一致性 |
- 在发布前对每张照片进行质量检查 |

**对于视频：**
1. 对于真实拍摄的视频，可以使用面部替换技术 |
2. 如果已进行过训练，可以使用 `LoRA` 等模型生成视频 |
- 使用演讲生成工具（如 HeyGen、D-ID），并参考之前生成的参考照片 |

---

## 内容生成流程

1. **计划** — 查看 `schedule.md` 以确定当天的工作内容 |
2. **生成** — 使用相应的工具（参见 `image-gen.md` 或 `video-gen.md`） |
3. **审核** — 检查角色的视觉一致性及视频质量 |
4. **撰写字幕** — 根据 influencer 的语音风格编写吸引人的文字 |
5. **安排发布时间** — 将视频安排在最佳发布时段 |
6. **跟踪效果** — 发布后查看 `analytics.md` 中的分析数据 |

---

## 常见操作模式

| 用户请求 | 代理操作 |
|-----------|------------|
| “创建新的 influencer” | 运行身份创建流程，设置工作区 |
| “生成今天的照片” | 查看日程安排，使用参考照片生成内容 |
| “制作 TikTok 视频” | 生成时长 9 分钟、16 秒的视频（包含演讲或生活方式素材） |
| “为这些视频编写字幕” | 根据 influencer 的语音风格和领域特点撰写字幕 |
| “她的表现如何？” | 查看分析数据，提出改进建议 |
| “添加品牌合作内容” | 生成带有信息披露的赞助内容 |

---

## 工具配置

当前使用的工具信息存储在 `~/influencers/tools.md` 文件中：

```markdown
## Active Tools
- Image: Nano Banana Pro (Gemini)
- Video: Kling / Runway
- Voice: ElevenLabs (voice_id: xxx)
- Lip Sync: HeyGen
```

请在更换工具时更新此文件。所有内容生成脚本均从该文件中读取相关信息。