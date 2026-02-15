---
name: agent-content-pipeline
description: 安全的内容工作流程（包括草稿、审核、修订、批准以及发布）需要人工参与审批；同时提供命令行界面（CLI）用于内容的列表管理、移动、审核以及发布到 LinkedIn 或其他平台。该流程适用于搭建内容处理流程、起草内容、管理审核流程或发布已批准的内容。
---

# 内容处理流程（Content Pipeline Skill）

采用安全的内容自动化机制，并在流程中加入人工审核环节。流程步骤为：草稿（Draft）→ 审核（Review）→ 批准（Approve）→ 发布（Post）。

## 设置（Setup）

```bash
npm install -g agent-content-pipeline
content init . # Creates folders + global config (in current directory)
```

**对于需要加密签名的内容（受密码保护的）：**
```bash
content init . --secure
```

该设置会创建以下文件夹结构：
- `drafts/`：正在处理中的草稿文件（每个文件对应一个草稿）
- `reviewed/`：已由人工审核的文件，等待您的修改
- `revised/`：您已修改的文件，等待再次审核
- `approved/`：已通过人工审核的文件，准备发布
- `posted/`：发布后的归档文件
- `templates/`：用于审核和自定义的模板文件
- `.content-pipeline/threads/`：用于记录审核反馈的线程日志（这些日志不会被公开）

## 您的权限（Your Permissions）

✅ **您可以执行以下操作：**
- 将文件写入 `drafts/` 目录
- 读取所有内容文件
- 根据反馈修改草稿
- 将修改后的文件移动到 `revised/` 目录
- 运行 `content list` 命令查看待处理的内容

❌ **您无法执行以下操作：**
- 将文件移动到 `approved/` 目录（只能由人工进行批准）
- 直接发布内容
- 设置文件的状态为 `approved`

## 创建内容（Creating Content）

**每个文件对应一个独立的发布记录。** 每条建议或草稿都应作为单独的发布记录处理，不能合并。

**文件命名规则：** `YYYY-MM-DD-<平台>-<slug>.md`

**使用前置内容（Frontmatter）：** 
```yaml
---
platform: linkedin    # linkedin | x | reddit (experimental)
title: Optional Title
status: draft
subreddit: programming  # Required for Reddit
---

Your content here.
```

**通知审核人员：** “草稿已准备好审核：`content review <文件名>`”

## 审核流程（The Review Loop）

```
drafts/ → reviewed/ → revised/ → approved/ → posted/
              ↑          │
              └──────────┘
               more feedback
```

1. 您将草稿文件写入 `drafts/` 目录。
2. 审核人员运行 `content review <文件名>` 命令：
   - 如果有反馈，文件会被移动到 `reviewed/` 目录，您会收到通知；
   - 如果没有反馈，系统会询问审核人员是否批准该文件，文件会被移动到 `approved/` 目录。
3. 如果收到反馈，您需要修改文件后将其移动回 `revised/` 目录。
4. 审核人员会再次审核 `revised/` 目录中的文件：
   - 如果还有反馈，文件会返回到 `reviewed/` 目录；
   - 如果审核通过，文件会被移动到 `approved/` 目录。
5. 最终内容需要通过手动运行 `content post` 命令进行发布。

### 收到反馈后的处理（After Receiving Feedback）

收到审核反馈后，请按照以下步骤操作：
1. 从 `reviewed/` 目录中读取文件内容。
2. 根据反馈修改文件。
3. 将修改后的文件移动回 `revised/` 目录。
4. 确认您所做的修改。
5. （可选）添加备注：`content thread <文件名> -- 来自审核人员`

## 平台使用指南（Platform Guidelines）

### LinkedIn
- 语言要专业且自然（针对荷兰语用户使用荷兰语）
- 文章长度建议为1-3段
- 文章结尾处应包含问题或行动号召（CTA）
- 文章末尾添加3-5个话题标签

### X（Twitter）
- 每条推文最多280个字符（除非使用付费账户）
- 表达要简洁明了
- 最多使用1-2个话题标签
- 尽量少使用评论线程（threads）
- 如果Firefox身份验证失败，您可以手动复制 `auth_token` 和 `ct0` 参数。

**手动获取身份验证信息的步骤：**
1. 打开 x.com 并登录。
2. 打开开发者工具（DevTools）→ 应用程序/存储（Application/Storage）→ Cookies → https://x.com
3. 复制 `auth_token` 和 `ct0` 参数。

### Reddit（测试阶段）
- 请注意：此功能仍处于测试阶段，API和子版块规则可能会发生变化。
- 文件前置内容中必须包含 `subreddit:` 字段。
- 标题应来自文件的前置内容中的 `title:` 部分（如果前置内容中没有标题，则使用文件的第一行作为标题）。
- 内容撰写需遵循相应子版块的规则和语言风格。

## 命令参考（Commands Reference）

```bash
content list                    # Show drafts and approved
content review <file>           # Review: feedback OR approve
content mv <dest> <file>        # Move file to drafts/reviewed/revised/approved/posted
content edit <file>             # Open in editor ($EDITOR or code)
content post <file>             # Post (prompts for confirmation)
content post <file> --dry-run   # Preview without posting
content thread <file>           # Add a note to the feedback thread
```

## 安全模型（Security Model）

我们的安全模型将内容起草（由AI完成）与内容审核/发布（由人工完成）分开：
- ✅ 代理（agent）负责起草内容。
- ✅ 代理会根据反馈修改内容。
- ❌ 代理无法批准内容（必须由人工通过 `content review` 命令进行批准）。
- ❌ 代理无法直接发布内容。

内容的发布操作必须通过命令行界面（CLI）手动完成，严禁由代理直接执行。

### 平台特定的安全设置（Platform-specific Security）

| 平台 | 身份验证方式 | 是否加密？ | 是否需要密码？ |
|----------|--------------|------------|-------------------|
| LinkedIn | 浏览器身份验证 | ✅ 是 | ✅ 是 |
| X/Twitter | Firefox令牌验证 | ✅ 是 | ✅ 是 |

两个平台都要求用户提供密码才能发布内容。令牌信息从Firefox中提取并在本地进行加密处理。