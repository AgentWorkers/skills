---
name: submit-directories
description: >
  **在将产品提交到 AI/创业项目目录时使用的方法**  
  该方法涵盖了整个流程：从收集产品信息、分析相关目录、自动提交申请，到处理验证码/身份验证（OAuth）以及 GitHub 的 Pull Request（PR），并在 `checkpoint.md` 文件中记录整个过程的进度。
---
# 提交产品到各种目录

## 概述

将产品提交到800多个AI工具目录的完整流程包括：收集产品信息 → 分析目标目录 → 制定提交计划 → 查找所需的表单 → 自动提交 → 手动浏览器提交 → 跟踪提交进度。

## 设置

### 安装依赖项

```bash
pip install -r requirements.txt
playwright install chromium
```

### 通过环境变量配置凭据

切勿在脚本中硬编码凭据。请在运行任何管道步骤之前设置这些凭据：

```bash
# Required
export SUBMIT_PRODUCT_URL="https://yourproduct.com"
export SUBMIT_PRODUCT_NAME="Your Product Name"
export SUBMIT_TAGLINE="Your one-line tagline"
export SUBMIT_EMAIL="you@throwaway.com"        # use throwaway email
export SUBMIT_AUTHOR_NAME="Jane Doe"

# Recommended
export SUBMIT_AUTHOR_FIRST="Jane"
export SUBMIT_AUTHOR_LAST="Doe"
export SUBMIT_USERNAME="youruser"
export SUBMIT_PASSWORD="throwaway-pass"        # use throwaway password

# Optional
export SUBMIT_GITHUB_URL="https://github.com/you/repo"
export SUBMIT_TWITTER_URL="https://twitter.com/yourhandle"
export SUBMIT_KEYWORDS="ai,saas,marketing,automation"
export SUBMIT_LOGO="logo.png"                  # relative to script dir
export SUBMIT_SCREENSHOT="site-image.png"      # relative to script dir
```

**提示：** 将这些凭据保存到本地的`.env`文件中（该文件已在`.gitignore`中），并通过以下命令加载它们：
```bash
set -a && source .env && set +a
```

### 放置资源文件

- `logo.png` — 产品Logo（用于文件上传字段）
- `site-image.png` — 产品截图（用于文件上传字段）

这两个文件应与脚本位于同一目录下。

## 第0阶段：收集产品信息

**请逐一收集信息**（切勿一次性提交所有信息）：

| 编号 | 字段 | 问题 |
|---|-------|----------|
| 1 | 产品URL | “请提供您的产品/初创网站的URL。” |
| 2 | 产品名称 | “请告知您的产品名称。” |
| 3 | 标语 | “请提供一个简短的标语。” |
| 4 | 产品描述 | “请用2-3句话描述产品的功能、目标用户群以及它的独特之处。” |
| 5 | 定价模式 | “您的定价模式是什么？”（免费/免费试用/开源/付费） |
| 6 | 关键词 | “请列出5-7个相关关键词。” |
| 7 | 用于提交的电子邮件地址 | “用于提交信息的电子邮件地址是什么？” |
| 8 | 名称 | “提交时使用的名称是什么？”（请分别提供名字和姓氏） |
| 9 | 用户名 | “如果需要注册，请提供首选的用户名。” |
| 10 | 密码 | “如果需要注册，请提供一个一次性使用的密码。⚠️ 请使用一次性密码——切勿使用真实密码。密码会在保存前从`submission_plan.json`中删除。” |
| 11 | GitHub URL | （可选） |
| 12 | Twitter/X | （可选） |

然后询问用户的提交偏好：
- “是否希望将产品提交到需要Google登录的目录？（您需要手动完成身份验证）”
- “是否跳过所有需要付费的目录，或者标记为需要审核？”
- “是否希望在验证码网站上自动填写表单，或者由您手动解决验证码？”
**资源文件提示：** 请让用户将`logo.png`和`site-image.png`文件放在项目根目录下。

## 第1阶段：配置

1. 设置所有必需的环境变量（参见上述“设置”部分）
2. 生成**30种独特的文本描述组合**（包括标题和描述）：
   - 从不同角度描述产品的特点、优势、定价信息和使用场景
   - 文字长度应有所差异（简短精炼或详细说明）
   - 使用不同的关键词，开头部分不能重复
3. 将这些描述保存到`submission_plan.json`文件中
4. 使用`checkpoint.md`文件更新产品信息（注意：不要包含密码）

## 第2阶段：分析并分类目录

```bash
.venv/bin/python analyze_directories.py         # HTTP-level: auth, captcha, pricing, dead domains
.venv/bin/python cleanup_and_categorize.py      # Triage errors, build browser_check_list.json
.venv/bin/python browser_verify.py              # Playwright verification (10 concurrent workers)
.venv/bin/python browser_verify.py --recheck-unknown  # Deep recheck unknowns
```

完成分析后，报告各目录的认证类型分布情况。

## 第3阶段：制定提交计划

过滤`directories.json`文件：
- `site_status = active`
- `auth_type = none` 或 `auth_type = email_password`
- 如果用户选择了`google_only`或`google_and_email`，则将这些目录也包含在内

创建`submission_plan.json`文件中的条目，每个条目包含一种描述组合、相应的凭据以及`status: pending`状态。

## 第4阶段：查找所需的表单

