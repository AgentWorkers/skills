---
name: web-deploy-github
description: 使用自动化工作流程，将单页静态网站创建并部署到 GitHub Pages 上。适用于构建作品集网站、个人简历页面、登录页面，或任何需要通过 GitHub Pages 进行部署的静态网站项目。该流程涵盖了从项目初始化到通过 GitHub Actions 实现自动部署的整个过程。
---

# 在 GitHub Pages 上进行 Web 部署

## 概述

本技能支持自主创建并将静态网站部署到 GitHub Pages。它遵循一个完整的工作流程，从项目结构初始化开始，通过 GitHub Actions 自动完成部署，特别适用于单页应用、作品集和登录页面的构建。

## 核心工作流程

### 1. 项目初始化

创建项目结构：

```bash
bash scripts/init_project.sh <project-name>
```

这将创建：
```
project-name/
├── index.html
├── styles.css
├── script.js
├── README.md
└── .github/
    └── workflows/
        └── deploy.yml
```

### 2. 开发

遵循以下原则开发网站：
- **优先考虑单页布局**：除非明确需要多个页面，否则应优化为单页布局。
- **自动生成代码**：生成完整的、可直接用于生产的代码，避免使用占位符。
- **现代设计**：使用现代 CSS（如 flexbox、grid）、响应式设计以及简洁的视觉风格。
- **无依赖项**：尽可能使用纯 HTML/CSS/JS；如果需要框架，则使用 CDN 链接。

使用 `assets/templates/` 目录下的模板作为起点：
- `base-html/` - 最基本的 HTML5 模板
- `portfolio/` - 作品集/简历模板，包含相应的分页结构
- `landing/` - 登录页面模板，包含标题栏和呼叫行动（CTA）按钮

### 3. 设置 GitHub 仓库

```bash
bash scripts/deploy_github_pages.sh <project-name> <github-username>
```

此脚本会执行以下操作：
1. 初始化 Git 仓库。
2. 通过 GitHub CLI 创建 GitHub 仓库。
3. 配置 GitHub Pages 的相关设置。
4. 提交初始代码。
5. 触发首次部署。

### 4. 部署

每当向 `main` 分支推送代码时，GitHub Actions 会自动执行部署流程：
- 检查代码。
- 将代码部署到 `gh-pages` 分支。
- 使网站在 `https://<username>.github.io/<project-name>/` 上上线。

## 架构指南

### HTML 结构
- 使用语义化的 HTML5 元素。
- 添加用于 SEO 和社交分享的元标签。
- 配置响应式视口。
- 添加网站图标（favicon）。

### CSS 设计
- 采用以移动设备为先的响应式设计。
- 使用 CSS 变量进行主题设置。
- 使用 flexbox 或 grid 进行布局设计。
- 实现平滑的过渡效果和动画效果。
- 在适当的情况下支持暗模式。

### JavaScript
- 优先使用原生 JavaScript。
- 采用渐进式增强（progressive enhancement）技术。
- 使用事件委托（event delegation）机制。
- 确保代码中没有控制台错误。

### 性能优化
- 优化图片大小。
- 对生产环境中的资源进行压缩。
- 在适当的位置实现懒加载（lazy loading）。
- 确保网站有快速的初始加载速度。

## 快速示例

### 示例 1：作品集/简历网站
**用户需求：** “为我创建一个作品集/简历网站。”

**操作步骤：**
1. 运行 `init_project.sh portfolio-cv` 命令。
2. 以 `assets/templates/portfolio/` 作为基础模板。
3. 生成包含标题栏、关于信息、技能、项目列表和联系信息的完整 HTML 页面。
4. 使用 `deploy_github_pages.sh portfolio-cv <username>` 命令进行部署。

### 示例 2：登录页面
**用户需求：** “为我的应用创建一个登录页面。”

**操作步骤：**
1. 运行 `init_project.sh app-landing` 命令。
2. 以 `assets/templates/landing/` 作为基础模板。
3. 生成包含标题栏、功能介绍、价格信息和呼叫行动按钮的页面。
4. 使用 `deploy_github_pages.sh app-landing <username>` 命令进行部署。

## 故障排除

### GitHub Pages 无法部署
- 检查仓库设置 → “Pages” → 确保 “Source” 设置为 `gh-pages` 分支。
- 确认 GitHub Actions 工作流程已成功执行。
- 检查 DNS 设置的传播情况（可能需要 5-10 分钟）。

### 权限问题
- 确保已登录 GitHub CLI：运行 `gh auth status` 命令。
- 检查 GitHub 仓库的权限设置。

### 构建失败
- 查看仓库中的 GitHub Actions 日志。
- 检查 `.github/workflows/deploy.yml` 文件的语法是否正确。
- 确认文件路径和引用是否正确。

## 资源

### scripts/
- `init_project.sh`：用于初始化项目结构。
- `deploy_github_pages.sh`：用于将代码部署到 GitHub Pages。

### references/
- `workflow.md`：详细的工作流程文档。
- `design-patterns.md`：设计最佳实践指南。

### assets/
- `templates/base-html/`：基本的 HTML5 模板。
- `templates/portfolio/`：作品集/简历模板。
- `templates/landing/`：登录页面模板。
- `.github/workflows/deploy.yml`：GitHub Actions 的工作流程配置文件。