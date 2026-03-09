---
name: auto-sec-blogger
description: AI-powered security blog automation system (identical to github.com/rebugui/intelligence-agent). Collects news from Google News, arXiv, HackerNews → generates blog posts with GLM-4.7 → publishes to Notion → auto-deploys to GitHub Pages via Git. Features Human-in-the-Loop approval workflow. Use when you want to automate blog writing, news collection, or content generation with the exact functionality of the original intelligence-agent repository. Triggers: "블로그 글 작성", "보안 뉴스 발행", "깃헙 블로그 발행", "intelligence agent", "지능형 에이전트", "자동 글쓰기".
---

# 智能代理（Intelligence Agent）

## 概述

这是一个自动化系统，能够自动收集安全新闻，利用大语言模型（LLM，具体为GLM-4.7）生成专业级别的博客文章，并将这些文章自动发布到Notion和GitHub Pages上。

**GitHub仓库链接**：https://github.com/rebugui/intelligence-agent

## 架构

```
뉴스 수집 (Google News, arXiv, HackerNews)
    ↓
GLM-4.7 글 작성 (전문 보안 블로그)
    ↓
Notion Draft 저장 (상태: Draft)
    ↓
사용자 검토 및 승인 (Human-in-the-Loop)
    ↓
Git Push → GitHub Actions → GitHub Pages
```

## 主要功能

### 1. 新闻收集（News Collection）
- **Google News**：基于关键词收集安全新闻
- **arXiv**：收集最新的安全研究论文
- **HackerNews**：收集热门的技术新闻
- **去重处理**：通过URL过滤重复的新闻

### 2. LLM文章生成（Content Generation）
- **模型**：GLM-4.7（来自Zhipu AI）
- **风格**：专业安全博客风格
- **文章结构**：
  - 标题（Header）
  - 摘要（3行概括）
  - 正文（详细分析）
  - 结论（观点总结）
  - 标签（关键词）
- **Mermaid图表**：用于可视化攻击流程和系统架构

### 3. 与Notion集成（Notion Integration）
- **状态管理**：文章状态可切换为：草稿（Draft）→ 审核中（Review）→ 已批准（Approved）→ 已发布（Published）
- **自动保存**：生成的文章会自动保存到Notion
- **用户审批**：需要用户通过状态变更来批准文章的发布

### 4. 基于Git的发布（Git Publishing）
- **自动提交**：将Markdown格式的文件提交到Git仓库
- **GitHub Actions**：自动执行Jekyll构建过程
- **GitHub Pages**：将生成的博客文章部署到GitHub Pages上

## 安装步骤

### 1. 安装依赖项

```bash
cd ~/.openclaw/workspace/skills/intelligence-agent/scripts
pip3 install -r requirements.txt
```

### 2. 设置环境变量

```bash
# ~/.openclaw/workspace/.env

# GLM API
GLM_API_KEY=your_glm_api_key
GLM_BASE_URL=https://api.z.ai/api/coding/paas/v4

# Notion
NOTION_API_KEY=ntn_xxx
NOTION_DATABASE_ID=xxx

# GitHub Pages
GITHUB_TOKEN=ghp_xxx
GITHUB_BLOG_REPO=username/username.github.io
BLOG_LOCAL_PATH=/path/to/blog/repo
```

## 使用方法

### 1. 运行完整流程（测试用）

```bash
cd ~/.openclaw/workspace/skills/intelligence-agent/scripts
python3 intelligence_pipeline.py --max-articles 5
```

### 2. 仅收集新闻

```python
from collector import NewsCollector

collector = NewsCollector()
articles = collector.fetch_all(max_results_per_source=15)
```

### 3. 仅生成博客文章

```python
from writer import BlogWriter

writer = BlogWriter()
post = writer.generate_article(article_data)
```

### 4. 仅发布到Notion

```python
from notion_publisher import NotionPublisher

publisher = NotionPublisher()
result = publisher.create_article(blog_post)
```

### 5. 仅通过Git发布

```python
from git_publisher_service import GitPublisherService

git_publisher = GitPublisherService()
git_publisher.publish(blog_posts)
```

## 工作流程详情

### 第一步：新闻收集

```python
# collector.py
class NewsCollector:
    def fetch_google_news(self, query="security vulnerability"):
        # Google News RSS 피드에서 수집
        pass

    def fetch_arxiv(self, category="cs.CR"):
        # arXiv 보안 논문 수집
        pass

    def fetch_hackernews(self):
        # HackerNews 트렌딩 기사 수집
        pass
```

### 第二步：筛选AI生成的文章

```python
# selector.py
class ArticleSelector:
    async def evaluate_and_select(self, articles, max_articles=5):
        # GLM-4.7으로 기사 품질 평가
        # 점수 기반 상위 기사 선별
        pass
```

### 第三步：生成博客文章

