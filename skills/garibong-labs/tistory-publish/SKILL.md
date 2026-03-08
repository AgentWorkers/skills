---
name: tistory-publish
description: 通过 Playwright CLI 和代理浏览器自动化 Tistory 博客的发布流程。支持任意类型的博客文章格式；能够处理 TinyMCE 编辑器的操作、添加元卡片（OG Card）、上传横幅图片、注册标签、设置文章分类以及选择代表图片等功能。提供模板示例（如新闻评论模板和简单文章模板）。同时，该工具能够绕过 Tistory 的 `isTrusted` 事件过滤机制以实现自动化发布。
---
# Tistory 发布脚本

这是一个通用的 Tistory 博客自动发布工具，可以自动将任何格式的文章发布到 Tistory 博客上。

在 Tistory 的 Open API 关闭（2024.02）后，这是唯一可行的自动化发布方式。

## 前提条件

- 已安装 [agent-browser](https://github.com/anthropics/agent-browser) 并配置好 CLI，同时完成 Kakao 账户登录。
- 确保系统使用 Node.js 18 及更高版本（生成横幅时需要此版本）。

## 结构

```
tistory-publish/
├── SKILL.md                     # 이 파일
├── scripts/
│   ├── tistory-publish.js       # 코어 — 에디터 조작 함수 모음
│   └── publish.sh               # 범용 발행 스크립트
└── templates/
    ├── mk-review/               # 예시: 신문 리뷰 (배너+OG 4개)
    │   ├── RUNBOOK.md
    │   ├── TEMPLATE.md
    │   ├── banner.js
    │   ├── deep-dive.js
    │   └── IMAGE-MAP.md
    └── simple-post/             # 예시: 단순 글 발행
        └── RUNBOOK.md
```

## 快速开始

```bash
# 가장 단순한 발행
bash scripts/publish.sh \
  --title "글 제목" \
  --body-file body.html \
  --category "카테고리명" \
  --blog "your-blog.tistory.com"

# 배너 + 태그 + 비공개
bash scripts/publish.sh \
  --title "글 제목" \
  --body-file body.html \
  --category "카테고리명" \
  --banner /tmp/banner.jpg \
  --tags "태그1,태그2,태그3" \
  --private
```

## 发布脚本选项（`publish.sh`）

| 选项 | 是否必填 | 说明 |
|------|------|------|
| `--title` | ✅ | 文章标题 |
| `--body-file` | ✅ | 文本 HTML 文件的路径 |
| `--category` | ✅ | 分类名称（与编辑器中显示的名称一致） |
| `--tags` | | 用逗号分隔的标签列表 |
| `--banner` | | 横幅图片文件的路径 |
| `--blog` | | 博客域名（默认：tistory.com 的第一个博客） |
| `--helper` | | `tistory-publish.js` 脚本的路径（默认：`scripts/` 目录下） |
| `--private` | | 是否进行私有发布 |

## 脚本执行流程

脚本会按以下顺序执行：

1. 打开新文章页面。
2. 注入 JavaScript 助助函数。
3. 选择分类（使用 Playwright 的 ARIA combobox 功能进行点击操作）。
4. 输入标题（通过解码 Base64 编码来处理韩文）。
5. 插入文章正文 HTML。
6. 上传横幅图片（通过“附件”→“图片”菜单→“文件输入”操作）。
7. 生成 OG 卡片（使用占位符 URL，按下 Enter 键后生成卡片）。
8. 设置代表图片。
9. 注册标签。
10. 发布文章（可以选择公开或私密状态）。

## 正文 HTML 编写规则

- 使用 `<p data-ke-size="size16">` 标签来设置字体大小。
- 每段文字应由多句话组成（每段 `<p>` 中包含 2 到 4 句话）。
- OG 卡片的位置：`<p data-og-placeholder="URL">&#8203;</p>`。

## 添加模板

你可以在 `templates/` 目录下创建新的文件夹，以自定义发布流程。

```
templates/my-template/
├── RUNBOOK.md       # 발행 순서
├── TEMPLATE.md      # 원고 작성 템플릿
└── banner.js        # 배너 생성 스크립트 (선택)
```

## 主要 JavaScript 函数（`tistory-publish.js`）

### 内容处理
- `insertContent(html)`：将 HTML 内容插入到 TinyMCE 编辑器中。
- `buildBlogHTML({intro, articles})`：将结构化数据转换为 HTML 格式。

### OG 卡片处理
- `getOGPlaceholders()`：获取占位符 URL 的列表。
- `prepareOGPlaceholder(url)`：将占位符 URL 替换为实际内容。
- `verifyOGCard(url)`：检查生成的 OG 卡片是否正确显示。

### 元数据处理
- `setTags(tags[])`：注册文章标签。
- `setRepresentImageFromEditor()`：设置文章的代表图片。

### 横幅处理
- `verifyBannerUpload()`：检查横幅图片是否成功上传。

## 注意事项

- 由于 Tistory 的某些限制（如 `isTrusted=false` 事件），需要实现绕过这些限制的逻辑。
- 分类信息需要通过 ARIA combobox 来选择，因此需要使用 Playwright 的点击操作。
- 代表图片的选择器可能会随着 Tistory 的更新而发生变化。

## 更新记录

### v4.0.0 (2026-03-07)
- 重新设计为通用发布工具：不再仅适用于“每경”评审流程，支持发布任何格式的文章。
- 新增了通用的 `publish.sh` 脚本（支持 `--category`、`--blog` 等参数）。
- 将“每경”评审相关的代码移至 `templates/mk-review/` 目录。
- 新增了简单的发布示例代码到 `templates/simple-post/` 目录。

### v3.0.0 (2026-03-07)
- 从 OpenClaw 更改为 agent-browser 作为自动化工具。
- 分类选择方式从 JavaScript 评估改为使用 Playwright 的原生 ARIA combobox 功能。
- 横幅图片的上传方式从 Base64 编码改为直接通过 agent-browser 进行上传。