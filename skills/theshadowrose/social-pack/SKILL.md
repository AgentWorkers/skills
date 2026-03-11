---
name: "SocialPack Multi-Platform Social Media Generator"
description: "根据一个简短的描述，生成适用于不同平台的社交媒体帖子。包括 Twitter 帖子、LinkedIn 帖子、Instagram 帖子和 Reddit 帖子。一个输入内容，对应一个平台。"
author: "@TheShadowRose"
version: "1.0.0"
tags: ["social-pack"]
license: "MIT"
---
# SocialPack 多平台社交媒体生成器

该工具能够根据用户提供的简短内容，自动生成适用于不同社交平台的帖子（包括 Twitter、LinkedIn、Instagram 和 Reddit）。只需提供一份简短的内容，即可生成适用于所有平台的帖子，并确保每个平台的格式都符合其规范。

---

**使用方法**

```javascript
const { SocialPack } = require('./src/social-pack');
const pack = new SocialPack();

const posts = await pack.generate({
  brief: 'Launched 30 AI agent tools on ClawHub today',
  platforms: ['twitter', 'linkedin', 'reddit'],
  tone: 'excited but professional'
});
```

---

**平台格式及限制**

| 平台 | 格式 | 限制 |
|---------|--------|--------|
| Twitter/X | 推文（280 字） | 会自动拆分成多条推文 |
| LinkedIn | 专业帖子 | 最长 3000 字，标签位于帖子底部 |
| Instagram | 说明文字 + 标签 | 最长 2200 字，标签数量限制为 30 个 |
| Reddit | 标题 + 正文 | 采用符合 Reddit 特色的表达方式 |
| Mastodon | 发文（Toot） | 最长 500 字 |

---

**主要功能：**

- **自动格式化**：根据各平台的规定进行内容格式化 |
- **标签生成**：生成相关且不会过于冗余的标签 |
- **推文拆分**：确保 Twitter 推文阅读起来自然流畅 |
- **语气适配**：同一条内容在不同平台上呈现不同的语气 |
- **A/B 测试**：可生成 2-3 个版本以供测试使用 |

---

## ⚠️ 免责声明

本软件按“原样”提供，不附带任何明示或暗示的保修声明。

**使用本软件的风险由您自行承担：**

- 作者对因使用或误用本软件而导致的任何损害、损失或后果（包括但不限于财务损失、数据丢失、安全漏洞、业务中断或间接/间接损害）概不负责。
- 本软件不构成财务、法律、交易或专业建议。
- 用户需自行评估本软件是否适合其使用场景、环境及风险承受能力。
- 本软件在准确性、可靠性、完整性或适用性方面不作任何保证。
- 作者对第三方在购买后如何使用、修改或分发本软件不承担任何责任。

通过下载、安装或使用本软件，即表示您已阅读并同意完全自行承担使用风险。

**数据声明：** 本软件会在您的系统上本地处理和存储数据。作者对因软件漏洞、系统故障或用户操作错误导致的数据丢失、损坏或未经授权的访问不承担任何责任。请始终为重要数据创建独立备份。除非用户明确配置，否则本软件不会向外传输数据。

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

🛠️ **需要定制功能？** 我们提供定制的 OpenClaw 代理和技能服务，价格从 500 美元起。只要您能详细描述需求，我就能为您实现。→ [在 Fiverr 上联系我](https://www.fiverr.com/s/jjmlZ0v)