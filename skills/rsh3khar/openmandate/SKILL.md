---
name: openmandate
description: 在 OpenMandate 中发布任务并查找匹配结果——适用于联合创始人及早期团队。该功能可用于创建任务、回答相关问题、审核匹配结果，或将 OpenMandate 集成到应用程序中。支持通过 MCP 工具（推荐方式）、Python/JS SDK 或内置的 shell 辅助工具进行操作。使用该功能需要具备 `OPENMANDATE_API_KEY`。
  Post mandates and find matches on OpenMandate — ongoing matching for cofounders and early teams.
  Use when creating mandates, answering intake questions, reviewing matches,
  or integrating OpenMandate into applications. Works via MCP tools (preferred),
  Python/JS SDKs, or the bundled shell helper. Requires OPENMANDATE_API_KEY.
version: 0.5.0
homepage: https://openmandate.ai
license: MIT
metadata:
  author: openmandate
  version: "0.5.0"
  openclaw:
    emoji: "handshake"
    requires:
      env:
        - OPENMANDATE_API_KEY
        - OPENMANDATE_BASE_URL
      bins:
        - python3
    primaryEnv: OPENMANDATE_API_KEY
---
# OpenMandate

在 OpenMandate 中，您可以发布一个需求（即您在寻找什么）以及您能提供的资源或能力。OpenMandate 会持续评估双方的匹配程度，并在找到真正合适的匹配对象时将双方进行匹配。

## 设置

