---
name: zenn_github
description: 通过管理连接至 GitHub 的仓库中的 Markdown 文件来发布 Zenn 文章（执行推送/拉取请求（push/PR）并合并更改），然后使用 Zenn CLI 进行预览。
---
# Zenn：GitHub 推送/PR 发布

## 概述
Zenn 通过同步 GitHub 仓库来实现内容发布。文章/书籍以 Markdown 格式保存在特定的目录中，而 Zenn CLI 可帮助您在本地预览和构建内容。

该流程既快速又安全：
- 在 PR 中起草内容（`published: false`）
- 使用 `zenn preview` 在本地预览内容
- 当 PR 准备就绪后，将 `published` 设置为 `true` 以完成发布

## 需要收集的信息：
- **仓库路径**（本地克隆路径）和 **GitHub 远程仓库地址**
- **发布分支**（与 Zenn 相连接的分支）
- **文章元数据**：标题、表情符号、类型（`tech` 或 `idea`）、主题、是否已发布
- **Markdown 文件的 slug/文件名**（建议使用 kebab-case 格式）
- **资源文件（图片）的存放路径**（推荐路径：`images/<slug>/...`）

## 文件存放规则（Zenn）：
- 文章必须作为单独的 `.md` 文件保存在 `articles/` 目录下。
- （可选）书籍文件保存在 `books/` 目录下。

推荐的仓库结构：

```
.
├─ articles/
│  └─ 20260216-openclaw-to-zenn.md
├─ books/                # optional
└─ images/               # optional, recommended
   └─ openclaw-to-zenn/
      ├─ cover.png
      └─ diagram.png
```

## Zenn CLI 使用方法（本地）
### 安装/初始化（每个仓库只需执行一次）
如果仓库中尚未配置 Zenn CLI，请执行以下操作：
```bash
npm init --yes
npm install zenn-cli
npx zenn init
```

### 在本地预览
```bash
npx zenn preview
```

### 创建新内容
```bash
npx zenn new:article
npx zenn new:book
```

### 列出现有内容
```bash
npx zenn list:articles
npx zenn list:books
```

## 文章模板（复制/粘贴）
创建 `articles/<slug>.md` 文件：

```md
---
title: "記事タイトル"
emoji: "🧩"
type: "tech" # tech or idea
topics: ["ruby", "rails", "ai"]
published: false
---

## TL;DR
- ...
- ...
- ...

## 背景
...

## 実装 / 検証
...

## 学び
...

## 参考
- ...
```

**注意事项：**
- 标题应放在文档的开头部分，因此正文中的标题应使用 `##` 标签开始。
- 为了构建系列文章，建议使用固定且简洁的主题。

## 推荐的工作流程：
### 1) 在特性分支中起草内容
1. 创建或编辑 `articles/<slug>.md` 文件（将 `published` 设置为 `false`）
2. 将图片（如果有）保存在 `images/<slug>/...` 目录下
3. 在本地预览内容：
   ```bash
   npx zenn preview
   ```

### 2) 提交 PR
```bash
git checkout -b article/<slug>
git add articles/<slug>.md images/<slug>/
git commit -m "Add draft: <title>"
git push -u origin article/<slug>
```
将内容提交到 Zenn 的发布分支。

### 3) 安全发布
**选项 A（最安全）**：通过另一个单独的 PR/提交来完成发布
1. 合并草稿 PR（此时 `published` 仍为 `false`）
2. 将 `published` 设置为 `true`，然后合并该 PR

**选项 B（更快）**：在同一 PR 中完成发布
- 在编写或审阅过程中保持 `published` 为 `false`
- 在合并前将 `published` 设置为 `true`

## 质量检查清单（最低要求）：
在将 `published` 设置为 `true` 之前，请确认以下内容：
- 不包含任何机密信息（如客户名称、内部链接、未发布的指标）
- 代码块可以正常运行，或者明确标注为伪代码
- 图片能够正确显示，且路径正确
- 链接有效
- 拼写、标题和格式均符合要求

## 常见问题及解决方法：
- 预览结果与 Zenn 网站或 CLI 显示的结果不一致：
  ```bash
  npm install zenn-cli@latest
  ```
- 图片无法显示：
  - 确保图片已提交并推送至仓库
  - 确保图片的路径格式为 `/images/<slug>/...`（而非 `./images/...`
- 文章未显示：
  - 文件必须位于 `articles/` 目录下
  - `published` 必须设置为 `true`
  - 确保正在更新的仓库是正确的发布分支

## 何时不适用此方法？
- 跳过 PR 审查直接发布会增加数据泄露的风险。
- 依赖 UI 或浏览器自动化功能可能会导致因 UI 变更而出现问题。
- 将多篇文章合并到一个文件中，或将文件放在 `articles/` 目录之外，会导致发布失败。