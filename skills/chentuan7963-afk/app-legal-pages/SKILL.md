---
name: app-legal-pages
description: 根据应用程序的功能文档，生成并部署应用程序的隐私政策（Privacy Policy）和服务条款（Terms of Service）的静态网页。当用户提供应用程序需求或功能文档时，可以使用此服务将准备好的法律文件通过 GitHub 和 Cloudflare Pages 发布到生产环境中。该服务包括草稿生成、一致性检查以及可部署的网页 URL 提供。
---
# 应用程序法律页面

为应用程序生成一个完整的法律信息网站，包括以下页面：
- `index.html`（法律首页）
- `privacy.html`（隐私政策）
- `terms.html`（服务条款）
- `styles.css`（共享样式）

## 工作流程

1. 收集所需的法律/产品相关信息。
2. 根据功能文档生成法律页面的草稿。
3. 运行严格的一致性检查。
4. 将生成的页面提交给用户审核/批准。
5. 检查 Cloudflare 部署的认证准备情况。
6. 如果认证信息缺失，请求用户完成认证。
7. 在用户明确确认后，自动将页面部署到 Cloudflare Pages。
8. 提供最终的公开网址。

## 1) 收集信息

需要收集或确认的信息包括：
- 应用程序名称
- 公司/实体名称（或个人发布者名称）
- 联系邮箱
- 所适用的法律管辖区域（国家/地区，可选；仅在明确提供时填写）
- 生效日期
- 应用程序功能文档（Markdown/文本格式）
- 数据处理相关细节：
  - 分析事件记录
  - 错误/崩溃日志
  - 设备/用户标识符
  - 使用的第三方 SDK/服务
  - 使用的权限（摄像头/位置/照片/麦克风/联系人/跟踪/通知等）

如果某些信息未知，请暂停流程并请求用户提供缺失的信息。在最终生成的页面中不要使用占位符（如 TODO/TEMP 等临时标记）。除非在输入文档或用户提示中明确说明，否则不要假设任何关于法律管辖区域、数据使用方式或权限设置的内容。

首先根据产品的具体声明生成相应的政策条款（例如：仅限离线使用、不使用云服务、不进行数据跟踪、不使用分析功能），并避免使用自带的通用法律模板。

## 2) 生成页面草稿

运行以下脚本：
```bash
python3 scripts/generate_legal_site.py \
  --input /path/to/app-feature.md \
  --out ./out/legal-site \
  --app-name "Your App" \
  --company "Your Company" \
  --base-email "chentuan7963@gmail.com" \
  --email-tag "quillnest" \
  --effective-date "2026-03-03" \
  --jurisdiction "California, United States"
```

**邮箱规则：**
- 建议使用 GitHub 用户的邮箱地址加上 `quillnest` 作为新的邮箱地址（例如：`chentuan7963@gmail.com + quillnest` → `chentuan7963+quillnest@gmail.com`）。
- 仅在需要固定邮箱地址时使用 `--email` 参数。

**语言规则：**
- 默认生成仅包含英文的法律页面。
- 从功能描述中排除非英文内容，以保持语言一致性。

脚本会自动从功能描述中识别可能的数据类别和权限信息。如果应用程序的实际行为与自动识别结果不符，请手动审核并调整输出内容。

## 3) 运行严格的一致性检查

在发布之前，运行以下脚本：
```bash
python3 scripts/check_consistency.py \
  --feature /path/to/app-feature.md \
  --privacy ./out/legal-site/privacy.html \
  --terms ./out/legal-site/terms.html
```

以下情况会导致检查失败：
- 包含占位符（如 TODO/TEMP/FIXME）
- 与产品声明相矛盾的内容（例如：声明“仅限离线使用”但实际包含云服务或数据跟踪功能）
- 功能文档中提及 EXIF 格式的数据，但未同时提供相应的隐私披露信息
- 服务条款中未明确指定法律管辖区域

## 4) 验证页面质量

在发布之前，需要检查以下内容：
- `privacy.html` 和 `terms.html` 页面是否存在。
- 所有页面中的应用程序名称、公司名称、联系邮箱及生效日期是否一致。
- 隐私政策中披露的权限内容是否与实际使用的数据处理方式相符（不得包含未经明确授权的跟踪或地区相关声明）。
- 是否提供了用户权利说明以及联系人和删除请求的路径。
- 页面中不得包含任何无法验证的法律声明。
- 最终生成的页面中不得包含占位符（如 TODO/TEMP/FIXME 等临时标记）。

如果应用程序使用了敏感权限或第三方 SDK，需确保这些信息在隐私政策中得到明确披露。

## 5) 审核流程（强制要求）

在部署之前，将生成的文件分享给用户并请求其明确批准。未经用户确认，不得自动进行部署。

## 6) 检查部署认证

运行以下脚本，以确认部署所需的认证信息是否齐全：
```bash
python3 scripts/deploy_cloudflare_pages.py --check-auth --site-dir ./out/legal-site --project-name your-project-name --production-branch main
```

当满足以下任一条件时，认证信息视为有效：
- `CLOUDFLARE_API_TOKEN` 和 `CLOUDFLARE_ACCOUNT_ID` 均已设置
- 使用 `wrangler whoami` 命令时能够成功验证用户身份

如果认证信息缺失，需要请求用户完成身份验证：
```bash
wrangler login
```

## 7) 自动部署到 Cloudflare Pages

在用户明确批准且认证信息齐全后，运行以下脚本进行自动部署：
```bash
python3 scripts/deploy_cloudflare_pages.py \
  --site-dir ./out/legal-site \
  --project-name your-project-name \
  --production-branch main
```

或者，也可以使用一次性部署流程：
```bash
python3 scripts/run_pipeline.py \
  --feature /path/to/app-feature.md \
  --out ./out/legal-site \
  --app-name "Your App" \
  --company "Your Company" \
  --base-email "you@gmail.com" \
  --email-tag "yourapp" \
  --effective-date "2026-03-05" \
  --project-name your-project-name \
  --production-branch main \
  --confirm-deploy
```

## 8) 提供结果

最终需要提供的内容包括：
- Cloudflare Pages 网站网址
- 隐私政策网址（`<site>/privacy.html`）
- 服务条款网址（`<site>/terms.html`）
- 使用的认证方式（`api-token` 或 `wrangler-login`）

## 注意事项：
- 不得声称法律合规性得到保证。
- 保持文字表述的简洁易读性。
- 保持页面结构的稳定性，以便将来方便修改。
- 建议在应用程序提交到应用商店之前，由专业法律人员进行审核。