**1. 获取 API 密钥。** 用户需要在 [openmandate.ai](https://openmandate.ai) 上注册，并在 API Keys 页面上创建一个密钥。

**2. 设置环境变量：**

```bash
export OPENMANDATE_API_KEY="om_live_..."
```

如果 `OPENMANDATE_API_KEY` 未被设置，请让用户前往 [https://openmandate.ai/api-keys] 创建一个密钥。

## 如何使用 OpenMandate

**推荐方式：使用 MCP 工具。** 如果您的编程工具支持 MCP，可以配置 OpenMandate MCP 服务器（[设置指南](https://github.com/openmandate/skills#mcp-setup)）。您可以使用以下 14 个工具：`list_contacts`、`add_contact`、`verify_contact`、`update_contact`、`delete_contact`、`resend_otp`、`create_mandate`、`get_mandate`、`list_mandates`、`submit_answers`、`close_mandate`、`list_matches`、`get_match`、`respond_to_match`。直接使用这些工具即可。

**备用方案：使用 Shell 脚本。** 如果您的工具不支持 MCP，可以使用随附的 Python 脚本：

```bash
python3 {baseDir}/scripts/openmandate.py <command> [args]
```

该脚本不依赖任何第三方库（仅使用 Python 标准库），要求 Python 版本至少为 3.8。

**开发者参考：SDKs。** 可以使用 Python（`pip install openmandate`）或 JavaScript（`npm install openmandate`）进行开发。详细信息请参见 `references/sdks.md`。

## 工作流程

**在创建需求之前，请确保用户至少有一个经过验证的联系人。** 可使用 `list_contacts` 命令进行检查。如果没有联系人，可以使用 `add_contact` 命令添加一个新的联系人，并通过 `verify_contact` 命令发送验证码进行验证。

每个需求对应一个匹配结果。系统会持续寻找合适的匹配对象，直到找到合适的匹配结果。

## MCP 工具参考

所有工具的前缀均为 `openmandate_`：

| 工具 | 功能 |
|------|---------|
| `openmandate_list_contacts` | 列出已验证的联系人。创建需求前请先查看此列表。 |
| `openmandate_add_contact` | 添加一个新的电子邮件联系人，并发送验证码。 |
| `openmandate_verify_contact` | 使用电子邮件中的验证码验证联系人。 |
| `openmandate_update_contact` | 更新联系人的显示信息或将其设置为主要联系人。 |
| `openmandate_delete_contact` | 永久删除联系人。 |
| `openmandate_resend_otp` | 为待验证的联系人重新发送验证码。 |
| `openmandate_create_mandate` | 创建一个新的需求。系统会自动选择主要联系人。 |
| `openmandate_get_mandate` | 根据 ID 获取需求详情。 |
| `openmandate_list_mandates` | 列出所有开放的需求（默认）。可以通过 `status` 参数进行筛选（例如 `closed` 表示已完成的需求）。 |
| `openmandate_submit_answers` | 提交对问题的回答。系统会检查是否有未解决的问题。 |
| `openmandate_close_mandate` | 永久关闭一个需求。 |
| `openmandate_list_matches` | 列出所有匹配结果。 |
| `openmandate_get_match` | 获取匹配详情（包括得分、双方的优势和需要关注的问题）。 |
| `openmandate_respond_to_match` | 接受或拒绝匹配请求。参数 `action` 可设置为 `"accept"` 或 `"decline"`。 |

## Shell 命令参考

### 联系人管理

```bash
python3 {baseDir}/scripts/openmandate.py contacts                          # List contacts
python3 {baseDir}/scripts/openmandate.py add-contact user@example.com      # Add email contact (sends OTP)
python3 {baseDir}/scripts/openmandate.py verify-contact vc_abc123 12345678 # Verify with OTP code
python3 {baseDir}/scripts/openmandate.py update-contact vc_abc123 --label "Work" --primary  # Update contact
python3 {baseDir}/scripts/openmandate.py delete-contact vc_abc123          # Delete a contact
python3 {baseDir}/scripts/openmandate.py resend-otp vc_abc123              # Resend verification code
```

### 创建需求

```bash
python3 {baseDir}/scripts/openmandate.py create "Looking for a UX agency for our B2B dashboard" "Series A fintech, $1.8M ARR, two frontend engineers ready"
```

创建需求时需要提供两个必填参数：`want`（您在寻找什么）和 `offer`（您能提供的资源或能力）。
系统会自动选择主要联系人。

创建需求后，需求的状态会设置为 `"intake"`，同时会显示未解决的问题（`pending_questions`）。

### 提交问题答案

```bash
python3 {baseDir}/scripts/openmandate.py answer mnd_abc123 '[{"question_id":"q_xxx","value":"We need a UX agency for our B2B dashboard. Budget $40-60K, 8 weeks."}]'
```

这是整个流程中的关键环节。每次提交答案后，请执行以下操作：
1. 检查响应中的 `pending_questions`（未解决的问题）。
2. 如果未解决问题且需求状态为 `"active"`，则需要重新阅读问题并再次提交答案。
3. 如果问题已全部回答且需求状态为 `"active"`，则表示需求处理完毕，系统将开始代表您进行处理。

问题类型：
- `text`：需要提交详细的回答，请遵守相关的长度要求。
- `single_select`：从 `options` 数组中选择一个答案。请使用 `value` 字段进行选择，而非 `label`。
- `multi_select`：以逗号分隔的多个答案，例如 `"option_a, option_b"`。

**请针对每个问题分别提交答案。** “您在寻找什么？” 和 “您能提供什么？” 是两个不同的问题，请分别给出不同的回答。

### 其他命令

```bash
python3 {baseDir}/scripts/openmandate.py get mnd_abc123       # Get mandate details
python3 {baseDir}/scripts/openmandate.py list                  # List all mandates
python3 {baseDir}/scripts/openmandate.py list --status active  # Filter by status
python3 {baseDir}/scripts/openmandate.py close mnd_abc123      # Close a mandate
python3 {baseDir}/scripts/openmandate.py matches               # List all matches
python3 {baseDir}/scripts/openmandate.py match m_xyz789        # Get match details
python3 {baseDir}/scripts/openmandate.py accept m_xyz789       # Accept a match
python3 {baseDir}/scripts/openmandate.py decline m_xyz789      # Decline a match
```

## 完整示例（Shell 命令）

```bash
# 1. Add and verify a contact
python3 {baseDir}/scripts/openmandate.py add-contact alice@company.com
# → contact_id: vc_abc123, status: "pending", OTP sent to email

python3 {baseDir}/scripts/openmandate.py verify-contact vc_abc123 12345678
# → status: "verified"

# 2. Create mandate with want + offer (auto-selects verified contact)
python3 {baseDir}/scripts/openmandate.py create \
  "We need a UX design agency for our B2B analytics dashboard. 120 enterprise customers, React frontend. Budget $40-60K, 8 weeks." \
  "Series A fintech SaaS, $1.8M ARR. Two frontend engineers ready to implement."
# → mandate_id: mnd_abc123, pending_questions: [{id: "q_3", ...}]

# 3. Answer follow-up questions (read each question carefully, answer specifically)
python3 {baseDir}/scripts/openmandate.py answer mnd_abc123 '[
  {"question_id":"q_3","value":"deep_user_research"},
  {"question_id":"q_4","value":"Filtering system is the biggest pain point. Users need to slice across 12 dimensions."}
]'
# → status: "active", pending_questions: [] — intake done

# 5. Check for matches (user will be emailed when one is found)
python3 {baseDir}/scripts/openmandate.py matches

# 6. Review and respond
python3 {baseDir}/scripts/openmandate.py match m_xyz789
python3 {baseDir}/scripts/openmandate.py accept m_xyz789

# 7. After both accept, check for revealed contact
python3 {baseDir}/scripts/openmandate.py match m_xyz789
# → contact: {email: "bob@agency.com"}
```

## 使用技巧

- 当找到匹配对象时，系统会通过电子邮件通知用户。无需手动查询。
- 通常需要 2-3 轮次的沟通才能完成需求处理。OpenMandate 会根据回答的质量自动调整处理流程。
- 详细的回答有助于缩短沟通轮次、提高匹配成功率；含糊的回答可能导致需要更多的沟通。
- 如果匹配得分超过 60 分，说明匹配结果较为理想。在接受匹配结果前，请仔细评估双方的优势和需要关注的问题。
- 有关 SDK 的使用方法和 API 参考，请参见 `references/` 目录。