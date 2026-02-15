---
description: 将 Markdown 文章发布到 note.com，同时支持图片上传、添加标签以及使用浏览器自动化功能。
---

# 通过浏览器自动化将Markdown文件发布到note.com

**适用场景**：将文章发布到note.com、管理草稿或自动化内容发布流程。

**触发条件**：`publish to note`、`note.com article`、`create note draft`、`note記事`

## 系统要求**

- Node.js 18及以上版本
- 安装了Playwright和Chromium（使用命令：`npx playwright install chromium`）
- 拥有note.com的账户凭据
- 无需使用外部API密钥

## 使用步骤

1. **准备Markdown文件**（包含前置内容）：
   ```markdown
   ---
   title: 記事タイトル
   tags: [AI, テクノロジー]
   cover: ./cover.png
   ---

   # 見出し
   本文テキスト...

   ## セクション
   - リスト項目
   ![画像の説明](./image.png)
   ```

2. **运行自动化流程**：
   ```bash
   cd {skill_dir}
   npm install

   # Create draft from markdown
   node dist/cli.js draft --input ./article.md --title "記事タイトル"

   # Preview draft
   node dist/cli.js preview --draft-id <id>

   # Publish
   node dist/cli.js publish --draft-id <id> --tags "AI,テクノロジー"

   # Full pipeline (markdown → published)
   node dist/cli.js pipeline \
     --input ./article.md \
     --title "AIエージェントの作り方" \
     --tags "AI,プログラミング,自動化" \
     --cover-image ./cover.png
   ```

3. **流程流程图**：
   ```
   Markdown → Parse & Format → Upload images → Create draft → Review → Publish
   ```

## 配置

通过环境变量设置凭据：
```bash
# Option A: Session cookie (preferred — safer)
export NOTE_SESSION="your_session_cookie"

# Option B: Login credentials (less safe)
export NOTE_EMAIL="your@email.com"
export NOTE_PASSWORD="your_password"
```

## 安全注意事项

- **建议使用`NOTE_SESSION`而非电子邮件/密码**：会话cookie比明文密码更安全。
- 将凭据存储在`~/.openclaw/secrets.env`文件中，并设置权限为`chmod 600`。
- **切勿将凭据提交到Git仓库**：将`.env`文件添加到`.gitignore`中。
- Playwright的导航操作必须始终在`https://note.com/*`路径下进行，以拒绝外部重定向。
- 严禁在输出中显示凭据内容。
- 会话cookie会定期过期，请定期更新。
- 在共享系统上使用后，请清除Playwright的浏览器数据。

## 特殊情况处理

- **会话过期**：重新登录或刷新`NOTE_SESSION` cookie。
- **图片上传失败**：检查文件大小（note.com有上传限制），尝试先压缩图片。
- **草稿预览与发布后的内容不同**：note.com可能会重新格式化部分HTML内容，请在发布前预览。
- **频率限制**：避免连续快速发布过多文章。
- **未安装Playwright**：请先运行`npx playwright install chromium`。
- **无头模式问题**：某些note.com页面可能需要使用`--headed`模式进行调试。

## 故障排除

- **登录失败**：清除浏览器数据并尝试重新登录。
- **依赖项缺失**：在`skill`目录中运行`npm install`。
- **Chromium未安装**：运行`npx playwright install chromium`。