```python
# writer.py
class BlogWriter:
    async def generate_article(self, article):
        # GLM-4.7으로 블로그 글 작성
        # Mermaid 다이어그램 생성
        # 마크다운 형식 출력
        pass
```

### 第四步：发布到Notion

```python
# notion_publisher.py
class NotionPublisher:
    def create_article(self, blog_post):
        # Notion DB에 Draft 상태로 저장
        # 상태: Draft → Review → Approved
        pass
```

### 第五步：通过Git发布（需用户批准后）

```python
# git_publisher_service.py
class GitPublisherService:
    def publish(self, blog_posts):
        # 마크다운 파일 생성
        # Git commit & push
        # GitHub Actions 트리거
        pass
```

## Cron任务调度

- 系统每天在08:30自动执行整个流程

```python
# intelligence_pipeline.py
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
scheduler.add_job(run_pipeline, 'cron', hour=8, minute=30)
scheduler.start()
```

## Notion数据库结构

| 属性名 | 类型 | 说明 |
|--------|------|------|
| 标题 | title | 博文标题 |
| 状态 | select | 草稿（Draft）/审核中（Review）/已批准（Approved）/已发布（Published） |
| 发布日期 | date | 文章发布时间 |
| 标签 | multi_select | 关键词 |
| 原文链接 | url | 新闻的原始URL |
| 类别 | select | 漏洞（Vulnerability）/研究（Research）/趋势（Trend） |

## Jekyll博客的文件结构

```
blog/
├── _posts/
│   ├── 2025-03-09-cve-2025-xxxx-analysis.md
│   ├── 2025-03-09-ai-security-trends.md
│   └── ...
├── _layouts/
│   ├── post.html
│   └── default.html
├── _config.yml
└── .github/
    └── workflows/
        └── jekyll.yml
```

## 故障排除

### GLM API的请求速率限制

```
❌ Error: Rate limit reached (429)
```

**解决方法**：
- 自动尝试3次
- 失败后等待60秒再重试

### Notion API错误

```
❌ Error: Notion API error
```

**解决方法**：
- 确认API密钥是否正确
- 确认数据库ID是否有效
- 检查是否具有足够的集成权限

### Git推送失败

```
❌ Error: Git push failed
```

**解决方法**：
- 确认GitHub Token是否有效
- 检查是否有权限访问远程仓库
- 确认使用的Git分支是否正确

## 文件结构

```
intelligence-agent/
├── SKILL.md (이 파일)
├── scripts/
│   ├── intelligence_pipeline.py (메인 파이프라인)
│   ├── collector.py (뉴스 수집)
│   ├── selector.py (AI 기사 선별)
│   ├── writer.py (블로그 글 작성)
│   ├── notion_publisher.py (Notion 발행)
│   ├── git_publisher_service.py (Git 발행)
│   ├── llm_client.py (GLM API 클라이언트)
│   ├── llm_client_async.py (비동기 GLM 클라이언트)
│   ├── prompt_manager.py (프롬프트 관리)
│   ├── prompts.yaml (프롬프트 템플릿)
│   ├── models.py (데이터 모델)
│   ├── utils.py (유틸리티)
│   ├── config.py (설정)
│   └── requirements.txt (의존성)
└── references/
    ├── architecture.md (상세 아키텍처)
    ├── prompts_guide.md (프롬프트 가이드)
    └── api_reference.md (API 레퍼런스)
```

## 环境变量设置

### 必需设置的环境变量

```bash
GLM_API_KEY          # GLM-4.7 API 키
NOTION_API_KEY       # Notion API 키
NOTION_DATABASE_ID   # Notion 데이터베이스 ID
```

### 可选设置

```bash
GITHUB_TOKEN         # GitHub 개인 액세스 토큰
GITHUB_BLOG_REPO     # GitHub 블로그 저장소 (username/repo)
BLOG_LOCAL_PATH      # 로컬 블로그 경로
```

## 测试

### 运行完整流程的测试

```bash
python3 test_full_pipeline.py
```

### Mermaid图表的测试

```bash
python3 test_mermaid_fix.py
```

## 参考资源

- [GitHub仓库链接](https://github.com/rebugui/intelligence-agent)
- [GLM API文档](https://open.bigmodel.cn/dev/api)
- [Notion API文档](https://developers.notion.com/)
- [Jekyll文档](https://jekyllrb.com/docs/)

## 资源文件

### scripts/
- 包含原始仓库中的所有Python脚本：
  - `intelligence_pipeline.py`：执行整个处理流程
  - `collector.py`：负责新闻收集
  - `selector.py`：筛选AI生成的文章
  - `writer.py`：生成博客文章
  - `notion_publisher.py`：将文章发布到Notion
  - `git_publisher_service.py`：通过Git发布文章
  - `llm_client.py`：与GLM API交互的客户端
  - `prompts.yaml`：提示语模板文件

### references/
- `architecture.md`：详细的系统架构说明
- `prompts_guide.md`：提示语编写指南
- `api_reference.md`：API使用参考文档