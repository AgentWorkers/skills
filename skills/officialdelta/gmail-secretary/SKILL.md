---
name: gmail-secretary
description: 使用 Haiku LLM 的 Gmail 分类辅助工具：负责邮件分类、标签添加以及回复草稿的生成（该工具基于 gog CLI 进行操作；绝不会自动发送邮件）。
---

# Gmail 助手（Alan）

## 安全规则（不可商量）
- **严禁自动发送邮件**。仅创建邮件草稿和摘要。
- 建议使用**标签**来管理邮件，而非直接移动或删除它们。
- 语音参考资料应侧重于**模式说明**（提供一些简短的、经过编辑的示例内容），而非完整的邮件存档。

## 标签（用户友好）
使用/创建以下标签：
- 紧急
- 需回复
- 待处理
- 稍后阅读
- 收到/账单
- 学校相关
- 俱乐部活动
- Mayo Clinic 相关
- 管理/账户相关

## 分类方式：基于 AI 助手的分类系统（使用 Haiku LLM）
分类过程通过 **Haiku LLM 助手**（通过 `sessions_spawn` 调用）来完成，而非使用正则表达式。
- `scripts/triage-and-draft.sh` 脚本会从收件箱中获取邮件并生成摘要，将其保存到 `cache/gmail-inbox-summaries.json` 文件中。
- AI 助手会读取这些摘要，对每封邮件进行分类，并将结果保存到 `cache/gmail-triage-labels.json` 文件中。
- `scripts/apply-labels.sh` 脚本会根据分类结果为邮件添加相应的 Gmail 标签。

### AI 助手分类的提示信息：
- 使用者是 Stanton College Prep 的学生（学习 IB/AP 课程）。
- 参与的俱乐部活动包括：FBLA、科学展览、医学协会（Psi Alpha）和 NHS。
- 执行的项目是与 Mayo Clinic 相关的癌细胞模拟研究。
- 公司（如 Apple、Google、Amazon 等）不属于“学校相关”类别。
- 新闻通讯或促销邮件应标记为“稍后阅读”。
- 与账户安全、密码或验证相关的邮件应标记为“管理/账户相关”。

## 相关文件：
- 语音参考资料（自动维护）：`references/voice.md`
- 邮件草稿队列：`/home/delta/.openclaw/workspace/cache/gmail-drafts.md`
- 分类结果摘要：`/home/delta/.openclaw/workspace/cache/gmail-triage.md`
- 收件箱摘要：`/home/delta/.openclaw/workspace/cache/gmail-inbox-summaries.json`
- 分类结果文件：`/home/delta/.openclaw/workspace/cache/gmail-triage-labels.json`

## 相关脚本：
- 从已发送的邮件中生成语音参考资料：`scripts/build-voice-reference.sh`（提取最近 50 封已发送邮件的示例内容）
- 从收件箱中获取邮件并生成摘要：`scripts/triage-and-draft.sh`
- 根据分类结果为邮件添加标签：`scripts/apply-labels.sh`

## 工作流程：
1. 运行 `triage-and-draft.sh` 脚本，从收件箱中获取邮件并生成摘要。
2. AI 助手（使用 Haiku LLM）根据 `gmail-inbox-summaries.json` 文件对邮件进行分类。
3. AI 助手将分类结果保存到 `gmail-triage-labels.json` 文件中。
4. 运行 `apply-labels.sh` 脚本，为邮件添加相应的 Gmail 标签。
5. AI 助手将分类结果摘要保存到 `cache/gmail-triage.md` 文件中，以便后续提醒使用。