```bash
.venv/bin/python discover_forms.py
```

访问每个需要提交的产品页面，提取表单字段的元数据，并更新`submission_plan.json`文件。同时记录查找到的表单数量、未找到的表单数量以及提交过程中出现的超时情况。

## 第5阶段：自动提交

```bash
.venv/bin/python submit_directories.py
```

报告提交结果：是否成功提交、是否存在匹配的表单、是否超时，或者是否需要手动处理。

## 第6阶段：手动浏览器提交

对于需要手动操作的网站，使用Playwright MCP（`mcp__playwright`命名空间）来完成提交流程：

### 面对验证码的网站
1. 使用`browser_navigate`导航到提交页面
2. 使用`browser_snapshot`获取页面内容
3. 使用`browser_fill_form`或`browser_type`填写所有表单字段
4. 要求用户解决验证码
5. 使用`browser_click`提交表单并验证结果

### 面对需要Google登录的网站
1. 使用`browser_navigate`导航到登录页面
2. 点击“使用Google登录”
3. 要求用户完成Google身份验证
4. 登录后，进入提交表单页面
5. 使用`browser_tabs`在OAuth弹窗和主页面之间切换

### 处理富文本或复杂的表单
- 对于使用TinyMCE/Quill编辑器的表单，直接使用`browser_evaluate`设置表单内容
- 对于下拉菜单（Combobox）类型的表单，使用`browser_click`选择选项
- 对于多步骤表单，每完成一个步骤后使用`browser_snapshot`获取新的表单字段
- 对于自定义上传组件（如Logo或截图），使用`browser_file_upload`功能

## 第7阶段：通过GitHub Pull Request提交

**要求：** 确保已安装并配置了`gh` CLI工具，并完成身份验证（使用`gh auth login`）。如果希望将您的仓库链接到提交记录中，请设置`SUBMIT_GITHUB_URL`。

对于某些特定的目录（如awesome-list），请将PR的URL记录在`checkpoint.md`文件中。

## 跟踪提交进度

在每个阶段完成后，更新`checkpoint.md`文件，记录各阶段的提交情况（包括成功提交的目录数量、失败的原因以及下一步的操作步骤）。

### 状态代码说明

| 状态 | 含义 |
|--------|---------|
| `submitted` | 提交成功 |
| `skipped_paid` | 需要支付费用 |
| `skipped_login_required` | 需要创建账户 |
| `captcha` | 需要手动解决验证码 |
| `no_form_found` | 页面上没有提交表单 |
| `no_fieldsmatched` | 表单存在，但没有匹配的字段 |
| `timeout` / `submit_timeout` | 提交过程超时 |
| `cloudflareblocked` | 遭到Cloudflare的访问限制 |
| `domain_parked` | 域名已失效 |

## 规则

1. **切勿盲目假设**——如果有任何不清楚的地方，请务必询问用户。
2. **切勿提交真实密码**——始终使用环境变量存储密码；密码会在保存前从`submission_plan.json`中自动删除。
3. **每个阶段完成后都要进行报告**——切勿让管道过程无声地运行。
4. **详细说明每个跳过的步骤**——向用户解释为什么某个目录被跳过。
5. **验证提交结果**——检查提交状态是否成功或出现错误。
6. **设置提交频率限制**——避免因频繁提交导致IP地址被封禁。
7. **在推送代码到Git之前删除个人敏感信息**——检查所有文件中是否包含用户的电子邮件地址、姓名和密码。

## 常见的提交障碍

| 障碍类型 | 发生频率 | 检测方法 |
|---------|-----------|-----------|
| 需要付费的目录 | 约20% | 网站上有定价信息、Stripe支付链接或提交页面上显示“$”符号 |
| 需要验证码的网站 | 约10% | 页面中包含`iframe[src*=recaptcha]`或`[data-turnstile]` |
| 需要登录的网站 | 约15% | 提交页面会重定向到登录页面 |
- 仅提供新闻通讯注册的表单 | 约10% | 实际上是电子邮件注册页面 |
- 域名已失效或无法访问的网站 | 约8% | 网站内容为空或DNS解析失败 |
| 遭到Cloudflare限制的网站 | 约3% | 页面显示验证码或返回403错误 |
- 需要反向链接的网站 | 约5% | 一些旧的网站目录要求提供反向链接 |

## 最具投资回报率的目录类型

1. 提供简单HTML表单的AI工具目录
2. 使用Google Forms的初创企业目录
3. 接受GitHub Pull Request的awesome-list目录（可免费获得高质量的外部链接）
4. NoCode/SaaS类型的聚合平台
5. 目录的Domain Authority（DA）值大于30的通用网站

## 文件参考

| 文件名 | 用途 |
|------|---------|
| `directories.json` | 包含所有827多个目录的详细信息 |
| `submission_plan.json` | 包含每个目标目录的提交信息（包含描述和表单字段，但不包含凭据） |
| `checkpoint.md` | 用于记录提交进度，是所有信息的来源 |
| `analyze_directories.py` | 用于进行HTTP层面的分析 |
| `cleanup_and_categorize.py` | 用于对目录进行分类和处理 |
| `browser_verify.py` | 用于使用Playwright进行浏览器自动化验证 |
| `discover_forms.py` | 用于查找表单字段 |
| `submit_directories.py` | 负责自动提交功能的脚本 |