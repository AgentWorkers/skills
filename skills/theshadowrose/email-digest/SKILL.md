---
name: "EmailDigest Daily Email Summary for Agents"
description: "智能电子邮件分类器及摘要生成工具，专为代理人员设计。用户可将获取到的电子邮件以数组形式传递给该工具，随后会收到一份按优先级划分的每日邮件摘要，其中包含紧急邮件、需要处理的邮件以及仅供参考的邮件。该工具兼容 Himalaya IMAP、各类平台邮件连接器，以及任何电子邮件处理流程。所有处理操作均在本地完成。"
author: "@TheShadowRose"
version: "1.0.1"
tags: ["email-digest"]
license: "MIT"
---
# EmailDigest：代理人员的每日邮件摘要工具

该工具可将未读邮件汇总成简洁的每日报告，支持邮件优先级排序、发送者筛选以及关键行动事项的提取，是个人代理人员的理想工具。

---

您的代理人员会将已获取的邮件数据提供给 EmailDigest。EmailDigest 会对这些邮件进行分类、排序和格式化处理，仅展示重要的信息，忽略无关内容。

## 您将获得的功能

```
📬 Email Digest — Feb 28, 2026

URGENT (2):
• Boss wants Q4 numbers by EOD — received 7:23 AM
• Client contract expires tomorrow — needs signature

ACTION NEEDED (3):
• PR review requested on auth-module (#142)
• Meeting reschedule request from Sarah
• Invoice #4021 payment confirmation needed

FYI (8):
• 3 newsletter digests
• 2 shipping notifications
• GitHub: 3 new issues in your repos

Spam filtered: 12 messages
```

## 配置方式

EmailDigest 可处理邮件数据数组——您的代理人员或邮件处理流程负责获取邮件数据，然后将其传递给 EmailDigest：

```javascript
const digest = new EmailDigest({
  prioritySenders: ['boss@company.com', 'partner@email.com'],
  urgencyKeywords: ['urgent', 'asap', 'deadline'],
  ignoreSenders: ['noreply@*', 'marketing@*']
});

// emails = array fetched via himalaya, platform connector, or any source
const result = digest.process(emails);
console.log(result.formatted);
```

该工具兼容 [himalaya](https://github.com/soywod/himalaya) 命令行工具、OpenClaw 邮件连接器，或任何能够生成包含 `from`、`subject` 和 `body` 字段的邮件对象的系统。

## 主要特性：

- **智能分类**：区分紧急邮件、需处理邮件、仅供参考的邮件以及可忽略的邮件
- **发送者优先级显示**：支持自定义 VIP 列表
- **关键行动事项提取**：自动提取需要执行的操作
- **邮件线索汇总**：将长篇邮件内容精简为关键要点
- **支持多种邮件来源**：适用于从 Himalaya、平台连接器或任何其他系统预获取的邮件数据
- **隐私保护**：所有处理过程均在本地完成，邮件数据不会离开您的设备

---

## ⚠️ 免责声明

本软件按“原样”提供，不附带任何明示或暗示的保修条款。

**使用本软件需自行承担风险：**

- 作者对因使用或误用本软件而导致的任何损害、损失或后果（包括但不限于财务损失、数据丢失、安全漏洞、业务中断或间接/附带损害）概不负责。
- 本软件不构成财务、法律、交易或专业建议。
- 用户需自行评估本软件是否适用于其具体使用场景、环境及风险承受能力。
- 作者不对软件的准确性、可靠性、完整性或适用性作出任何保证。
- 作者不对第三方购买后对软件的使用、修改或分发行为负责。

通过下载、安装或使用本软件，即表示您已阅读并同意完全自行承担相关风险。

**数据隐私声明：** 本软件会在您的系统上本地处理和存储数据。作者对因软件漏洞、系统故障或用户操作失误导致的数据丢失、损坏或未经授权的访问行为概不负责。请务必定期备份重要数据。除非用户明确配置，否则本软件不会向外传输数据。

---

## 支持与联系方式

| | |
|---|---|
| 🐛 **问题报告** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*本软件基于 [OpenClaw](https://github.com/openclaw/openclaw) 开发——感谢您的支持！*

---

🛠️ **需要定制功能？** 我们提供定制的 OpenClaw 代理程序和功能服务，价格从 500 美元起。只要您能描述需求，我就能为您实现。→ [在 Fiverr 上联系我](https://www.fiverr.com/s/jjmlZ0v)