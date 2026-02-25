---
name: social-media-platform
description: 构建一个基于插件的社交媒体管理平台，支持多平台发布、内容日程安排、品牌信息管理、通过 LangGraph 实现的 AI 内容生成以及数据分析功能。该平台可用于开发社交媒体工具、内容调度系统或多平台发布流程。涵盖与 Facebook、Instagram、YouTube、Twitter/X 和 TikTok 的集成方案。
---
# 社交媒体平台构建器

构建一个完整的社交媒体管理系统，该系统支持插件架构、人工智能驱动的内容生成以及多平台发布功能。

## 架构

```
┌─────────────────────────────────────┐
│         Frontend (5 pages)          │
│  Dashboard│Compose│Calendar│Analytics│Settings│
├─────────────────────────────────────┤
│         API Layer (FastAPI)         │
│  Posts CRUD│Publishing│Calendar│AI  │
├─────────────────────────────────────┤
│      Plugin Registry (per-platform) │
│  Twitter│Instagram│YouTube│FB│TikTok│Manual│
├─────────────────────────────────────┤
│    LangGraph Content Pipeline       │
│  Voice→Research→Draft→Optimize→Save │
├─────────────────────────────────────┤
│         Supabase (6 tables)         │
└─────────────────────────────────────┘
```

## 第一步：Supabase 数据表设计

创建 6 个数据表：
- `social_posts`：id、平台、内容、状态（草稿/计划中/已发布/失败）、媒体链接、发布时间、帖子链接、互动指标（JSONB 格式）
- `platform_connections`：id、平台、账户名称、凭据（JSONB 格式）、状态、权限范围
- `content_calendar`：id、帖子 ID（外键）、计划发布时间、平台、状态
- `brand_voices`：id、名称、描述、语气、示例语句（JSONB 数组）、是否为默认语音
- `social_analytics`：id、帖子 ID（外键）、平台、浏览量、点击量、点赞数、分享数、评论数、数据获取时间
- `publish_queue`：id、帖子 ID（外键）、平台、状态、重试次数、错误信息

预先创建 3-5 个品牌语音示例：
- **默认语音**：权威性、清晰、教育性
- **随意语气**：对话式、友好、使用缩写
- **激励语气**：激励性、直接、行动导向

## 第二步：插件系统

采用基类模式进行设计：

```python
class SocialPlugin:
    platform: str
    def validate_credentials(self, creds: dict) -> bool
    def publish(self, content: str, media_urls: list = None) -> dict
    def get_analytics(self, post_id: str) -> dict
    def format_content(self, content: str, max_length: int) -> str

class PluginRegistry:
    _plugins: dict[str, SocialPlugin] = {}
    def register(self, plugin: SocialPlugin)
    def get(self, platform: str) -> SocialPlugin
    def list_active(self) -> list[str]
```

针对不同平台的实现方式：
- **Twitter**：使用 tweepy 或 v2 API。帖子长度限制为 280 字符。免费 tier 每月可发布 100 条帖子。
- **Facebook**：使用 Graph API v21.0。需要页面访问令牌。帖子发布路径为 `/{page_id}/feed`。
- **Instagram**：通过 FB 页面令牌使用 Graph API。帖子发布路径为 `/{ig_user_id}/media` 或 `/{ig_user_id}/media_publish`。需要上传图片。
- **YouTube**：使用 google-auth 和 google-api-python-client。需要 `youtube.upload` 权限范围。支持分块上传功能。
- **TikTok**：使用内容发布 API（需要应用审核和演示视频）。作为备用方案，可以使用手动发布模式。
- **手动发布**：不依赖 API——自动生成帖子内容并推荐最佳发布时间。适用于所有未连接的平台。

## 第三步：LangGraph 内容处理流程

该流程包含 6 个核心节点：

```
load_voice → research_context → generate_drafts → optimize_per_platform → finalize → END
```

- **load_voice**：从 Supabase 中加载选定的品牌语音数据。
- **research_context**：查询知识库或 RAG（Retrieval, Augmentation, Generation）系统以获取相关领域的内容。
- **generate_drafts**：使用大型语言模型（LLM）生成 2-3 个符合该品牌语音风格的草稿。
- **optimize_per_platform**：根据不同平台调整每个草稿的内容（长度、标签、媒体素材建议）。
- **finalize**：将草稿保存到 `social_posts` 表中，并标记为草稿状态。

## 第四步：API 端点

提供约 19 个核心 API 端点：
- `GET/POST /api/social/posts`：执行创建、读取、更新、删除操作。
- `POST /api/social/posts/{id}/publish`：将帖子发布到指定平台。
- `GET/POST /api/social/calendar`：查看日历并安排发布计划。
- `GET/POST /api/social/analytics`：获取汇总的互动数据。
- `GET/POST /api/social/voices`：管理品牌语音设置。
- `GET/POST /api/social/connections`：管理平台连接信息。
- `POST /api/social/generate`：使用人工智能生成内容（触发 LangGraph 流程）。

## 第五步：前端页面设计

整个系统采用统一的深色主题设计，包含以下 5 个页面：
1. **控制面板**：按平台显示帖子数量、近期活动记录以及快速发布功能。
2. **内容编辑页面**：提供丰富的编辑工具、多平台选择功能、语音选择器以及每个平台的实时预览功能。
3. **日历页面**：以月份为单位显示帖子安排情况，不同平台用不同颜色区分；支持拖动操作调整发布时间。
4. **分析页面**：使用 Chart.js 绘制随时间变化的互动数据图表。
5. **设置页面**：提供平台连接信息填写表单（支持 OAuth 流程）以及品牌语音编辑功能。

## 关键设计原则：
- **凭据存储方式**：所有平台的认证信息（API 密钥、OAuth 令牌、页面令牌等）统一存储在 `credentials` JSONB 列中。
- **优雅降级**：始终提供手动发布作为备用方案——即使无法使用 API 也能生成帖子内容。
- **平台内容限制**：严格执行每个平台的规则（Twitter 最长 280 字符、Instagram 需要图片、YouTube 需要视频、Facebook 最大 63K 字节）。
- **发布队列与重试机制**：失败发布的帖子会被放入重试队列，并采用指数级退避策略进行重试。